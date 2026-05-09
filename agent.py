import asyncio
import json
import os
from datetime import datetime

from dotenv import load_dotenv
from browser_use import Agent
from browser_use.llm import ChatOllama

load_dotenv()

# Load persona and journey
persona = json.load(open("personas.json"))["ST-1"]
journey = json.load(open("journeys.json"))["JRN-101"]

# Connect to local Ollama model
llm = ChatOllama(
    model=os.getenv("MODEL_NAME")
)

# Build testing task
task = f"""
You are acting as this user persona:

Name: {persona['name']}
Segment: {persona['segment']}
Bio: {persona['bio']}

Traits:
{', '.join(persona['traits'])}

Goals:
{', '.join(persona['goals'])}

Open ChatGPT website.

Perform this conversational journey step-by-step:

"""

for step in journey["steps"]:
    task += f"""
Step {step['step']}:
Action: {step['action']}
Expected Result: {step['expected']}
"""

task += """

After completing all steps,
summarize whether the conversation was successful.
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