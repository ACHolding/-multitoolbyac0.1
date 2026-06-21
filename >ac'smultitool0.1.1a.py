import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import socket
import subprocess
import threading
import platform
import pyperclip
import urllib.request

class CatsMultitool:
    def __init__(self, root):
        self.root = root
        self.root.title("ac holding multitool 0.1.13")
        self.root.geometry("1000x680")
        self.root.configure(bg="#0A0A0A")

        # LOIC Style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TNotebook", background="#0A0A0A")
        self.style.configure("TNotebook.Tab", background="#1A1A1A", foreground="#00FF00", padding=[12, 6], font=("Courier", 10, "bold"))
        self.style.map("TNotebook.Tab", background=[("selected", "#003300")])
        self.style.configure("TButton", background="#003300", foreground="#00FF00", borderwidth=3, font=("Courier", 11, "bold"))

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=8, pady=8)

        tabs = [
            ("WiFi Scanner", self.build_wifi_tab),
            ("Port Scanner", self.build_port_tab),
            ("HTTP Repeater", self.build_burp_tab),
        ]
        
        for tab_name, build_func in tabs:
            frame = tk.Frame(self.notebook, bg="#0A0A0A")
            self.notebook.add(frame, text=tab_name)
            build_func(frame)

        # Status bar
        self.status = tk.Label(root, text="AC HOLDINGS MULTITOOL v0.1.13 | LOIC MODE | NYAH~", 
                             bg="#000000", fg="#00FF00", font=("Courier", 9), anchor="w")
        self.status.pack(side="bottom", fill="x", padx=5, pady=3)

    def _safe_insert(self, widget, text):
        def insert():
            widget.insert(tk.END, text)
            widget.see(tk.END)
        self.root.after(0, insert)

    # ====================== WIFI ======================
    def build_wifi_tab(self, frame):
        tk.Label(frame, text="=== WIFI SCANNER ===", bg="#0A0A0A", fg="#00FF00", font=("Courier", 14, "bold")).pack(pady=10)
        tk.Button(frame, text="LAUNCH WIFI SCAN", bg="#003300", fg="#00FF00", font=("Courier", 12, "bold"),
                  command=self.scan_wifi, height=2, width=30).pack(pady=10)
        self.wifi_output = scrolledtext.ScrolledText(frame, height=20, bg="#000000", fg="#00FF00", font=("Courier", 10))
        self.wifi_output.pack(padx=10, pady=10, fill="both", expand=True)

    def scan_wifi(self):
        self._safe_insert(self.wifi_output, "SCANNING NETWORKS...\n")
        def run():
            try:
                if platform.system() == "Darwin":  # macOS
                    result = subprocess.check_output(["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-s"], timeout=10).decode()
                elif platform.system() == "Windows":
                    result = subprocess.check_output("netsh wlan show networks", shell=True, timeout=10).decode()
                else:
                    result = subprocess.check_output("nmcli dev wifi list || iwlist scan 2>/dev/null", shell=True, timeout=10).decode()
                self._safe_insert(self.wifi_output, result + "\nSCAN COMPLETE ~ NYAH!\n")
            except Exception as e:
                self._safe_insert(self.wifi_output, f"ERROR: {e}\nTry running with sudo on macOS if needed.\n")
        threading.Thread(target=run, daemon=True).start()

    # ====================== PORT SCANNER ======================
    def build_port_tab(self, frame):
        tk.Label(frame, text="=== PORT SCANNER ===", bg="#0A0A0A", fg="#00FF00", font=("Courier", 14, "bold")).pack(pady=10)
        
        tk.Label(frame, text="Target:", bg="#0A0A0A", fg="#00FF00").pack(anchor="w", padx=10)
        self.port_target = tk.Entry(frame, width=40, bg="#1A1A1A", fg="#00FF00", insertbackground="#00FF00")
        self.port_target.pack(padx=10, fill="x")
        self.port_target.insert(0, "127.0.0.1")
        
        tk.Button(frame, text="LAUNCH PORT SCAN", bg="#003300", fg="#00FF00", font=("Courier", 12, "bold"),
                  command=self.scan_ports, height=2, width=30).pack(pady=10)
        
        self.port_output = scrolledtext.ScrolledText(frame, height=20, bg="#000000", fg="#00FF00", font=("Courier", 10))
        self.port_output.pack(padx=10, pady=10, fill="both", expand=True)

    def scan_ports(self):
        target = self.port_target.get().strip()
        self._safe_insert(self.port_output, f"SCANNING {target}...\n")
        def scan():
            for port in range(1, 501):
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(0.3)
                    if s.connect_ex((target, port)) == 0:
                        self._safe_insert(self.port_output, f"[OPEN] Port {port}\n")
                    s.close()
                except:
                    pass
            self._safe_insert(self.port_output, "PORT SCAN COMPLETE ~ NYAH!\n")
        threading.Thread(target=scan, daemon=True).start()

    # ====================== HTTP REPEATER ======================
    def build_burp_tab(self, frame):
        tk.Label(frame, text="=== HTTP REPEATER ===", bg="#0A0A0A", fg="#00FF00", font=("Courier", 14, "bold")).pack(pady=10)

        tk.Label(frame, text="URL:", bg="#0A0A0A", fg="#00FF00").pack(anchor="w", padx=10)
        self.url_entry = tk.Entry(frame, width=80, bg="#1A1A1A", fg="#00FF00", insertbackground="#00FF00")
        self.url_entry.pack(padx=10, fill="x", pady=2)
        self.url_entry.insert(0, "https://example.com")

        method_frame = tk.Frame(frame, bg="#0A0A0A")
        method_frame.pack(fill="x", padx=10, pady=5)
        tk.Label(method_frame, text="Method:", bg="#0A0A0A", fg="#00FF00").pack(side="left")
        self.method_var = tk.StringVar(value="GET")
        for m in ["GET", "POST", "PUT", "DELETE"]:
            tk.Radiobutton(method_frame, text=m, variable=self.method_var, value=m, bg="#0A0A0A", fg="#00FF00", selectcolor="#003300").pack(side="left", padx=8)

        tk.Label(frame, text="Body:", bg="#0A0A0A", fg="#00FF00").pack(anchor="w", padx=10, pady=(8,0))
        self.body_text = scrolledtext.ScrolledText(frame, height=6, bg="#1A1A1A", fg="#00FF00")
        self.body_text.pack(padx=10, fill="x", pady=5)

        tk.Button(frame, text="LAUNCH REQUEST", bg="#003300", fg="#00FF00", font=("Courier", 12, "bold"),
                  command=self.send_http, height=2, width=30).pack(pady=12)

        self.http_output = scrolledtext.ScrolledText(frame, height=12, bg="#000000", fg="#00FF00", font=("Courier", 10))
        self.http_output.pack(padx=10, pady=10, fill="both", expand=True)

    def send_http(self):
        self.http_output.delete(1.0, tk.END)
        url = self.url_entry.get().strip()
        method = self.method_var.get()
        body = self.body_text.get("1.0", tk.END).strip()
        self._safe_insert(self.http_output, f"[{method}] {url}\n")
        
        def run():
            try:
                if method == "GET":
                    req = urllib.request.Request(url, method=method)
                else:
                    data = body.encode('utf-8') if body else None
                    req = urllib.request.Request(url, data=data, method=method)
                    req.add_header('Content-Type', 'application/x-www-form-urlencoded')
                with urllib.request.urlopen(req, timeout=10) as resp:
                    data = resp.read(4096).decode('utf-8', errors='ignore')
                    self._safe_insert(self.http_output, f"Status: {resp.status}\n\n{data}\n")
            except Exception as e:
                self._safe_insert(self.http_output, f"ERROR: {e}\n")
        threading.Thread(target=run, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = CatsMultitool(root)
    root.mainloop()