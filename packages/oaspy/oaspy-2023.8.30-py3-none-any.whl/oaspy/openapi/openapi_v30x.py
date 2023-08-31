# -*- coding: utf-8 -*-

import re
import orjson
from ..insomnia import validate_v4
from ..utils import open_file

work_space = []
# envs = []
groups_list = []
# requests = []

# tags = []s
# paths = []
servers = []

cookie_jar = []
api_spec = []


schema_export = {
    "openapi": "3.0.3",
    "info": {
        "title": "awesome api - OpenAPI 3.0",
        "description": "my awesome api",

        "termsOfService": "http://awesome.io/terms",
        "contact": {
            "email": "apiteam@awesome.io"
        },
        "license": {
            "name": "MIT",
            "url": "https://opensource.org/license/mit/"
        },
        "version": "1.0.0"
    },
    "paths": [],
    "servers": [],
    "tags": [],
    "components": {
        "securitySchemes": {
            "bearerAuth": {
                "type": "http",
                "scheme": "bearer",
            },
        },
    },
}

default_responses = {
    "200": {"description": "successful"},
    "201": {"description": "created"},
    "400": {"description": "bad request"},
    "401": {"description": "authorization failed"},
    "403": {"description": "Forbidden"},
    "422": {"description": "validation failed"},
    "500": {"description": "unknown server error"},
}


def create_envs(envs_list=None):
    """create_envs(create_servers), procesa los entornos (envs)"""
    print("create_envs procesando entornos...")
    servers_list = []

    try:
        for item in envs_list:
            variables = {}
            print("nombre:", item["name"])
            data = item["data"]
            obj = {
                "description": item["name"],
            }

            if data is not None:
                for key in data:
                    print("item data key:", key)
                    variables[key] = {"default": data[key]}

            url = list(variables.keys())
            if len(url) > 0:
                first = url[0]
                obj["url"] = data[first]
                obj["variables"] = variables
                servers_list.append(obj)

        # print()
        # print("create_envs variables:", variables)
        # print()
        # print("create_envs servers_list:", servers_list)
        return servers_list
    except Exception as e:
        print("create_envsException...", e)
        return None



def create_groups():
    pass


def create_requests():
    pass


def create_tags(groups_list, tags_list=None):
    # recorrer los grupos?
    print("create_tags procesando tags")
    tag_list = []

    for item in groups_list:
        # print("el item es:", item)
        tag_list.append(
            {
                "name": item["name"] if "name" in item else "Missing group name",
                "description": item["description"] if "description" in item else "",
            }
        )

    return tag_list


