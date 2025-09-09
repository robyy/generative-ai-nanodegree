import os

from dotenv import load_dotenv

load_dotenv()

***REMOVED*** = os.getenv("***REMOVED***")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
