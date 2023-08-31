# ChainLink

ChainLink is a Python SDK designed to simplify the creation of chatbot-based applications using Gradio. The SDK offers an efficient way to interact with Language Learning Models (LLMs) and deploy Gradio applications around these models.

## Contents
1. [Capabilities](#capabilities)
2. [Installation](#installation)
3. [Quickstart/Usage](#quickstartusage)

## Capabilities

ChainLink's capabilities are all focused around two classes - the `Model` class and the `App` class.

The `Model` class implements the ability to talk to a specific LLM/chatbot, while the `App` class implements the Gradio application around the specific `Model`.

## Installation
To install ChainLink, you can use pip to install directly from the GitHub repository:
```bash
pip install git+https://github.com/jacobrenn/chainlink
```

## Quickstart/Usage
Here's a simple example of how you can use ChainLink to create an LLM-powered application, and then deploy it:

```python
import chainlink.model as Model
import chainlink.app as App

model = Model(openai_api_key='<your OpenAI API key>', model='gpt-3.5-turbo', model_type='chat_openai', memory=True)
app = App(model, feedback=True)
app.deploy()
```

**We are currently still working on building the implementation and documentation around ChainLink, so if you have any specific questions please feel free to reach out to us directly.**