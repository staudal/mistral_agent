from typing import Annotated, List, Dict
from autogen import AssistantAgent
from autogen_mistralai.config import LLM_CONFIG

def format_papers(
    papers: Annotated[List[Dict], "A list of papers, each with title, authors, year, citation_count, and url."]
) -> Annotated[str, "A formatted, readable list of papers."]:
    if not papers:
        return "No papers found."
    agent = AssistantAgent(
        name="Paper Formatter",
        system_message=(
            "You are a helpful AI assistant. "
            "Given a list of research papers (with title, authors, year, citation count, and URL), "
            "format them as a readable, bulleted list. "
            "Each paper should be on its own line, with all details clearly labeled. "
        ),
        llm_config=LLM_CONFIG,
    )
    prompt = f"Format the following list of research papers as a readable, bulleted list.\n\n{papers}"
    reply = agent.generate_reply(
        messages=[{"role": "user", "content": prompt}]
    )
    if not reply:
        return "No reply from LLM."
    if isinstance(reply, dict):
        reply_content = reply.get("content", "")
    else:
        reply_content = str(reply)
    return reply_content
