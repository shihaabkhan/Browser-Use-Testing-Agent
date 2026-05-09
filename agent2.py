import asyncio
import json
import os
from datetime import datetime

from dotenv import load_dotenv
from browser_use import Agent
#from browser_use.llm import ChatOllama
from browser_use import Agent, ChatGoogle


load_dotenv()

# Load persona and journey
persona = json.load(open("personas.json"))["ST-1"]
journey = json.load(open("journeys.json"))["JRN-101"]

# Connect to local Ollama model
# llm = ChatOllama(
#     model=os.getenv("MODEL_NAME")
# )

llm = ChatGoogle(model='gemini-2.5-pro')

# Build testing task
task = """
You are testing a website using browser automation.

Follow these instructions EXACTLY.

STEP 1:
Open this URL:
https://www.wikipedia.org/

STEP 2:
Wait until the Wikipedia homepage fully loads.

STEP 3:
Find the search input box.

STEP 4:
Click the search input box.

STEP 5:
Type exactly:
Operating System

STEP 6:
Press Enter key.

STEP 7:
Wait for the article page to fully load.

STEP 8:
Read only the first introduction paragraph.

STEP 9:
Answer these questions using the article content:

1. What is an operating system?

STEP 10:
Generate 3 quiz questions related to operating systems.

STEP 11:
Summarize whether the test succeeded or failed.

IMPORTANT RULES:
- Do NOT repeatedly navigate to the same URL
- Do NOT search multiple times
- Do NOT open random URLs
- Stay only on Wikipedia
- Complete one step before moving to next step
- If page already loaded, continue instead of restarting
"""

# Create Browser Agent
agent = Agent(
    task=task,
    llm=llm,
    headless=False
)

async def main():
    result = await agent.run()

    print("\n===== FINAL RESULT =====\n")
    print(result)

asyncio.run(main())