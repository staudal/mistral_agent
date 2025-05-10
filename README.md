# Research Paper Agent

This project provides an AI agent that can search for scientific research papers using natural language queries, leveraging the Semantic Scholar API, Mistral LLM, and a modular tool-based architecture.

## Features
- Accepts natural language queries like:
  - "Find 6 research papers on climate change that has at least 10 citations and is published between 2012 and 2016."
  - "Find 3 research papers about machine learning with more than 1200 citations and that has been published after 2010."
- Extracts topic, citation, and year constraints from the query.
- Uses the Semantic Scholar API to find relevant papers.
- Formats the results in a readable, bulleted list (title, authors, year, citations, URL).

## Directory Structure
```
autogen_mistralai/
  agent/
    research_paper_agent.py      # Main agent logic
  tools/
    semantic_scholar_search_tool.py  # Tool for querying Semantic Scholar
    format_papers_tool.py            # Tool for formatting paper lists
```

## How to Run
1. **Navigate to the project root:**
   ```sh
   cd /Users/jakobstaudal/aiagent
   ```
2. **Run the agent using Python's module syntax:**
   ```sh
   python -m autogen_mistralai.agent.research_paper_agent
   ```
   This will execute the example query in `main()`.

3. **Modify the Query:**
   - Edit the `task` variable in `autogen_mistralai/agent/research_paper_agent.py` to use your own search prompt.

## Example Output
```
1. Climate Change 2014 - Synthesis Report
   Authors: Jean-Pascal van Ypersele de Strihou
   Year: 2015
   Citations: 4753
   URL: https://www.semanticscholar.org/paper/d5ab152a21eff7560fae68710c082da76ac86f23

2. Climate Change 2013: The Physical Science Basis
   Authors: Reinhard F. Stocker, D. Qin, G. Plattner, ...
   Year: 2013
   Citations: 13142
   URL: https://www.semanticscholar.org/paper/10aa6b29ca7077ac5656c9df7f2efc8cab158851
```