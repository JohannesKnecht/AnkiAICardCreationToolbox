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
    if knowledge_base_dir is None:
        knowledge_base_dir = PROJECT_KNOWLEDGE_BASE_DIR

    downloaded = trafilatura.fetch_url(url)
    data = trafilatura.extract(downloaded)

    with open(f"{knowledge_base_dir}/{json_name}_raw.json", "w") as outfile:
        json.dump({"data": data}, outfile)

    response = get_model().invoke(get_messages(data, additional_info)).content

    with open(f"{knowledge_base_dir}/{json_name}.json", "w") as outfile:
        json.dump({"data": response}, outfile)


def create_knowledge_base_with_config(config: dict[str, str], name: str, knowledge_base_dir: str | None) -> None:
    create_knowledge_base(
        url=config["url"],
        json_name=name,
        additional_info=config["additional_info"],
        knowledge_base_dir=knowledge_base_dir,
    )


def create_knowledge_base_with_config_name(name: str, knowledge_base_dir: str | None) -> None:
    create_knowledge_base_with_config(
        config=knowledge_base_config[name], name=name, knowledge_base_dir=knowledge_base_dir
    )
