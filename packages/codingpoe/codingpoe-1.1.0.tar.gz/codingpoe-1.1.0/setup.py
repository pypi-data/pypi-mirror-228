from setuptools import setup, find_packages
from pathlib import Path

base_path = Path(__file__).parent
long_description = (base_path / "README.md").read_text()

VERSION = '1.1.0'
DESCRIPTION = 'A simple package that use Poe AI models'
LONG_DESCRIPTION = 'A Python API wrapper for Poe.com, using Httpx. With this, you will have free access to ChatGPT, Claude, Llama, Google-PaLM and more! 🚀'

setup(
    name="codingpoe",
    version=VERSION,
    author="Coding Team",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=['httpx==0.24.1', 'ballyregan==1.0.6','websocket-client'],
    keywords=['python', 'poe', 'quora', 'chatgpt', 'claude', 'poe-api', 'api', 'codingteam'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent"
    ],
    url="https://github.com/codingtuto/codingpoe"
)