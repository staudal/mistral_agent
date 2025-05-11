import requests
from typing import Annotated, List, Optional, TypedDict

class Paper(TypedDict):
    title: str
    authors: List[str]
    year: int
    citation_count: int
    url: str

def semantic_scholar_search(
    topic: Annotated[str, "The research topic to search for."],
    min_citations: Annotated[Optional[int], "Minimum number of citations"],
    year_from: Annotated[Optional[int], "Start year (inclusive)"],
    year_to: Annotated[Optional[int], "End year (inclusive)"],
    count: Annotated[int, "Number of papers to return"]
) -> Annotated[List[Paper], "A list of research papers matching the criteria."]:
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": topic,
        "limit": count,
        "fields": "title,authors,year,citationCount,url"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    results = []
    for paper in data.get("data", []):
        # Filter by year and citation count
        year = paper.get("year")
        citation_count = paper.get("citationCount")
        if year_from and (year is None or year < year_from):
            continue
        if year_to and (year is None or year > year_to):
            continue
        if min_citations and (citation_count is None or citation_count < min_citations):
            continue
        authors_data = paper.get("authors", [])
        if isinstance(authors_data, list):
            authors = [a.get("name", "") for a in authors_data if isinstance(a, dict)]
        else:
            authors = [str(authors_data)]
        results.append({
            "title": paper.get("title", ""),
            "authors": authors,
            "year": year,
            "citation_count": citation_count,
            "url": paper.get("url", "")
        })
        if len(results) >= count:
            break
    return results
