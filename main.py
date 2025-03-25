from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool 
from tools import search_tool, wiki_tool, datetime_tool, openyt, opengithub, openvscode
import json
import re
import pyttsx3
engine = pyttsx3.init()

def say(text):
    engine.say(text)
    engine.runAndWait()

load_dotenv()

class JarvisResponse(BaseModel):
    query: str
    response: str
    details: dict
    tools_used: list[str]


llm = ChatGroq(model="llama-3.2-90b-vision-preview")  


prompt = ChatPromptTemplate.from_messages([
    ("system", """
    You are Jarvis, a highly intelligent AI companion built for versatility and precision. Assist with any query—research, calculations, real-time info, actions like opening YouTube, or casual questions—delivering clear, witty, and actionable responses.

    Instructions:
    - Begin with "Sir".
    - For simple actions (e.g., opening YouTube), respond naturally and perform the task.
    - For informational queries, provide structured info in JSON if possible:
      - 'query': restate the query.
      - 'response': direct answer.
      - 'details': supporting info (e.g., sources, context) as a dictionary.
      - 'tools_used': list tools (e.g., "internal knowledge", "search", "wikipedia", "current_datetime", "open_youtube", "open_github", "open_vscode").
    - Use tools when needed: "current_datetime" for time, "search" for web info, "wikipedia" for facts, "open_youtube" to open YouTube, "open_github" to open github. "open_vscode" to open visual studio code (vs code).
    - If unclear, ask for clarification concisely.

    Keep it sharp, sophisticated, and mission-ready. Use chat history if relevant: {chat_history}
    """),
    ("placeholder", "{chat_history}"),
    ("human", "{query}"),
    ("placeholder", "{agent_scratchpad}"),
])

search = DuckDuckGoSearchRun()
search_tool = Tool(
    name="search",
    func=search.run,
    description="Search the web for information"
)

wikipedia_api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=100)
wiki_tool = WikipediaQueryRun(api_wrapper=wikipedia_api_wrapper)

tools = [search_tool, wiki_tool, datetime_tool, openyt, opengithub, openvscode]

agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

def parse_response(output):
    json_match = re.search(r'\{.*\}', output, re.DOTALL)
    if json_match:
        try:
            json_data = json.loads(json_match.group(0))
            return JarvisResponse(**json_data)
        except (json.JSONDecodeError, ValueError):
            return output 
    return output 


while True:
    query = input("How may I assist you today, Sir? (or 'exit' to quit) ")
    if query.lower() == "exit" or query.lower() == "quit":
        break
    raw_response = agent_executor.invoke({"query": query})
    structured_response = parse_response(raw_response["output"])
    # print("Raw Response:", raw_response)
    print("Structured Response:", structured_response)
    say(structured_response)