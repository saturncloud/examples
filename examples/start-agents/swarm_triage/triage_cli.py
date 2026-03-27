import os
import sys
from dotenv import load_dotenv
from swarm import Swarm, Agent

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    print("❌ Error: OPENAI_API_KEY not found in .env file.")
    sys.exit(1)

client = Swarm()

# --- 1. Define the Agents ---
triage_agent = Agent(
    name="Triage Agent",
    instructions="You are the frontline customer support router. Greet the user and transfer them to the correct department (Sales, Tech, or Billing) immediately. Do not answer specific questions yourself.",
)

sales_agent = Agent(
    name="Sales Agent",
    instructions="You handle sales inquiries. Explain pricing tiers (Basic $29, Pro $59, Enterprise $99) and try to close the deal. If the user asks a technical question, use transfer_to_tech. If they ask about refunds, use transfer_to_billing. If they demand a human, use escalate_to_human.",
)

tech_agent = Agent(
    name="Tech Support Agent",
    instructions="You handle technical issues. Ask for error codes and provide troubleshooting steps. If the user asks about pricing, use transfer_to_sales. If they ask about refunds, use transfer_to_billing. If they demand a human, use escalate_to_human.",
)

billing_agent = Agent(
    name="Billing Agent",
    instructions="You handle billing and refund requests. Be polite and ask for invoice numbers. If the user asks about pricing, use transfer_to_sales. If they ask a technical question, use transfer_to_tech. If they demand a human, use escalate_to_human.",
)

human_agent = Agent(
    name="Human Escalation",
    instructions="You are the safety net. Inform the user that you are escalating their ticket to a real human representative who will email them shortly. Do not attempt to solve their problem. If they want to start over, use transfer_to_triage.",
)

# --- 2. Define Handoff Functions (Docstrings are read by the AI!) ---
def transfer_to_sales():
    """Transfer to the Sales department for pricing, upgrades, and purchases."""
    return sales_agent

def transfer_to_tech():
    """Transfer to the Technical Support department for bugs, crashes, and errors."""
    return tech_agent

def transfer_to_billing():
    """Transfer to the Billing department for refunds, invoices, and payment issues."""
    return billing_agent

def transfer_to_triage():
    """Transfer back to the main Triage routing menu if the user wants to start over."""
    return triage_agent

def escalate_to_human():
    """Escalate to a human agent if the user is angry, asks for a human, or asks something completely off-topic."""
    return human_agent

# --- 3. Attach Omni-Directional Routing Capabilities ---
triage_agent.functions  = [transfer_to_sales, transfer_to_tech, transfer_to_billing, escalate_to_human]
sales_agent.functions   = [transfer_to_tech, transfer_to_billing, transfer_to_triage, escalate_to_human]
tech_agent.functions    = [transfer_to_sales, transfer_to_billing, transfer_to_triage, escalate_to_human]
billing_agent.functions = [transfer_to_sales, transfer_to_tech, transfer_to_triage, escalate_to_human]
human_agent.functions   = [transfer_to_triage]

# --- 4. The Interactive Loop ---
print("==================================================")
print("🐝 OpenAI Swarm Triage (Full Mesh Routing)")
print("🔄 Active Agents: Triage, Sales, Tech Support, Billing, Escalation")
print("💡 Type 'exit' to quit.")
print("==================================================\n")

active_agent = triage_agent
messages = []

while True:
    try:
        user_input = input("\n🧑 You: ")
        if user_input.lower() in ['exit', 'quit']:
            break
        if not user_input.strip():
            continue

        messages.append({"role": "user", "content": user_input})

        response = client.run(
            agent=active_agent,
            messages=messages
        )

        messages = response.messages
        active_agent = response.agent

        print(f"🤖 [{active_agent.name}]: {response.messages[-1]['content']}")

    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
