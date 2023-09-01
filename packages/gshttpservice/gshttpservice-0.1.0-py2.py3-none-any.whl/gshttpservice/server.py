#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2022 Alibaba Group Holding Limited.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import cgi
import json
import os
import traceback
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from urllib.parse import parse_qs
from urllib.parse import urlparse

from .utils import ParamError
from .utils import gs_manager
from .utils import ws_manager


class GSHttpServer(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super(GSHttpServer, self).__init__(*args, **kwargs)

    def do_GET(self):
        try:
            if self.path.startswith("/api/graphservice/query/gremlin"):
                self._do_gremlin_query()
            elif self.path.startswith("/api/graphservice/algorithm"):
                self._do_algo_analysis()
            elif self.path.startswith("/api/graphservice/unloadData"):
                self._do_unload_data()
            elif self.path.startswith("/api/graphservice/closeInstance"):
                self._do_close_instance()
            elif self.path.startswith("/api/graphservice/setInterval"):
                self._do_set_interval()
            elif self.path.startswith("/api/graphservice/getInstance"):
                self._do_get_instance()
            elif self.path.startswith("/api/graphservice/graphSchema"):
                self._do_get_graph_schema()
            elif self.path.startswith("/api/graphservice/addColumn"):
                self._do_add_column()
            else:
                # forbidden
                self._send_response(
                    403,
                    "Forbidden: GET request resource failed with invalid URL {0}".format(
                        self.path
                    ),
                )
            return
        except ParamError as e:
            self._send_response(400, "Error: {0}".format(str(e)))
        except Exception as e:
            print(e, traceback.format_exc())
            # internal server error
            self._send_response(
                500,
                "Internal server error: {0}".format(
                    str(traceback.format_exc())
                ),
            )
        return

    def do_POST(self):
        try:
            # route
            if self.path == "/api/graphservice/createInstance":
                self._do_create_instance()
            elif self.path == "/api/graphservice/loadData":
                self._do_load_data()
            elif self.path == "/api/graphservice/uploadFile":
                self._do_upload_file()
            else:
                # forbidden
                self._send_response(
                    403,
                    "Forbidden: POST request resource failed with invalid URL {0}".format(
                        self.path
                    ),
                )
            return
        except ParamError as e:
            self._send_response(400, "Error: {0}".format(str(e)))
        except Exception as e:
            print(e, traceback.format_exc())
            # internal server error
            self._send_response(
                500,
                "Internal server error: {0}".format(
                    str(traceback.format_exc())
                ),
            )
        return

    def _send_response(self, code, message="", **kwargs):
        success = True
        if code >= 400 and code < 600:
            success = False
        self.send_response(code)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        response_data = {"success": success, "code": code, "message": message}
        response_data.update(**kwargs)
        self.wfile.write(json.dumps(response_data).encode("utf-8"))

    def _do_algo_analysis(self):
        query = parse_qs(urlparse(self.path).query)
        context_key, rlt = gs_manager.algo_analysis(query)
        self._send_response(
            200,
            "Algorithm analysis successful",
            context_name=context_key,
            result=rlt,
        )

    def _do_gremlin_query(self):
        query = parse_qs(urlparse(self.path).query)
        rlt = gs_manager.query(query)
        self._send_response(200, "Gremlin query successful", result=rlt)

    def _do_create_instance(self):
        content_length = int(self.headers["Content-Length"])
        content = self.rfile.read(content_length).decode("utf-8")
        instance_id = gs_manager.create_instance(content)
        self._send_response(
            200,
            "Create graphscope instance successful",
            instance_id=instance_id,
        )

    def _do_close_instance(self):
        query = parse_qs(urlparse(self.path).query)
        gs_manager.close_instance(query)
        self._send_response(200, "Close graphscope instance successful")

    def _do_get_instance(self):
        query = parse_qs(urlparse(self.path).query)
        rlt = gs_manager.get_instance(query)
        self._send_response(200, "Get instance successful", result=rlt)

    def _do_get_graph_schema(self):
        query = parse_qs(urlparse(self.path).query)
        rlt = gs_manager.get_graph_schema(query)
        self._send_response(200, "Get graph schema successful", result=rlt)

    def _do_add_column(self):
        query = parse_qs(urlparse(self.path).query)
        graph_name, graph_url = gs_manager.add_column(query)
        self._send_response(
            200,
            "Add column successful",
            graph_name=graph_name,
            graph_url=graph_url,
            hostname=gs_manager.hostname,
            hostip=gs_manager.hostip,
        )

    def _do_set_interval(self):
        query = parse_qs(urlparse(self.path).query)
        ws_manager.set_interval(query)
        self._send_response(200, "Set param interval successful")

    def _do_upload_file(self):
        ctype, pdict = cgi.parse_header(self.headers["Content-Type"])
        records_path = {}
        if ctype == "multipart/form-data":
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={
                    "REQUEST_METHOD": "POST",
                    "CONTENT_TYPE": self.headers["Content-Type"],
                },
            )
            # instance_id is unique for each user
            instance_id = form.getvalue("instance_id")
            # get user workspace
            user_workspace = ws_manager.create_user_workspace(instance_id)
            # upload file
            files = form["file"]
            if not isinstance(files, list):
                files = [files]
            for record in files:
                record_path = os.path.join(user_workspace, record.filename)
                open(record_path, "wb").write(record.file.read())
                records_path[record.filename] = record_path
        self._send_response(
            200, "Upload file successful", records=json.dumps(records_path)
        )

    def _do_load_data(self):
        content_length = int(self.headers["Content-Length"])
        content = self.rfile.read(content_length).decode("utf-8")
        graph_name, graph_url = gs_manager.load_data(content)
        self._send_response(
            200,
            "Load graph data successful",
            graph_name=graph_name,
            graph_url=graph_url,
            hostname=gs_manager.hostname,
            hostip=gs_manager.hostip,
        )

    def _do_unload_data(self):
        query = parse_qs(urlparse(self.path).query)
        gs_manager.unload_data(query)
        self._send_response(200, "Unload graph data successful")


def run(server_class=HTTPServer, handler_class=GSHttpServer, port=9527):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print("GSHttpService is listening on {0} ...".format(port))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("KeyboardInterrupt received, stopping GSHttpService ...")
        gs_manager.close()
    httpd.server_close()
