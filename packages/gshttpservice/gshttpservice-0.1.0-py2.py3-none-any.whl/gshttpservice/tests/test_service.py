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
import pytest

import http.client
import urllib.parse


@pytest.fixture(scope="module")
def conn():
    conn = http.client.HTTPConnection("localhost", 9527)
    yield conn
    conn.close()


def do_get(conn, path, params):
    conn.request("GET", "{0}?{1}".format(path, params))
    r = conn.getresponse()
    if r.status > 400 and r.status < 600:
        raise RuntimeError(r.reason + ": " + path)
    return r.read()


def do_post(conn, path, params, headers={"Content-type": "application/json"}):
    conn.request("POST", path, params, headers)
    r = conn.getresponse()
    if r.status > 400 and r.status < 600:
        raise RuntimeError(r.read() + ": " + path)
    return r.read()


def test_service(conn):
    # create instance
    params = json.dumps({"num_workers": 2, "vineyard_shared_mem": "10Gi"})
    data = do_post(conn, "/api/graphservice/createInstance", params)
    instance_id = json.loads(data.decode("utf-8"))["instance_id"]

    # load modern graph
    dataset_path = os.environ["MODERN_GRAPH_PATH"]
    params = json.dumps(
        {
            "type": "LOCAL",
            "directed": True,
            "oid_type": "int64_t",
            "instance_id": instance_id,
            "dataSource": {
                "nodes": [
                    {
                        "label": "person",
                        "id_field": "id",
                        "location": os.path.join(dataset_path, "person.csv"),
                        "config": {
                            "header_row": True,
                            "delimiter": "|"
                        }
                    },
                    {
                        "label": "software",
                        "id_field": "id",
                        "location": os.path.join(dataset_path, "software.csv"),
                        "config": {
                            "header_row": True,
                            "delimiter": "|"
                        }
                    }
                ],
                "edges": [
                    {
                        "label": "knows",
                        "location": os.path.join(dataset_path, "knows.csv"),
                        "srcLabel": "person",
                        "dstLabel": "person",
                        "srcField": "src_id",
                        "dstField": "dst_id",
                        "config": {
                            "header_row": True,
                            "delimiter": "|"
                        }
                    },
                    {
                        "label": "create",
                        "location": os.path.join(dataset_path, "created.csv"),
                        "srcLabel": "person",
                        "dstLabel": "software",
                        "srcField": "src_id",
                        "dstField": "dst_id",
                        "config": {
                            "header_row": True,
                            "delimiter": "|"
                        }
                    }
                ]
            }
        }
    )
    data = do_post(conn, "/api/graphservice/loadData", params)
    graph_name = json.loads(data.decode("utf-8"))["graph_name"]
    print("graph_name: " , graph_name)

    # gremlin query
    params = urllib.parse.urlencode({"gremlinSQL": "g.V()", "graph_name": graph_name})
    print(do_get(conn, "/api/graphservice/query/gremlin", params))
    
    # get schema
    params = urllib.parse.urlencode({"graph_name": graph_name})
    print(do_get(conn, "/api/graphservice/graphSchema", params))

    # get instance
    print(do_get(conn, "/api/graphservice/getInstance", ""))

    # close instance
    params = urllib.parse.urlencode({"instance_id": instance_id})
    print(do_get(conn, "/api/graphservice/closeInstance", params))
