from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool 
from datetime import datetime
import webbrowser
import os
import subprocess

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
    if query:
        webbrowser.open(f"{query}")
    else:
        webbrowser.open("https://youtube.com")
    return "Youtube opened successfully"

def open_github(query=""):
    if query:
        webbrowser.open(f"https://github.com/search?q={query}")
    else:
        webbrowser.open("https://github.com")
    return "Github opened successfully"

def open_vscode(query=""):
    os.system("code .")

def get_system_info(query=""):
    Id = subprocess.check_output(['systeminfo']).decode('utf-8').split('\n')
    new = []
    for item in Id:
        new.append(str(item.split("\r")[:-1]))
    return new

def google_search(query=""):
    if query:
        webbrowser.open(f"https://www.google.com/search?q={query}")
    else:
        webbrowser.open("https://google.com")

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
    description="Opens github on the device using the webbrowser python module when no query is given and when query is given it searches that"
)
openvscode = Tool(
    name="open_vscode",
    func=open_vscode,
    description="Opens vs code on the device using the os python module"
)
getsysinfo = Tool(
    name="get_system_info",
    func=get_system_info,
    description="Gets the compelete system info using the subprocess module and returns a list"
)

googleSearch = Tool(
    name="google_search",
    func=google_search,
    description="Opens google when no query is given and searches the query when query is given"
) 