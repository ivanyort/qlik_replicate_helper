import inspect
import util
from collections import OrderedDict
import json
import pandas as pd

def addtables(*args):
    # function name
    this_name = inspect.currentframe().f_code.co_name
    # args[0] is the input file path
    input_file = args[0]
    # generate the output filename
    output_file = util.name_output_file(this_name,input_file,args)

    with open(input_file, "r") as f:
        data = json.load(f, object_pairs_hook=OrderedDict)

    ##########################################
    output_json = data

    # Existing tables
    tasks = output_json["cmd.replication_definition"]["tasks"]
    existing = []
    
    first = tasks[0]
    explicit  = (
        first
        .get("source")
        .get("source_tables")
        .get("explicit_included_tables",[])
    )
    # se explicit_included_tables não existe entao garantimos que ele exista com uma lista vazia. Assim mantemos os pointeiros de referencia
    if (len(explicit)==0):
        first["source"]["source_tables"]["explicit_included_tables"] = explicit

    for tbl in explicit:
        owner = tbl.get("owner")
        name  = tbl.get("name")
        existing.append((owner, name))

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

    #######

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(
            output_json,
            f,
            ensure_ascii=False,  # if you want UTF‑8 output
            indent=4             # pretty‑print with 2‑space indents
        )

    return output_file
