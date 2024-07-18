from typing import List, Union, Generator, Iterator
import requests
import json


class Pipeline:
    def __init__(self):
        # Optionally, you can set the id and name of the pipeline.
        # Best practice is to not specify the id so that it can be automatically inferred from the filename, so that users can install multiple versions of the same pipeline.
        # The identifier must be unique across all pipelines.
        # The identifier must be an alphanumeric string that can include underscores or hyphens. It cannot contain spaces, special characters, slashes, or backslashes.
        # self.id = "ollama_pipeline"
        self.name = "Ollama Custom Pipeline"

    async def on_startup(self):
        # This function is called when the server is started.
        print(f"on_startup:{__name__}")
        pass

    async def on_shutdown(self):
        # This function is called when the server is stopped.
        print(f"on_shutdown:{__name__}")
        pass

    def pipe(
        self, user_message: str, model_id: str, messages: List[dict], body: dict
    ) -> Union[str, Generator, Iterator]:
        # This is where you can add your custom pipelines like RAG.
        print(f"pipe:{__name__}")

        print("user_message", user_message)
        print("messages", messages)
        print("body", body)

        OLLAMA_BASE_URL = "http://192.168.4.6:11434"
        MODEL = "phi3"

        """
        user_message: hello < message from user        
        messages: [
            {
                'role': 'user',
                'content': 'hello'
            }
        ]
        
        body = {
            'stream': True,
            'model': ollama_custom_pipeline',
            'messages': [
                {
                    'role': 'user',
                    'content': 'hello'
                }
            ],
            'user': {
                'id': '52a539da-0e71-4266-beae-17531c0285a0',
                'name': 'user_name',
                'email': 'leviethung1280@gmail.com',
                'role': 'admin'
            }
        }
        
        """

        if "user" in body:
            print("######################################")
            print(f'# User: {body["user"]["name"]} ({body["user"]["id"]})')
            print(f"# Message: {user_message}")
            print("################1#####################")

        try:
            r = requests.post(
                url=f"{OLLAMA_BASE_URL}/api/chat",
                json={**body, "model": MODEL},
                stream=True,
            )

            r.raise_for_status()

            if body["stream"]:
                for line in r.iter_lines():
                    response = json.loads(line)
                    if response.get("done"):
                        break
                    yield response.get("message", {}).get("content")
            else:
                return r.json()
        except Exception as e:
            return f"Error: {e}"
