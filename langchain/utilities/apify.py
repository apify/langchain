from typing import Any, Callable, Dict, List, Optional

from pydantic import BaseModel, root_validator

from langchain.document_loaders import ApifyDatasetLoader
from langchain.document_loaders.base import Document
from langchain.utils import get_from_dict_or_env


class ApifyWrapper(BaseModel):
    apify_client: Any
    apify_client_async: Any

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that API key and python package exists in environment."""
        apify_api_key = get_from_dict_or_env(values, "apify_api_key", "APIFY_API_KEY")

        try:
            from apify_client import ApifyClient, ApifyClientAsync

            values["apify_client"] = ApifyClient(apify_api_key)
            values["apify_client_async"] = ApifyClientAsync(apify_api_key)
        except ImportError:
            raise ValueError(
                "Could not import apify-client python package. "
                "Please it install it with `pip install apify-client`."
            )

        return values

    def run(
        self,
        urls: List[str],
        *,
        actor_name: str = "jirimoravcik/content-crawler-copy",
        run_input: Optional[Dict] = None,
        mapping_function: Optional[Callable[[Dict], Document]] = None,
    ):
        run_input = run_input or {
            "extendOutputFunction": "($) => {\n    const result = {};\n    // Uncomment to add a title to the output\n    // result.pageTitle = $('title').text().trim();\n\n    return result;\n}",
            "proxyConfiguration": {"useApifyProxy": True},
            "saveHtml": "link",
            "saveSnapshots": True,
            "startUrls": list(map(lambda url: {"url": url}, urls)),
            "crawlerType": "browserPuppeteer",
            "maxDepth": 9999,
            "maxPagesPerCrawl": 9999999,
            "maxConcurrency": 200,
        }
        mapping_function = mapping_function or (
            lambda item: Document(
                page_content=item["text"], metadata={"source": item["url"]}
            )
        )
        actor_call = self.apify_client.actor(actor_name).call(run_input=run_input)

        return ApifyDatasetLoader(
            dataset_id=actor_call["defaultDatasetId"],
            mapping_function=mapping_function,
        )

    async def arun(
        self,
        urls: List[str],
        *,
        actor_name: str = "jirimoravcik/content-crawler-copy",
        run_input: Optional[Dict] = None,
        mapping_function: Optional[Callable[[Dict], Document]] = None,
    ):
        run_input = run_input or {
            "extendOutputFunction": "($) => {\n    const result = {};\n    // Uncomment to add a title to the output\n    // result.pageTitle = $('title').text().trim();\n\n    return result;\n}",
            "proxyConfiguration": {"useApifyProxy": True},
            "saveHtml": "link",
            "saveSnapshots": True,
            "startUrls": list(map(lambda url: {"url": url}, urls)),
            "crawlerType": "browserPuppeteer",
            "maxDepth": 9999,
            "maxPagesPerCrawl": 9999999,
            "maxConcurrency": 200,
        }
        mapping_function = mapping_function or (
            lambda item: Document(
                page_content=item["text"], metadata={"source": item["url"]}
            )
        )
        actor_call = await self.apify_client_async.actor(actor_name).call(
            run_input=run_input
        )

        return ApifyDatasetLoader(
            dataset_id=actor_call["defaultDatasetId"],
            mapping_function=mapping_function,
        )
