VALID_MODES = ["pilot", "a", "b"]

SCREENS = [
    "blocked", "consent", "demographics", "scenario",
    "email_phase1", "transition", "email_phase2",
    "survey", "debrief", "complete"
]

PHASE1_IDS = ["P1", "P2", "P3", "P4", "L1", "L2", "L3", "L4"]
PHASE2_IDS = ["P5", "P6", "P7", "P8", "L5", "L6", "L7", "L8"]

MODE_LABELS = {
    "pilot": "Pilot",
    "a": "Group A — Generic Warning",
    "b": "Group B — AI Scaffold"
}

PHASE1_COUNT = 8
PHASE2_COUNT = 8
TOTAL_EMAILS = 16