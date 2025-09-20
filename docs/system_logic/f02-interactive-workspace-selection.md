# Logic Flow: F-02 - Interactive Workspace Selection

## 1. Objective
To provide a simple, interactive command-line interface for the user to select the specific folder of PDFs they wish to process for the current session.

## 2. Preconditions
- The application has been started by the user.
- The `config.py` file exists at the project root.
- The `DEFAULT_WORKSPACE` variable in `config.py` points to a valid, existing directory on the file system.

## 3. Success Workflow
1.  **START:** The feature is initiated by the `main.py` script.
2.  **Read Config:** The application reads the `DEFAULT_WORKSPACE` path string from `config.py`.
3.  **Scan for Directories:** The application scans the `DEFAULT_WORKSPACE` and compiles a list of all immediate sub-directories.
4.  **Display Options:** The application prints a numbered list of the discovered sub-directories to the console.
5.  **Prompt for Input:** The application prompts the user to select a folder by typing its corresponding number.
6.  **Receive and Validate Input:** The user enters their choice. The application validates that the input is a number and that it falls within the valid range of the list (e.g., between 1 and the total number of folders).
7.  **Confirm Selection:** The application displays the full path of the chosen folder and asks the user for final confirmation, e.g., "Process this folder? (y/n)".
8.  **Receive Confirmation:** The user enters 'y' or 'n'.
9.  **Store Path:** Upon receiving a 'y', the application stores the full, validated path of the selected folder in a variable for use in subsequent steps.
10. **END:** The feature's logic concludes successfully, passing control back to the main application flow.

## 4. Edge Cases & Error Handling
-   **Path Does Not Exist:** If the `DEFAULT_WORKSPACE` path from `config.py` does not point to a real directory, the application will print a fatal error message (e.g., "Error: Workspace directory not found at '[path]'") and exit gracefully.
-   **No Sub-directories Found:** If the `DEFAULT_WORKSPACE` is empty or contains no folders, the application will print an informational message (e.g., "No folders found in the workspace.") and exit.
-   **Invalid Numerical Input:** If the user's input at Step 6 is not a number or is outside the valid range, the application will print an error (e.g., "Invalid selection. Please enter a number from 1 to X.") and loop back to Step 5 (Prompt for Input).
-   **Selection Not Confirmed:** If the user enters 'n' at Step 8, the application will loop back to Step 4 (Display Options), allowing them to choose again.