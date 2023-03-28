"""Logic for loading documents from Apify datasets."""
from typing import Any, Callable, Dict, List

from pydantic import BaseModel, root_validator

from langchain.docstore.document import Document
from langchain.document_loaders.base import BaseLoader
from langchain.utils import get_from_dict_or_env


class ApifyDatasetLoader(BaseLoader, BaseModel):
    """Logic for loading documents from Apify datasets."""

    apify_client: Any
    dataset_id: str
    """The ID of the dataset on the Apify platform."""
    dataset_mapping_function: Callable[[Dict], Document]
    """A function that takes a single dictionary (Apify dataset item) and converts it to an instance of the Document class."""

    def __init__(
        self, dataset_id: str, dataset_mapping_function: Callable[[Dict], Document]
    ):
        """Initialize the loader with dataset ID and a mapping function.

        Args:
            dataset_id (str): The ID of the dataset on the Apify platform.
            dataset_mapping_function (Callable): A function that takes a single dictionary (Apify dataset item) and converts it to an instance of the Document class.
        """
        super().__init__(
            dataset_id=dataset_id, dataset_mapping_function=dataset_mapping_function
        )

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that API key and python package exist in the current environment."""
        apify_api_key = get_from_dict_or_env(values, "apify_api_key", "APIFY_API_KEY")

        try:
            from apify_client import ApifyClient

            values["apify_client"] = ApifyClient(apify_api_key)
        except ImportError:
            raise ValueError(
                "Could not import apify-client python package. "
                "Please it install it with `pip install apify-client`."
            )

        return values

    def load(self) -> List[Document]:
        """Load documents."""
        dataset_items = self.apify_client.dataset(self.dataset_id).list_items().items
        return list(map(self.dataset_mapping_function, dataset_items))
