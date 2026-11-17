
import ollama

def generate_response(prompt):
    response = ollama.chat(
        model="qwen2.5:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]


def summarize_text(text):
    prompt = f"""
    Summarize the following document.
    Give the main points in simple English.

    Document:
    {text}
    """

    return generate_response(prompt)

def generate_quiz(text):
    prompt = f"""
    Create 5 multiple-choice questions based on the following document.

    Each question must have:
    - One question
    - Four options (A, B, C, D)
    - Correct answer

    Document:
    {text}
    """

    return generate_response(prompt)

def generate_study_plan(subject, hours, days):
    prompt = f"""
    Create a practical study plan.

    Subject: {subject}
    Available hours per day: {hours}
    Number of days: {days}

    Divide the topics into daily tasks.
    Include revision time.
    Present the plan day by day.
    """

    return generate_response(prompt)

def explain_topic(topic):
    prompt = f"""
    Explain the following topic in simple English.

    Topic: {topic}

    Use clear and easy language.
    Keep the explanation beginner-friendly.
    """

    return generate_response(prompt)
