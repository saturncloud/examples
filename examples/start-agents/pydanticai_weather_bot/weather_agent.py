import os
import httpx
from dotenv import load_dotenv
from pydantic_ai import Agent

# 1. Initialize environment variables
load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("Environment Error: OPENAI_API_KEY is not defined.")

# 2. Configure the PydanticAI Agent
agent = Agent(
    'openai:gpt-4o-mini',
    system_prompt=(
        "You are a concise, highly accurate weather assistant. "
        "Use the provided tool to fetch real-time weather data for the user's requested location. "
        "Extract the location from the prompt, fetch the data, and present the findings clearly, "
        "including temperature and wind speed."
    ),
)

# 3. Define the Tool utilizing Pydantic validation natively
@agent.tool_plain
def get_realtime_weather(location: str) -> str:
    """Fetches current weather data for a specified city or location."""
    print(f"   [System] Executing tool: Geocoding '{location}'...")
    
    # Step A: Convert city name to coordinates
    geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1&format=json"
    geo_response = httpx.get(geocode_url).json()
    
    if not geo_response.get("results"):
        return f"System Error: Could not find geographical coordinates for '{location}'."
        
    lat = geo_response["results"][0]["latitude"]
    lon = geo_response["results"][0]["longitude"]
    country = geo_response["results"][0].get("country", "Unknown Region")
    
    print(f"   [System] Executing tool: Fetching weather for Lat: {lat}, Lon: {lon}...")
    
    # Step B: Fetch weather using coordinates
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,wind_speed_10m&timezone=auto"
    weather_data = httpx.get(weather_url).json()
    
    current = weather_data.get("current", {})
    temp = current.get("temperature_2m", "Unknown")
    wind = current.get("wind_speed_10m", "Unknown")
    
    return f"Location: {location}, {country}. Temperature: {temp}°C, Wind Speed: {wind} km/h."

# 4. Execution Logic
if __name__ == "__main__":
    print("--- PydanticAI Weather Bot ---")
    print("Agent is ready. (Type 'exit' to quit)")
    
    while True:
        user_query = input("\nAsk for the weather: ")
        
        if user_query.lower() in ['exit', 'quit']:
            print("Terminating process.")
            break
            
        if user_query.strip():
            try:
                # Execute the agent synchronously
                result = agent.run_sync(user_query)
                
                # FIXED: Access the text payload via .output instead of .data
                print(f"\nAgent: {result.output}")
                
            except Exception as e:
                print(f"\nAPI Execution Error: {e}")