import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

class Agents:
    def __init__(self, google, gpt, claude):
        self.google = google
        self.gpt = gpt
        self.claude = claude

    def google_agent(self):
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")
        model = ChatGoogleGenerativeAI(api_key=api_key, model="gemini-2.0-flash", 
                                       temperature=0.1,
                                       max_output_tokens=None,
                                       )
        return model
    
    def gpt_agent(self):
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        model = ChatOpenAI(model="gpt-4o-mini", temperature=0.1, 
                           max_tokens=None, openai_api_key=api_key)
        return model
    
    def claude_agent(self):
        load_dotenv()
        api_key = os.getenv("ANTHROPIC_API_KEY")
        model = ChatAnthropic(model="claude-3-haiku", temperature=0.1, 
                              max_tokens=None, anthropic_api_key=api_key)
        return model
    
    
