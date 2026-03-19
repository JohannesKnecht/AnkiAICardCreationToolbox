"""Knowledge base creation from web sources."""

import json
import logging
import traceback
import uuid

import trafilatura

from ankiaicardcreationtoolboxbackend.knowledge_base.chain import get_messages, get_model
from ankiaicardcreationtoolboxbackend.knowledge_base.knowledge_base_config import (
    PROJECT_KNOWLEDGE_BASE_DIR,
    knowledge_base_config,
)

logger = logging.getLogger(__name__)


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

    request_id = uuid.uuid4().hex[:8]
    logger.info(
        "knowledge-base creation started",
        extra={"request_id": request_id, "url": url, "json_name": json_name},
    )

    # --- Fetch stage ---
    logger.debug("fetch_url starting", extra={"request_id": request_id, "url": url})
    downloaded: str | None = None
    try:
        downloaded = trafilatura.fetch_url(url)
    except Exception:  # broad catch is intentional: log traceback then re-raise unchanged
        logger.error(
            "fetch_url raised an unexpected exception",
            extra={"request_id": request_id, "url": url, "traceback": traceback.format_exc()},
        )
        raise

    if downloaded is None:
        logger.warning(
            "fetch_url returned None — page could not be retrieved",
            extra={"request_id": request_id, "url": url},
        )
    else:
        logger.info(
            "fetch_url completed",
            extra={"request_id": request_id, "url": url, "downloaded_bytes": len(downloaded)},
        )

    # --- Extract stage ---
    logger.debug(
        "extract starting",
        extra={"request_id": request_id, "downloaded_is_none": downloaded is None},
    )
    data: str | None = None
    try:
        data = trafilatura.extract(downloaded)
    except Exception:  # broad catch is intentional: log traceback then re-raise unchanged
        logger.error(
            "extract raised an unexpected exception",
            extra={"request_id": request_id, "url": url, "traceback": traceback.format_exc()},
        )
        raise

    if data is None:
        logger.warning(
            "extract returned None — no text could be extracted",
            extra={
                "request_id": request_id,
                "url": url,
                "downloaded_was_none": downloaded is None,
                "downloaded_bytes": None if downloaded is None else len(downloaded),
            },
        )
    else:
        logger.info(
            "extract completed",
            extra={"request_id": request_id, "url": url, "extracted_chars": len(data)},
        )

    # --- Persist raw output (even when extraction failed, for diagnostics) ---
    with open(f"{knowledge_base_dir}/{json_name}_raw.json", "w") as outfile:
        json.dump({"data": data}, outfile)

    if data is None:
        downloaded_summary = "None (fetch failed)" if downloaded is None else f"{len(downloaded)} bytes fetched"
        msg = (
            f"Failed to extract content from {url!r} (request_id={request_id}). "
            f"fetch_url: {downloaded_summary}; trafilatura.extract returned None. "
            "Check network connectivity, page structure, or trafilatura version."
        )
        logger.error(
            "knowledge-base creation aborted: extraction produced no content",
            extra={
                "request_id": request_id,
                "url": url,
                "downloaded_bytes": None if downloaded is None else len(downloaded),
                "extracted_chars": None,
            },
        )
        raise ValueError(msg)

    # --- LLM summarisation stage ---
    logger.info(
        "LLM summarisation starting",
        extra={"request_id": request_id, "extracted_chars": len(data)},
    )
    response = get_model().invoke(get_messages(data, additional_info)).content
    response_chars = len(response) if isinstance(response, str) else None
    logger.info(
        "LLM summarisation completed",
        extra={
            "request_id": request_id,
            "response_type": type(response).__name__,
            "response_chars": response_chars,
        },
    )

    with open(f"{knowledge_base_dir}/{json_name}.json", "w") as outfile:
        json.dump({"data": response}, outfile)

    logger.info(
        "knowledge-base creation succeeded",
        extra={"request_id": request_id, "json_name": json_name},
    )


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