def create_paths(requests_list, groups_list=None):
    """procesa la lista de requests y groups"""
    print("procesando requests...")
    request_paths = {}
    i = 0

    for item in requests_list:
        parent_id = item["parentId"] if "parentId" in item else None
        desc_name = item["name"]
        dirty_url = item["url"]
        body = item["body"] if "body" in item else None
        desc = item["description"] if "description" in item else None

        new_url = re.sub(r"\{\{.*?\}\}", "", dirty_url)
        method = item["method"].lower()

        _endpoint = [new_url][0]
        _method = [method][0]
        _group = None

        if parent_id is not None:
            _group = next((d.get("name") for d in groups_list if d.get("id") == parent_id), "default")
            # for item in groups_list:
            #     if item["id"] == parent_id:
            #         _group = item["name"]
            #         break

        obj_request = {
            _endpoint: {
                _method: {
                    "description": desc if desc is not None else "description not available",
                    "summary": desc_name,
                    "tags": [_group],
                    "parameters": [],
                    "responses": default_responses,
                }
            }
        }

        if method in {"post", "put", "patch"}:
            if body is not None:
                mime_type = body["mimeType"] if "mimeType" in body else None
                request_body = {}

                match mime_type:
                    case "application/json":
                        example = body["text"] if "text" in body else None

                        if not example:
                            print("=================")
                            print("application/json: no hay example:")
                            print("_endpoint:", _endpoint)
                            print("_method:", _method)
                            print("desc_name:", desc_name)
                            print("omitiendo...")
                            continue

                        try:
                            example = orjson.loads(example)
                        except Exception:
                            print("orjson.loads example Exception...")
                            example = str(example)

                        request_body = {
                            "requestBody": {
                                "required": True,
                                "content": {
                                    mime_type: {
                                        "schema": {
                                            "type": "object",
                                            "example": example,
                                        }
                                    }
                                },
                            },
                        }
                    case "multipart/form-data":
                        params = body["params"] if "params" in body else None
                        # print("multipart/form-data params:", params)
                        if not params:
                            print("=================")
                            print("multipart/form-data: no hay example:")
                            print("_endpoint:", _endpoint)
                            print("_method:", _method)
                            print("desc_name:", desc_name)
                            print("omitiendo...")
                            continue

                        obj_request = {}
                        obj = {}

                        print("=================")
                        print("validando los params")
                        print("_endpoint:", _endpoint)
                        print("_method:", _method)
                        print("desc_name:", desc_name)

                        for item in params:
                            # print("param item", item)
                            disabled = False

                            if "disabled" in item:
                                disabled = item["disabled"]

                            if disabled is False:
                                # print("el item:", item["name"])
                                if "type" in item:
                                    if item["type"] == "file":
                                        obj = {"type": "string", "format": "binary"}
                                        obj_request["file"] = obj
                                else:
                                    name = [item["name"]][0]
                                    # print()
                                    # print("else del params item name:", name)
                                    obj = {"type": "string", "format": "uuid"}
                                    obj_request[name] = obj

                        request_body = {
                            "requestBody": {
                                "required": True,
                                "content": {
                                    mime_type: {
                                        "schema": {
                                            "type": "object",
                                            "properties": obj_request,
                                        }
                                    }
                                },
                            },
                        }
                    case _:
                        print("=================")
                        print("unknown mime_type:", mime_type)
                        print("_endpoint:", _endpoint)
                        print("_method:", _method)
                        print("desc_name:", desc_name)
                        print("omitiendo...")
                        continue

                # print("===========================")
                # print("armando el request_body")
                # print("_endpoint:", _endpoint)
                # print("_method:", _method)
                # print("desc_name:", desc_name)
                # print()

                # obj_request[_endpoint][_method].update(request_body)
            else:
                print("=================")
                print("no hay body", mime_type)
                print("_endpoint:", _endpoint)
                print("_method:", _method)
                print("desc_name:", desc_name)
                continue

        # print("obj_request")
        # print(obj_request)
        request_paths.update(obj_request)
        r_pause = 300
        # print("===========Aqui una pausa de ===========", r_pause)
        if i >= r_pause:
            break
        i += 1

    # print("============request_paths===============")
    # print(request_paths)
    # print("===========================")
    return request_paths


def create_schema(json_data):
    if "servers" in json_data:
        schema_export["servers"] = json_data["servers"]

    if "paths" in json_data:
        schema_export["paths"] = json_data["paths"]

    if "tags" in json_data:
        schema_export["tags"] = json_data["tags"]

    return schema_export

# TO FIX
def generate_v30x(file_name):
    """lee un archivo de insomnia v4"""

    json_data = open_file(file_name)
    # resources = None

    if json_data is None:
        print("generate_v30x: no se pudo leer el json_data")
        return None

    resources = validate_v4(json_data)
    print("listo para procesar...")
    # print(resources)
    # print("======================")

    envs_result = create_envs(resources["envs"])
    # print("create_envs:", envs_result)
    tags_result = create_tags(resources["groups"])
    groups_list = resources["groups"]
    # print("=============groups=============")
    # print(groups)
    # print("=============groups=============")
    paths_result = create_paths(resources["requests"], groups_list)

    create_schema({"servers": envs_result, "tags": tags_result, "paths": paths_result})
    print("listo!...")

    # print()
    # print("el json listo de oas303...")
    # print("=================================")
    # print(schema_export)
    return schema_export
