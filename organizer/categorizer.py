from pathlib import Path

File_Categories = {
    '.pdf'  : 'Document',
    '.docx' : 'Document',
    '.txt'  : 'Document',
    '.jpg'  : 'Images',
    '.jpeg' : 'Images',
    '.bmp'  : 'Images',
    '.png'  : 'Images',
    '.mp3'  : 'Audios',
    '.mp4'  : 'Vedios',
    '.zip'  : 'Archives',
    '.mov'  : 'Vedios',
    '.mkv'  : 'Vedios',
    '.avi'  : 'Vedios',
    '.wav'  : 'Audios',
    '.aac'  : 'Audios',
    '.rar'  : 'Archives',
    '.7z'   : 'Archives'
}

def get_category(file_path):
      return (File_Categories.get(file_path.suffix,'others'))