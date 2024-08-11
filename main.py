from core.engine import HackingAssistantEngine
from rich.console import Console

def main():
    console = Console()
    hacking_assistant = HackingAssistantEngine(console)
    try:
        hacking_assistant.run()
    except Exception as e:
        console.print(f"[bold red]Critical error: {e}[/bold red]")

if __name__ == "__main__":
    main()
