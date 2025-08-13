# Ledger Live Account Injector — console GUI cloned from your `epic.py`
# Exact style: same ANSI colors + block-art banner + prompt styling

import os
import json
import random
import string
import subprocess
import psutil

# =====================================
# Colors & block cells (copied style)
# =====================================
C0 = "\033[38;2;255;255;255m"  # white
C1 = "\033[38;2;214;90;66m"   # orange/red accent

BXX = "\033[48;2;12;12;12m  "
B00 = "\033[48;2;49;49;49m  "
B01 = "\033[48;2;189;189;189m  "
B02 = "\033[48;2;255;255;255m  "
B03 = "\033[48;2;82;82;82m  "
B04 = "\033[48;2;173;66;58m  "
B05 = "\033[48;2;115;115;99m  "
B06 = "\033[48;2;90;197;189m  "
B07 = "\033[48;2;214;90;66m  "
B08 = "\033[48;2;66;156;140m  "
B09 = "\033[48;2;255;132;99m  "

# =====================================
# Banner (style lifted from epic.py)
# =====================================
banner = f"""
   {BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{B00}{B00}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}
   {BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{B00}{B00}{BXX}{BXX}{BXX}{B00}{B00}{B01}{B00}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}
   {BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{B00}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{B00}{B02}{B02}{B00}{B00}{B00}{B01}{B01}{B00}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}
   {BXX}{BXX}{BXX}{BXX}{B00}{B00}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{B00}{B02}{B02}{B02}{B02}{B01}{B01}{B01}{B01}{B00}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}
   {BXX}{BXX}{BXX}{B00}{B03}{B00}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{B00}{B02}{B02}{B02}{B02}{B00}{B01}{B01}{B00}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}
   {BXX}{BXX}{B00}{B03}{B00}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{B00}{B02}{B02}{B02}{B02}{B00}{BXX}{B00}{B00}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{B00}{BXX}
   {BXX}{BXX}{B00}{B03}{B03}{B00}{BXX}{BXX}{BXX}{B00}{B00}{B02}{B02}{B02}{B02}{B02}{B00}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{B00}{BXX}{B00}{B00}{BXX}{C0}
   {BXX}{BXX}{BXX}{B00}{B03}{B03}{B00}{BXX}{B00}{B02}{B02}{B02}{B02}{B02}{B01}{B00}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{B00}{B03}{B00}{B00}{BXX}{BXX}    Ledger Live Injector {C1}v{C0}1.0{C1}
   {BXX}{BXX}{BXX}{BXX}{B00}{B03}{B03}{B00}{B02}{B02}{B02}{B02}{B02}{B01}{B00}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{B00}{B03}{B03}{B00}{BXX}{BXX}    ====================={C0}
   {BXX}{BXX}{BXX}{BXX}{B00}{B03}{B03}{B03}{B02}{B02}{B02}{B02}{B02}{B01}{B00}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{B00}{B03}{B03}{B03}{B00}{BXX}{BXX}    Select a chain and
   {BXX}{BXX}{BXX}{B00}{B03}{B03}{B03}{B02}{B02}{B02}{B02}{B02}{B01}{B01}{B03}{B00}{BXX}{BXX}{BXX}{BXX}{BXX}{B00}{B00}{B00}{BXX}{B00}{B03}{B00}{B00}{BXX}{BXX}{BXX}    enter an address; the
   {BXX}{BXX}{BXX}{B00}{B03}{B03}{B03}{B02}{B02}{B02}{B02}{B02}{B03}{B01}{B01}{B04}{B00}{BXX}{BXX}{BXX}{B00}{B03}{B05}{B05}{B00}{B03}{B00}{BXX}{BXX}{BXX}{BXX}{BXX}    account will be added
   {BXX}{BXX}{BXX}{B00}{B03}{B03}{B03}{B03}{B02}{B02}{B01}{B03}{B06}{B00}{B01}{B07}{B07}{B00}{B00}{BXX}{B00}{B05}{B05}{B05}{B05}{B03}{B00}{BXX}{BXX}{BXX}{BXX}{BXX}    to Ledger Live config.
   {BXX}{BXX}{BXX}{B00}{B03}{B03}{B04}{B03}{B01}{B01}{B03}{B02}{B08}{B00}{B04}{B07}{B03}{B05}{B05}{B00}{B03}{B03}{B00}{B05}{B03}{B03}{B00}{BXX}{BXX}{BXX}{BXX}{BXX}    
   {BXX}{BXX}{BXX}{BXX}{B00}{B03}{B07}{B07}{B03}{B01}{B03}{B00}{B00}{B09}{B09}{B03}{B05}{B05}{B05}{B05}{B05}{B00}{BXX}{B00}{B00}{B00}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}
   {BXX}{BXX}{BXX}{BXX}{BXX}{B00}{B04}{B04}{B00}{B00}{B03}{B03}{B03}{B09}{B07}{B03}{B05}{B05}{B05}{B05}{B03}{B00}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}
   {BXX}{BXX}{BXX}{BXX}{BXX}{B00}{B03}{B09}{B00}{B00}{B00}{B00}{B07}{B04}{B07}{B03}{B03}{B05}{B05}{B03}{B00}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}
   {BXX}{BXX}{BXX}{BXX}{B00}{B03}{B03}{B04}{B09}{B04}{B00}{B09}{B09}{B07}{B07}{B03}{B03}{B03}{B03}{B03}{B00}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}
   {BXX}{BXX}{B00}{B00}{B03}{B00}{B00}{B09}{B09}{B09}{B04}{B09}{B07}{B07}{B03}{B03}{B03}{B00}{B00}{B03}{B03}{B00}{B00}{BXX}{BXX}{B00}{B00}{B00}{BXX}{BXX}{BXX}{BXX}
   {BXX}{B00}{B03}{B03}{B00}{BXX}{BXX}{B00}{B09}{B07}{B07}{B07}{B07}{B03}{B03}{B03}{B00}{BXX}{BXX}{B00}{B03}{B05}{B05}{B00}{B00}{B00}{B00}{B00}{B00}{B00}{BXX}{BXX}
   {B00}{B03}{B03}{B03}{B00}{BXX}{BXX}{BXX}{B00}{B07}{B07}{B03}{B03}{B03}{B03}{B00}{BXX}{BXX}{B00}{B00}{B05}{B05}{B00}{B00}{B00}{B00}{B00}{B00}{BXX}{BXX}{BXX}{BXX}
   {B00}{B03}{B03}{B00}{BXX}{BXX}{BXX}{BXX}{BXX}{B00}{B00}{B00}{B03}{B03}{B00}{B00}{B00}{B00}{B00}{B00}{B05}{B05}{B05}{B00}{B00}{B00}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}
   {BXX}{B00}{B03}{B00}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{B00}{B03}{B03}{B03}{B00}{B00}{B00}{B00}{B05}{B05}{B00}{B00}{B00}{B00}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}
   {BXX}{BXX}{B00}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{B00}{B00}{B03}{B03}{B03}{B03}{B03}{B03}{B00}{B05}{B03}{B05}{B00}{B00}{B00}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}
   {BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{B00}{B03}{B03}{B03}{B03}{B03}{B03}{B03}{B03}{B00}{B05}{B00}{B05}{B00}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}
   {BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{B00}{B03}{B00}{B03}{B03}{B03}{B03}{B03}{B00}{B03}{B00}{BXX}{B00}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}
   {BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{B00}{BXX}{B00}{B03}{B00}{B03}{B00}{BXX}{B00}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}
   {BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{B00}{BXX}{B00}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}{BXX}

"""

