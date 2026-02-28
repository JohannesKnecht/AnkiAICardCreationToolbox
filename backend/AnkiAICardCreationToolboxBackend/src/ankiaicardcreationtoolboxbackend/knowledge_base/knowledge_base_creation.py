"""Knowledge base creation from web sources."""

import json

import trafilatura

from ankiaicardcreationtoolboxbackend.knowledge_base.chain import get_messages, get_model
from ankiaicardcreationtoolboxbackend.knowledge_base.knowledge_base_config import (
    PROJECT_KNOWLEDGE_BASE_DIR,
    knowledge_base_config,
)


def create_knowledge_base(
    url: str, json_name: str, additional_info: str, knowledge_base_dir: str | None = None
) -> None:
    """Fetch a URL, summarise its content, and save both raw and processed JSON.

    Args:
        url: The web URL to fetch content from.
        json_name: The base file name for the output JSON files.
        additional_info: Extra instructions for the summarisation model.
        knowledge_base_dir: Directory to store the output files.
            Defaults to the project data directory.
    """
    if knowledge_base_dir is None:
        knowledge_base_dir = PROJECT_KNOWLEDGE_BASE_DIR

    downloaded = trafilatura.fetch_url(url)
    data = trafilatura.extract(downloaded)

    with open(f"{knowledge_base_dir}/{json_name}_raw.json", "w") as outfile:
        json.dump({"data": data}, outfile)

    if data is None:
        msg = f"Failed to extract content from {url}"
        raise ValueError(msg)

    response = get_model().invoke(get_messages(data, additional_info)).content

    with open(f"{knowledge_base_dir}/{json_name}.json", "w") as outfile:
        json.dump({"data": response}, outfile)


def create_knowledge_base_with_config(config: dict[str, str], name: str, knowledge_base_dir: str | None) -> None:
    """Create a knowledge base using the given config dictionary.

    Args:
        config: A dictionary containing ``url`` and ``additional_info`` keys.
        name: The name used for the output JSON files.
        knowledge_base_dir: Directory to store the output files.
    """
    create_knowledge_base(
        url=config["url"],
        json_name=name,
        additional_info=config["additional_info"],
        knowledge_base_dir=knowledge_base_dir,
    )


def create_knowledge_base_with_config_name(name: str, knowledge_base_dir: str | None) -> None:
    """Create a knowledge base by looking up the config by name.

    Args:
        name: The configuration name to look up in ``knowledge_base_config``.
        knowledge_base_dir: Directory to store the output files.
    """
    create_knowledge_base_with_config(
        config=knowledge_base_config[name], name=name, knowledge_base_dir=knowledge_base_dir
    )
