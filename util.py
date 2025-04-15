import inspect
import os
import re
import json
from collections import OrderedDict
from pathlib import Path
from main import next_seq

def name_output_file(this_name,input_file,args):
    # próxima sequência
    seq = next_seq()    

    # separa o diretório do nome do arquivo
    dir_name = os.path.dirname(input_file)

    # separa nome base e extensão
    base_name, ext = os.path.splitext(os.path.basename(input_file))

    # opcional: limpa sufixos numéricos conforme seu padrão
    _pattern = re.compile(r'^(?P<name>.*)_(?P<numbers>\d+)_(?P<other>[^_]+)$')
    m = _pattern.match(Path(base_name).stem)
    if m:
        base_name = m.group('name')

    seq_padded = f"{seq:02d}"

    # monta o nome do arquivo de saída
    new_filename = f"{base_name}_{seq_padded}_{this_name}{ext}"

    # junta com o diretório original
    output_file = os.path.join(dir_name, new_filename)
    
    print(f"Executing step {seq} {args} -> {output_file}")
    return output_file

def get_existing_tables(task_json):    
    tasks = task_json["cmd.replication_definition"]["tasks"]
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

    return existing

def save_output(file,output_json):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(
            output_json,
            f,
            ensure_ascii=False,
            indent=4
        )
    return file

def load_task_template(input_file):
    with open(input_file, "r") as f:
        data = json.load(f, object_pairs_hook=OrderedDict)
    return data
