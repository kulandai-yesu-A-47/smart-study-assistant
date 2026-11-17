
from backend.ai_service import generate_response


def validate_study_plan(plan, hours, days):

    prompt = f"""
    Check this study plan.

    Available hours per day: {hours}
    Number of days: {days}

    Study Plan:
    {plan}

    Check:
    1. Does the plan contain exactly {days} days?
    2. Does each day stay within {hours} study hours?

    If valid, reply only: VALID

    If invalid, explain the problems briefly.
    """

    result = generate_response(prompt)

    return result.strip()


def run_study_agent(subject, hours, days):

    prompt = f"""
    Create a practical study plan.

    Subject: {subject}
    Available hours per day: {hours}
    Number of days: {days}

    Divide topics into daily tasks.
    Make sure each day stays within the available hours.
    Include revision time.
    """

    plan = generate_response(prompt)

    validation = validate_study_plan(plan, hours, days)

    if validation != "VALID":

        correction_prompt = f"""
        Correct this study plan based on the validation feedback.

        Subject: {subject}
        Available hours per day: {hours}
        Number of days: {days}

        Original plan:
        {plan}

        Validation feedback:
        {validation}

        Return the corrected plan.
        Make sure every day stays within the available hours.
        """

        plan = generate_response(correction_prompt)

    return plan
