import os
import sys
import asyncio
from colorama import init, Fore, Style
import inquirer

# Initialize colorama
init(autoreset=True)

# Fixed border width
BORDER_WIDTH = 80

# Function to display a styled border
def print_border(text: str, color=Fore.CYAN, width=BORDER_WIDTH):
    text = text.strip()
    if len(text) > width - 4:
        text = text[:width - 7] + "..."
    padded_text = f" {text} ".center(width - 2)
    print(f"{color}┌{'─' * (width - 2)}┐{Style.RESET_ALL}")
    print(f"{color}│{padded_text}│{Style.RESET_ALL}")
    print(f"{color}└{'─' * (width - 2)}┘{Style.RESET_ALL}")

# Display banner
def _banner():
    banner = r"""


██╗░░██╗░█████╗░████████╗░██████╗████████╗██╗░░░██╗███████╗███████╗
██║░░██║██╔══██╗╚══██╔══╝██╔════╝╚══██╔══╝██║░░░██║██╔════╝██╔════╝
███████║██║░░██║░░░██║░░░╚█████╗░░░░██║░░░██║░░░██║█████╗░░█████╗░░
██╔══██║██║░░██║░░░██║░░░░╚═══██╗░░░██║░░░██║░░░██║██╔══╝░░██╔══╝░░
██║░░██║╚█████╔╝░░░██║░░░██████╔╝░░░██║░░░╚██████╔╝██║░░░░░██║░░░░░
╚═╝░░╚═╝░╚════╝░░░░╚═╝░░░╚═════╝░░░░╚═╝░░░░╚═════╝░╚═╝░░░░░╚═╝░░░░░


    """
    print(f"{Fore.GREEN}{banner:^80}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")
    print_border("HOTSTUFF TESTNET", Fore.GREEN)
    print(f"{Fore.YELLOW}│ {'Website'}: {Fore.CYAN}https://thogtoolhub.com/{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}│ {'Discord'}: {Fore.CYAN}https://discord.gg/MnmYBKfHQf{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}│ {'Telegram Channel'}: {Fore.CYAN}https://t.me/thogairdrops{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")

# Clear screen
def _clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# Script handlers
async def run_faucet(language: str):
    from scripts.faucet import run_faucet as faucet_run
    await faucet_run(language)

async def run_gm(language: str):
    from scripts.gm import run_gm as gm_run
    await gm_run(language)

async def cmd_exit(language: str):
    messages = {"vi": "Exiting...", "en": "Exiting..."}
    print_border(messages[language], Fore.GREEN)
    sys.exit(0)

# Menu command map
SCRIPT_MAP = {
    "faucet": run_faucet,
    "gm": run_gm,
    "exit": cmd_exit
}

# Available scripts per language
def get_available_scripts(language):
    scripts = {
        'vi': [
            {"name": "1. Faucet USDC | USDT", "value": "faucet"},
            {"name": "2. Auto GM Check-in", "value": "gm"},
            {"name": "X. Exit", "value": "exit"},
        ],
        'en': [
            {"name": "1. Faucet USDC | USDT", "value": "faucet"},
            {"name": "2. GM Check-in", "value": "gm"},
            {"name": "X. Exit", "value": "exit"},
        ]
    }
    return scripts[language]

def run_script(script_func, language):
    """Run script whether it is async or not."""
    if asyncio.iscoroutinefunction(script_func):
        asyncio.run(script_func(language))
    else:
        script_func(language)

def select_language():
    while True:
        _clear()
        _banner()
        print(f"{Fore.GREEN}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")
        print_border("SELECT LANGUAGE", Fore.YELLOW)
        questions = [
            inquirer.List(
                'language',
                message=f"{Fore.CYAN}Please select:{Style.RESET_ALL}",
                choices=[("1. Vietnamese", 'vi'), ("2. English", 'en')],
                carousel=True
            )
        ]
        answer = inquirer.prompt(questions)
        if answer and answer['language'] in ['vi', 'en']:
            return answer['language']
        print(f"{Fore.RED}{'❌ Invalid choice':^76}{Style.RESET_ALL}")

def main():
    _clear()
    _banner()
    language = select_language()

    messages = {
        "vi": {
            "running": "Running: {}",
            "completed": "Completed: {}",
            "error": "Error: {}",
            "press_enter": "Press Enter to continue...",
            "menu_title": "MAIN MENU",
            "select_script": "Select a script to run",
            "locked": "🔒 This script is locked! Please join our group for more info or purchase to unlock."
        },
        "en": {
            "running": "Running: {}",
            "completed": "Completed: {}",
            "error": "Error: {}",
            "press_enter": "Press Enter to continue...",
            "menu_title": "MAIN MENU",
            "select_script": "Select a script to run",
            "locked": "🔒 This script is locked! Please join our group for more info or purchase to unlock."
        }
    }

    while True:
        _clear()
        _banner()
        print(f"{Fore.YELLOW}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")
        print_border(messages[language]["menu_title"], Fore.YELLOW)
        print(f"{Fore.CYAN}│ {messages[language]['select_script'].center(BORDER_WIDTH - 4)} │{Style.RESET_ALL}")

        available_scripts = get_available_scripts(language)
        questions = [
            inquirer.List(
                'script',
                message=f"{Fore.CYAN}{messages[language]['select_script']}{Style.RESET_ALL}",
                choices=[script["name"] for script in available_scripts],
                carousel=True
            )
        ]
        answers = inquirer.prompt(questions)
        if not answers:
            continue

        selected_script_name = answers['script']
        selected_script = next(script for script in available_scripts if script["name"] == selected_script_name)
        selected_script_value = selected_script["value"]

        script_func = SCRIPT_MAP.get(selected_script_value)
        if script_func is None:
            print_border("Not implemented", Fore.RED)
            input(f"{Fore.YELLOW}⏎ {messages[language]['press_enter']}{Style.RESET_ALL:^76}")
            continue

        try:
            print_border(messages[language]["running"].format(selected_script_name), Fore.CYAN)
            run_script(script_func, language)
            print_border(messages[language]["completed"].format(selected_script_name), Fore.GREEN)
            input(f"{Fore.YELLOW}⏎ {messages[language]['press_enter']}{Style.RESET_ALL:^76}")
        except Exception as e:
            print_border(messages[language]["error"].format(str(e)), Fore.RED)
            input(f"{Fore.YELLOW}⏎ {messages[language]['press_enter']}{Style.RESET_ALL:^76}")

if __name__ == "__main__":
    main()
