import inspect
import util
from collections import OrderedDict
import json
import pandas as pd

def addtables(*args):
    this_name   = inspect.currentframe().f_code.co_name
    input_file  = args[0]
    output_file = util.name_output_file(this_name,input_file,args)
    output_json = util.load_task_template(input_file=input_file)

    ##############################################################################################################################
    existing = util.get_existing_tables(task_json=output_json)
    explicit = output_json["cmd.replication_definition"]["tasks"][0]["source"]["source_tables"]["explicit_included_tables"]

    # Tables do insert
    newtables = []
    df = pd.read_excel(args[1])
    for _, row in df.iterrows():
            owner = row.get("SCHEMA")
            name  = row.get("TABLE_NAME")
            if owner is None or name is None:
                # pula linhas sem os dois campos
                continue
            key = (owner, name)
            if key not in newtables and key not in existing:
                # adiciona novo registro ao JSON                
                newtables.append(key)    
    
    for owner, name in newtables:
        newentry = OrderedDict()
        newentry["owner"] = owner
        newentry["name"] = name
        newentry["estimated_size"] = 10000
        newentry["validation_sampling_percentage"] = 0
        explicit.append(newentry)
    ##############################################################################################################################

    return util.save_output(file=output_file,output_json=output_json)