import requests
import json
from typing import Generator, Union
from typing_extensions import TypedDict

class Token(TypedDict):
    id: int
    text: str
    logprob: float
    special: bool

class Error(TypedDict):
    error: str

class GeneratedText(TypedDict):
    generated_text: Union[str, None]

class Line(TypedDict):
    token: Token
    generated_text: Union[str, None]


def get_stream(endpoint, data, headers):
    s = requests.Session()
    with s.post(endpoint, json=data, headers=headers, stream=True) as r:
        if r.status_code != 200:
            yield {"error": r.text}
        for line in r.iter_lines():
            if line:
                try:
                    json_string = line.split(b':', 1)[1] # Split on the first colon and take the second part
                    yield json.loads(json_string)
                except:
                    continue

class ModelType():
    CORE_MODEL = 'core-model'

class LlmApi():
    base_endpoint = "https://llm-api-express-yix5m2x4pq-uk.a.run.app/api/v1"

    def __init__(self, api_token):
        self.api_token = api_token
    
    def generate(self, text: str, model_type: str = ModelType.CORE_MODEL) -> Union[GeneratedText, Error]:
        endpoint = self.base_endpoint + "/generate"
        headers = {
            "x-api-token": self.api_token,
            "Content-Type": "application/json"
        }
        data = {
            "model": model_type,
            "generateType": "generate",
            "input": text
        }
        response = requests.post(endpoint, headers=headers, json=data)
        try:
            return response.json()
        except:
            return {"error": response.text}

    def generate_stream(self, text, model_type=ModelType.CORE_MODEL) -> Generator[Union[Line, Error], None, None]:
        endpoint = self.base_endpoint + "/generate"
        headers = {
            "x-api-token": self.api_token,
            "Content-Type": "application/json"
        }
        data = {
            "model": model_type,
            "generateType": "generate_stream",
            "input": text
        }
        
        for line in get_stream(endpoint, data, headers):
            yield line