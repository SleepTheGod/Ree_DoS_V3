import tkinter as tk
from tkinter import messagebox
import threading
import subprocess
import sys

class StressTestGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Advanced Stress Test GUI")
        self.geometry("600x400")
        
        self.create_widgets()
        
    def create_widgets(self):
        # Input fields
        tk.Label(self, text="Target IP:").grid(row=0, column=0, padx=10, pady=10)
        self.target_ip_entry = tk.Entry(self)
        self.target_ip_entry.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(self, text="Target Port:").grid(row=1, column=0, padx=10, pady=10)
        self.target_port_entry = tk.Entry(self)
        self.target_port_entry.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(self, text="Protocol (TCP/UDP):").grid(row=2, column=0, padx=10, pady=10)
        self.protocol_entry = tk.Entry(self)
        self.protocol_entry.grid(row=2, column=1, padx=10, pady=10)
        
        tk.Label(self, text="Request Data:").grid(row=3, column=0, padx=10, pady=10)
        self.request_data_entry = tk.Entry(self)
        self.request_data_entry.grid(row=3, column=1, padx=10, pady=10)
        
        tk.Label(self, text="Site URL:").grid(row=4, column=0, padx=10, pady=10)
        self.site_url_entry = tk.Entry(self)
        self.site_url_entry.grid(row=4, column=1, padx=10, pady=10)
        
        tk.Label(self, text="Method Name:").grid(row=5, column=0, padx=10, pady=10)
        self.method_name_entry = tk.Entry(self)
        self.method_name_entry.grid(row=5, column=1, padx=10, pady=10)
        
        tk.Label(self, text="Parameters (comma-separated):").grid(row=6, column=0, padx=10, pady=10)
        self.params_entry = tk.Entry(self)
        self.params_entry.grid(row=6, column=1, padx=10, pady=10)
        
        # Start button
        self.start_button = tk.Button(self, text="Start Stress Test", command=self.start_stress_test)
        self.start_button.grid(row=7, column=0, columnspan=2, pady=20)
        
        # Log display
        self.log_text = tk.Text(self, height=10, width=70)
        self.log_text.grid(row=8, column=0, columnspan=2, padx=10, pady=10)
        
    def start_stress_test(self):
        # Gather input data
        target_ip = self.target_ip_entry.get()
        target_port = self.target_port_entry.get()
        protocol = self.protocol_entry.get()
        request_data = self.request_data_entry.get()
        site = self.site_url_entry.get()
        method_name = self.method_name_entry.get()
        params = self.params_entry.get().split(',')
        
        if target_ip and target_port and protocol:
            self.run_script(target_ip, target_port, protocol, request_data)
        elif site and method_name:
            self.run_script(site=site, method_name=method_name, params=params)
        else:
            messagebox.showerror("Error", "Please provide the necessary input data.")

    def run_script(self, target_ip=None, target_port=None, protocol=None, site=None, method_name=None, params=None, request_data=None):
        cmd = [sys.executable, "main.py"]
        if target_ip and target_port and protocol:
            cmd += ["-l4", protocol, target_ip, str(target_port)]
        elif site and method_name:
            cmd += ["-x", site, method_name] + params
        
        # Run the script and capture output
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.log_text.delete(1.0, tk.END)
        for line in process.stdout:
            self.log_text.insert(tk.END, line.decode())
        process.wait()

if __name__ == "__main__":
    app = StressTestGUI()
    app.mainloop()
