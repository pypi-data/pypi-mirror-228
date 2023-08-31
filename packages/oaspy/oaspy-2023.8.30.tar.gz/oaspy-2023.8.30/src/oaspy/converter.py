# -*- coding: utf-8 -*-

from .openapi import generate_v30x
from .utils import save_file


def convert(file_name, from_schema=None, output_file=None):
    if from_schema == "v30":
        result_oa3 = generate_v30x(file_name)

        if result_oa3 is not None:
            print("generando archivo de OpenApi 3.0.x...")
            output_file_name = output_file or "export_openapi_v303.json"
            save_file(output_file_name, result_oa3)
    elif from_schema == "v31":
        print("convert Error: not implemented yet...")
        # raise NotImplementedError("convert: Can't use openapi v3.1.x yet!")
    else:
        print("convert Error: unknow schema...")
