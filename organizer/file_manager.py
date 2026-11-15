from pathlib import Path
import shutil

def create_category_folder(base_path,folder):
      base_path = Path(base_path)      
      destination = Path(base_path/folder)
      destination.mkdir(parents=True,exist_ok=True)
      return destination

def  move_file(source,destination):
        source = Path(source)
        destination = Path(destination)
        if not source.exists():
            raise FileNotFoundError(f"Source file does not exists : {source}")
        if not source.is_file():
            raise ValueError(f"Source is not a file : {source}")
        if not destination.exists():
            raise NotADirectoryError(f"Destination Directory does not exists : {destination}")
        if not destination.is_dir():
            raise ValueError(f"Destinatio  is not a directory : {destination}")
        
        destination_file = Path(destination/source.name)

        counter = 1
        while destination_file.exists():
              new_name = f"{source.stem}_{counter}{source.suffix}"
              destination_file = destination/new_name
              counter += 1
        
        shutil.move(str(source),str(destination_file))

        return destination_file