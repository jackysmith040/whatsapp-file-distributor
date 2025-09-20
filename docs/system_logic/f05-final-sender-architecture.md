# Logic Flow: F-05 - Final Sender Architecture

## 1. High-Level Architecture (Composition)
This system uses a **Composition** approach. A main `WhatsAppFileSender` (Facade) coordinates the work, using a selected backend component (`PlaywrightSender` or `NeonizeSender`) to perform the platform-specific tasks. The backends themselves are internally modular, using private helper methods.

---

## 2. Part 1: `config.py` Specification
The `config.py` file requires two new variables.

```python
# Select the backend for sending WhatsApp messages.
# Options: "playwright", "neonize"
WHATSAPP_BACKEND = "playwright"

# Default time in minutes to wait between sending each message.
DEFAULT_STAGGER_MINUTES = 2
```

-----

## Part 2: `WhatsAppFileSender` (Facade) Logic Flow

This is the main service that orchestrates the sending process.

  - **File:** `src/core/sender.py`

**`send_queue(self, sorted_queue, stagger_minutes)` Logic:**

  - **Input:** `sorted_queue` (List), `stagger_minutes` (int)
  - **Output:** `successful_sends` (List), `failed_sends` (List)

**Workflow:**

1.  **START:** Receive `sorted_queue` and `stagger_minutes`.
2.  **INITIALIZE:** Create `successful_sends`, `failed_sends` lists. Ensure `_UNSENT_FILES/` directory exists.
3.  **ITERATE QUEUE:** For each `item` in `sorted_queue`, with an index `i`:
    a. Calculate a staggered send time `now + timedelta(minutes = (i * stagger_minutes))`.
    b. Log the scheduling of the file.
    c. **`try`**: Call `self.backend.send_file(...)`. If successful, add `item` to `successful_sends`.
    d. **`except Exception as e`**: Log the error, add `item` to `failed_sends`, and move the source file to `_UNSENT_FILES/`.
4.  **RETURN:** Return `successful_sends` and `failed_sends`.

-----

## Part 3: `PlaywrightSender` (Backend) Logic Flow

This component handles all browser automation.

  - **File:** `src/core/sender_backends/playwright_sender.py`

**Public Method: `send_file(...)` Workflow:**

1.  This method orchestrates a sequence of private helper methods in a `try...except` block.
2.  Each helper method will incorporate small, random, human-like delays.

**Private Helper Methods:**

  - **`_navigate_to_group(group_name)`:**
    1.  Type `group_name` into the chat search bar.
    2.  Click the first search result.
    3.  **Verify:** Read the text from the main chat header and confirm it matches the `group_name` before proceeding. If it doesn't match, raise a `VerificationError`.
  - **`_attach_file(file_path)`:**
    1.  Click the "attach" (paperclip) icon.
    2.  Click the "Document" button.
    3.  Input `file_path` into the OS file chooser.
  - **`_add_caption_and_send()`:**
    1.  Wait for the file preview to appear.
    2.  Fill the caption box with a pre-defined message.
    3.  Click the final "send" button.
    4.  Wait for an element that confirms the message has been sent (e.g., status ticks).

-----

## Part 4: `NeonizeSender` (Backend) Logic Flow (Placeholder)

  - **File:** `src/core/sender_backends/neonize_sender.py`

**Public Method: `send_file(...)` Workflow:**

1.  Orchestrates calls to its private helper methods (e.g., `_resolve_group_jid`, `_upload_and_send_document`).

<!-- end list -->

