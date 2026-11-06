
from backend.app.services.progress_service import (
    save_learning_progress,
    get_learning_progress
)

student_id = "student_001"
target_career = "ML Engineer"

# Save completed weeks
save_result = save_learning_progress(
    student_id,
    target_career,
    [1, 2, 3]
)

print("Save Result:", save_result)

# Retrieve saved progress
progress = get_learning_progress(
    student_id,
    target_career
)

print("Retrieved Progress:", progress)
