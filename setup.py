from setuptools import setup

setup(
    name='SimpleWebUI',
    version='1.0',
    author="Limour",
    author_email="limour@limour.top",
    packages=['SimpleWebUI'],
    install_requires=[
        'httpx',
        'aiohttp',
    ],
)