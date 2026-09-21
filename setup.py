from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="agent-replay",
    version="0.1.0",
    author="Agent Replay Contributors",
    description="Local-first agent debugging for the 'it worked yesterday' moments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thehypewipe/agent-replay",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Debuggers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "click>=8.0.0",
        "rich>=10.0.0",
        "anthropic>=0.18.0",
        "openai>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "agent-replay=agent_replay.cli:cli",
        ],
    },
)
