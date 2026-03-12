import streamlit as st
import os
import httpx
from dotenv import load_dotenv
from pydantic_ai import Agent

# Initialize environment variables
load_dotenv()

# --- UI CONFIGURATION ---
st.set_page_config(
    page_title="PydanticAI Weather Agent",
    page_icon="🌤️",
    layout="centered",
)

st.title("Weather Information Agent")
st.markdown("Real-time meteorological data retrieval via PydanticAI tool calling.")

# Verify Environment
if not os.getenv("OPENAI_API_KEY"):
    st.error("Environment Error: OPENAI_API_KEY is not defined in the environment variables.")
    st.stop()

# --- AGENT INITIALIZATION ---
@st.cache_resource(show_spinner=False)
def initialize_agent():
    """Initializes the PydanticAI agent and defines its external tools. Cached for performance."""
    agent = Agent(
        'openai:gpt-4o-mini',
        system_prompt=(
            "You are a concise, highly accurate weather assistant. "
            "Use the provided tool to fetch real-time weather data for the user's requested location. "
            "Extract the location from the prompt, fetch the data, and present the findings clearly, "
            "including temperature and wind speed. Do not hallucinate metrics."
        ),
    )

    @agent.tool_plain
    def get_realtime_weather(location: str) -> str:
        """Fetches current weather data for a specified city or location."""
        # Geocoding Request
        geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1&format=json"
        geo_response = httpx.get(geocode_url).json()
        
        if not geo_response.get("results"):
            return f"System Error: Could not find geographical coordinates for '{location}'."
            
        lat = geo_response["results"][0]["latitude"]
        lon = geo_response["results"][0]["longitude"]
        country = geo_response["results"][0].get("country", "Unknown Region")
        
        # Weather Request
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,wind_speed_10m&timezone=auto"
        weather_data = httpx.get(weather_url).json()
        
        current = weather_data.get("current", {})
        temp = current.get("temperature_2m", "Unknown")
        wind = current.get("wind_speed_10m", "Unknown")
        
        return f"Location: {location}, {country}. Temperature: {temp}°C, Wind Speed: {wind} km/h."
        
    return agent

agent = initialize_agent()

# --- STATE MANAGEMENT ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "System online. Which location's weather would you like to check?"}
    ]

# Render chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- EXECUTION LOGIC ---
if prompt := st.chat_input("Ask for the weather in a specific city..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Executing Open-Meteo tool call sequence..."):
            try:
                # Execute the agent synchronously
                result = agent.run_sync(prompt)
                
                # Render and store response
                st.markdown(result.output)
                st.session_state.messages.append({"role": "assistant", "content": result.output})
                
            except Exception as e:
                st.error(f"API Execution Error: {str(e)}")