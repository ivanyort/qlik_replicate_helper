import inspect
import util
from collections import OrderedDict
import json

def renametask(*args):
    this_name   = inspect.currentframe().f_code.co_name
    input_file  = args[0]
    output_file = util.name_output_file(this_name,input_file,args)
    output_json = util.load_task_template(input_file=input_file)

    ##############################################################################################################################
    output_json["cmd.replication_definition"]["tasks"][0]["task"]["name"] = args[1]
    ##############################################################################################################################

    return util.save_output(file=output_file,output_json=output_json)