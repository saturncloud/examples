import streamlit as st
import nest_asyncio
import os
import requests
import pytz
from datetime import datetime
from dotenv import load_dotenv

from agno.agent import Agent
from agno.models.nebius import Nebius
from agno.tools.calcom import CalComTools

# Apply asyncio patch for running agents in Streamlit
nest_asyncio.apply()

# Load environment variables
load_dotenv()

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI Scheduling Assistant",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("📅 Autonomous Scheduling Assistant")
st.markdown("""
This agent connects to your **Cal.com** account to check availability and book meetings autonomously.
Tell it what you need, and it will handle the logistics.
""")

# --- SIDEBAR CONFIGURATION ---
st.sidebar.header("⚙️ Configuration")

nebius_key = os.getenv("NEBIUS_API_KEY")
calcom_key = os.getenv("CALCOM_API_KEY")

if not nebius_key or not calcom_key:
    st.sidebar.error("⚠️ Missing API Keys in .env file!")
    st.stop()

# 1. Dynamic Timezone Selection (UPGRADED TO DROPDOWN)
all_timezones = pytz.all_timezones
# Default to America/New_York, but fallback to 0 (Africa/Abidjan) if not found
default_tz_index = all_timezones.index("America/New_York") if "America/New_York" in all_timezones else 0

user_timezone = st.sidebar.selectbox(
    "Your Timezone", 
    options=all_timezones,
    index=default_tz_index,
    help="Select your local timezone so meetings are booked correctly."
)

# 2. Dynamic Event Type Fetching
@st.cache_data(ttl=600) # Cache API response for 10 mins
def fetch_calcom_events(api_key):
    url = "https://api.cal.com/v2/event-types"
    headers = {"Authorization": f"Bearer {api_key}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        # Create a dictionary mapping "Title" -> "ID"
        return {event['title']: event['id'] for event in data['data']['eventTypeGroups'][0]['eventTypes']}
    except Exception as e:
        st.sidebar.error(f"Failed to fetch Cal.com events: {e}")
        return {}

event_options = fetch_calcom_events(calcom_key)

if not event_options:
    st.sidebar.warning("No Event Types found in your Cal.com account.")
    st.stop()

selected_event_name = st.sidebar.selectbox("Select Meeting Type to Book", options=list(event_options.keys()))
selected_event_id = event_options[selected_event_name]


# --- AGENT SETUP (Cached Resource) ---
@st.cache_resource
def get_scheduling_agent(calcom_api_key, event_id, timezone):
    
    # Define system instructions
    instructions = f"""You are a scheduling assistant. Today is {datetime.now().strftime("%Y-%m-%d")}.
Your goal is to autonomously manage calendar bookings using the available tools.

IMPORTANT REASONING STEPS:
1. **Check Availability First:** Always use `get_available_slots(start_date, end_date)` before attempting to book.
2. **Book the Slot:** If a slot is available, use `create_booking(start_time, name, email)`.
3. **Verify:** After booking, confirm it exists using `get_upcoming_bookings(email)`.

When asked to book a call, you MUST follow these steps sequentially. Do not skip verification. confirm to the user only after verification succeeds.
"""
    # Initialize tools with selected settings
    tools = CalComTools(
        user_timezone=timezone,
        api_key=calcom_api_key,
        event_type_id=event_id
    )

    # Initialize agent (Removed show_tool_calls for Agno v2 compatibility)
    return Agent(
        name="Calendar Assistant",
        instructions=[instructions],
        model=Nebius(
            id="Qwen/Qwen3-30B-A3B-Instruct-2507",
            api_key=os.getenv("NEBIUS_API_KEY")
        ),
        tools=[tools],
        markdown=True,
    )

# Load the agent with current sidebar settings
agent = get_scheduling_agent(calcom_key, selected_event_id, user_timezone)


# --- CHAT INTERFACE ---

# Initialize chat history
if "messages" not in st.session_state:
    # Add an initial greeting from the assistant
    st.session_state.messages = [
        {"role": "assistant", "content": f"Hello! I'm ready to schedule **'{selected_event_name}'** meetings for you in the **{user_timezone}** timezone.\n\nWhat would you like me to do?"}
    ]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("e.g., 'Book a meeting with John Doe tomorrow at 10am'"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        with st.spinner("Checking calendar and reasoning..."):
            try:
                # Run the agent
                response = agent.run(prompt)
                st.markdown(response.content)
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response.content})
            except Exception as e:
                st.error(f"An error occurred: {e}")