# =====================================
# Paths & constants
# =====================================
APPDATA_PATH = os.getenv('APPDATA') or ''
LEDGER_PATH = os.path.join(APPDATA_PATH, 'Ledger Live')
APP_JSON = os.path.join(LEDGER_PATH, 'app.json')
BASE_SETTINGS = os.path.join(os.path.dirname(__file__), 'baseSettings.json')
SEED_IDENTIFIER = os.path.join(os.path.dirname(__file__), 'seedIdentifier.json')

CHAINS = {
    'ETH': {"name": 'ethereum', "derivation": "44'/60'/0'/0/0"},
    'SOL': {"name": 'solana', "derivation": "m/44'/501'/0'"}
}

clear = lambda: os.system("cls")

def title(t: str):
    try:
        os.system(f"title {t}")
    except Exception:
        pass

def kill_ledger_live():
    for proc in psutil.process_iter(['pid','name']):
        try:
            if (proc.info.get('name') or '').lower() == 'ledger live.exe':
                proc.terminate()
        except Exception:
            continue

def random_name(k=14):
    return ''.join(random.choice(string.ascii_letters) for _ in range(k))

def do_add_account(chain_key: str):
    chain = CHAINS[chain_key]

    address = input(f"  {C1}>{C0} Address to add{C1}:{C0} ").strip()
    acc_name = input(f"  {C1}>{C0} Wallet name (blank=random){C1}:{C0} ").strip() or random_name()

    seed_identifier = json.load(open(SEED_IDENTIFIER, 'r', encoding='utf-8'))["identifier"]
    currency = chain["name"]

    acc_data = {
        "data": {
            "id": f"js:2:{currency}:{address}:",
            "name": acc_name,
            "seedIdentifier": seed_identifier,
            "starred": False,
            "used": True,
            "derivationMode": "",
            "index": 1,
            "freshAddress": address,
            "freshAddressPath": chain["derivation"],
            "freshAddresses": [{"address": address, "derivationPath": chain["derivation"]}],
            "blockHeight": 0,
            "syncHash": "0x0000",
            "creationDate": "2024-01-01T00:00:00.000Z",
            "operationsCount": 0,
            "operations": [],
            "pendingOperations": [],
            "currencyId": currency,
            "unitMagnitude": 18,
            "lastSyncDate": "2024-01-16T14:16:40.422Z",
            "balance": "0",
            "spendableBalance": "0",
            "nfts": [],
            "balanceHistoryCache": {},
            "subAccounts": [],
            "swapHistory": []
        },
        "version": 1
    }

    with open(APP_JSON, 'r+', encoding='utf-8') as f:
        app_json = json.load(f)

        if not app_json["data"]["settings"].get("lastSeenDevice"):
            app_json["data"]["settings"] = json.load(open(BASE_SETTINGS, 'r', encoding='utf-8'))

        if "accounts" not in app_json["data"]:
            app_json["data"]["accounts"] = []

        app_json["data"]["accounts"].append(acc_data)

        f.seek(0)
        f.truncate(0)
        json.dump(app_json, f, indent=2)

    print(f"\n  Added account {C1}{acc_name}{C0} on {C1}{currency}{C0}.")
    print(f"  Seed ID: {seed_identifier}")
    print(f"  Address: {address}")

    input(f"\n  Press {C1}'{C0}ENTER{C1}'{C0} to kill Ledger Live and return to menu")
    kill_ledger_live()

