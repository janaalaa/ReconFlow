import subprocess
import sqlite3

TARGET = "yahoo.com"

def run_subfinder():
    print("[*] Running Subfinder...")

    result = subprocess.run(
        ["subfinder", "-d", TARGET],
        capture_output=True,
        text=True
    )

    return result.stdout.splitlines()


def save_assets(assets):

    conn = sqlite3.connect("reconflow.db")
    c = conn.cursor()

    for asset in assets:
        c.execute(
            "INSERT OR IGNORE INTO assets (target_domain, asset_value, status) VALUES (?, ?, 'Free')",
            (TARGET, asset)
        )

    conn.commit()
    conn.close()


def main():

    assets = run_subfinder()

    print(f"[+] Found {len(assets)} assets")

    save_assets(assets)

    print("[+] Assets added to database")


if __name__ == "__main__":
    main()
