from core.engine import HackingAssistantEngine
from rich.console import Console

def main():
    console = Console()
    hacking_assistant = HackingAssistantEngine(console)
    hacking_assistant.run()

if __name__ == "__main__":
    main()
