import ast
import copy
from autogen import AssistantAgent, UserProxyAgent, ChatResult, register_function
from autogen.coding import LocalCommandLineCodeExecutor
from autogen_mistralai.tools.semantic_scholar_search_tool import semantic_scholar_search
from autogen_mistralai.config import LLM_CONFIG
from autogen_mistralai.tools.format_papers_tool import format_papers

ReAct_prompt = """
Answer the following questions as best you can. You have access to the tools provided.

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do and what tool to use
Action: the action to take is ALWAYS one of the provided tools
Action Input: the input to the action
Observation: the result of the action. Only observe tools' outputs.
... (this thought/action/action input/observation can repeat N times)
Thought: I now know the answer
Answer: Format the research papers as a readable, bulleted list. For each paper, include the title, authors, year, citation count, and URL.

Begin!
Question: {input}
"""

def react_prompt_message(sender, recipient, context):
    return ReAct_prompt.format(input=context["question"])

def create_research_paper_agent() -> AssistantAgent:
    agent = AssistantAgent(
        name="ResearchPaperAssistant",
        system_message="""
        Only use tools. Don't try to reason. Reply TERMINATE when the task is done.
        """,
        llm_config=copy.deepcopy(LLM_CONFIG)
    )
    return agent

def create_user_proxy(code_executor: LocalCommandLineCodeExecutor):
    user_proxy = UserProxyAgent(
        name="User",
        llm_config=None,
        is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().lower().endswith("terminate"),
        human_input_mode="NEVER",
        max_consecutive_auto_reply=10,
        code_execution_config={
            "executor": code_executor
        },
    )
    return user_proxy

def create_local_code_executor():
    return LocalCommandLineCodeExecutor(
        timeout=100,
    )

def setup_agents():
    code_executor = create_local_code_executor()
    user_proxy = create_user_proxy(code_executor)
    research_paper_agent = create_research_paper_agent()

    # Register the semantic scholar search tool
    print("registering semantic scholar search tool")
    register_function(
        semantic_scholar_search,
        caller=research_paper_agent,
        executor=user_proxy,
        name="semantic_scholar_search",
        description="Search for research papers by topic, citation count, year range, and count."
    )

    # Register the format papers tool
    print("registering format papers tool")
    register_function(
        format_papers,
        caller=research_paper_agent,
        executor=user_proxy,
        name="format_papers",
        description="Format a list of research papers into a readable, bulleted list."
    )

    return user_proxy, research_paper_agent

def get_tool_calls(chat_result: ChatResult):
    tool_call_history = []
    for message in chat_result.chat_history:
        if "tool_calls" in message.keys():
            tool_calls = map(lambda x: { "name": x["function"]["name"], "arguments": ast.literal_eval(x["function"]["arguments"]) }, message["tool_calls"])
            tool_call_history.extend(list(tool_calls))
    return tool_call_history

def main():
    user_proxy, research_paper_agent = setup_agents()
    # Example task
    task = "Find 2 research papers on machine learning that has at least 1000 citations between 2012 and 2016"
    user_proxy.initiate_chat(
        research_paper_agent,
        message=task,
    )

if __name__ == "__main__":
    main() 