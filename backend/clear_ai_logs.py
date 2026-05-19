import os
import sys

# Add backend directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.nhatky_ai import NhatKyChatAI

db = SessionLocal()
try:
    deleted = db.query(NhatKyChatAI).delete()
    db.commit()
    print(f"Successfully cleared {deleted} mock AI chat logs from database!")
except Exception as e:
    db.rollback()
    print(f"Error clearing logs: {e}")
finally:
    db.close()
