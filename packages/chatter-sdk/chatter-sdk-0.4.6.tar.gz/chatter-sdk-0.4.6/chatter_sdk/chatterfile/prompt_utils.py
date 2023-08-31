from jinja2 import Template


def render_prompt(prompt, variables):
    template_render = lambda x: Template(x).render(variables)

    if isinstance(prompt, str):
        return template_render(prompt)

    elif isinstance(prompt, list):
        return [{k: template_render(v) for k, v in entry.items()} for entry in prompt]


