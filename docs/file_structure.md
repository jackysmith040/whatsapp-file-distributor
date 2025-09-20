report_whatsapp_automation:
    docs:
        tasks:
            tasks.md
        brainstormed_thought_process.md
        draft_thought_process.md
        file_structure.md
        prd.md
        session_summary.md

    src:
        __init__.py
        core:
            __init__.py
            dispatcher.py   # Builds and processes the send queue
            file_handler.py # Scans directories and finds files
            sender.py       # Handles the playwright sending logic
            sorter.py       # Handles the sorting based on file size
        utils:
        __init__.py
        logger.py       # Logging configuration

    .gitignore
    config.py               # User-facing configuration
    main.py                 # Main entry point of the application
    README.md
    requirements.txt
