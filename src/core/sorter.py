from typing import List, Dict, Any
import logging


class FileSorter:
    """
    A dedicated service class responsible for sorting the dispatch queue.
    """

    def sort_by_size(
        self, hydrated_queue: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Sorts a hydrated queue by the 'file_size' key in ascending order.
        """
        if not hydrated_queue:
            return []

        logging.info(
            f"Sorting dispatch queue with {len(hydrated_queue)} items by file size."
        )

        # The key is a lambda function that tells sorted() to look at the 'file_size'
        # value inside each dictionary for sorting.
        sorted_queue = sorted(hydrated_queue, key=lambda item: item.get("file_size", 0))

        return sorted_queue
