
from backend.app.database import check_database_connection

try:
    check_database_connection()
except Exception as e:
    print("MongoDB connection failed:", e)
