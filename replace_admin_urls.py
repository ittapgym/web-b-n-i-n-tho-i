import os
import re

admin_dir = r"d:\peach_store\peach_admin"

def process_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    original = content
    
    # 1. replace 'http://127.0.0.1:8000' with the fallback checks
    # For normal JS/HTML strings, we can use the window.API_BASE variable or fallback
    # In order to make it cleaner, let's substitute it with window.API_BASE || 'http://127.0.0.1:8000'
    
    # Target 'http://127.0.0.1:8000' followed by anything that is not single quote
    content = re.sub(
        r"'http://127.0.0.1:8000([^']*)'",
        r"(window.API_BASE || 'http://127.0.0.1:8000') + '\1'",
        content
    )
    
    content = re.sub(
        r"\"http://127.0.0.1:8000([^\"]*)\"",
        r"(window.API_BASE || 'http://127.0.0.1:8000') + '\1'",
        content
    )

    # Target template literals: `http://127.0.0.1:8000...`
    content = re.sub(
        r"`http://127.0.0.1:8000([^`]*)`",
        r"`${window.API_BASE || 'http://127.0.0.1:8000'}\1`",
        content
    )

    if content != original:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated: {file_path}")
    else:
        print(f"No changes: {file_path}")

for root, dirs, files in os.walk(admin_dir):
    for file in files:
        if file.endswith((".html", ".js")):
            process_file(os.path.join(root, file))
