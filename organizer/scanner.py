from pathlib import Path

def scan_directory(path):
      path = Path(path)

      if not path.exists():
            print("Directory does not exists")
            return []

      if not path.is_dir():
            print("The path is not a directory")
      
      files = []
      for item in path.iterdir():
              if item.is_file():
                     files.append(item)

      return files