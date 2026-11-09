import re

from generative_ai.ollama_service import (
    generate_ai_response,
    generate_interview_response
)


def generate_interview_questions(
    target_career,
    skills=None,
    difficulty="medium",
    num_questions=5
):

    if not target_career:
        raise ValueError("Target career is required.")

    if difficulty not in ["easy", "medium", "hard"]:
        raise ValueError("Difficulty must be easy, medium, or hard.")

    if not 1 <= num_questions <= 10:
        raise ValueError("Number of questions must be between 1 and 10.")

    skills = skills or []

    # Define the main interview focus for each supported career.
    career_focus = {

        "ML Engineer": """
- Python programming for machine learning
- NumPy and Pandas
- Statistics and probability fundamentals
- Supervised and unsupervised learning
- Regression, classification, and clustering
- Model evaluation and cross-validation
- Feature engineering and model optimization
- Practical machine learning scenarios
""",

        "Data Analyst": """
- SQL queries, joins, and aggregations
- Python for data analysis
- Pandas and NumPy
- Statistics and probability
- Data cleaning and exploratory data analysis
- Excel and data visualization
- Analytical thinking and business scenarios
""",

        "Full Stack Developer": """
- JavaScript and React
- Node.js and Express.js
- REST API development
- MongoDB and SQL databases
- Authentication and authorization
- Frontend-backend integration
- Debugging and application architecture
"""
    }

    focus = career_focus.get(
        target_career,
        f"Technical concepts and practical scenarios relevant to {target_career}"
    )

    skill_text = ", ".join(skills) if skills else "No specific skills provided"

    prompt = f"""
You are an experienced technical interviewer conducting a placement
interview for the selected career.

USER'S CHOSEN CAREER: {target_career}

Candidate's resume skills:
{skill_text}

INTERVIEW TOPICS TO PRIORITIZE:
{focus}

Difficulty: {difficulty}

Generate exactly {num_questions} unique technical interview questions.

Question distribution:
- Cover the fundamental concepts of the selected career.
- Include practical implementation questions.
- Include scenario-based questions.
- Include questions that test problem-solving and technical understanding.
- Use the candidate's skills only when they are relevant to the selected career.

Strict rules:
- Every question must be relevant to {target_career}.
- Do not generate questions for an unrelated career.
- Do not ask React, Node.js, or MongoDB questions in an ML Engineer
  interview unless a question genuinely requires them.
- Do not ask questions merely because a technology appears in the resume.
- Match the requested difficulty.
- Do not provide answers, hints, or explanations.
- Make every question technically meaningful and suitable for a
  college placement interview.
- Do not repeat questions.

Output format:

INTERVIEW QUESTIONS

Q1. Question
Q2. Question
Continue until all {num_questions} questions are generated.
"""

    questions = generate_interview_response(prompt)

    return {
        "target_career": target_career,
        "difficulty": difficulty,
        "total_questions": num_questions,
        "skills": skills,
        "questions": questions
    }

def evaluate_interview_answer(question, answer, target_career):

    if not question.strip():
        raise ValueError("Interview question cannot be empty.")

    if not answer.strip():
        raise ValueError("Candidate answer cannot be empty.")

    prompt = f"""
You are an experienced technical interviewer.

Evaluate this candidate's answer fairly.

Target Career: {target_career}

Question:
{question}

Candidate Answer:
{answer}

Evaluate these four criteria:
1. Correctness
2. Clarity
3. Depth
4. Relevance

Use this concise format:

INTERVIEW EVALUATION

Score: X/10

Correctness:
Brief explanation.

Clarity:
Brief explanation.

Depth:
Brief explanation.

Relevance:
Brief explanation.

Strengths:
- Important strengths.

Areas for Improvement:
- Specific improvements.

Ideal Answer:
A technically accurate example of a strong answer.

Final Feedback:
Short constructive feedback.

Do not give undeserved high scores.
Evaluate only the answer provided.
Do not invent candidate experience or qualifications.
"""

    evaluation = generate_ai_response(prompt)

    return {
        "target_career": target_career,
        "question": question,
        "candidate_answer": answer,
        "evaluation": evaluation
    }


def generate_follow_up_question(question, answer, evaluation, target_career):

    if not question.strip():
        raise ValueError("Original question cannot be empty.")

    if not answer.strip():
        raise ValueError("Candidate answer cannot be empty.")

    prompt = f"""
You are an experienced technical interviewer.

Generate ONE practical follow-up question based on the candidate's answer.

Target Career: {target_career}

Original Question:
{question}

Candidate Answer:
{answer}

Evaluation:
{evaluation}

Identify a concept that needs deeper explanation.
Do not repeat the original question.
Do not provide an answer or hints.

Output:

FOLLOW-UP QUESTION

Question: Your follow-up question
"""

    follow_up = generate_ai_response(prompt)

    return {
        "target_career": target_career,
        "original_question": question,
        "follow_up_question": follow_up
    }


