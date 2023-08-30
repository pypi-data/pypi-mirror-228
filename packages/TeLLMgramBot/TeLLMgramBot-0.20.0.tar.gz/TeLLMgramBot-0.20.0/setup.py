from setuptools import setup, find_packages

setup(
    name='TeLLMgramBot',
    version='0.20.0',
    packages=find_packages(),
    license='MIT',
    author='RoninATX',
    author_email='ronin.atx@gmail.com',
    description='OpenAI GPT, driven by Telegram',
    url='https://github.com/Digital-Heresy/TeLLMgramBot',
    install_requires=[
        'openai',
        'PyYAML',
        'httpx',
        'beautifulsoup4',
        'typing',
        'validators'
    ],
    python_requires='>=3.10',
)
