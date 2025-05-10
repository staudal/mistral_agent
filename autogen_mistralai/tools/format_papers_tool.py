from typing import Annotated, List, Dict

def format_papers(
    papers: Annotated[List[Dict], "A list of papers, each with title, authors, year, citation_count, and url."]
) -> Annotated[str, "A formatted, readable list of papers."]:
    if not papers:
        return "No papers found."
    lines = []
    for i, paper in enumerate(papers, 1):
        authors = paper.get('authors', [])
        if isinstance(authors, str):
            authors = [a.strip() for a in authors.split(',')]
        lines.append(
            f"{i}. {paper.get('title', 'No title')}\n"
            f"   Authors: {', '.join(authors)}\n"
            f"   Year: {paper.get('year', 'N/A')}\n"
            f"   Citations: {paper.get('citation_count', 'N/A')}\n"
            f"   URL: {paper.get('url', '')}\n"
        )
    return "\n".join(lines) 