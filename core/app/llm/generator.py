from core import GlobalConstants
from core.app.llm.prompt import prompt
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser

llm = ChatOllama(model=GlobalConstants.LOCAL_LLM, temperature=.8)

generator = prompt | llm | StrOutputParser()
