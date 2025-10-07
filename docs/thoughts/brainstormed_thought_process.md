# Project Plan: WhatsApp PDF Distributor

## 1. Project Goal
To create a Python script that automates the process of sending specific PDF report files from a local folder to designated WhatsApp groups based on pattern matching in the filenames.

## 2. User Story
As a user, I want to run a script that:
1.  Prompts me to select a folder containing PDF reports.
2.  Automatically identifies which reports go to which WhatsApp groups based on predefined rules.
3.  Sends the files in an orderly fashion, sorted by size (smallest first).
4.  Provides feedback on the process.
5.  Reliably handles failures by setting aside any files that could not be sent.

## 3. Core Workflow
The script will operate in a two-phase model:

### Phase 1: Discovery & Queuing
1.  **Initialize:** The script starts and loads the mapping configuration from a `config.py` file.
2.  **Select Workspace:** Prompts the user to select a directory from the default workspace (e.g., the Desktop). A confirmation step is included.
3.  **Scan & Match:** The script scans the selected directory for all PDF files. It applies the mapping rules (keywords/regex) to each filename to determine the target WhatsApp group.
4.  **Build Queue:** It creates an in-memory "dispatch queue." Each item in the queue will be an object or dictionary containing the full file path and its target group name.
5.  **Sort Queue:** The entire queue is sorted based on file size, from smallest to largest, to ensure quicker feedback on initial sends.

### Phase 2: Processing & Sending
1.  **Iterate Queue:** The script begins processing the sorted dispatch queue, one file at a time.
2.  **Send Message:** For each file, it uses `pywhatkit` to send the file to the target WhatsApp group.
3.  **Log Events:** The script provides real-time updates to the user (e.g., "Sending 'report.pdf' to 'CEO Group'...") and logs events to a file for debugging.
4.  **Handle Failures:** If `pywhatkit` fails to send a file, the script will add the item to a "failed items" list. The original file is then moved to a predefined `_UNSENT_FILES/` directory.
5.  **Completion Summary:** Once the queue is empty, the script provides a summary to the user, reporting how many files were sent successfully and explicitly listing any files that failed.

## 4. Technical Stack
-   **Language:** Python 3.12
-   **Core Libraries:**
    -   `pathlib`: For robust, cross-platform file system path manipulation.
    -   `pywhatkit`: For interfacing with WhatsApp Web to send messages.
    -   `logging`: For structured event logging for diagnostics.
    -   `icecream`: For enhanced debugging during development.

## 5. Key Architectural Decisions
-   **Configuration-driven Mapping:** The logic for mapping filenames to WhatsApp groups will be externalized to a `config.py` file to allow for easy updates without changing application code.
    ```python
    # config.py example
    GROUP_MAPPING = [
        {"group_name": "CEO Page", "keywords": ["overall daily sales", "total sales"]},
        {"group_name": "Kumasi Group", "keywords": ["kumasi", "knust"]},
    ]
    ```
-   **Modularity (Service Locator):** Core components (e.g., `FolderReader`, `WhatsappSender`) will be managed via a dictionary, allowing for easy dependency swapping and testing (a simple form of Inversion of Control).
-   **Decoupled Phases:** The strict separation of the "Discovery & Queuing" phase from the "Processing & Sending" phase makes the system more resilient and easier to debug.

## 6. Error Handling
-   **Unsent Files Directory:** A dedicated `_UNSENT_FILES/` folder will be created in the selected workspace to store any files that fail to send.
-   **Clear Reporting:** The user will be explicitly notified of any failures at the end of the script's execution, with a clear list of the affected files.

## 7. Identified Risks & Constraints
-   **`pywhatkit` Dependency:** The core functionality relies on the `pywhatkit` library, which automates a web browser. This introduces potential fragility:
    -   The script may break if WhatsApp updates its web interface.
    -   It requires the user to be logged into WhatsApp Web and have their phone connected.
    -   The sending process can be slow compared to an API-based method.
-   **Not for Unattended Use:** Due to the `pywhatkit` dependency, this tool is best suited for interactive, user-initiated sessions rather than as a fully automated, background server process.