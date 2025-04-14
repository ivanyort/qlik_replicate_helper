import inspect
import util
from collections import OrderedDict
import json

def renametask(*args):
    # function name
    this_name = inspect.currentframe().f_code.co_name
    # args[0] is the input file path
    input_file = args[0]
    # generate the output filename
    output_file = util.name_output_file(this_name,input_file,args)

    with open(input_file, "r") as f:
        data = json.load(f, object_pairs_hook=OrderedDict)

    #######
    # code
    output_json = data
    output_json["cmd.replication_definition"]["tasks"][0]["task"]["name"] = args[1]
    #######

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(
            output_json,
            f,
            ensure_ascii=False,  # if you want UTF‑8 output
            indent=4             # pretty‑print with 2‑space indents
        )

    return output_file
