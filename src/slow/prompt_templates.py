SYSTEM_PROMPT = (
    "You are a planning agent that outputs only valid JSON per the Subgoal schema."
)

USER_PROMPT_TEMPLATE = (
    "State summary:\n{state}\n\n"
    "Available skills: {skills}\n\n"
    "Respond with a Subgoal JSON only."
)