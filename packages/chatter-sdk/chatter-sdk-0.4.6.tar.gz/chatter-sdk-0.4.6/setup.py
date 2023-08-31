from setuptools import setup, find_packages

setup(
    name='chatter-sdk',
    version='0.4.6',
    packages=find_packages(),
    install_requires=[
        'requests',
        'PyYAML',
        'jinja2',
        'openai',
        'anthropic'
    ],
    author='Anish Agrawal',
    author_email='anish@trychatter.ai',
    description='SDK to interact with Chatter!',
)
