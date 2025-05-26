import os
from typing import List

def split_file_to_batches(input_file: str, output_dir: str, batch_size: int, header: bool = True) -> List[str]:
    os.makedirs(output_dir, exist_ok=True)
    output_files = []
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    if header:
        header_line = lines[0]
        data_lines = lines[1:]
    else:
        header_line = ''
        data_lines = lines

    for i in range(0, len(data_lines), batch_size):
        batch = data_lines[i:i+batch_size]
        batch_filename = os.path.join(output_dir, f'batch_{i // batch_size + 1}.csv')
        with open(batch_filename, 'w', encoding='utf-8') as out:
            if header:
                out.write(header_line)
            out.writelines(batch)
        output_files.append(batch_filename)

    return output_files