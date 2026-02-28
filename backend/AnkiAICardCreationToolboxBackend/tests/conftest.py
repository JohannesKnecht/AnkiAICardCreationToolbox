import os

from dotenv import load_dotenv

load_dotenv()

if not os.environ.get("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY not set")

# Use the cheapest model for tests unless explicitly overridden
if not os.environ.get("OPENAI_MODEL_OVERRIDE"):
    os.environ["OPENAI_MODEL_OVERRIDE"] = "gpt-4.1-nano"
