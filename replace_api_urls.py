import os
import re

frontend_dir = r"d:\peach_store\frontend\src"

def process_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    original = content
    
    # 1. Replace 'http://127.0.0.1:8000' or "http://127.0.0.1:8000" in normal strings
    # We want to replace it with `${import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'}` if it's used inside a template literal,
    # or if we are inside normal single quotes like 'http://127.0.0.1:8000/api/admin/loyalty-configs', we can convert the single quotes to template literals
    # Example: 'http://127.0.0.1:8000/xyz' -> `${import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'}/xyz`
    
    # Let's target: 'http://127.0.0.1:8000' followed by path, enclosed in single quotes
    # E.g., 'http://127.0.0.1:8000/api/admin/loyalty-configs'
    content = re.sub(
        r"'http://127.0.0.1:8000([^']*)'",
        r"`${import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'}\1`",
        content
    )
    
    # Target double quotes similarly
    content = re.sub(
        r"\"http://127.0.0.1:8000([^\"]*)\"",
        r"`${import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'}\1`",
        content
    )

    # Target template literals: `http://127.0.0.1:8000...`
    # E.g., `http://127.0.0.1:8000/don-hang/xoa/${orderId}`
    # E.g., `http://127.0.0.1:8000${url}`
    content = re.sub(
        r"`http://127.0.0.1:8000([^`]*)`",
        r"`${import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'}\1`",
        content
    )

    # 2. Specific case: in api.js files where it's assigned to a constant or key-value
    # const API_BASE = 'http://127.0.0.1:8000'
    content = content.replace(
        "const API_BASE = 'http://127.0.0.1:8000'",
        "const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'"
    )
    # baseURL: 'http://127.0.0.1:8000',
    content = content.replace(
        "baseURL: 'http://127.0.0.1:8000',",
        "baseURL: import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000',"
    )

    if content != original:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated: {file_path}")
    else:
        print(f"No changes: {file_path}")

for root, dirs, files in os.walk(frontend_dir):
    for file in files:
        if file.endswith((".vue", ".js")):
            process_file(os.path.join(root, file))
