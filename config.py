from pathlib import Path

# The directory where the script will look for folders containing PDFs.
home_directory = Path.home()
DEFAULT_WORKSPACE = home_directory / "Desktop"

# Maps keywords to a LIST of target groups.
RULE_MAPPING = [
    {
        "keywords": ["system", "dynamical"],
        "target_groups": ["iampeace"],
    },
    {
        "keywords": ["end"],
        "target_groups": ["iampeace"],
    },
]

# --- Sending Engine Settings ---
DEFAULT_STAGGER_MINUTES = 0.05

# --- Message Content ---
MESSAGE_CAPTION = "Here is the report you requested."

# --- Browser Backend Settings ---
USER_DATA_DIR = "selenium_user_data"
HEADLESS_MODE = False

# --- Backend Selectors (Simplified) ---
SELECTORS = {
    "search_box": ("xpath", '//*[@id="side"]/div[1]/div/div[2]/div/div/div[1]/p'),
    # Updated to use your static group selection XPath
    "search_result_by_name": (
        "xpath",
        '//*[@id="pane-side"]/div[1]/div/div/div[2]/div/div/div/div[2]',
    ),
    "attach_button": (
        "xpath",
        '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div/div[1]/div/span/div/div/div[1]/div[1]/span',
    ),
    "file_input": ("css", "input[accept*='*'][type='file']"),
    "caption_box": (
        "css",
        "div[data-testid='caption-input-container'] div[data-testid='caption-input']",
    ),
    "send_button": (
        "xpath",
        '//*[@id="app"]/div[1]/div[3]/div/div[2]/div[2]/span/div/div/div/div[2]/div/div[2]/div[2]/div/div/span',
    ),
}
