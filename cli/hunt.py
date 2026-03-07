import sys
import requests
import getpass

API_URL = "http://127.0.0.1:5000"
USER = getpass.getuser()

def send_request(endpoint, asset):
    print(f"[*] {USER} is sending {endpoint} request for {asset}...")
    try:
        response = requests.post(f"{API_URL}/{endpoint}", json={"asset": asset, "user": USER})
        data = response.json()
        if response.status_code == 200:
            print(f"[+] SUCCESS: {data['message']}")
        else:
            print(f"[-] FAILED: {data['message']}")
    except Exception:
        print("[-] ERROR: Could not connect to the server. Is it running?")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 cli/hunt.py [claim/release] [asset]")
        sys.exit(1)

    action = sys.argv[1]
    asset = sys.argv[2]

    if action in ["claim", "release"]:
        send_request(action, asset)
    else:
        print("[-] Unknown action. Use 'claim' or 'release'.")
