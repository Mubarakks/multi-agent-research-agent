from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search,scrape_url
# import os
from dotenv import load_dotenv
load_dotenv()

# model setup
llm=ChatGroq(model="openai/gpt-oss-20b",temperature=0)

# 1st agent
def search_agent():
    return create_agent(
        model = llm,
        tools=[web_search]
    )


# 2nd 
def reader_agent():
    return create_agent(
        model =llm,
        tools=[scrape_url]
    )

# writer chain

writer_prompt = ChatPromptTemplate.from_messages([
    ('system','you are an expert research write. write clear and structured and insightful reports.'),
    ('human',"""write a detailed research report on the topic below.
    
   Topic :{topic}

   Research Gathered:
   {research}

   Structure the report as :
   - Introduction
   - Key findings (minimum 3 well explained points) 
   - Conclusion
   - Sources (list all URLs found in the research)

   Be detailed, factual and professional.
    """),
])

writer_chain =writer_prompt|llm|StrOutputParser()

# critics chain to judge the output

critic_prompt = ChatPromptTemplate.from_messages([
    ('system','you are a sharp and constructive research critic. be honest and specific.'),
    ('human',""" Review the research report below and evaluate it strictly.
    Report:
    {report}

    Respond in this exact format:

    Score:X/10

    Strengths:
    - ...
    - ...

    Areas to Improve:
    - ...
    - ... 

    One line verdict:
    ...

""")
])

critic_chain =critic_prompt | llm | StrOutputParser()

