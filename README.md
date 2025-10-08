***
# WhatsApp PDF Distributor

A Python utility that automates sending PDF files from your desktop to specific WhatsApp groups based on keywords in the filenames. This tool is designed to streamline the process of distributing reports and documents reliably.

## ✨ Features

- **Rule-Based Routing**: Supports defining filename keyword to WhatsApp group mappings either directly inside `config.py` or externally via a CSV file for dynamic configuration.
- **Interactive Folder Selection**: Prompts you to choose which folder of reports to process each time it runs, making it highly flexible.
- **Prioritized Sending**: Automatically sorts files by size, sending the smallest first for faster feedback.
- **Persistent Session**: Saves your WhatsApp login session, so QR code scanning is only needed once.
- **Modular \& Professional Structure**: Clean separation between configuration, services, and main app logic for easy maintenance.


## 📢 New: CSV-Based Mapping Rules

You can now define your mapping rules externally in a CSV file instead of modifying `RULE_MAPPING` directly in `config.py`. This allows non-programmers to update routing rules easily without touching the source code.

### Example CSV Structure (`rule_mapping.csv`):

| keywords | target_groups |
| :-- | :-- |
| system;dynamical | alpha |
| end | beta;gamma |

- Separate multiple values with semicolons (`;`).
- The column names correspond to the keys used in the rule dictionaries (`keywords`, `target_groups`).
- The program parses this CSV and dynamically applies the mappings at runtime.
- This supports multiple values per key as lists.


### How it works

- Each row in the CSV corresponds to one mapping rule.
- Values in each cell are split by semicolons into a list.
- Your software uses these dynamic rules to route PDF files to the correct WhatsApp groups based on filename keywords.

***

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or newer
- Google Chrome installed (for WhatsApp Web access)


### Installation \& Setup

1. **Place Files**: Ensure all project files are in a single directory, e.g.:
```
whatsapp_distributor/
├── config.py
├── main.py
├── requirements.txt
├── rule_mapping.csv   # (CSV for mapping rules, optional if you want to use CSV input)
└── src/
    └── ...
```

2. **Create a Virtual Environment** (Recommended; isolates dependencies)

#### Windows

Open Command Prompt or PowerShell and run:

```powershell
python -m venv venv
.\venv\Scripts\activate
```


#### MacOS / Linux (Ubuntu, Mint)

Open Terminal and run:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install Dependencies**

Once virtual environment is active, install required packages:

```bash
pip install -r requirements.txt
```

4. **Configure Mapping Rules**

- To configure directly in code, edit `RULE_MAPPING` in `config.py`.
- To configure using CSV, edit `rule_mapping.csv` following the example above.

***

## 📂 Running the Application

Start the app with:

```bash
python main.py
```

- On the first run, a Chrome window will open asking you to scan the WhatsApp QR code.
- The session will be saved so you won’t need to scan again in future runs.
- You will be prompted to select the folder containing your PDF reports for sending.

***

## 💡 Useful Tips

- Keep your mapping rule keys fixed; only update values either in the CSV or `config.py`.
- Use semicolons (`;`) within CSV cells to separate multiple keywords or target groups.
- Always activate your project's virtual environment before running the application to ensure consistent dependencies.
- Organize your PDF files in clearly named folders on your Desktop for easy selection.
- For troubleshooting, verify your Chrome browser and Python version meet the prerequisites.
- If WhatsApp Web changes, updating Chrome or the WhatsApp Web client might be necessary for compatibility.

***
