from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool 
from datetime import datetime
import webbrowser
import os

search = DuckDuckGoSearchRun()
search_tool = Tool(
    name="search",
    func=search.run,
    description="Search the web for information",
)

wikipedia_api_wrapper = WikipediaAPIWrapper(top_k_results=1,doc_content_chars_max=100)
wiki_tool = WikipediaQueryRun(api_wrapper=wikipedia_api_wrapper)

def current_date_and_time(query=""):
    now = datetime.now()
    return now.strftime("%B %d, %Y, %I:%M %p")

def open_youtube(query=""):
    webbrowser.open("https://youtube.com")
    return "Youtube opened successfully"

def open_github(query=""):
    webbrowser.open("https://github.com")
    return "Github opened successfully"

def open_vscode(query=""):
    os.system("code .")

datetime_tool = Tool(
    name="current_datetime",
    func=current_date_and_time,
    description="Get the current date and time in the format 'Month Day, Year, Hour:Minute AM/PM'"
)
openyt = Tool(
    name="open_youtube",
    func=open_youtube,
    description="Opens youtube on the device using the webbrowser python module"
)

opengithub = Tool(
    name="open_github",
    func=open_github,
    description="Opens github on the device using the webbrowser python module"
)
openvscode = Tool(
    name="open_vscode",
    func=open_vscode,
    description="Opens vs code on the device using the os python module"
)