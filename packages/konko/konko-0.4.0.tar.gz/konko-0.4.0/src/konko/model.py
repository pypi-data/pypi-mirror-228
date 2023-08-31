from openai.api_resources.model import Model as _Model
import openai.util as util
from . import config

class Model(_Model):
    @classmethod
    def list(
        cls,
        api_key=None,
        request_id=None,
        api_version=None,
        organization=None,
        api_base=None,
        api_type=None,
        headers=None,
        **params,):
        
        requestor, url = cls._ListableAPIResource__prepare_list_requestor(
            api_key,
            api_version,
            organization,
            api_base,
            api_type,
        )

        headers = headers or {}

        if config.OPENAI_API_KEY:
            headers["X-OpenAI-Api-Key"] = config.OPENAI_API_KEY

        response, _, api_key = requestor.request(
            "get", url, params, headers=headers, request_id=request_id
        )
        openai_object = util.convert_to_openai_object(
            response, api_key, api_version, organization
        )
        openai_object._retrieve_params = params
        return openai_object    