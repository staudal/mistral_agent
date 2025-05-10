import autogen
import json
from autogen_mistralai.agent.research_paper_agent import setup_agents, find_final_answer
from autogen_mistralai.config import LLM_CONFIG

user_proxy, agent = setup_agents()
critic_agent = autogen.AssistantAgent(
    name="critic_agent",
    llm_config=LLM_CONFIG
)

prompts = [
    "Find 5 research papers on artificial intelligence that has at least 1000 citations between 2001 and 2025",
    "Find 3 research papers on deep learning that has at least 200 citations between 2003 and 2020",
]

for prompt in prompts:
    # Get agent response using the chat loop and extract the final answer
    chat_result = user_proxy.initiate_chat(agent, message=prompt)
    agent_response = find_final_answer(chat_result)
    if not agent_response:
        # fallback: try to get the last message content
        agent_response = chat_result.chat_history[-1].get("content", "")

    # Critic prompt
    critic_prompt = f"""
You are evaluating an AI research paper recommendation agent.

Evaluate the response based on these criteria:
- Completeness (1-5): addresses every part of the request.
- Quality (1-5): accurate, clear, and effectively structured.
- Robustness (1-5): handles ambiguities, errors, or nonsensical input well.
- Consistency (1-5): maintains consistent reasoning with specified user needs.
- Specificity (1-5): provides detailed and relevant recommendations with clear justifications.

Additionally:
- Check if the agent response provided clear context and justifications.
- Determine if the agent accurately interpreted ambiguous prompts.
- Assess realism, practicality, and feasibility of recommendations.

User Prompt: {prompt}
Agent Response: {agent_response}

Provide your evaluation as JSON with fields:
- completeness
- quality
- robustness
- consistency
- specificity
- feedback (a brief descriptive explanation including specific examples from the response)
"""

    critic_evaluation = critic_agent.generate_reply([{"role": "user", "content": critic_prompt}])
    # Try to parse JSON, fallback to raw output if parsing fails
    try:
        result = json.loads(critic_evaluation if isinstance(critic_evaluation, str) else critic_evaluation.get("content", ""))
    except Exception:
        result = critic_evaluation

    print(f"Prompt: {prompt}\nAgent Response: {agent_response}\nCritic Evaluation: {result}\n{'-'*60}\n") 