"""
Application configuration loader.
Loads variables from a local .env file (if present) into the process
environment using python-dotenv, then exposes simple typed settings.
"""
import os
from dotenv import load_dotenv

# Load variables from .env into the environment. This is a no-op if
# no .env file exists (e.g. in CI or production where env vars are
# injected directly), which keeps local dev and deployment consistent.
load_dotenv()

# Port the Uvicorn server should bind to. Defaults to 8000 if not set.
PORT: int = int(os.getenv("PORT", "8000"))

# Current application environment (e.g. "development", "production").
APP_ENV: str = os.getenv("APP_ENV", "development")