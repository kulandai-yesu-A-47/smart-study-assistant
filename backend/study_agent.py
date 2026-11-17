
from backend.ai_service import generate_response


def run_study_agent(subject, hours, days):

    study_minutes = int(hours * 60)

    if study_minutes < 3:
        return "Please provide at least 3 minutes of study time."

    prompt = f"""
    Create a concise {days}-day learning plan for {subject}.

    Give exactly {days} numbered days.
    For each day, provide:
    - One learning topic
    - One practical task

    Do not include timings or schedules.
    Keep the response concise.
    """

    topics = generate_response(prompt)

    study_time = study_minutes // 2
    practice_time = study_minutes // 4
    revision_time = study_minutes - study_time - practice_time

    plan = f"AI Study Plan: {subject}\n"

    for day in range(1, days + 1):

        start = 10 * 60
        study_end = start + study_time
        practice_end = study_end + practice_time
        revision_end = practice_end + revision_time

        def format_time(minutes):
            hour = (minutes // 60) % 24
            minute = minutes % 60
            return f"{hour:02d}:{minute:02d}"

        plan += f"""
### Day {day}

**Learning:** {format_time(start)} - {format_time(study_end)}

**Practice:** {format_time(study_end)} - {format_time(practice_end)}

**Revision:** {format_time(practice_end)} - {format_time(revision_end)}

**Daily Total:** {hours} hours

"""

    plan += "\n### AI Suggested Topics and Tasks\n"
    plan += topics

    return plan
