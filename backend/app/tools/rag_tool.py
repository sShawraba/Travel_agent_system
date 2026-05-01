"""Mock RAG tool for destination retrieval."""

# Hardcoded destination database
DESTINATIONS = {
    "tokyo": {
        "destination": "Tokyo, Japan",
        "description": "Vibrant metropolis blending ancient traditions with cutting-edge technology. Famous for temples, gardens, street food, and nightlife."
    },
    "bali": {
        "destination": "Bali, Indonesia",
        "description": "Tropical paradise with stunning beaches, rice terraces, and spiritual temples. Perfect for relaxation and water sports."
    },
    "paris": {
        "destination": "Paris, France",
        "description": "City of light and romance. Home to the Eiffel Tower, museums, galleries, and world-class cuisine."
    },
    "new_zealand": {
        "destination": "New Zealand",
        "description": "Adventure capital with dramatic landscapes, hiking trails, and extreme sports. Perfect for outdoor enthusiasts."
    },
    "dubai": {
        "destination": "Dubai, UAE",
        "description": "Luxury destination with modern architecture, shopping, and desert adventures. Known for luxury resorts and high-end experiences."
    },
    "barcelona": {
        "destination": "Barcelona, Spain",
        "description": "Mediterranean city famous for Gaudí's architecture, beaches, tapas culture, and vibrant nightlife."
    },
    "marrakech": {
        "destination": "Marrakech, Morocco",
        "description": "Exotic city with bustling souks, stunning palaces, and nearby deserts. Rich in culture and history."
    },
    "iceland": {
        "destination": "Iceland",
        "description": "Land of fire and ice with waterfalls, glaciers, and natural hot springs. Ideal for adventure and nature lovers."
    },
}


def retrieve_destination(travel_style: str, query: str = "") -> dict:
    """Retrieve destination based on travel style and query."""
    # Simple mapping of travel styles to destinations
    style_mapping = {
        "adventure": "new_zealand",
        "luxury": "dubai",
        "cultural": "marrakech",
        "relaxation": "bali",
        "budget": "barcelona",
    }
    
    # Check query for specific tropical/island preferences
    query_lower = query.lower()
    if any(word in query_lower for word in ["tropical", "island", "beach", "ocean", "paradise"]):
        destination_key = "bali"
    else:
        destination_key = style_mapping.get(travel_style, "tokyo")
    
    destination = DESTINATIONS.get(destination_key, DESTINATIONS["tokyo"])
    
    return destination
