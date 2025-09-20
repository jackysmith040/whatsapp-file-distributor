# Logic Flow: F-03 (Revised) - Advanced Queuing Logic

## 1. Objective
To scan a target folder for PDF files and build a dispatch queue where a single file can be mapped to **multiple target groups** based on one or more matching keyword rules.

## 2. Success Workflow
1.  **START:** The feature is initiated with a `target_folder` and the `RULE_MAPPING`.
2.  **INITIALIZE:** Create two empty lists: `dispatch_queue` and `unmatched_files`.
3.  **SCAN FOLDER:** Find all PDF files in the `target_folder`.
4.  **ITERATE FILES:** For each PDF file found:
    a. Set a flag `file_was_matched = False`.
    b. **ITERATE RULES:** For each `rule` in the `RULE_MAPPING`:
        i. Check if any `keyword` in the rule's `keywords` list is present in the PDF's filename (case-insensitive).
        ii. If a keyword match is found:
            - Set `file_was_matched = True`.
            - **ITERATE GROUPS:** For each `group_name` in that rule's `target_groups` list:
                - Create a dispatch item: `{'file_path': <Path_to_PDF>, 'group_name': group_name}`.
                - Append the item to the `dispatch_queue`.
    c. After checking **all** rules, if `file_was_matched` is still `False`, add the PDF's path to the `unmatched_files` list.
5.  **RETURN:** After all files are processed, return the final `dispatch_queue` and `unmatched_files` lists.

---
# Logic Flow: F-03 - Automated Discovery & Queuing

## 1. Objective
To scan a target folder for PDF files, apply the predefined mapping rules from the configuration, and build a structured "dispatch queue" of files to be sent.

## 2. Preconditions
- The application has successfully completed F-02, providing a valid `selected_folder` path.
- The `GROUP_MAPPING` rules have been successfully loaded from `config.py`.

## 3. Data Structures
- **Input:**
    - `target_folder`: A `Path` object to the directory selected by the user.
    - `mapping_rules`: The `GROUP_MAPPING` list of dictionaries.
- **Output:**
    - `dispatch_queue`: A list of dictionaries. Each dictionary represents a file to be sent and has the format: `{'file_path': Path, 'group_name': str}`.
    - `unmatched_files`: A simple list of `Path` objects for all PDFs that did not match any rule.

## 4. Success Workflow
1.  **START:** The feature is initiated, receiving the `target_folder` and `mapping_rules`.
2.  **INITIALIZE:** Create two empty lists: `dispatch_queue` and `unmatched_files`.
3.  **SCAN FOLDER:** Scan the top level of the `target_folder` and create a list of all files ending with `.pdf` (case-insensitive).
4.  **ITERATE FILES:** For each PDF `Path` object found in the folder:
    a. Set a flag `match_found = False`.
    b. Get the lowercase version of the PDF's filename for matching.
    c. **ITERATE RULES:** For each `rule` dictionary in the `mapping_rules`:
        i. **ITERATE KEYWORDS:** For each `keyword` string in the rule's `keywords` list:
            - If the lowercase `keyword` is present in the lowercase filename:
                - Create a dispatch item: `{'file_path': <Path_to_PDF>, 'group_name': rule['group_name']}`.
                - Append this item to the `dispatch_queue`.
                - Set `match_found = True`.
                - **Break** the inner keyword and rule loops (adhering to the "first match wins" principle).
        ii. If `match_found` is `True`, break the rule loop.
    d. If, after checking all rules, `match_found` is still `False`, append the PDF's `Path` to the `unmatched_files` list.
5.  **RETURN:** After all PDF files have been processed, return the populated `dispatch_queue` and `unmatched_files` lists to the main application flow.

## 5. Edge Cases & Clarifications
-   **No PDFs Found:** If the scan in Step 3 yields no PDF files, the feature will correctly return two empty lists.
-   **Filename Matching Logic:** The matching is case-insensitive.
-   **Ambiguous Matches:** If a filename could match multiple rules in `config.py`, the **first rule that matches in the list wins**. The order of rules in the configuration file is therefore significant.

---

