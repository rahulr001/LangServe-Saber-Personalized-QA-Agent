from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from app.utils import local_llm
from app.prompt import prompt

llm = ChatOllama(model=local_llm, temperature=.8)

generator = prompt | llm | StrOutputParser()