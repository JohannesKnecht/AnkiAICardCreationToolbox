import json
import tempfile

import trafilatura


def create_knowledge_base(knowledge_base_dir=None):
    tempdir = None
    if knowledge_base_dir is None:
        tempdir = tempfile.TemporaryDirectory()
        knowledge_base_dir = tempdir.name

    downloaded = trafilatura.fetch_url('https://www.supermemo.com/en/blog/twenty-rules-of-formulating-knowledge')
    data = trafilatura.extract(downloaded)

    with open(f'{knowledge_base_dir}/raw_knowledge_base.json', 'w') as outfile:
        json.dump({"data": data}, outfile)

    from langchain.chat_models import init_chat_model
    from langchain.messages import HumanMessage, AIMessage, SystemMessage

    model = init_chat_model("gpt-5")

    system_msg = SystemMessage("Turn this document about formulating knowledge into a concise document:")
    human_msg = HumanMessage(data)

    messages = [system_msg, human_msg]
    response = model.invoke(messages).content

    with open(f'{knowledge_base_dir}/knowledge_base.json', 'w') as outfile:
        json.dump({"data": response}, outfile)

    if tempdir:
        tempdir.cleanup()
