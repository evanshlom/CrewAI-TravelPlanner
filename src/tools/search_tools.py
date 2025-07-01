from crewai_tools import BaseTool, tool
from typing import Type
from pydantic import BaseModel, Field
from crewai_tools import SerperDevTool

# Initialize SerperDev for web search
search_tool = SerperDevTool()

class EventSearchInput(BaseModel):
    """Input schema for event search."""
    query: str = Field(..., description="Search query for events")

class HotelSearchInput(BaseModel):
    """Input schema for hotel search."""
    location: str = Field(..., description="Location to search hotels")
    dates: str = Field(None, description="Optional date range")

@tool("search_stadium_events", args_schema=EventSearchInput)
def search_stadium_events(query: str) -> str:
    """Search for events at Allegiant Stadium and Las Vegas venues."""
    return search_tool.run(f"Allegiant Stadium events {query} Las Vegas shows concerts")

@tool("search_hotel_deals", args_schema=HotelSearchInput)
def search_hotel_deals(location: str, dates: str = None) -> str:
    """Search for affordable hotel deals."""
    search_query = f"cheap affordable hotels {location} deals"
    if dates:
        search_query += f" {dates}"
    return search_tool.run(search_query)

@tool("search_flights")
def search_flights(origin: str, destination: str = "Las Vegas") -> str:
    """Search for flight information to Las Vegas."""
    return search_tool.run(f"flights from {origin} to {destination} budget airlines cheap")