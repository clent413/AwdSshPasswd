import tkinter as tk
from tkinter import scrolledtext, messagebox
import paramiko
import threading

class SSHConnector:
    def __init__(self, ip, username, password, port, command, output_label):
        self.ip = ip
        self.username = username
        self.password = password
        self.port = port
        self.command = command
        self.output_label = output_label

    def connect(self):
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(self.ip, username=self.username, password=self.password, port=self.port)
            stdin, stdout, stderr = client.exec_command(self.command)
            output = stdout.read().decode('utf-8')
            error = stderr.read().decode('utf-8')
            client.close()
            if error:
                self.output_label.config(state=tk.NORMAL)
                self.output_label.insert(tk.END, f"Error on {self.ip}: {error}\n")
                self.output_label.config(state=tk.DISABLED)
            else:
                self.output_label.config(state=tk.NORMAL)
                self.output_label.insert(tk.END, f"Output from {self.ip}: {output}\n")
                self.output_label.config(state=tk.DISABLED)
        except Exception as e:
            self.output_label.config(state=tk.NORMAL)
            self.output_label.insert(tk.END, f"Failed to connect to {self.ip}: {str(e)}\n")
            self.output_label.config(state=tk.DISABLED)

def load_ips_and_connect(ip_list, username, password, port, command, output_label):
    for ip in ip_list:
        connector = SSHConnector(ip, username, password, port, command, output_label)
        connector.connect()

def start_connections(output_label):
    try:
        with open('ip.txt', 'r') as file:
            ips = [line.strip() for line in file.readlines()]
            username = username_entry.get()
            password = password_entry.get()
            port = int(port_entry.get()) if port_entry.get() else 22
            command = command_entry.get()
            threading.Thread(target=load_ips_and_connect, args=(ips, username, password, port, command, output_label), daemon=True).start()
            output_label.config(state=tk.NORMAL)
            output_label.insert(tk.END, f"Loaded {len(ips)} IPs from ip.txt and started connections\n")
            output_label.config(state=tk.DISABLED)
    except FileNotFoundError:
        messagebox.showerror("Error", "ip.txt file not found.")

# GUI setup
root = tk.Tk()
root.title("AwdSshExecGUI    V0.1")

# Input fields
tk.Label(root, text="用户名").grid(row=0, column=0)
username_entry = tk.Entry(root)
username_entry.grid(row=0, column=1)
username_entry.insert(0, "")

tk.Label(root, text="密码").grid(row=1, column=0)
password_entry = tk.Entry(root, show="*")
password_entry.grid(row=1, column=1)
password_entry.insert(0, "")

tk.Label(root, text="端口").grid(row=2, column=0)
port_entry = tk.Entry(root)
port_entry.grid(row=2, column=1)
port_entry.insert(0, "")

tk.Label(root, text="IP").grid(row=3, column=0)
ip_entry = tk.Entry(root)
ip_entry.grid(row=3, column=1)
ip_entry.insert(0, "")

tk.Label(root, text="命令").grid(row=4, column=0)
command_entry = tk.Entry(root)
command_entry.grid(row=4, column=1)
command_entry.insert(0, "")

# Execute button
execute_button = tk.Button(root, text="start", command=lambda: start_connections(output_label))
execute_button.grid(row=5, column=0, columnspan=2)

# Output label
output_label = scrolledtext.ScrolledText(root, state=tk.DISABLED)
output_label.grid(row=6, column=0, columnspan=2, sticky='nsew')

root.mainloop()