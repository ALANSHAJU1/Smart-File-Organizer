
import streamlit as st
from pathlib import Path

from organizer.scanner import scan_directory
from organizer.categorizer import get_category
from organizer.file_manager import create_category_folder, move_file
from organizer.duplicate_detector import find_duplicates
from organizer.logger_config import setup_logger


# -------------------------------
# PAGE CONFIGURATION
# -------------------------------

st.set_page_config(
    page_title="Smart File Organizer",
    page_icon="📁",
    layout="wide"
)

st.title("📁 Smart File Organizer")
st.write("Automatically organize your files into categorized folders.")

logger = setup_logger()


# -------------------------------
# HELPER FUNCTION
# -------------------------------

def get_unique_destination(source, destination_folder):

    source = Path(source)
    destination_folder = Path(destination_folder)

    destination_file = destination_folder / source.name

    counter = 1

    while destination_file.exists():
        new_name = f"{source.stem}_{counter}{source.suffix}"
        destination_file = destination_folder / new_name
        counter += 1

    return destination_file


# -------------------------------
# SIDEBAR CONFIGURATION
# -------------------------------

st.sidebar.header("⚙️ Settings")

directory_path = st.sidebar.text_input(
    "Directory Path",
    placeholder="C:/Users/YourName/Downloads"
)

dry_run = st.sidebar.checkbox(
    "Enable Dry Run Mode",
    value=True,
    help="Preview file movements without changing your files."
)

if dry_run:
    st.sidebar.info("Preview mode: No files will be moved.")
else:
    st.sidebar.warning("Live mode: Files will actually be moved.")


# -------------------------------
# MAIN ORGANIZATION FUNCTION
# -------------------------------

if st.button("🚀 Organize Files", type="primary"):

    if not directory_path.strip():
        st.error("Please enter a directory path.")

    else:

        base_path = Path(directory_path).expanduser()

        if not base_path.exists():
            st.error("The specified directory does not exist.")

        elif not base_path.is_dir():
            st.error("The specified path is not a directory.")

        else:

            base_path = base_path.resolve()

            logger.info("Organization started: %s", base_path)
            logger.info("Mode: %s", "DRY RUN" if dry_run else "LIVE")

            with st.spinner("Scanning and processing files..."):

                try:

                    # STEP 1: Scan directory

                    files = scan_directory(base_path)

                    if not files:
                        st.info("No files found in the selected directory.")

                    else:

                        # STEP 2: Detect duplicates

                        duplicates = find_duplicates(files)

                        # STEP 3: Initialize counters

                        moved_count = 0
                        preview_count = 0
                        failed_count = 0

                        results = []

                        # STEP 4: Process files

                        for file in files:

                            try:

                                category = get_category(file)

                                folder = base_path / category

                                destination_file = get_unique_destination(
                                    file,
                                    folder
                                )

                                if dry_run:

                                    results.append({
                                        "File": file.name,
                                        "Category": category,
                                        "Destination": str(destination_file),
                                        "Status": "Preview"
                                    })

                                    logger.info(
                                        "[DRY RUN] Would move %s -> %s",
                                        file.name,
                                        destination_file
                                    )

                                    preview_count += 1

                                else:

                                    folder = create_category_folder(
                                        base_path,
                                        category
                                    )

                                    result = move_file(file, folder)

                                    results.append({
                                        "File": file.name,
                                        "Category": category,
                                        "Destination": str(result),
                                        "Status": "Moved"
                                    })

                                    logger.info(
                                        "File moved successfully: %s",
                                        result
                                    )

                                    moved_count += 1

                            except (OSError, ValueError) as e:

                                logger.error(
                                    "Failed to process %s: %s",
                                    file,
                                    e
                                )

                                results.append({
                                    "File": file.name,
                                    "Category": "Unknown",
                                    "Destination": "-",
                                    "Status": f"Failed: {e}"
                                })

                                failed_count += 1

                        # STEP 5: Display results

                        st.divider()

                        st.subheader("📊 Organization Summary")

                        col1, col2, col3, col4 = st.columns(4)

                        col1.metric("Files Scanned", len(files))

                        col2.metric(
                            "Duplicates Detected",
                            sum(len(group) for group in duplicates.values())
                        )

                        col3.metric(
                            "Files Previewed" if dry_run else "Files Moved",
                            preview_count if dry_run else moved_count
                        )

                        col4.metric("Failed", failed_count)

                        # STEP 6: Display duplicate information

                        if duplicates:

                            st.subheader("⚠️ Duplicate Files Detected")

                            for file_hash, duplicate_files in duplicates.items():

                                with st.expander(
                                    f"Duplicate group ({len(duplicate_files)} files)"
                                ):

                                    st.write(f"SHA-256: `{file_hash}`")

                                    for duplicate in duplicate_files:
                                        st.write(f"📄 {duplicate.name}")

                        else:

                            st.success("No duplicate files detected.")

                        # STEP 7: Display file processing table

                        st.subheader("📋 Processing Results")

                        st.dataframe(
                            results,
                            use_container_width=True,
                            hide_index=True
                        )

                        if dry_run:
                            st.info(
                                "Preview completed. Your original files "
                                "have not been moved."
                            )

                        elif failed_count == 0:
                            st.success("File organization completed successfully!")

                        else:
                            st.warning(
                                "Organization completed with some errors. "
                                "Check the results table and logs."
                            )

                        logger.info("Organization completed.")

                except (OSError, ValueError) as e:

                    logger.error("Application failed: %s", e)

                    st.error(f"An error occurred: {e}")


# -------------------------------
# FOOTER
# -------------------------------

st.divider()

st.caption("Smart File Organizer | Built with Python and Streamlit")
