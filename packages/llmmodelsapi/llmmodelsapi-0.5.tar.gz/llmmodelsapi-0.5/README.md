# LLM-API-Express-SDK-Python
SDK for interfacing with LLM API using Python.

## Installation
```bash
pip install llmmodelsapi
```

## Usage
```python
from llmmodelsapi import LlmApi, ModelType

if __name__ == '__main__':
    api_token = "YOUR_API_TOKEN"
    llm_api = LlmApi(api_token=api_token)

    # Get full response as a single object
    response = llm_api.generate("What is deep learning, in one sentence?", ModelType.CORE_MODEL)
    if "error" in response:
        # Handle error
        print(response["error"])
    else:
        # Handle generated text
        print(response["generated_text"])

    # Get response as a stream
    response_streaming = llm_api.generate_stream("What is deep learning, in one sentence?", ModelType.CORE_MODEL)
    for line in response_streaming:
        if "error" in line:
            # Handle error
            print(line["error"])
        else:
            # Handle generated text
            print(line["token"]["text"])
```