import inspect
import util
from collections import OrderedDict
import json
import pandas as pd

def renametables(*args):
    this_name   = inspect.currentframe().f_code.co_name
    input_file  = args[0]
    output_file = util.name_output_file(this_name,input_file,args)
    output_json = util.load_task_template(input_file=input_file)

    ##############################################################################################################################
    existing = util.get_existing_tables(task_json=output_json)

    # Tables do rename
    newtables = []
    df = pd.read_excel(args[1])
    for _, row in df.iterrows():
            owner = row.get("SCHEMA")
            name  = row.get("TABLE_NAME")
            new_owner = row.get("NEW_SCHEMA")
            new_name  = row.get("NEW_TABLE_NAME")
            
            if owner is None or name is None or new_owner is None or new_name is None:                
                continue

            key = (owner, name,new_owner,new_name)
            newtables.append(key)    

    tasks = output_json["cmd.replication_definition"]["tasks"][0]
        
    manipulations  = (
        tasks
        .get("manipulations",[])
    )
    if (len(manipulations)==0):
        output_json["cmd.replication_definition"]["tasks"][0]["manipulations"] = manipulations

    for owner, name, new_owner, new_name in newtables:
        key = (owner, name)
        if key not in existing:
            continue
        
        key = f"{owner}.{name}"
        
        # tabela ja foi manipulada ?
        manipulation = OrderedDict()
        for m in manipulations:            
            if m["name"]==key:
                manipulation = m
                break
        
        if len(manipulation)==0:
            # essa tabela nao foi manipulada
            manipulation["name"] = key
            manipulation["table_manipulation"] = OrderedDict()
            manipulations.append(manipulation)

        table_manipulation = manipulation.get("table_manipulation",[])
        if len(table_manipulation)==0:
            table_manipulation["owner"] = owner
            table_manipulation["name"]  = name
            table_manipulation["new_table_name"]=new_name
            table_manipulation["new_owner_name"]=new_owner
            table_manipulation["source_table_settings"] = OrderedDict()
            table_manipulation["source_table_settings"]["unload_segments"]= OrderedDict()
            table_manipulation["source_table_settings"]["unload_segments"]["ranges"] = OrderedDict()
            table_manipulation["source_table_settings"]["unload_segments"]["entry_names"] = OrderedDict()            

        else:
            table_manipulation["new_table_name"]=new_name
            table_manipulation["new_owner_name"]=new_owner

    ##############################################################################################################################
    
    return util.save_output(file=output_file,output_json=output_json)