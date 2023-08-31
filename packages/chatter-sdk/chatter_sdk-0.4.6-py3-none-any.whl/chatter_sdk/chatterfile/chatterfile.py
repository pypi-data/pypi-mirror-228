import inspect
import os
import re
import yaml
from chatter_sdk.chatterfile.prompt_utils import render_prompt
from chatter_sdk.chatterfile.run_utils import run_llm


class Chatterfile:
    def __init__(self, path='./Chatterfile'):
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        script_path = os.path.dirname(os.path.abspath(module.__file__))
        self._path = os.path.join(script_path, path)
        self._configs = {}
        self._keys = {}
        self._prompts = {}
        self._read_chatterfile()

    def _read_chatterfile(self):
        with open(self._path, 'r') as f:
            chatterfile_content = f.read()

        chunks = chatterfile_content.split('@')[1:]

        for chunk in chunks:
            first_line, yaml_str = chunk.split('\n', 1)
            key = first_line.split(':', 1)[1].strip()
            parsed_yaml = yaml.safe_load(yaml_str.replace('\t', '    '))

            if first_line.startswith('config'):
                self._configs[key] = parsed_yaml
            if first_line.startswith('keys'):
                self._keys[key] = {}
                for api_key_name, api_key_value in parsed_yaml.items():
                    if len(api_key_value) <= 30:
                        self._keys[key][api_key_name] = os.environ.get(api_key_value, "")
                    else:
                        self._keys[key][api_key_name] = api_key_value

            elif first_line.startswith('prompt_id'):
                parsed_yaml['prompt'] = self._convert_to_jinja_template(parsed_yaml.get('prompt'))
                self._prompts[key] = parsed_yaml

    def _convert_to_jinja_template(self, prompt):
        if isinstance(prompt, str) and "{" in prompt and "}" in prompt:
            if not "{{" in prompt and not "}}" in prompt:
                return re.sub(r"{([^{}]+)}", r"{{\1}}", prompt)

        elif isinstance(prompt, list):
            return [{k: self._convert_to_jinja_template(v) for k, v in entry.items()} for entry in prompt]

        return prompt

    def get_config(self, id):
        return self._configs.get(id)

    def get_prompt(self, prompt_id):
        return self._prompts.get(prompt_id)

    def get_prompts(self):
        return self._prompts

    def render_prompt(self, prompt_id, variables):
        prompt = self._prompts.get(prompt_id)['prompt']
        return render_prompt(prompt, variables)

    def run_prompt(self, prompt_id, variables, model_family=None, model=None, params=None, prompt_override=None,
                   key_id=None, simplified=False):
        prompt = self.get_prompt(prompt_id)
        if prompt is None:
            raise ValueError(f"Prompt with id {prompt_id} not found")

        if not self._keys:
            raise ValueError(f"No keys found in Chatterfile")

        # Inject overrides
        if model_family is not None:
            prompt['model_family'] = model_family
        if model is not None:
            prompt['model'] = model
        if params is not None:
            prompt['params'] = params
        if prompt_override is not None:
            prompt['prompt'] = prompt_override

        # Ensure required keys are not None
        if prompt['model_family'] is None or prompt['model'] is None or prompt['prompt'] is None:
            raise ValueError("model_family, model, and prompt must not be None")

        prompt['prompt'] = render_prompt(prompt['prompt'], variables)

        # get keys for model_family
        key_to_use = self._keys.get(key_id, None) if key_id else list(self._keys.values())[0][prompt['model_family']]
        if key_to_use is None:
            raise ValueError(f"No key found for model_family {prompt['model_family']}")

        return run_llm(prompt, key_to_use, simplified=simplified)

