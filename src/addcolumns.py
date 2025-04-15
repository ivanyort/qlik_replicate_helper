import inspect
import util
from collections import OrderedDict
import json
import pandas as pd
import fnmatch

def addcolumns(*args):
    this_name   = inspect.currentframe().f_code.co_name
    input_file  = args[0]
    output_file = util.name_output_file(this_name,input_file,args)
    output_json = util.load_task_template(input_file=input_file)
    
    ##############################################################################################################################
    existing = util.get_existing_tables(task_json=output_json)
    
    # columns to add
    newcolumns_rules = []
    df = pd.read_excel(args[1])
    for _, row in df.iterrows():
            owner_wildcard   = row.get("SCHEMA")
            naname_wildcard  = row.get("TABLE_NAME")            
            new_column       = row.get("NEW_COLUMN")
            value            = row.get("VALUE")
            type             = row.get("TYPE")
            lenght           = row.get("LENGHT")
            overwrite        = row.get("OVERWRITE")
            if owner_wildcard is None or naname_wildcard is None or new_column is None or value is None or type is None or lenght is None or overwrite is None:
                continue

            overwrite = overwrite.upper()

            key = (owner_wildcard, naname_wildcard, new_column,value,type,lenght,overwrite)
            newcolumns_rules.append(key) 

    newcolumns = []
    seen = set()  # armazena tuplas (owner, name, new_column)

    for owner_pattern, name_pattern, new_column, value, col_type, length, overwrite in newcolumns_rules:
        for owner, name in existing:
            if fnmatch.fnmatch(owner, owner_pattern) and fnmatch.fnmatch(name, name_pattern):
                key = (owner, name, new_column)
                if key not in seen:
                    seen.add(key)
                    newcolumns.append((owner, name, new_column, value, col_type, length, overwrite))

    newcolumns.sort(key=lambda x: (x[0], x[1], x[2]))

    tasks = output_json["cmd.replication_definition"]["tasks"][0]
        
    manipulations  = (
        tasks
        .get("manipulations",[])
    )
    if (len(manipulations)==0):
        output_json["cmd.replication_definition"]["tasks"][0]["manipulations"] = manipulations

    for owner, name, new_column, value, col_type, length, overwrite in newcolumns:
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
            table_manipulation["name"] =name                        

        transform_columns = table_manipulation.get("transform_columns",[])
        if len(transform_columns)==0:
            table_manipulation["transform_columns"] = transform_columns

        newentry = OrderedDict()     
        newentry["column_name"]=""
        newentry["new_column_name"]=new_column
        newentry["action"]="ADD"
        newentry["new_data_type"]=col_type
        newentry["length"]=lenght
        newentry["computation_expression"]=value                                                           

        # verifica se a coluna ja existe
        exists = 0
        for idx, existing_column in enumerate(transform_columns):
            if new_column==existing_column["new_column_name"]:
                if overwrite=="Y":
                    transform_columns[idx] = newentry
                exists = 1
                break

        if (exists==0):
            transform_columns.append(newentry)

    ##############################################################################################################################

    return util.save_output(file=output_file,output_json=output_json)
