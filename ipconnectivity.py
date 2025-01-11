import tkinter as tk
from tkinter import ttk
import paramiko
from cryptography.fernet import Fernet
from typing import Dict, List

class VPNClient:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("VPN Client")

        self.country_var = tk.StringVar()
        self.country_options = ["USA", "UK", "Canada", "Australia", "Japan"]
        self.country_menu = ttk.OptionMenu(self.window, self.country_var, self.country_options[0])
        self.country_menu.pack()

        self.server_var = tk.StringVar()
        self.server_options: Dict[str, List[str]] = {
            "USA": ["New York", "Los Angeles", "Chicago"],
            "UK": ["London", "Manchester", "Birmingham"],
            "Canada": ["Toronto", "Vancouver", "Montreal"],
            "Australia": ["Sydney", "Melbourne", "Brisbane"],
            "Japan": ["Tokyo", "Osaka", "Nagoya"]
        }
        self.server_menu = ttk.OptionMenu(self.window, self.server_var, self.server_options["USA"][0])
        self.server_menu.pack()

        self.username_label = tk.Label(self.window, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.window)
        self.username_entry.pack()
        self.password_label = tk.Label(self.window, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.window, show="*")
        self.password_entry.pack()

        self.connect_button = tk.Button(self.window, text="Connect", command=self.connect)
        self.connect_button.pack()

    def connect(self):
        try:
            country = self.country_var.get()
            server = self.server_var.get()
            username = self.username_entry.get()
            password = self.password_entry.get()

            vpn_servers: Dict[str, str] = {
                "USA": "198.7.59.119",
                "UK": "178.238.11.6",
                "Canada": "192.206.151.131",
                "Australia": "110.33.122.75",
                "Japan": "133.11.93.0"
            }
            vpn_server_ip = vpn_servers[country]

            key = Fernet.generate_key()
            cipher_suite = Fernet(key)

            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            ssh_client.connect(hostname=vpn_server_ip, port=22, username=username, password=password)

            tunnel = ssh_client.get_transport().open_channel(
                kind="session",
                dest_addr=(vpn_server_ip, 8080),
                src_addr=("localhost", 22)
            )

            encrypted_tunnel = cipher_suite.encrypt(tunnel)

            print("Connected to VPN server in", country)
        except paramiko.AuthenticationException as e:
            print("Authentication failed:", e)
        except Exception as e:
            print("Error:", e)

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    vpn_client = VPNClient()
    vpn_client.run()
