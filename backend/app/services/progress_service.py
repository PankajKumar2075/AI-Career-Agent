
from datetime import datetime, timezone

from backend.app.database import learning_progress_collection


def save_learning_progress(student_id, target_career, completed_weeks):

    progress_data = {
        "student_id": student_id,
        "target_career": target_career,
        "completed_weeks": completed_weeks,
        "updated_at": datetime.now(timezone.utc)
    }

    learning_progress_collection.update_one(
        {
            "student_id": student_id,
            "target_career": target_career
        },
        {
            "$set": progress_data
        },
        upsert=True
    )

    return {
        "message": "Learning progress saved successfully",
        "completed_weeks": completed_weeks
    }


def get_learning_progress(student_id, target_career):

    progress = learning_progress_collection.find_one(
        {
            "student_id": student_id,
            "target_career": target_career
        },
        {
            "_id": 0
        }
    )

    if progress is None:
        return {
            "student_id": student_id,
            "target_career": target_career,
            "completed_weeks": []
        }

    return progress
