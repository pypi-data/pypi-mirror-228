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

import json
import os
import shutil
import socket
import sys
import threading
import time

import graphscope
from graphscope.framework.loader import Loader

if "DEBUG" in os.environ:
    graphscope.set_option(show_log=True, log_level="DEBUG")


def str_to_bool(s):
    return s.lower() in ["true", "1", "t", "y", "yes"]


class _ReprableString(str):
    """A special class that prevents `repr()` adding extra `""` to `str`.

    It is used to optimize the user experiences to preseve `\n` during printing exceptions.
    """

    def __repr__(self) -> str:
        return self


class ParamError(Exception):
    def __init__(self, message=None, detail=None):
        if message is not None and not isinstance(message, str):
            message = repr(message)
        super().__init__(_ReprableString(message))

    def __str__(self):
        return self.args[0] or ""


class WorkspaceManager(object):
    """Class for manage resource."""

    def __init__(self):
        # root workspace
        self._workspace = os.path.join(
            os.path.expanduser("~"), ".gshttpserver"
        )
        self._dataset = os.path.join(self._workspace, "user-dataset")
        os.makedirs(self._dataset, exist_ok=True)
        # default to 3 dags
        self._interval = 3 * 24 * 60 * 60
        # expired file detection
        self._expired_file_detecting_timer = None
        self._expired_file_detecting_timer = threading.Timer(
            interval=self._interval,
            function=self._detect_file_impl,
            args=(
                self._interval,
                self._dataset,
            ),
        )
        self._expired_file_detecting_timer.daemon = True
        self._expired_file_detecting_timer.start()

    @property
    def workspace(self):
        return self._workspace

    @property
    def dataset(self):
        return self._dataset

    def _reset_expired_file_detecting_timer(self):
        if self._expired_file_detecting_timer:
            self._expired_file_detecting_timer.cancel()
        self._expired_file_detecting_timer = threading.Timer(
            interval=self._interval,
            function=self._detect_file_impl,
            args=(
                self._interval,
                self._dataset,
            ),
        )
        self._expired_file_detecting_timer.daemon = True
        self._expired_file_detecting_timer.start()

    def _get_file_or_dir_age(self, path):
        return os.stat(path).st_ctime

    def _detect_file_impl(self, interval, path):
        seconds = time.time() - interval
        if os.path.exists(path):
            for rootdir, subdirs, subfiles in os.walk(path):
                # subdir
                for name in subdirs:
                    subdir = os.path.join(rootdir, name)
                    if seconds >= self._get_file_or_dir_age(subdir):
                        print("[Expired]: Remove dir {0}".format(subdir))
                        shutil.rmtree(subdir)
                # subfile
                for name in subfiles:
                    subfile = os.path.join(rootdir, name)
                    if seconds >= self._get_file_or_dir_age(subfile):
                        print("[Expired]: Remove file {0}".format(subfile))
                        os.remove(subfile)
        # reset timer
        self._reset_expired_file_detecting_timer()

    def set_interval(self, query):
        if "interval" not in query:
            raise ParamError("Param interval(s) is needed.")
        interval = int(query["interval"][0])
        if interval > 0:
            self._interval = interval
            # reset expired file detection timer
            self._reset_expired_file_detecting_timer()

    def create_user_workspace(self, instance_id):
        if instance_id is None:
            raise ParamError("Param instance_id is needed to create workspace")
        user_workspace = os.path.join(self._dataset, instance_id)
        os.makedirs(user_workspace, exist_ok=True)
        return user_workspace


class DataSourceParser(object):
    SUPPORT_DATA_SOURCE = ["LOCAL", "URL"]

    def __init__(self, ds_type, config={}):
        if ds_type not in self.SUPPORT_DATA_SOURCE:
            raise ParamError(
                "Data source {0} is not supported".format(ds_type)
            )
        self._ds_type = ds_type
        self._config = config

    def _str_to_integer(self, s):
        try:
            i = int(s)
            return i
        except Exception:
            return s

    def _parse_loader(self, item):
        if self._ds_type == "LOCAL":
            header_row = (
                item["config"]["header_row"]
                if "header_row" in item["config"]
                else True
            )
            delimiter = (
                item["config"]["delimiter"]
                if "delimiter" in item["config"]
                else ","
            )
            return Loader(
                item["location"], header_row=header_row, delimiter=delimiter
            )
        elif self._ds_type == "URL":
            key = self._config["accessKey"]
            secret = self._config["accessSecret"]
            endpoint = self._config["endpoint"]
            return Loader(
                item["location"], key=key, secret=secret, endpoint=endpoint
            )
        raise RuntimeError(
            "Data source type {0} is not implemented yet".format(self._ds_type)
        )

    def parse_vertex(self, v):
        label = v["label"]
        id_field = (
            self._str_to_integer(v["id_field"]) if "id_field" in v else 0
        )
        loader = self._parse_loader(v)
        return (label, id_field, loader)

    def parse_edge(self, e):
        label = e["label"]
        src_label = e["srcLabel"]
        dst_label = e["dstLabel"]
        src_field = (
            self._str_to_integer(e["srcField"]) if "srcField" in e else 0
        )
        dst_field = (
            self._str_to_integer(e["dstField"]) if "dstField" in e else 1
        )
        loader = self._parse_loader(e)
        return (label, src_label, dst_label, src_field, dst_field, loader)


