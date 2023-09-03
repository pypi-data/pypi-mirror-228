from setuptools import setup, find_packages

setup(
    name='kvcc',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pyaudio',
        'speech_recognition',
        'openai',
    ],
    entry_points={
        'console_scripts': [
            'kvcc=kvcc.main:main',
        ],
    },
)
