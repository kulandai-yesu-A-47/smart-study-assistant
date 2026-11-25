import json

from backend.ai_service import generate_response

MAX_ATTEMPTS = 3          # how many times the agent may retry the AI plan
START_HOUR = 10           # daily study starts at 10:00


# ---------------------------------------------------------------
# TOOL 1: JSON reader (extracts a JSON list from the AI text)
# ---------------------------------------------------------------
def parse_plan(raw_text):
    """Returns a Python list if the AI text contains a JSON list, else None."""
    start = raw_text.find("[")
    end = raw_text.rfind("]")

    if start == -1 or end == -1 or end <= start:
        return None

    try:
        data = json.loads(raw_text[start:end + 1])
    except json.JSONDecodeError:
        return None

    return data if isinstance(data, list) else None


# ---------------------------------------------------------------
# TOOL 2: Validator (checks the AI plan, returns a list of problems)
# ---------------------------------------------------------------
def validate_plan(plan, days):
    if plan is None:
        return ["The output was not a valid JSON array."]

    problems = []

    if len(plan) != days:
        problems.append(f"Expected exactly {days} items but got {len(plan)}.")

    seen_topics = set()

    for number, item in enumerate(plan, start=1):

        if not isinstance(item, dict):
            problems.append(f"Item {number} must be an object with 'topic' and 'task'.")
            continue

        topic = str(item.get("topic", "")).strip()
        task = str(item.get("task", "")).strip()

        if not topic:
            problems.append(f"Day {number} has an empty topic.")
        if not task:
            problems.append(f"Day {number} has an empty task.")

        if topic and topic.lower() in seen_topics:
            problems.append(f"Day {number} repeats the topic '{topic}'.")
        seen_topics.add(topic.lower())

    return problems


# ---------------------------------------------------------------
# TOOL 3: Scheduler (pure Python time calculation)
# ---------------------------------------------------------------
def format_time(minutes):
    hour = (minutes // 60) % 24
    minute = minutes % 60
    return f"{hour:02d}:{minute:02d}"


def build_schedule(hours):
    total = int(hours * 60)
    learning = total // 2
    practice = total // 4
    revision = total - learning - practice

    start = START_HOUR * 60
    learning_end = start + learning
    practice_end = learning_end + practice
    revision_end = practice_end + revision

    return {
        "learning": (format_time(start), format_time(learning_end)),
        "practice": (format_time(learning_end), format_time(practice_end)),
        "revision": (format_time(practice_end), format_time(revision_end)),
    }


# ---------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------
def planning_prompt(subject, days):
    return f"""
    You are a study planner.
    Create a {days}-day learning plan for the subject: {subject}.

    Return ONLY a JSON array with exactly {days} items.
    Each item must have these keys:
    - "topic": one learning topic (different on every day)
    - "task": one practical task for that day

    Example format:
    [
      {{"topic": "Topic name", "task": "Practical task"}}
    ]

    Do not add any text before or after the JSON.
    Do not include timings.
    """


def refine_prompt(subject, days, previous_output, problems):
    problem_text = "\n".join(f"- {p}" for p in problems)

    return f"""
    You are a study planner.
    Your previous answer for a {days}-day plan for "{subject}" had problems:

    {problem_text}

    Previous answer:
    {previous_output[:3000]}

    Fix ALL the problems.
    Return ONLY a JSON array with exactly {days} items.
    Each item must have the keys "topic" and "task".
    Do not add any text before or after the JSON.
    """


# ---------------------------------------------------------------
# THE AGENT: Plan -> Validate -> Refine (loop) -> Schedule -> Assemble
# ---------------------------------------------------------------
def run_study_agent(subject, hours, days):

    log = []

    # Step 1: check the inputs
    if hours <= 0 or days <= 0:
        return "Please provide at least 1 hour and 1 day."

    log.append(f"Step 1: Inputs checked ({subject}, {hours} h/day, {days} days).")

    # Step 2 to 4: AI plans, agent validates, agent asks AI to fix mistakes
    prompt = planning_prompt(subject, days)
    best_plan = None
    final_problems = ["No attempt was made."]

    for attempt in range(1, MAX_ATTEMPTS + 1):

        raw_output = generate_response(prompt)
        plan = parse_plan(raw_output)
        problems = validate_plan(plan, days)

        if plan is not None:
            best_plan = plan

        if not problems:
            log.append(f"Step 2 (attempt {attempt}): AI plan generated and passed validation.")
            final_problems = []
            break

        log.append(
            f"Step 2 (attempt {attempt}): validation failed with {len(problems)} problem(s). "
            "Asking the AI to fix them."
        )
        final_problems = problems
        prompt = refine_prompt(subject, days, raw_output, problems)

    # Step 5: if still not perfect, repair what we can in plain Python
    if final_problems:

        if best_plan is None:
            return (
                "The AI could not produce a usable study plan. "
                "Please try again or use a smaller number of days."
            )

        log.append("Step 3: AI output still had problems, so the agent repaired it automatically.")

    plan_items = []

    for number in range(1, days + 1):

        item = best_plan[number - 1] if best_plan and number <= len(best_plan) else {}

        if not isinstance(item, dict):
            item = {}

        topic = str(item.get("topic", "")).strip() or f"Revision of {subject}"
        task = str(item.get("task", "")).strip() or f"Practice what you learned about {subject}."

        plan_items.append((topic, task))

    # Step 6: Python builds the time schedule
    schedule = build_schedule(hours)
    log.append("Step 4: Time schedule calculated (50% learning, 25% practice, 25% revision).")

    # Step 7: assemble the final plan
    result = f"# AI Study Plan: {subject}\n"

    for number, (topic, task) in enumerate(plan_items, start=1):
        result += f"""
### Day {number}: {topic}

**Task:** {task}

**Learning:** {schedule['learning'][0]} - {schedule['learning'][1]}

**Practice:** {schedule['practice'][0]} - {schedule['practice'][1]}

**Revision:** {schedule['revision'][0]} - {schedule['revision'][1]}

**Daily Total:** {hours} hours
"""

    log.append("Step 5: Final plan assembled.")

    result += "\n---\n### Agent Workflow Log\n"
    for line in log:
        result += f"- {line}\n"

    return result
