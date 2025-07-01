#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.markdown import Markdown
from src.main import run

console = Console()

def main():
    load_dotenv()
    
    if not os.getenv("ANTHROPIC_API_KEY"):
        console.print("[red]Error: ANTHROPIC_API_KEY not found in .env file[/red]")
        return
    
    # Welcome message
    console.print(Panel(Markdown("""
# Allegiant Travel Planning Assistant

I'll help you plan affordable trips to Las Vegas, including:
- Budget flights and hotels
- Allegiant Stadium events
- Money-saving tips

Type 'quit' to exit.
"""), style="bold blue"))
    
    # Chat loop
    while True:
        user_input = Prompt.ask("\n[bold green]You[/bold green]")
        
        if user_input.lower() in ['quit', 'exit']:
            console.print("[blue]Thanks for using Allegiant Travel Planning![/blue]")
            break
        
        console.print("\n[yellow]Researching your travel options...[/yellow]\n")
        
        try:
            result = run(user_input)
            console.print(Panel(
                Markdown(str(result)),
                title="[bold blue]Travel Assistant[/bold blue]",
                style="blue"
            ))
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")

if __name__ == "__main__":
    main()