def menu():
    clear()
    print(banner)
    print(f"  {C1}>{C0} Select blockchain{C1}:{C0}")
    print(f"    {C1}[1]{C0} Ethereum (ETH)")
    print(f"    {C1}[2]{C0} Solana (SOL)")
    print(f"    {C1}[Q]{C0} Quit")

    choice = input(f"\n  {C1}>{C0} Enter choice{C1}:{C0} ").strip().lower()
    if choice == '1':
        do_add_account('ETH')
        menu()
    elif choice == '2':
        do_add_account('SOL')
        menu()
    elif choice == 'q':
        return
    else:
        print(f"  {C1}!{C0} Invalid choice")
        input(f"  Press {C1}'{C0}ENTER{C1}'{C0} to try again")
        menu()

def main():
    title('Ledger Live Injector')
    clear()
    print(banner)
    input(f"  Press {C1}'{C0}ENTER{C1}'{C0} to continue")
    menu()
    print(f"\n  Launching Ledger Live...")
    try:
        exe_path = os.path.join('C:\\Program Files\\Ledger Live', 'Ledger Live.exe')
        if os.path.isfile(exe_path):
            subprocess.Popen([exe_path])
        else:
            subprocess.Popen(['Ledger Live.exe'])
        print(f"  {C1}>{C0} Launched.")
    except Exception as e:
        print(f"  {C1}!{C0} Could not start Ledger Live: {e}")

if __name__ == '__main__':
    main()
