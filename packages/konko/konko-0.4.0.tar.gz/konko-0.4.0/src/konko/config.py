import os

#Set module-level variables

## Set the KONKO API configuration variables
KONKO_API_BASE = os.environ.get("KONKO_API_BASE", "https://api.konko.ai/v1")
KONKO_API_KEY = os.environ.get("KONKO_API_KEY")

## Set the OPENAI API configuration variables
OPENAI_API_BASE = os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

## Other model providers coming soon