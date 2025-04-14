import inspect
import os
import re
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