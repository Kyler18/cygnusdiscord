from supabase import create_client, Client
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, LLMChain
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Supabase client
url = os.getenv("SUPABASE_URL")
DBkey = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, DBkey)

# Query 'messages' table to get all rows from a specific author
author = "re1yk"
response = supabase.table("messages").select("*").eq("author", author).execute()
messages = response.data

# Initialize OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")

# Parse the messages with OpenAI query
parsed_messages = []
graded_response = []

for message in messages:
    parsed_messages.append(author)
    parsed_messages.append(message)

# Define your OpenAI query
template = template = """
Provide me a token count for all content in {parsed_messages}. This should be the first thing in your response for every answer.

You are an AI trained to analyze the sentiment of messages and grade their helpfulness on a scale of 1-100.

Helpfulness in this context is a coach/student relationship with the author being the coach or student and providing assistance to students.

Here is some criteria you can use to provide a grade:

Availability: Frequency, response time, extra effort.
Guidance Quality: Clear feedback, resources, balanced critique.
Knowledge: Domain expertise, updated info, advanced concepts.
Listening: Active listening, understanding student needs.
Relationship: Safe environment, trust, respect.
Goals: Clear objectives, progress tracking, strategy adjustment.
Empowerment: Independent thinking, decision-making, confidence building.
Networking: Professional introductions, growth opportunities.
Adaptability: Adjusts techniques, feedback responsiveness.
Soft Skills: Communication, leadership, self-awareness.
Outcomes: Skills improvement, milestones achieved.

Here is the message content:

{parsed_messages}

Please analyze these messages and grade their helpfulness as a whole not for each message. Do your best to provide a summarized grade in an integer format.
"""
prompt = PromptTemplate(template=template, input_variables=["parsed_messages"])

llm_chain = LLMChain(prompt=prompt, llm=llm)
response = llm_chain.run(parsed_messages)
graded_response.append(response)

# Store the parsed messages back into your Supabase database
data = {
        'author': author,
        'result': graded_response,
    }
supabase.table("analysis").insert(data).execute()

# Return the parsed messages
print(parsed_messages)