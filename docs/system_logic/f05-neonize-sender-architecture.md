# Logic Flow: F-05 - NeonizeSender Backend

## 1. Objective
To design a service that uses the `neonize` library's direct API to connect to WhatsApp, resolve group names to their internal IDs (JIDs), and send PDF documents.

---

## 2. `NeonizeSender` Logic Flow
This document details the methods and logic for the `NeonizeSender` class.

- **File:** `src/core/sender_backends/neonize_sender.py`
- **Class:** `NeonizeSender`

### `__init__(self)` Method
- **Objective:** To initialize the `neonize` client instance.
- **Workflow:**
    1. Create an instance of the `NewClient`, providing a session name (e.g., from `config.py`).
    2. Store the client instance as `self.client`.

### `connect(self)` Method (Public)
- **Objective:** To establish a connection to WhatsApp.
- **Workflow:**
    1. Call `self.client.connect()`.
    2. The method should wait for a successful connection event before returning, or time out with an error if the connection fails.

### `disconnect(self)` Method (Public)
- **Objective:** To cleanly disconnect from WhatsApp.
- **Workflow:**
    1. Call the `neonize` client's method for closing the connection.

### `_resolve_group_jid(self, group_name: str)` Method (Private)
- **Objective:** To find the unique WhatsApp Group ID (JID) for a given human-readable group name. This is the most critical step.
- **Workflow:**
    1. Call the `neonize` client's function to get a list of all groups the user is subscribed to (e.g., `client.get_subscribed_groups()`).
    2. **ITERATE GROUPS:** For each `group` object in the returned list:
        a. Compare `group.name` with the `group_name` provided to this method.
        b. If a case-insensitive match is found, return the `group.jid`.
    3. If the loop completes without finding a match, raise a `GroupNotFoundError` with a message: "Could not find group '[group_name]'."

### `send_file(self, file_path: Path, group_name: str)` Method (Public)
- **Objective:** To send a specified PDF file to a group. This is the main method called by the `WhatsAppFileSender` facade.
- **Workflow:**
    1. **`try`** the following steps to gracefully handle API errors:
        a. **RESOLVE:** Call `jid = self._resolve_group_jid(group_name)`.
        b. **READ FILE:** Open `file_path` in binary read mode (`"rb"`) and read its contents into a variable `doc_data`.
        c. **BUILD MESSAGE:** Call `doc_msg = self.client.build_document_message(doc_data, filename=file_path.name, caption=MESSAGE_CAPTION, mime_type='application/pdf')`.
        d. **SEND:** Call `self.client.send_message(jid, message=doc_msg)`.
    2. **`except Exception as e`**:
        a. Log the specific error from the `neonize` library.
        b. Raise our standard `SendError` to notify the calling facade of the failure.