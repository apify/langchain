from typing import Any, Callable, Dict, Optional

from pydantic import BaseModel, root_validator

from langchain.document_loaders import ApifyDatasetLoader
from langchain.document_loaders.base import Document
from langchain.utils import get_from_dict_or_env


class ApifyWrapper(BaseModel):
    """Wrapper around Apify.

    To use, you should have the ``apify-client`` python package installed,
    and the environment variable ``APIFY_API_KEY`` set with your API key, or pass
    `apify_api_key` as a named parameter to the constructor.
    """
    apify_client: Any
    apify_client_async: Any

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that API key and python package exist in the current environment."""
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

    def call(
        self,
        actor_id: str,
        run_input: Dict,
        dataset_mapping_function: Callable[[Dict], Document],
    ):
        """Run an Actor on the Apify platform, wait for it to finish and get results.

        Args:
            actor_id (str): The ID or name of the Actor on the Apify platform.
            run_input (Dict): The input of the Actor you're trying to run.
            dataset_mapping_function (Callable): A function that takes a single dictionary (Apify dataset item) and converts it to an instance of the Document class.

        Returns:
            ApifyDatasetLoader: A loader that will fetch the data from the Actor run's default dataset.
        """
        actor_call = self.apify_client.actor(actor_id).call(run_input=run_input)

        return ApifyDatasetLoader(
            dataset_id=actor_call["defaultDatasetId"],
            dataset_mapping_function=dataset_mapping_function,
        )

    async def arun(
        self,
        actor_id: str,
        run_input: Optional[Dict],
        dataset_mapping_function: Optional[Callable[[Dict], Document]],
    ):
        """Run an Actor on the Apify platform, wait for it to finish and get results.

        Args:
            actor_id (str): The ID or name of the Actor on the Apify platform.
            run_input (Dict): The input of the Actor you're trying to run.
            dataset_mapping_function (Callable): A function that takes a single dictionary (Apify dataset item) and converts it to an instance of the Document class.

        Returns:
            ApifyDatasetLoader: A loader that will fetch the data from the Actor run's default dataset.
        """
        actor_call = await self.apify_client_async.actor(actor_id).call(
            run_input=run_input
        )

        return ApifyDatasetLoader(
            dataset_id=actor_call["defaultDatasetId"],
            dataset_mapping_function=dataset_mapping_function,
        )
