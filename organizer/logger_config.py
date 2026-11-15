import logging
from pathlib import Path

def setup_logger():
    project_root = Path(__file__).resolve().parent.parent
    
    log_directory = project_root/'logs'
    log_directory.mkdir(parents=True,exist_ok=True)

    logger = logging.getLogger("Smart File Organization")
    logger.setLevel(logging.INFO)

    logger.propagate = False

    if logger.handlers:
        return logger

    log_file = log_directory/"organizer.log"

    file_handler = logging.FileHandler(
        log_file,
        encoding="utf-8"
    )

    # 7. Create console handler
    console_handler = logging.StreamHandler()

    # 8. Define log format
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 9. Apply formatter
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # 10. Attach handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
