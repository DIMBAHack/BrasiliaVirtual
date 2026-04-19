"""
Serviço de agentes IA: Claude, GPT e Gemini.
Cada método retorna uma instância pronta para uso.
"""
import os
from dotenv import load_dotenv

load_dotenv()


class AgentsService:

    @staticmethod
    def claude_agent():
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(
            model="claude-3-haiku-20240307",
            temperature=0.1,
            max_tokens=1024,
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY", ""),
        )

    @staticmethod
    def gpt_agent():
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.1,
            max_tokens=1024,
            openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        )

    @staticmethod
    def google_agent():
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0.1,
            google_api_key=os.getenv("GOOGLE_API_KEY", ""),
        )
