# Product Requirements Document: WhatsApp PDF Distributor v1.0

## 1. Overview
To create a Python script that automates sending specific PDF report files from a local folder to designated WhatsApp groups. The process is driven by matching patterns in the filenames to a predefined configuration, ensuring that the right report goes to the right audience reliably.

## 2. Core Features

-   **F-01: Configuration-Driven Mapping:** The application will not have hardcoded rules. Instead, it will read from a `config.py` file where the user can define which keywords in a filename map to which WhatsApp group names. This allows for easy updates without changing the core application logic.

-   **F-02: Interactive Workspace Selection:** The script will prompt the user to select the folder containing the PDF reports at runtime. This makes the tool flexible and avoids hardcoding file paths.

-   **F-03: Automated Discovery & Queuing:** The script will automatically scan the selected folder for all PDF files. It will then apply the mapping rules from the configuration to build an in-memory "dispatch queue" of files to be sent.

-   **F-04: Prioritized Sending (Size-Based Sorting):** To provide faster initial feedback, the entire dispatch queue will be sorted to send the smallest files first.

-   **F-05: WhatsApp Dispatch Engine:** The core sending logic will process the sorted queue one item at a time, using the `playwright` library to interface with WhatsApp Web and send the file to its target group.

-   **F-06: Real-time Feedback & Logging:** The user will see real-time status updates in the console as the script processes files. Simultaneously, a detailed log file will be generated for technical diagnostics and debugging.

-   **F-07: Robust Failure Handling:** If a file fails to send for any reason (e.g., WhatsApp Web issue), the application will not crash. It will move the problematic file to a dedicated `_UNSENT_FILES/` folder for manual review and continue with the rest of the queue.

-   **F-08: Final Execution Summary:** After processing the entire queue, the script will present a clear summary to the user, reporting the total number of successful sends and explicitly listing any files that failed.

## 3. Technical Stack (Proposed)
-   **Language:** Python 3.12
-   **Core Libraries:**
    -   `pathlib`: For robust, cross-platform file system path manipulation.
    -   `playwright`: For interfacing with WhatsApp Web to send messages.
    -   `logging`: For structured event logging for diagnostics.
    -   `icecream`: For enhanced debugging during development.