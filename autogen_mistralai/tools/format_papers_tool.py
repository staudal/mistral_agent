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
            "Do not include any extra commentary or explanation. "
            "Return 'TERMINATE' when the task is done."
        ),
        llm_config=LLM_CONFIG,
    )
    # Prepare the input for the LLM
    paper_lines = []
    for i, paper in enumerate(papers, 1):
        authors = paper.get('authors', [])
        if isinstance(authors, str):
            authors = [a.strip() for a in authors.split(',')]
        paper_lines.append(
            f"{i}. Title: {paper.get('title', 'No title')}\n"
            f"   Authors: {', '.join(authors)}\n"
            f"   Year: {paper.get('year', 'N/A')}\n"
            f"   Citations: {paper.get('citation_count', 'N/A')}\n"
            f"   URL: {paper.get('url', '')}"
        )
    papers_text = "\n".join(paper_lines)
    prompt = f"Format the following list of research papers as a readable, bulleted list.\n\n{papers_text}"
    reply = agent.generate_reply(
        messages=[{"role": "user", "content": prompt}]
    )
    if not reply:
        return "No reply from LLM."
    if isinstance(reply, dict):
        reply_content = reply.get("content", "")
    else:
        reply_content = str(reply)
    # Remove 'TERMINATE' if present
    reply_content = reply_content.replace("TERMINATE", "").strip()
    return reply_content 