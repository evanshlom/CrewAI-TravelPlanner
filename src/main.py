from .crew import AllegiantTravelCrew
import os
from dotenv import load_dotenv

def run(query: str):
    """Run the crew with a query."""
    load_dotenv()
    
    inputs = {
        'query': query
    }
    
    crew_instance = AllegiantTravelCrew().crew()
    result = crew_instance.kickoff(inputs=inputs)
    return result

if __name__ == "__main__":
    # Example usage
    result = run("I want to plan a budget trip to Vegas for a Raiders game")
    print(result)