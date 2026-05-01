"""LLM service for Gemini integration."""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage


class LLMService:
    """Service for LLM operations."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.llm = None  # Lazy initialization
    
    def _get_llm(self):
        """Get or create the LLM client (lazy initialization)."""
        if self.llm is None:
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                google_api_key=self.api_key,
                temperature=0.3
            )
        return self.llm
    
    async def synthesize_response(
        self,
        query: str,
        travel_style: str,
        destination: str,
        description: str,
        temperature: str,
        condition: str
    ) -> str:
        """Synthesize final travel plan using LLM."""
        
        prompt = f"""Based on the user's travel query and the analysis below, provide a concise travel recommendation:

User Query: {query}
Travel Style: {travel_style}
Recommended Destination: {destination}
Description: {description}
Current Weather: {temperature}, {condition}

Please provide a brief, compelling explanation (2-3 sentences) for why this destination matches their travel style."""
        
        # Get LLM client (lazy initialized)
        llm = self._get_llm()
        
        # Using invoke (synchronous call wrapped in async)
        message = HumanMessage(content=prompt)
        response = llm.invoke([message])
        
        return response.content
