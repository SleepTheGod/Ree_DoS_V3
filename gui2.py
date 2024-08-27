import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import subprocess
import threading

class StressTestGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Stress Test GUI")

        # Create and place widgets
        self.create_widgets()

    def create_widgets(self):
        # Layer 4 Stress Testing
        tk.Label(self.root, text="Layer 4 Stress Testing", font=("Arial", 14)).grid(row=0, column=0, columnspan=2, pady=10)
        
        tk.Label(self.root, text="Protocol:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.protocol_var = tk.StringVar()
        ttk.Combobox(self.root, textvariable=self.protocol_var, values=["TCP", "UDP"]).grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Target IP:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.ip_entry = tk.Entry(self.root)
        self.ip_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Target Port:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.port_entry = tk.Entry(self.root)
        self.port_entry.grid(row=3, column=1, padx=10, pady=5)

        self.start_button = tk.Button(self.root, text="Start Layer 4 Stress Test", command=self.start_layer4_stress_test)
        self.start_button.grid(row=4, column=0, columnspan=2, pady=10)

        # XML-RPC Stress Testing
        tk.Label(self.root, text="XML-RPC Stress Testing", font=("Arial", 14)).grid(row=5, column=0, columnspan=2, pady=10)

        tk.Label(self.root, text="Site URL:").grid(row=6, column=0, padx=10, pady=5, sticky="e")
        self.site_entry = tk.Entry(self.root)
        self.site_entry.grid(row=6, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Method Name:").grid(row=7, column=0, padx=10, pady=5, sticky="e")
        self.method_entry = tk.Entry(self.root)
        self.method_entry.grid(row=7, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Parameters (comma-separated):").grid(row=8, column=0, padx=10, pady=5, sticky="e")
        self.params_entry = tk.Entry(self.root)
        self.params_entry.grid(row=8, column=1, padx=10, pady=5)

        self.start_xmlrpc_button = tk.Button(self.root, text="Start XML-RPC Stress Test", command=self.start_xmlrpc_stress_test)
        self.start_xmlrpc_button.grid(row=9, column=0, columnspan=2, pady=10)

    def run_command(self, command):
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            messagebox.showinfo("Result", result.stdout)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", e.stderr)

    def start_layer4_stress_test(self):
        protocol = self.protocol_var.get()
        ip = self.ip_entry.get()
        port = self.port_entry.get()

        if not protocol or not ip or not port:
            messagebox.showwarning("Input Error", "Please fill all fields.")
            return

        command = f"python main.py -l4 {protocol.lower()} {ip} {port}"
        threading.Thread(target=self.run_command, args=(command,)).start()

    def start_xmlrpc_stress_test(self):
        site = self.site_entry.get()
        method = self.method_entry.get()
        params = self.params_entry.get()

        if not site or not method:
            messagebox.showwarning("Input Error", "Please fill all required fields.")
            return

        param_list = params.split(",") if params else []
        param_str = " ".join(param_list)
        command = f"python main.py -x {site} {method} {param_str}"
        threading.Thread(target=self.run_command, args=(command,)).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = StressTestGUI(root)
    root.mainloop()
