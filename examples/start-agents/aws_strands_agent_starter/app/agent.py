import os
import json
import urllib.request
import urllib.parse
from dotenv import load_dotenv

from strands import Agent, tool
from strands.models.openai import OpenAIModel

# Load environment variables
load_dotenv()

@tool
def get_realtime_weather(location: str) -> str:
    """Fetches current weather data for a specified city or location."""
    print(f"   [System] Strands SDK executing tool: Geocoding '{location}'...")
    headers = {"User-Agent": "Strands-Agent-API/1.0"}
    
    try:
        # Step A: Convert city name to coordinates safely
        safe_location = urllib.parse.quote(location)
        geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={safe_location}&count=1&format=json"
        
        req = urllib.request.Request(geocode_url, headers=headers)
        with urllib.request.urlopen(req, timeout=15.0) as response:
            geo_data = json.loads(response.read().decode())
        
        if not geo_data.get("results"):
            return f"System Error: Could not find geographical coordinates for '{location}'."
            
        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]
        country = geo_data["results"][0].get("country", "Unknown Region")
        
        print(f"   [System] Strands SDK executing tool: Fetching weather for Lat: {lat}, Lon: {lon}...")
        
        # Step B: Fetch weather using coordinates
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,wind_speed_10m&timezone=auto"
        
        req2 = urllib.request.Request(weather_url, headers=headers)
        with urllib.request.urlopen(req2, timeout=15.0) as response2:
            weather_data = json.loads(response2.read().decode())
        
        current = weather_data.get("current", {})
        temp = current.get("temperature_2m", "Unknown")
        wind = current.get("wind_speed_10m", "Unknown")
        
        return f"Location: {location}, {country}. Temperature: {temp}°C, Wind Speed: {wind} km/h."
        
    except Exception as e:
        print(f"   [Tool Error] API connection failed: {str(e)}")
        return f"System Error: Network failure inside the weather tool - {str(e)}"

def initialize_agent() -> Agent:
    """Initializes and returns the Strands SDK Agent."""
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("Environment Error: OPENAI_API_KEY is not defined.")

    llm_provider = OpenAIModel(
        client_args={
            "api_key": os.getenv("OPENAI_API_KEY"),
            "timeout": 60.0,
            "max_retries": 3
        },
        model_id="gpt-4o-mini" 
    )

    return Agent(
        model=llm_provider,
        tools=[get_realtime_weather],
        system_prompt=(
            "You are a concise, highly accurate weather assistant. "
            "Use the provided tool to fetch real-time weather data for the user's requested location. "
            "Extract the location from the prompt, fetch the data, and present the findings clearly."
        )
    )

# Singleton instance of the agent to avoid re-initializing on every API call
strands_agent = initialize_agent()

def invoke_agent(user_query: str) -> str:
    """Passes the prompt to the Strands framework and returns the string response."""
    result = strands_agent(user_query)
    
    # Convert the Strands AgentResult object into a standard Python string
    return str(result)