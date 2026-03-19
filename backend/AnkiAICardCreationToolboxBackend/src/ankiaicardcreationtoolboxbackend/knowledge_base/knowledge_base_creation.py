"""Knowledge base creation from web sources."""

import json
import logging

import requests
import trafilatura

from ankiaicardcreationtoolboxbackend.knowledge_base.chain import get_messages, get_model
from ankiaicardcreationtoolboxbackend.knowledge_base.knowledge_base_config import (
    PROJECT_KNOWLEDGE_BASE_DIR,
    knowledge_base_config,
)

logger = logging.getLogger(__name__)


def _fetch_html(url: str) -> str | None:
    """Fetch URL content as an HTML string.

    Sends only gzip/deflate in ``Accept-Encoding`` to prevent servers from
    returning ZSTD-compressed data that trafilatura cannot reliably decompress
    (``zstandard.decompress`` fails for streaming ZSTD frames that omit the
    content-size field in the frame header).

    Args:
        url: The web URL to fetch.

    Returns:
        The decoded HTML text, or ``None`` if the request fails.
    """
    try:
        response = requests.get(
            url,
            headers={"Accept-Encoding": "gzip, deflate"},
            timeout=30,
        )
        response.raise_for_status()
        return response.text
    except requests.RequestException as exc:
        logger.warning("Failed to fetch page from %s: %s", url, exc)
        return None


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

    Raises:
        ValueError: When text cannot be extracted from the fetched page.
    """
    if knowledge_base_dir is None:
        knowledge_base_dir = PROJECT_KNOWLEDGE_BASE_DIR

    downloaded = _fetch_html(url)

    data = trafilatura.extract(downloaded)

    with open(f"{knowledge_base_dir}/{json_name}_raw.json", "w") as outfile:
        json.dump({"data": data}, outfile)

    if data is None:
        logger.warning("trafilatura.extract returned None for %s", url)
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
