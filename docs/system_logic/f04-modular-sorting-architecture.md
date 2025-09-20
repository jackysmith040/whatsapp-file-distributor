# Logic Flow: F-04 - Modular Sorting Architecture

This document details the three distinct logical components required to implement the sorting feature according to the director's design.

---

### **Part 1: `DispatcherController._create_base_queue`**

-   **Objective:** To apply the additive mapping rules to a folder of PDFs and produce a "base" queue. This method is kept pure and does not interact with the file system beyond discovering files.
-   **Input:** `target_folder` (Path), `rule_mapping` (List)
-   **Output:** `base_queue` (List of dictionaries: `{'file_path': Path, 'group_name': str}`)

**Workflow:**
1.  **START:** Receive `target_folder` and `rule_mapping`.
2.  **INITIALIZE:** Create `base_queue = []` and `unmatched_files = []`.
3.  **DISCOVER:** Find all PDF file paths in the `target_folder`.
4.  **ITERATE FILES:** For each `pdf_path`:
    a. Set `file_was_matched = False`.
    b. **ITERATE RULES:** For each `rule` in `rule_mapping`:
        i. If a keyword in the `rule` matches the `pdf_path`'s name:
            - Set `file_was_matched = True`.
            - For each `group_name` in the rule's `target_groups`, append `{'file_path': pdf_path, 'group_name': group_name}` to `base_queue`.
    c. If `file_was_matched` is `False`, append `pdf_path` to `unmatched_files`.
5.  **RETURN:** Return the `base_queue` and `unmatched_files`.

---

### **Part 2: `DispatcherController._hydrate_queue_with_sizes`**

-   **Objective:** To "hydrate" the base queue by adding file size information and to handle any files that may have been deleted since discovery.
-   **Input:** `base_queue` (List of dictionaries)
-   **Output:** `hydrated_queue` (List of dictionaries: `{'file_path': Path, 'group_name': str, 'file_size': int}`)

**Workflow:**
1.  **START:** Receive the `base_queue`.
2.  **INITIALIZE:** Create an empty list: `hydrated_queue`.
3.  **ITERATE QUEUE:** For each `item` in the `base_queue`:
    a. **`try`** to get the file size in bytes from `item['file_path'].stat().st_size`.
    b. If successful:
        i. Add a new key to the item: `item['file_size'] = size`.
        ii. Append the now-hydrated `item` to `hydrated_queue`.
    c. **`except FileNotFoundError`**:
        i. Log a warning: "File not found during hydration, it may have been deleted: [filename]".
        ii. **`continue`** to the next item (this effectively filters out the missing file).
4.  **RETURN:** Return the `hydrated_queue`.

---

### **Part 3: `FileSorter.sort_by_size`**

-   **Objective:** To perform a clean, single-responsibility sort on a hydrated queue.
-   **Input:** `hydrated_queue` (List of dictionaries)
-   **Output:** `sorted_queue` (The same list, but sorted)

**Workflow:**
1.  **START:** Receive the `hydrated_queue`.
2.  **VALIDATE:** If the queue is empty, return it immediately.
3.  **SORT:** Sort the `hydrated_queue` list in-place or return a new sorted list. The sort key is the value of each dictionary's `'file_size'` key. The order is ascending.
4.  **RETURN:** Return the `sorted_queue`.