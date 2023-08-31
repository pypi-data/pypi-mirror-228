import openai

from konko import config
from konko.chat_completion import ChatCompletion
from konko.model import Model
from konko.version import VERSION

# Initialize the Konko SDK to use user defined environment variables
openai.api_base = config.KONKO_API_BASE
openai.api_key = config.KONKO_API_KEY

# Initialize Konko-specific variables
api_base = config.KONKO_API_BASE
api_key = config.KONKO_API_KEY

# Function to set Konko API base
def set_api_base(base):
    global api_base
    api_base = base
    openai.api_base = base

# Function to set Konko API key
def set_api_key(key):
    global api_key
    api_key = key
    openai.api_key = key

# Function to set OpenAI API key
def set_openai_api_key(new_key):
    config.OPENAI_API_KEY = new_key

__version__ = VERSION
__all__ = [
    "ChatCompletion",
    "Model",
]

# Enable custom error messaging
class CustomAuthenticationError(Exception):
    pass

# Save a reference to the original function
original_default_api_key = openai.util.default_api_key

def custom_default_api_key():
    try:
        return original_default_api_key()
    except openai.error.AuthenticationError:
        raise CustomAuthenticationError("\nError: No Konko API key provided."
                                        "\n\nEither set an environment variable KONKO_API_KEY=<API-KEY> or use konko.set_api_key(<API-KEY>)."
                                        "\n\nVisit https://docs.konko.ai/ to request your API key") from None

# Perform the monkey patching
openai.util.default_api_key = custom_default_api_key
