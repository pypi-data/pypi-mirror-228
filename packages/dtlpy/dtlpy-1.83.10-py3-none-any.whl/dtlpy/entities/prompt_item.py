import logging
import io
import json

logger = logging.getLogger(name='dtlpy')


class Prompt:
    def __init__(self, key):
        """
        Create a new Prompt. Prompt can have multiple value, e.g. text and image.

        :param key: unique identifier of the prompt in the item
        """
        self.key = key
        self.elements = list()

    def add(self, value, mimetype='text'):
        """

        :param value: url or strint of the input
        :param mimetype: mimetype of the input. options: `text`, `image/*`, `video/*`, `audio/*`
        :return:
        """
        self.elements.append({'mimetype': mimetype,
                              'value': value})

    def to_json(self):
        """
        Convert Prompt entity to the item json

        :return:
        """
        return {
            self.key: [
                {
                    "mimetype": e['mimetype'],
                    "value": e['value']
                } for e in self.elements
            ]
        }


class PromptItem:
    def __init__(self, name):
        """
        Create a new Prompt Item. Single item can have multiple prompt, e.g. a conversation.

        :param name: name of the item (filename)
        """
        self.name = name
        self.type = "prompt"
        self.prompts = list()

    def to_json(self):
        """
        Convert the entity to a platform item.

        :return:
        """
        prompts_json = {
            "shebang": "dataloop",
            "metadata": {
                "dltype": self.type
            },
            "prompts": {}
        }
        for prompt in self.prompts:
            for prompt_key, prompt_values in prompt.to_json().items():
                prompts_json["prompts"][prompt_key] = prompt_values
        return prompts_json

    def to_bytes_io(self):
        byte_io = io.BytesIO()
        byte_io.name = self.name
        byte_io.write(json.dumps(self.to_json()).encode())
        byte_io.seek(0)
        return byte_io

    def add(self, prompt):
        """
            add a prompt to the prompt item
            promptId: id of the prompt
            prompt: a dictionary. keys are prompt message id, values are prompt messages
            responses: a list of annotations representing responses to the prompt
        """
        self.prompts.append(prompt)


if __name__ == "__main__":
    # Create a new Prompt item
    dataset = dl.datasets.get(dataset_id="64b402ffbdb89a0fdfc10da1")
    prompts = PromptItem('conversation_#1')
    prompt1 = Prompt(key='prompt-1')
    prompt1.add(mimetype='image/jpg',
                value='https://gate.dataloop.ai/api/v1/items/64e5deaefe649e838dc9687f/stream')
    prompts.add(prompt=prompt1)
    prompt2 = Prompt(key='2')
    prompt2.add(mimetype='text', value='where are you from')
    prompt2.add(mimetype='audio', value='http://item.jpg')
    prompts.add(prompt=prompt2)
    print(json.dumps(prompts.to_json(), indent=4))
    # upload
    item: dl.Item = dataset.items.upload(prompts, remote_name="sdk-test_2.json")
