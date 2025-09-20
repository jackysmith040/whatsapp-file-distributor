import logging
from config import RULE_MAPPING, DEFAULT_WORKSPACE
from src.core.file_handler import FolderReader
from src.core.dispatcher import DispatcherController
from src.core.sorter import FileSorter
from src.core.sender import WhatsAppFileSender
from src.utils.logger import setup_logging

def main():
    """Main entry point for the application."""
    setup_logging()
    logging.info("--- WhatsApp PDF Distributor v4.0 ---")

    # --- PHASE 1: PREPARATION (Console only) ---
    folder_reader = FolderReader(workspace_path=DEFAULT_WORKSPACE)
    dispatcher = DispatcherController(rule_mapping=RULE_MAPPING)
    sorter = FileSorter()

    selected_folder = folder_reader.select_folder()
    if not selected_folder:
        logging.info("No folder selected. Exiting.")
        return

    queue, unmatched = dispatcher.get_processed_queue(target_folder=selected_folder)
    sorted_queue = sorter.sort_by_size(queue)

    if not sorted_queue:
        logging.info("Queue is empty. Nothing to send.")
        if unmatched: print("\nUnmatched files:", *[f.name for f in unmatched], sep="\n  - ")
        return

    print("\n--- Sending Plan ---")
    for item in sorted_queue: print(f"  - Send '{item['file_path'].name}' to '{item['group_name']}'")
    if input("\nProceed? (y/n): ").lower() not in ['y', 'yes']:
        print("Sending cancelled.")
        return

    # --- PHASE 2: AUTOMATION ---
    sender = WhatsAppFileSender()
    try:
        sender.initialize()
        successful, failed = sender.send_queue(sorted_queue)

        print("\n--- Sending Complete ---")
        print(f"✅ Successful sends: {len(successful)}")
        print(f"❌ Failed sends: {len(failed)}")
        if failed:
            print("Failed items:")
            for item in failed: print(f"  - '{item['file_path'].name}' to '{item['group_name']}'")

    except Exception as e:
        logging.critical(f"A critical error occurred in the main application: {e}")
    finally:
        sender.shutdown()
        logging.info("--- Application Finished ---")


if __name__ == "__main__":
    main()