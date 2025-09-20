from pathlib import Path
from typing import List, Dict, Any, Tuple
from config import DEFAULT_WORKSPACE


class FolderReader:
    """
    A service class responsible for all interactions with the file system
    related to finding, selecting, and interpreting folders.
    """

    def __init__(self, workspace_path: str | Path = DEFAULT_WORKSPACE):
        self.workspace = Path(workspace_path)


    def select_folder(self) -> Path | None:
        """
        Interactively prompts the user to select a sub-directory from the workspace.
        (This method remains unchanged from the previous implementation)
        """
        if not self.workspace.is_dir():
            print(f"❌ Error: Workspace directory not found at '{self.workspace}'")
            return None

        sub_folders = [f for f in self.workspace.iterdir() if f.is_dir()]
        if not sub_folders:
            print(f"ℹ️ Info: No folders found in the workspace: '{self.workspace}'")
            return None

        while True:
            print("\nPlease select a folder to process:")
            for i, folder in enumerate(sub_folders, 1):
                print(f"  [{i}] {folder.name}")

            try:
                choice_str = input("Enter the number of your choice: ")
                choice_idx = int(choice_str) - 1
                if 0 <= choice_idx < len(sub_folders):
                    selected_path = sub_folders[choice_idx]
                else:
                    print("⚠️ Invalid number. Please try again.")
                    continue
            except ValueError:
                print("⚠️ That's not a number. Please try again.")
                continue

            while True:
                confirm_str = input(
                    f"\nYou have selected: '{selected_path.name}'. Process this folder? (y/n): "
                ).lower()
                if confirm_str in ["y", "yes"]:
                    return selected_path
                elif confirm_str in ["n", "no"]:
                    break
                else:
                    print("⚠️ Invalid input. Please enter 'y' or 'n'.")

            print("\nReturning to folder list...")
