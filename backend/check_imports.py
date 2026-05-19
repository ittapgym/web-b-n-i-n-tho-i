import sys
import os
sys.path.append(os.getcwd())

try:
    from app.main import app  # noqa: F401
    print("Import success!")
except Exception as e:
    print(f"Import failed: {e}")
    import traceback
    traceback.print_exc()
