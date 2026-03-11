import os
import json
import urllib.request
import urllib.parse
from dotenv import load_dotenv
from google.adk.agents import Agent

# Load environment variables securely
load_dotenv()

# 1. Define a tool with a REAL internet connection
def get_realtime_weather(location: str) -> str:
    """Fetches real-time weather data for a specified location."""
    print(f"[System] Executing ADK Tool: Fetching live weather for {location}...")
    headers = {"User-Agent": "Google-ADK-Agent/1.0"}
    
    try:
        # Step A: Convert city name to coordinates safely
        safe_location = urllib.parse.quote(location)
        geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={safe_location}&count=1&format=json"
        
        req = urllib.request.Request(geocode_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10.0) as response:
            geo_data = json.loads(response.read().decode())
            
        if not geo_data.get("results"):
            return f"System Error: Could not find geographical coordinates for '{location}'."
            
        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]
        
        # Step B: Fetch real-time weather using coordinates
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,wind_speed_10m"
        
        req2 = urllib.request.Request(weather_url, headers=headers)
        with urllib.request.urlopen(req2, timeout=10.0) as response2:
            weather_data = json.loads(response2.read().decode())
            
        temp = weather_data.get("current", {}).get("temperature_2m", "Unknown")
        wind = weather_data.get("current", {}).get("wind_speed_10m", "Unknown")
        
        return f"Live Data -> Temperature: {temp}°C, Wind Speed: {wind} km/h."
    except Exception as e:
        return f"System Error: Network failure - {str(e)}"

# 2. Initialize the primary ADK agent
root_agent = Agent(
    name="production_weather_agent",
    model="gemini-2.5-flash", 
    description="A helpful assistant agent capable of checking real-time weather.",
    instruction="You are an expert, helpful assistant. Use the get_realtime_weather tool to answer user questions factually.",
    tools=[get_realtime_weather]
)