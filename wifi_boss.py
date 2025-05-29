import subprocess
import re
from colorama import Fore, Style, init

# Initialize colorama for Windows support
init(autoreset=True)

def get_manufacturer(bssid):
    """Map BSSID's OUI to manufacturer using a local lookup table."""
    oui_to_vendor = {
        "00:14:22": "Microsoft",
        "00:19:5B": "Apple",
        "00:0D:B9": "Intel",
        "00:1B:44": "Cisco",
        "00:0F:44": "Dell",
        "00:14:6F": "HP",
        "00:24:1D": "Lenovo",
        "00:17:31": "Netgear",
        "00:01:6C": "Linksys",
        "00:0E:84": "Samsung",
    }
    if bssid == "N/A":
        return "N/A"
    oui = bssid.split(":")[:3]
    oui_key = ":".join(oui)
    return oui_to_vendor.get(oui_key, "Unknown")

def scan_wifi():
    """Scan for available WiFi networks with detailed information on Windows"""
    try:
        result = subprocess.run(
            ['netsh', 'wlan', 'show', 'networks', 'mode=BSSID'],
            capture_output=True, text=True, check=True
        )
        networks = []
        current_network = None
        for line in result.stdout.splitlines():
            line = line.strip()
            if line.startswith('SSID '):
                if current_network:
                    networks.append(current_network)
                ssid_part = line.split(':', 1)
                ssid = ssid_part[1].strip() if len(ssid_part) > 1 else 'N/A'
                current_network = {
                    'ssid': ssid,
                    'signal': 'N/A',
                    'security': 'N/A',
                    'bssid': 'N/A',
                    'manufacturer': 'N/A',
                }
            elif line.startswith('    BSSID '):
                bssid_part = line.split(':', 1)
                bssid = bssid_part[1].strip() if len(bssid_part) > 1 else 'N/A'
                current_network['bssid'] = bssid
                current_network['manufacturer'] = get_manufacturer(bssid)
            elif line.startswith('    Signal : '):
                signal_part = line.split(':', 2)
                current_network['signal'] = signal_part[2].strip() if len(signal_part) > 2 else 'N/A'
            elif line.startswith('    Authentication : '):
                auth_part = line.split(':', 1)
                current_network['security'] = auth_part[1].strip() if len(auth_part) > 1 else 'N/A'
        if current_network:
            networks.append(current_network)
        return networks
    except subprocess.CalledProcessError as e:
        print(f"Error scanning WiFi: {e}")
        return []

def get_wifi_password(ssid):
    """Retrieve the password for a saved WiFi profile."""
    try:
        result = subprocess.run(
            ['netsh', 'wlan', 'show', 'profile', f'name="{ssid}"', 'key=clear'],
            capture_output=True, text=True, check=True
        )
        match = re.search(r'Key Content\s+:\s+(.+)', result.stdout)
        return match.group(1) if match else "N/A"
    except subprocess.CalledProcessError:
        return "Profile not found"

def get_ip_address():
    """Get current device IP address on Windows"""
    try:
        result = subprocess.run(['ipconfig'], capture_output=True, text=True, check=True)
        match = re.search(r'IPv4 Address[\. ]+: (\d+\.\d+\.\d+\.\d+)', result.stdout)
        return match.group(1) if match else "N/A"
    except (subprocess.CalledProcessError, AttributeError):
        return "N/A"

def main():
    # Custom logo with dark blue color and creator name
    logo = f"""{Fore.BLUE}
██╗    ██╗██╗███████╗██╗    ███████╗ ██████╗ █████╗ ███╗   ██╗
██║    ██║██║██╔════╝██║    ██╔════╝██╔════╝██╔══██╗████╗  ██║
██║ █╗ ██║██║█████╗  ██║    ███████╗██║     ███████║██╔██╗ ██║
██║███╗██║██║██╔══╝  ██║    ╚════██║██║     ██╔══██║██║╚██╗██║
╚███╔███╔╝██║██║     ██║    ███████║╚██████╗██║  ██║██║ ╚████║
 ╚══╝╚══╝ ╚═╝╚═╝     ╚═╝    ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝
                                                              
{Fore.BLUE}Created by DR4C0{Style.RESET_ALL}
{Style.RESET_ALL}"""

    print(logo)

    while True:
        user_input = input(f"{Fore.BLUE}Enter command (scan/password/exit): {Style.RESET_ALL}").strip().lower()
        if user_input == "scan":
            print(f"\n{Fore.BLUE}WiFi Scanner Results:{Style.RESET_ALL}")
            print(f"{Fore.BLUE}{'SSID':<20} {'Signal':<6} {'Security':<8} {'BSSID':<17} {'Manufacturer':<12}{Style.RESET_ALL}")
            print(f"{Fore.BLUE}{'-'*80}{Style.RESET_ALL}")
            for network in scan_wifi():
                print(f"{Fore.BLUE}{network['ssid']:<20} {network['signal']:<6} {network['security']:<8} "
                      f"{network['bssid']:<17} {network['manufacturer']:<12}{Style.RESET_ALL}")
            print(f"\n{Fore.BLUE}Current Device IP Address: {get_ip_address()}{Style.RESET_ALL}")
        elif user_input.startswith("password"):
            parts = user_input.split()
            if len(parts) < 2:
                print(f"{Fore.BLUE}Please provide an SSID after 'password'.{Style.RESET_ALL}")
                continue
            ssid = ' '.join(parts[1:])
            password = get_wifi_password(ssid)
            print(f"\n{Fore.BLUE}Password for '{ssid}': {password}{Style.RESET_ALL}")
        elif user_input == "exit":
            print(f"{Fore.BLUE}Exiting...{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.BLUE}Invalid command. Use 'scan', 'password', or 'exit'.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()




    