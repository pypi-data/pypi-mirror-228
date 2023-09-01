from setuptools import setup, find_packages

setup(name="redemption-ai",
      version="0.0.0",
      description="AI-powered (OpenAI API) tools for chat-like interactions and personal AI assistance.",
      packages=find_packages(include=["RAI", "RAI.*"]),
      author="Ausar686",
      author_email='glebyushkov@mail.ru',
      install_requires=[
      	"numpy",
		"openai",
		"orjson",
		"pandas",
		"pydantic",
		"requests",
		"tiktoken",
		"notebook==6.*",
		"jupyterlab"
      ])