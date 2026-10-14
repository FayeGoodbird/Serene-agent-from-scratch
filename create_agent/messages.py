"""Shared inputs for all steps."""

# Generic coach prompt, used before Serene's persona is introduced (steps 1-2).
COACH_PROMPT = (
    "You are a calm coach who helps people with their problems. "
    "You are empathetic and understanding."
)

# The user turns every step replays.
messages = [
    {"role": "user", "content": "I'm stressed. I can't stop eating."},
    {"role": "user", "content": "I ate the biscuits because work was awful."},
    {"role": "user", "content": "I'm never going to look good again."},
]
