import openai
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT


def run_llm(prompt, key, simplified=False):
    model_family = prompt["model_family"]

    if model_family == 'OpenAI':
        return run_openai(prompt, key, simplified)
    elif model_family == 'Anthropic':
        return run_anthropic(prompt, key, simplified)


def run_openai(prompt_config, key, simplified):
    openai.api_key = key
    prompt = prompt_config["prompt"]

    if isinstance(prompt, str):
        prompt = [{"role": "user", "content": prompt}]

    if not simplified:
        return openai.ChatCompletion.create(model=prompt_config["model"], messages=prompt, **prompt_config['params'])
    else:
        completion = openai.ChatCompletion.create(model=prompt_config["model"], messages=prompt, **prompt_config['params'])
        if completion.choices[0].message.get('function_call') is None:
            return completion.choices[0].message['content']
        else:
            return completion.choices[0].message['function_call']['arguments']


def run_anthropic(prompt_config, key, simplified):
    anthropic = Anthropic(api_key=key)

    if not simplified:
        return anthropic.completions.create(model=prompt_config["model"],
                                            prompt=prompt_config["prompt"],
                                            **prompt_config['params'])
    else:
        completion = anthropic.completions.create(model=prompt_config["model"],
                                                  prompt=prompt_config["prompt"],
                                                  **prompt_config['params'])
        return completion.completion


