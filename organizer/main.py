
from pathlib import Path

from organizer.scanner import scan_directory
from organizer.categorizer import get_category
from organizer.file_manager import create_category_folder, move_file
from organizer.duplicate_detector import find_duplicates
from organizer.logger_config import setup_logger


def main():

    # True = Preview only; False = Actually organize files
    DRY_RUN = False

    logger = setup_logger()

    base_path = Path("../organizer_test")

    logger.info("=" * 50)
    logger.info("File organizer started")
    logger.info("Mode: %s", "DRY RUN" if DRY_RUN else "LIVE")
    logger.info("Scanning directory: %s", base_path.resolve())

    try:
        # STEP 1: Scan directory
        files = scan_directory(base_path)

        logger.info("Found %d files", len(files))

        if not files:
            logger.info("No files found. Nothing to organize.")
            return

        # STEP 2: Detect duplicate files
        duplicates = find_duplicates(files)

        if duplicates:
            logger.warning("Duplicate files detected")

            for file_hash, duplicate_files in duplicates.items():
                logger.warning("Hash: %s", file_hash)

                for duplicate in duplicate_files:
                    logger.warning("Duplicate: %s", duplicate.name)
        else:
            logger.info("No duplicate files found")

        # STEP 3: Organize files
        moved_count = 0
        skipped_count = 0
        failed_count = 0

        for file in files:

            try:
                category = get_category(file)

                # Destination folder (only a path at this stage)
                folder = base_path / category

                # Find a unique destination filename
                destination_file = folder / file.name

                counter = 1

                while destination_file.exists():
                    new_name = f"{file.stem}_{counter}{file.suffix}"
                    destination_file = folder / new_name
                    counter += 1

                if DRY_RUN:
                    # Preview mode: Do not create folders or move files
                    logger.info(
                        "[DRY RUN] Would move: %s -> %s",
                        file.name,
                        destination_file
                    )

                    skipped_count += 1

                else:
                    # Live mode: Create folder and move file
                    folder = create_category_folder(
                        base_path,
                        category
                    )

                    result = move_file(file, folder)

                    logger.info("File moved successfully: %s", result)

                    moved_count += 1

            except (OSError, ValueError) as e:
                logger.error("Failed to process %s: %s", file, e)
                failed_count += 1

        # STEP 4: Summary
        logger.info("=" * 50)
        logger.info("ORGANIZATION SUMMARY")
        logger.info("Total files scanned: %d", len(files))
        logger.info("Files moved: %d", moved_count)

        if DRY_RUN:
            logger.info("Files included in preview: %d", skipped_count)

        logger.info("Failed files: %d", failed_count)
        logger.info("File organizer completed")
        logger.info("=" * 50)

    except (OSError, ValueError) as e:
        logger.error("Application failed: %s", e)


if __name__ == "__main__":
    main()
