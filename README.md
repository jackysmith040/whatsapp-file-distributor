# WhatsApp PDF Distributor

A Python utility that automates sending PDF files from your desktop to specific WhatsApp groups based on keywords in the filenames. This tool is designed to streamline the process of distributing reports and documents reliably.

## ✨ Features

  * **Rule-Based Routing**: Uses a simple configuration file (`config.py`) to map filename keywords to one or more WhatsApp groups.
  * **Interactive Folder Selection**: Prompts you to choose which folder of reports to process each time it runs, making it highly flexible.
  * [cite\_start]**Prioritized Sending**: Automatically sorts the files to be sent by size, sending the smallest ones first for faster feedback. [cite: 1]
  * **Persistent Session**: Remembers your WhatsApp login, so you only need to scan the QR code once.
  * **Modular & Professional Structure**: Built with a clean architecture that separates configuration, services, and the main application logic for easy maintenance.

## 🚀 Getting Started

Follow these steps to get the application up and running.

### Prerequisites

  * Python 3.10 or newer.
  * Google Chrome browser installed.

### Installation & Setup

1.  **Place Files**: Ensure all project files are in a single folder. The structure should look like this:

    ```
    whatsapp_distributor/
    ├── config.py
    ├── main.py
    ├── requirements.txt
    └── src/
        └── ...
    ```

2.  **Install Dependencies**: Open your terminal in the project folder and install the required Python libraries from the `requirements.txt` file.

    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Your Rules**: Open the **`config.py`** file and edit the `RULE_MAPPING` section. This is where you define which documents go to which groups.

      * `keywords`: A list of words to look for in the PDF filename (case-insensitive).
      * `target_groups`: The exact name(s) of the WhatsApp group(s) or contact(s) to send the file to.

    <!-- end list -->

    ```python
    # Example from config.py
    # You can have more than one group.
    # Read my docs for better system design information.
    RULE_MAPPING = [
        {
            "keywords": ["system", "dynamical"],
            "target_groups": ["{group_name}"],
        },
        {
            "keywords": ["end"],
            "target_groups": ["{group_name}"],
        },
    ]
    ```

## ⚙️ How to Use

1.  **Organize Your Files**: Place the folders containing your PDF reports on your Desktop. The script uses your Desktop as the default workspace to look for these folders.

2.  **Run the Application**: Open your terminal in the project's root directory and run the main script.

    ```bash
    python main.py
    ```

3.  **First-Time Login**: The first time you run the script, a Chrome browser will open. You will need to scan the WhatsApp QR code with your phone to log in. The script will save your session so you won't have to do this again.

4.  **Follow the Prompts**: The script will ask you to select which folder you want to process and will show you a plan of which files will be sent. Confirm the plan to begin the automation.