def evaluate_and_generate_follow_up(question, answer, target_career):

    prompt = f"""
You are an experienced technical interviewer.

Evaluate the candidate's answer and generate one adaptive follow-up question.

Target Career: {target_career}

Interview Question:
{question}

Candidate's Answer:
{answer}

Keep the evaluation concise but useful.

Evaluate:
1. Technical correctness
2. Clarity
3. Depth of understanding
4. Relevance to the question

Use EXACTLY this output structure:

INTERVIEW EVALUATION

Score: X/10

Correctness:
Brief explanation.

Clarity:
Brief explanation.

Depth:
Brief explanation.

Relevance:
Brief explanation.

Strengths:
- List important strengths.

Areas for Improvement:
- List specific improvements.

Ideal Answer:
Provide a technically accurate but concise example of a strong answer.

Final Feedback:
Give short constructive feedback.

FOLLOW-UP QUESTION

Question: Ask ONE practical question that explores a weakness or concept that needs deeper explanation in the candidate's answer.

Important:
- Be fair when assigning the score.
- Do not give undeserved high scores.
- Evaluate only the answer provided.
- Do not invent candidate experience or qualifications.
- Do not repeat the original question.
- Do not provide the follow-up answer or hints.
- Keep the complete response concise.
"""

    result = generate_interview_response(prompt)

    # Separate evaluation and follow-up question.
    match = re.search(
        r"FOLLOW[- ]UP QUESTION\s*:?\s*([\s\S]*)",
        result,
        re.IGNORECASE
    )

    if match:
        follow_up = match.group(1).strip()
        evaluation = result[:match.start()].strip()

    else:
        # Fallback: detect a question generated without the heading.
        question_match = re.search(
            r"(?:^|\n)Question:\s*(.+\?)",
            result,
            re.IGNORECASE
        )

        if question_match:
            follow_up = question_match.group(1).strip()
            evaluation = result[:question_match.start()].strip()
        else:
            evaluation = result.strip()
            follow_up = "Follow-up question could not be generated."

    return {
        "evaluation": evaluation,
        "follow_up_question": follow_up
    }


def generate_interview_summary(interview_results):

    scores = []

    for item in interview_results:
        match = re.search(
            r"Score:\s*(\d+(?:\.\d+)?)\s*/\s*10",
            item["evaluation"],
            re.IGNORECASE
        )

        if match:
            scores.append(float(match.group(1)))

    if not scores:
        return {
            "average_score": None,
            "performance_level": "Not Available",
            "message": "Unable to calculate interview score."
        }

    average_score = round(sum(scores) / len(scores), 2)

    if average_score >= 8:
        performance = "Excellent"
    elif average_score >= 6:
        performance = "Good"
    elif average_score >= 4:
        performance = "Needs Improvement"
    else:
        performance = "Poor"

    return {
        "average_score": average_score,
        "maximum_score": 10,
        "questions_evaluated": len(scores),
        "performance_level": performance
    }



def run_mock_interview(questions, answers, target_career):

    if not questions:
        raise ValueError("At least one interview question is required.")

    if len(questions) != len(answers):
        raise ValueError("Number of questions and answers must match.")

    interview_results = []

    for i in range(len(questions)):

        question = questions[i]
        answer = answers[i]

        if not question.strip() or not answer.strip():
            raise ValueError("Questions and answers cannot be empty.")

        print(f"\nEvaluating Answer {i + 1}/{len(questions)}...")

        # One AI request handles both evaluation and follow-up.
        result = evaluate_and_generate_follow_up(
            question=question,
            answer=answer,
            target_career=target_career
        )

        interview_results.append({
            "question_number": i + 1,
            "question": question,
            "answer": answer,
            "evaluation": result["evaluation"],
            "follow_up_question": result["follow_up_question"]
        })

    summary = generate_interview_summary(interview_results)

    return {
        "target_career": target_career,
        "total_questions": len(questions),
        "interview_summary": summary,
        "interview_results": interview_results
    }


if __name__ == "__main__":

    questions = [
        "What is overfitting in machine learning?"
    ]

    answers = [
        """
        Overfitting happens when a machine learning model
        learns the training data too well, including noise.
        It performs well on training data but poorly on
        unseen data. We can reduce it using regularization
        and cross-validation.
        """
    ]

    result = run_mock_interview(
        questions=questions,
        answers=answers,
        target_career="ML Engineer"
    )

    print("\n===== COMPLETE MOCK INTERVIEW REPORT =====")

    print("\nTarget Career:", result["target_career"])
    print("Total Questions:", result["total_questions"])

    for item in result["interview_results"]:

        print("\n===================================")
        print("Question:", item["question"])

        print("\nCandidate Answer:")
        print(item["answer"])

        print("\nAI Evaluation:")
        print(item["evaluation"])

        print("\nFollow-up Question:")
        print(item["follow_up_question"])


    print("\n===== OVERALL INTERVIEW SUMMARY =====")

    print("Average Score:",
        result["interview_summary"]["average_score"], "/10")

    print("Performance Level:",
        result["interview_summary"]["performance_level"])