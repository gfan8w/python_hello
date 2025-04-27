"""
    main file for accessing services.
"""

import os
from datetime import datetime
import aiohttp

from streaming_with_function_calling_fastapi.config.main import config

os.environ["OPENWEATHER_API_KEY"] = config.OPENWEATHER_API_KEY
os.environ["OPENWEATHER_API_ID"] = config.OPENWEATHER_API_ID


async def get_weather_information(city: str, latitude: int, longitude: int) -> str:
    """Gets the weather information for a given latitude and longitude."""
    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        current_day, current_month = datetime.now().day, datetime.now().month
        params = {
            "q": city,
            # "lat": latitude,
            # "lon": longitude,
            "id":os.environ.get("OPENWEATHER_API_ID"),
            "appid": os.environ.get("OPENWEATHER_API_KEY"),
            "month": current_month,
            "day": current_day,
        }
        result = None
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status != 200:
                    return "Sorry, I couldn't find the weather information for the given location."
                result = await response.json()
        # we format the response to be more user friendly
        result = result.get("result")
        if not result:
            return (
                "Sorry, I couldn't find the weather information for the given location."
            )
        return f"""
        For given Location:
            Mean temperature: {result['temp']['mean']} Kelvin
            Mean humidity: {result['humidity']['mean']} %
            Mean wind_speed: {result['wind']['mean']} m/s
            Mean pressure: {result['pressure']['mean']} hPa
            Mean precipitation: {result['precipitation']['mean']} mm
        """
    except Exception:  # pylint: disable=broad-except
        return "Sorry, I couldn't find the weather information for the given location."
