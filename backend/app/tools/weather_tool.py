"""Mock weather tool for destination weather info."""

import random


def get_weather(destination: str) -> dict:
    """Get weather information for a destination."""
    weather_conditions = ["Sunny", "Partly Cloudy", "Clear Skies", "Warm", "Perfect"]
    condition = random.choice(weather_conditions)
    
    # Simulated temperatures based on destination
    if "tropical" in destination.lower() or "bali" in destination.lower():
        temp = f"{random.randint(28, 32)}°C"
    elif "paris" in destination.lower():
        temp = f"{random.randint(12, 18)}°C"
    elif "iceland" in destination.lower():
        temp = f"{random.randint(5, 10)}°C"
    else:
        temp = f"{random.randint(20, 28)}°C"
    
    return {
        "temperature": temp,
        "condition": condition
    }
