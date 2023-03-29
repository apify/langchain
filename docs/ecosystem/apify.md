# Apify

This page covers how to use the Apify within LangChain.
It is broken into two parts: installation and setup, and then references to specific Apify wrappers.

## Installation and Setup
- Install the Python package with `pip install apify-client`.
- Get an Apify API key and either set it as an environment variable (`APIFY_API_KEY`) or pass it to the `ApifyWrapper` as `apify_api_key` in the constructor.


## Wrappers

### Utility

You can use the `ApifyWrapper` to run Actors on the Apify platform.

```python
from langchain.utilities import ApifyWrapper
```

For a more detailed walkthrough of this wrapper, see [this notebook](../modules/agents/tools/examples/apify.ipynb).


### Tool

You can also easily load this wrapper as a Tool (to use with an Agent).
You can do this with:
```python
from langchain.agents import load_tools
tools = load_tools(["apify"])
```

For more information on this, see [this page](../modules/agents/tools/getting_started.md).

### Loader

You can also use our `ApifyDatasetLoader` to get data from Apify dataset.

```python
from langchain.document_loaders import ApifyDatasetLoader
```

For a more detailed walkthrough of this loader, see [this notebook](../modules/indexes/document_loaders/examples/apify_dataset.ipynb).
