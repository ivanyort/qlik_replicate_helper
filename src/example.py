import inspect
import util
from collections import OrderedDict
import json

def example(*args):
    this_name   = inspect.currentframe().f_code.co_name
    input_file  = args[0]
    output_file = util.name_output_file(this_name,input_file,args)
    output_json = util.load_task_template(input_file=input_file)

    ##############################################################################################################################
    ##############################################################################################################################

    return util.save_output(file=output_file,output_json=output_json)