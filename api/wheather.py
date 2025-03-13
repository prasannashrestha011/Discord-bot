import os
from urllib import response
from dotenv import load_dotenv
import httpx
load_dotenv()
WHEATHER_API_KEY=os.getenv("WHEATHER_API_KEY")
async def get_weather(city:str)->str:
    print(WHEATHER_API_KEY)
    url=f"http://api.weatherapi.com/v1/current.json?key={WHEATHER_API_KEY}&q={city}"
    try:
        async with httpx.AsyncClient() as client:
            response=await client.get(url)
            
            if response.status_code==404:
                return "❌ City not found. Please try again with a valid city name."
            if response.status_code==401:
                return "🔑 Request unauthorized. Please check your API key."
        
            data=response.json()
            city=data["location"]["name"]
            country=data["location"]["country"]
            temp_c = data["current"]["temp_c"]
            condition = data["current"]["condition"]["text"]
            humidity = data["current"]["humidity"]
            wind_kph = data["current"]["wind_kph"]

            return (
            f"🌍 **Weather in {city}, {country}**\n"
            f"🌡 Temperature: {temp_c}°C\n"
            f"🌫 Condition: {condition}\n"
            f"💧 Humidity: {humidity}%\n"
            f"🌬 Wind Speed: {wind_kph} kph"
            )

    except Exception as e:
        return "Failed to fetch the wheather data"