#!/usr/bin/env python3
"""
Quick test runner for the Smart Travel Planner backend.
Run this to verify the setup without Docker.
"""

import sys
import os
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

def test_imports():
    """Test that all imports work."""
    print("🔍 Testing imports...")
    try:
        from app.core.config import settings
        from app.models.schemas import TravelPlanRequest
        from app.tools.classifier_tool import classify_travel_style
        from app.tools.rag_tool import retrieve_destination
        from app.tools.weather_tool import get_weather
        from app.services.agent_service import AgentService
        from app.services.llm_service import LLMService
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False


def test_classifier():
    """Test the classifier tool."""
    print("\n🧪 Testing Classifier Tool...")
    from app.tools.classifier_tool import classify_travel_style
    
    test_cases = [
        ("adventure hiking", "adventure"),
        ("luxury resort", "luxury"),
        ("cultural museum", "cultural"),
        ("beach relax", "relaxation"),
        ("cheap backpack", "budget"),
    ]
    
    for query, expected in test_cases:
        result = classify_travel_style(query)
        style = result["travel_style"]
        status = "✅" if expected in style or style == "balanced" else "⚠️"
        print(f"{status} '{query}' → {style}")
    
    return True


def test_rag():
    """Test the RAG tool."""
    print("\n🧪 Testing RAG Tool...")
    from app.tools.rag_tool import retrieve_destination
    
    styles = ["adventure", "luxury", "cultural", "relaxation", "budget"]
    
    for style in styles:
        result = retrieve_destination(style)
        print(f"✅ {style} → {result['destination']}")
    
    return True


def test_weather():
    """Test the weather tool."""
    print("\n🧪 Testing Weather Tool...")
    from app.tools.weather_tool import get_weather
    
    destinations = ["Bali, Indonesia", "Tokyo, Japan", "Paris, France"]
    
    for destination in destinations:
        result = get_weather(destination)
        print(f"✅ {destination} → {result['temperature']}, {result['condition']}")
    
    return True


def test_agent():
    """Test the agent service."""
    print("\n🧪 Testing Agent Service...")
    from app.services.agent_service import AgentService
    import asyncio
    
    async def run_test():
        service = AgentService()
        result = await service.run_agent("I want to relax at a beach")
        print(f"✅ Query: 'I want to relax at a beach'")
        print(f"   Style: {result['travel_style']}")
        print(f"   Destination: {result['destination']}")
        print(f"   Weather: {result['weather_info']}")
        return True
    
    try:
        return asyncio.run(run_test())
    except Exception as e:
        print(f"❌ Agent test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 50)
    print("Smart Travel Planner - Backend Tests")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Classifier", test_classifier),
        ("RAG", test_rag),
        ("Weather", test_weather),
        ("Agent", test_agent),
    ]
    
    results = {}
    for name, test_func in tests:
        try:
            results[name] = test_func()
        except Exception as e:
            print(f"❌ {name} failed: {e}")
            results[name] = False
    
    print("\n" + "=" * 50)
    print("Test Results")
    print("=" * 50)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for name, result in results.items():
        status = "✅" if result else "❌"
        print(f"{status} {name}")
    
    print(f"\nPassed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
