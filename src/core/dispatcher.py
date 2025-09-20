# Custom Dispatcher
# Basically In two parts
# File Discovery and File Queuing

import logging
from pathlib import Path
from typing import List, Dict, Any, Tuple

class DispatcherController:
    """
    A service class responsible for creating and hydrating the dispatch queue.
    """
    def __init__(self, rule_mapping: List[Dict[str, Any]]):
        self.rule_mapping = rule_mapping

    def _discover_pdfs(self, target_folder: Path) -> List[Path]:
        """Private method to find all PDF files in a given directory."""
        logging.info(f"Scanning for PDF files in '{target_folder.name}'...")
        return [
            file_path for file_path in target_folder.iterdir()
            if file_path.is_file() and file_path.suffix.lower() == '.pdf'
        ]

    def _create_base_queue(self, target_folder: Path) -> Tuple[List[Dict[str, Any]], List[Path]]:
        """Private method to apply mapping rules and create a base queue."""
        pdf_files = self._discover_pdfs(target_folder)
        if not pdf_files:
            return [], []

        logging.info(f"Found {len(pdf_files)} PDF file(s). Applying mapping rules...")
        base_queue = []
        unmatched_files = []

        for pdf_path in pdf_files:
            file_was_matched = False
            pdf_name_lower = pdf_path.name.lower()
            for rule in self.rule_mapping:
                if any(keyword.lower() in pdf_name_lower for keyword in rule.get("keywords", [])):
                    file_was_matched = True
                    for group_name in rule.get("target_groups", []):
                        base_queue.append({'file_path': pdf_path, 'group_name': group_name})
            if not file_was_matched:
                unmatched_files.append(pdf_path)
        return base_queue, unmatched_files

    def _hydrate_queue_with_sizes(self, base_queue: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Private method to add file sizes and handle FileNotFoundError."""
        logging.info("Hydrating queue with file sizes...")
        hydrated_queue = []
        for item in base_queue:
            try:
                file_path = item['file_path']
                file_size = file_path.stat().st_size
                item['file_size'] = file_size
                hydrated_queue.append(item)
            except FileNotFoundError:
                logging.warning(f"File not found during hydration, skipping: {item['file_path'].name}")
                continue
        return hydrated_queue

    def get_processed_queue(self, target_folder: Path) -> Tuple[List[Dict[str, Any]], List[Path]]:
        """
        Public method to orchestrate the creation and hydration of the queue.
        """
        base_queue, unmatched_files = self._create_base_queue(target_folder)
        hydrated_queue = self._hydrate_queue_with_sizes(base_queue)
        return hydrated_queue, unmatched_files