class GSManager(object):
    """Class for wrapper and operate gs engine."""

    def __init__(self):
        self._sess = {}
        self._graph = {}
        self._interactive = {}
        self._context = {}
        self._hostname = socket.gethostname()
        self._hostip = socket.gethostbyname(self._hostname)

    @property
    def hostname(self):
        return self._hostname

    @property
    def hostip(self):
        return self._hostip

    def _handle_rlt(self, context, need_sort=False, limit=None):
        # now only support vertex_data context
        df = context.to_dataframe({"id": "v.id", "result": "r"})
        if need_sort:
            df = df.sort_values(by=["id"])
            df.reset_index(drop=True, inplace=True)
        if limit is not None:
            df = df.head(limit)
        return context.key, df.to_json()

    def get_graph_schema(self, query):
        if "graph_name" not in query:
            raise ParamError("Param graph_name is needed to get graph schema.")
        graph_name = query["graph_name"][0]
        if str(graph_name) not in self._graph:
            raise RuntimeError("Graph {0} is not exists.".format(graph_name))
        graph = self._graph[str(graph_name)]
        return json.dumps(graph.schema.to_dict())

    def algo_analysis(self, query):
        """Run algorithm on analytical engine"""
        if "graph_name" not in query:
            raise ParamError(
                "Param graph_name is needed to algorithm analytsis."
            )
        algo = query["name"][0]
        graph_name = query["graph_name"][0]
        if str(graph_name) not in self._graph:
            raise RuntimeError("Graph {0} is not exists.".format(graph_name))
        graph = self._graph[str(graph_name)]

        # run algo on projected graph
        vertex_label = (
            query["vertex_label"][0] if "vertex_label" in query else ""
        )
        edge_label = query["edge_label"][0] if "edge_label" in query else ""
        project_graph = None
        if vertex_label and edge_label:
            vertices = {}
            edges = {}
            for v_label in vertex_label.split(";"):
                vertices.update({v_label: None})
            for e_label in edge_label.split(";"):
                edges.update({e_label: None})
            project_graph = graph.project(vertices=vertices, edges=edges)
            vineyard_id = project_graph.vineyard_id
            print(
                "project v: {0}, e: {1} on graph {2}".format(
                    vertices, edges, graph_name
                )
            )
            self._graph[str(vineyard_id)] = project_graph

        # run algo
        algo_params = {}
        for k, v in query.items():
            # fixed params not related to algo
            if k not in [
                "name",
                "graph_name",
                "limit",
                "sortById",
                "vertex_label",
                "edge_label",
            ]:
                algo_params[k] = v[0]
        print("Run algo {0} with params: {1}".format(algo, algo_params))

        if project_graph is None:
            exec_algo = "graphscope.{0}(graph, **algo_params)".format(algo)
        else:
            exec_algo = "graphscope.{0}(project_graph, **algo_params)".format(
                algo
            )
        context = eval(exec_algo)
        context_key = context.key
        self._context[str(context_key)] = context

        # need sort
        need_sort = (
            str_to_bool(query["sortById"][0]) if "sortById" in query else False
        )
        # limit
        limit = int(query["limit"][0]) if "limit" in query else None
        return self._handle_rlt(context, need_sort, limit)

    def add_column(self, query):
        if "graph_name" not in query:
            raise ParamError("Param graph_name is needed to add column.")
        if "context_name" not in query:
            raise ParamError("Param context_name is needed to add column.")
        if "column_name" not in query:
            raise ParamError("Param column_name is needed to add column.")
        graph_name = query["graph_name"][0]
        context_name = query["context_name"][0]
        column_name = query["column_name"][0]
        if str(graph_name) not in self._graph:
            raise RuntimeError("Graph {0} is not exists.".format(graph_name))
        if context_name not in self._context:
            raise RuntimeError(
                "Context {0} is not exists.".format(context_name)
            )
        print("Add column '{0}' on graph {1}".format(context_name, graph_name))
        graph = self._graph[str(graph_name)]
        context = self._context[context_name]
        new_graph = graph.add_column(context, {column_name: "r"})
        new_graph_vineyard_id = new_graph.vineyard_id
        self._graph[str(new_graph_vineyard_id)] = new_graph
        # interactive engine
        graph_url = ""
        if "need_gremlin" in query:
            interactive = graph.session.gremlin(new_graph)
            self._interactive[str(new_graph_vineyard_id)] = interactive
            graph_url = interactive.graph_url[0]
        return new_graph_vineyard_id, graph_url

    def query(self, query):
        """Gremlin query with interactive engine"""
        if "graph_name" not in query:
            raise ParamError(
                "Param graph_name is needed to execute gremlin query."
            )
        graph_name = query["graph_name"][0]
        if str(graph_name) not in self._interactive:
            raise RuntimeError(
                "Interactive with graph {0} is not exists".format(graph_name)
            )
        query_statement = query["gremlinSQL"][0]
        # get interactive with graph name
        interactive = self._interactive[str(graph_name)]
        # query
        rlt = interactive.execute(query_statement).all()
        return str(rlt)

    def unload_data(self, query):
        if "graph_name" not in query:
            raise ParamError("Param graph_name is needed to unload data.")
        graph_name = query["graph_name"][0]
        if str(graph_name) not in self._graph:
            raise ParamError("Graph {0} is not exists.".format(graph_name))
        graph = self._graph[str(graph_name)]
        graph.unload()
        del self._graph[str(graph_name)]

    def load_data(self, content):
        # default values
        data = {
            "type": "LOCAL",
            "directed": True,
            "dataSource": {},
            "config": {},
        }
        data.update(json.loads(content))
        # get graphscope instance by id
        if "instance_id" not in data:
            raise ParamError("Param instance_id is needed to load data.")
        instance_id = data["instance_id"]
        if str(instance_id) not in self._sess:
            raise RuntimeError(
                "GraphScope instance {0} is not exists".format(instance_id)
            )
        sess = self._sess[str(instance_id)]
        # parser
        parser = DataSourceParser(data["type"], data["config"])
        # vertices
        vertices = {}
        if "nodes" in data["dataSource"]:
            for v in data["dataSource"]["nodes"]:
                label, id_field, loader = parser.parse_vertex(v)
                # now select all properties
                vertices[label] = (loader, None, id_field)
        # edges
        edges = {}
        if "edges" in data["dataSource"]:
            for e in data["dataSource"]["edges"]:
                (
                    label,
                    src_label,
                    dst_label,
                    src_field,
                    dst_field,
                    loader,
                ) = parser.parse_edge(e)
                # handle sublabel, select all properties and set the
                # first two columns as src and dst field
                item = (
                    loader,
                    None,
                    (src_field, src_label),
                    (dst_field, dst_label),
                )
                if label in edges:
                    edges[label].append(item)
                else:
                    edges[label] = [item]
        # load graph
        oid_type = data["oid_type"] if "oid_type" in data else "string"
        g = sess.load_from(
            edges,
            vertices,
            oid_type=oid_type,
            directed=data["directed"],
            generate_eid=True,
        )
        # index graph with unique vineyard id
        vineyard_id = g.vineyard_id
        self._graph[str(vineyard_id)] = g
        # interactive
        interactive = sess.gremlin(g)
        self._interactive[str(vineyard_id)] = interactive
        graph_url = interactive.graph_url[0]
        return vineyard_id, graph_url

    def create_instance(self, content):
        data = json.loads(content)
        # only "hosts" supported
        data.update({"cluster_type": "hosts"})
        sess = graphscope.session(**data)
        instance_id = sess.session_id
        self._sess[str(instance_id)] = sess
        return instance_id

    def close_instance(self, query):
        if "instance_id" not in query:
            raise ParamError("Param instance_id is needed to close instance.")
        instance_id = query["instance_id"][0]
        if str(instance_id) not in self._sess:
            raise RuntimeError(
                "Instance {0} is not exists".format(instance_id)
            )
        sess = self._sess[str(instance_id)]
        sess.close()
        del self._sess[str(instance_id)]

    def get_instance(self, query):
        return list(self._sess.keys())

    def close(self):
        try:
            for _, sess in self._sess.items():
                sess.close()
        except Exception:
            pass


gs_manager = GSManager()
ws_manager = WorkspaceManager()
