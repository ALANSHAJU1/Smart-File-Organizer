import hashlib
from pathlib import Path

def calculate_file_hash(file_path):
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found : {file_path}")
    
    if not file_path.is_file():
        raise ValueError(f"Not a file : {file_path}")

    sha256 = hashlib.sha256()

    with open(file_path,'rb')as file:
        while True:
            chunk = file.read(4096)
        
            if not chunk:
               break
            
            sha256.update(chunk)

    return sha256.hexdigest()

def find_duplicates(files):
    hash_dic = {}

    for file in files:
        hash = calculate_file_hash(file)
        if hash not in hash_dic:
            hash_dic[hash] = []

        hash_dic[hash].append(Path(file))

    duplicates = {}
    for hash,file in hash_dic.items():
        if len(hash_dic[hash]) > 1:
            duplicates[hash] = file

    return duplicates
