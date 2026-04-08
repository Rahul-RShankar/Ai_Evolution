from setuptools import setup, find_packages

setup(
    name="ai_evolution",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "requests",
        "flask",
        "flask-cors",
        "ddgs"
    ],
)
