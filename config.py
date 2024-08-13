# config.py
import os
from dotenv import load_dotenv

load_dotenv()  # This loads the variables from .env file

openai_api_key = os.environ.get("openai_api_key")
aws_access_key_id = os.environ.get("aws_access_key_id")
aws_secret_access_key = os.environ.get("aws_secret_access_key")