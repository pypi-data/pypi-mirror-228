from setuptools import setup, find_packages

setup(
    name='phonegpt',
    version='1.2',
    packages=find_packages(),
    install_requires=[
        'twilio',
        'openai',
        'Flask',
    ],

    author='Ehsan Amiri',
    author_email='e.amiri89@gmail.com',
    description='Make interactive phone call, using Twilio and OpenAI',
)