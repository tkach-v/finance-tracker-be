import os

PROFILERS_ENABLED = os.environ.get("PROFILERS_ENABLED", "False").lower() == "true"
