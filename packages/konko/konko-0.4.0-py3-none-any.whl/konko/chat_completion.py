from openai.api_resources.chat_completion import ChatCompletion as _ChatCompletion
from . import config

class ChatCompletion(_ChatCompletion):
    @classmethod
    def create(cls, *args, **kwargs):
        headers = kwargs.get('headers') or {}
        if config.OPENAI_API_KEY:
            headers["X-OpenAI-Api-Key"] = config.OPENAI_API_KEY
        kwargs['headers'] = headers
        return super().create(*args, **kwargs)

    @classmethod
    async def acreate(cls, *args, **kwargs):
        headers = kwargs.get('headers') or {}
        if config.OPENAI_API_KEY:
            headers["X-OpenAI-Api-Key"] = config.OPENAI_API_KEY
        kwargs['headers'] = headers
        return await super().acreate(*args, **kwargs)