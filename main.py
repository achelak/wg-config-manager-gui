import os
import subprocess
import netifaces
import pystray
from PIL import Image
from typing import Tuple

def is_vpn_disconnected() -> Tuple[bool, str]:
    """
    Check if a VPN tunnel is disconnected.

    Returns:
        A tuple with a boolean indicating if the VPN tunnel is disconnected
        and the name of the tunnel interface if it is connected.
    """
    interfaces = netifaces.interfaces()
    for interface in interfaces:
        if interface.startswith("tun"):
            return False, interface
    return True, ""


def switch_vpn(icon: pystray.Icon, item: pystray.MenuItem) -> None:
    """
    Switch VPN connection to selected configuration file.

    Args:
        icon: The pystray.Icon instance.
        item: The pystray.MenuItem instance representing the selected VPN configuration file.
    """
    if str(item) == "Exit":
        icon.stop()
    elif str(item) == "Disconnect":
        disconnected, interface = is_vpn_disconnected()
        if not disconnected:
            subprocess.run(["sudo", "tunsafe", "stop", interface])
            message = "VPN connection has been disconnected."
        else:
            message = "VPN connection is already disconnected."
        os.system(f'notify-send "VPN Manager" "{message}"')
    else:
        vpn_dir = "/home/artem/vpn"
        vpn_path = os.path.join(vpn_dir, str(item))
        disconnected, interface = is_vpn_disconnected()
        if not disconnected:
            subprocess.run(["sudo", "tunsafe", "stop", interface])
        subprocess.run(["sudo", "tunsafe", "start", "-d", vpn_path])
        message = f"VPN connection switched to {item}"
        os.system(f'notify-send "VPN Manager" "{message}"')


vpn_dir = "/home/artem/vpn"
menu_items = []
for filename in os.listdir(vpn_dir):
    if filename.endswith(".conf"):
        menu_items.append(pystray.MenuItem(filename, switch_vpn))
menu_items.append(pystray.MenuItem("Disconnect", switch_vpn))
menu_items.append(pystray.MenuItem("Exit", switch_vpn))

menu = pystray.Menu(*menu_items)
icon = Image.open("icon.png")
systray = pystray.Icon("VPN Manager", icon, menu=menu)

systray.run()

