import asyncio
import json
import os
from datetime import datetime

from dotenv import load_dotenv
from browser_use import Agent
#from langchain_ollama import ChatOllama
from browser_use import Agent, ChatGoogle

# =========================
# LOAD ENV VARIABLES
# =========================

load_dotenv()

# =========================
# LOAD PERSONA + JOURNEY
# =========================

persona_id = "ST-1"
journey_id = "JRN-102"

with open("personas.json", "r", encoding="utf-8") as f:
    personas = json.load(f)

with open("journeys.json", "r", encoding="utf-8") as f:
    journeys = json.load(f)

persona = personas[persona_id]
journey = journeys[journey_id]

# =========================
# CONNECT TO OLLAMA
# =========================

# llm = ChatOllama(
#     model=os.getenv("MODEL_NAME"),
#     base_url=os.getenv("OLLAMA_BASE_URL")
# )

llm = ChatGoogle(model='gemini-2.5-pro')

# =========================
# BUILD TASK
# =========================

task = f"""
You are an AI QA Testing Agent simulating a real human user interacting with ChatGPT.

-------------------------
PERSONA DETAILS
-------------------------
Name: {persona['name']}
Segment: {persona['segment']}
Bio: {persona['bio']}

Traits:
{', '.join(persona['traits'])}

Goals:
{', '.join(persona['goals'])}

-------------------------
TEST OBJECTIVE
-------------------------
Evaluate ChatGPT as a STUDY ASSISTANT for a computer science student.

Focus on:
- Clarity of explanations
- Context retention across steps
- Accuracy of technical responses
- Usefulness for exam preparation

-------------------------
TEST PLATFORM
-------------------------
https://chatgpt.com

-------------------------
EXECUTION RULES (CRITICAL)
-------------------------
1. Perform steps strictly in order (Step 1 → Step N)
2. DO NOT skip any step
3. WAIT for full AI response before proceeding
4. Treat each response as complete only when the answer is fully visible and finished
5. Do NOT evaluate partial or loading responses
6. Maintain conversation context across all steps
7. If AI asks a follow-up question, respond naturally before continuing
8. After each step, validate based ONLY on the expected result

-------------------------
TASK INSTRUCTIONS
-------------------------
1. Open ChatGPT website https://chatgpt.com
2. Execute the conversation journey step-by-step
3. After each step:
   - Perform the action
   - Wait for full response
   - Validate against expected result
   - Mark pass/fail observation
4. Continue until all steps are completed
5. At the end, summarize full execution

-------------------------
JOURNEY STEPS
-------------------------
"""
for step in journey["steps"]:
    task += f"""

Step {step['step']}
------------------
Action:
{step['action']}

Expected Result:
{step['expected']}
"""

task += """

Final Instructions:
-------------------
After all steps are completed:
- Summarize overall execution
- Mention issues observed
- Mention whether the journey succeeded or failed
"""

# =========================
# CREATE BROWSER AGENT
# =========================

agent = Agent(
    task=task,
    llm=llm,
    headless=False
)

# =========================
# MAIN EXECUTION
# =========================

async def main():

    print("\n==============================")
    print("STARTING AI TESTING AGENT")
    print("==============================\n")

    result = await agent.run()

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    results_dir = "results"

    # Create folder if it doesn't exist
    os.makedirs(results_dir, exist_ok=True)

    # =========================
    # CREATE JSON REPORT
    # =========================

    json_report = {
        "timestamp": timestamp,
        "persona_id": persona_id,
        "persona_name": persona["name"],
        "journey_id": journey_id,
        "journey_name": journey["name"],
        "result": str(result)
    }

    #json_filename = f"test_report_{timestamp}.json"

    json_filename = os.path.join(
    results_dir,
    f"test_report_{timestamp}.json"
    )

    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump(json_report, f, indent=4)

    # =========================
    # CREATE MARKDOWN REPORT
    # =========================

    md_content = f"""
# AI Testing Agent Report

## Test Information

- Timestamp: {timestamp}
- Persona ID: {persona_id}
- Persona Name: {persona['name']}
- Journey ID: {journey_id}
- Journey Name: {journey['name']}

---

# Persona Details

- Segment: {persona['segment']}
- Bio: {persona['bio']}

## Traits

"""

    for trait in persona["traits"]:
        md_content += f"- {trait}\n"

    md_content += "\n## Goals\n\n"

    for goal in persona["goals"]:
        md_content += f"- {goal}\n"

    md_content += "\n---\n"
    md_content += "\n# Journey Steps\n"

    for step in journey["steps"]:
        md_content += f"""
## Step {step['step']}

**Action:**  
{step['action']}

**Expected Result:**  
{step['expected']}
"""

    md_content += f"""

---

# Final Execution Result

```text
{result}

"""
    #md_filename = f"test_report_{timestamp}.md"

    md_filename = os.path.join(
    results_dir,
    f"test_report_{timestamp}.md"
    )

    with open(md_filename, "w", encoding="utf-8") as f:
        f.write(md_content)

# =========================
# PRINT OUTPUT
# =========================

    print("\n==============================")
    print("TEST EXECUTION COMPLETED")
    print("==============================\n")

    print(f"JSON Report Saved: {json_filename}")
    print(f"Markdown Report Saved: {md_filename}")

    print("\n==============================")
    print("FINAL RESULT")
    print("==============================\n")

    print(result)


asyncio.run(main())