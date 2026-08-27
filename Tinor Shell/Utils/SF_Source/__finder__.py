import tkinter as tk
from tkinter import ttk, messagebox
import requests
import time
import random
import webbrowser
from threading import Thread
import os

# ================= CONFIG =================
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; SocialFinder/1.0)"}
REQUEST_DELAY = (1.0, 2.0)
TIMEOUT = 10
RESULT_FILE = "matches.txt"
RESULT_DIR = "results"
os.makedirs(RESULT_DIR, exist_ok=True)
RESULT_PATH = os.path.join(RESULT_DIR, RESULT_FILE)

# ================= UTILS =================
def load_sites(filename="sites.txt"):
    sites = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            if "|" not in line:
                continue
            name, url = line.strip().split("|", 1)
            sites.append((name.strip(), url.strip()))
    return sites

def generate_variations(base):
    variants = set()
    variants.update([base, base.lower(), base.upper(), base.capitalize()])
    for i in range(1, 6):
        variants.update([
            f"{base}{i}", f"{base.lower()}{i}", f"{base.capitalize()}{i}"
        ])
    return sorted(variants)

def score_profile(html, username, keywords):
    score = 5
    if username.lower() in html.lower():
        score += 2
    for kw in keywords:
        if kw.lower() in html.lower():
            score += 2
    return score

def write_match(username, site):
    with open(RESULT_PATH, "a", encoding="utf-8") as f:
        f.write(f"{username} - LIKELY on {site}\n")

# ================= GUI =================
class SocialFinderGUI:
    def __init__(self, root):
        self.root = root
        root.title("Social Media Finder")
        root.geometry("900x550")

        # Inputs
        ttk.Label(root, text="Base Username:").pack(anchor="w", padx=10, pady=(10, 0))
        self.username_entry = ttk.Entry(root, width=40)
        self.username_entry.pack(anchor="w", padx=10)

        ttk.Label(root, text="Keywords (comma separated):").pack(anchor="w", padx=10, pady=(10, 0))
        self.keywords_entry = ttk.Entry(root, width=60)
        self.keywords_entry.pack(anchor="w", padx=10)

        self.start_button = ttk.Button(root, text="Start Scan", command=self.start_scan)
        self.start_button.pack(pady=10)

        # Scrollable frame for clickable results
        self.frame = tk.Frame(root)
        self.frame.pack(fill="both", expand=True, padx=10, pady=(0,10))
        self.canvas = tk.Canvas(self.frame)
        self.scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0,0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.found_matches = {}  # for merging duplicates

    def log_match(self, username, site, url):
        key = f"{username}_{site}"
        if key in self.found_matches:
            return
        self.found_matches[key] = True

        # Save to matches.txt immediately
        write_match(username, site)

        # Add clickable button
        btn = ttk.Button(
            self.scrollable_frame,
            text=f"{username} - {site}",
            command=lambda u=url: webbrowser.open(u),
            width=80
        )
        btn.pack(pady=2)

    def start_scan(self):
        base = self.username_entry.get().strip()
        keywords = self.keywords_entry.get().strip()
        if not base:
            messagebox.showerror("Error", "Please enter a username")
            return

        # Reset
        self.start_button.config(state="disabled")
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.found_matches = {}
        open(RESULT_PATH, "w").close()  # clear old results

        # Run scan in background
        thread = Thread(target=self.run_scan, args=(base, keywords), daemon=True)
        thread.start()

    def run_scan(self, base_username, keyword_input):
        keywords = [k.strip() for k in keyword_input.split(",") if k.strip()]
        sites = load_sites()
        usernames = generate_variations(base_username)
        total_tasks = len(sites) * len(usernames)
        task_count = 0

        self.log_info(f"[*] Loaded {len(sites)} sites")
        self.log_info(f"[*] Username variations: {len(usernames)}")
        self.log_info(f"[*] Keywords: {keywords}\n")

        for site_name, site_url in sites:
            for username in usernames:
                task_count += 1
                self.log_info(f"[{task_count}/{total_tasks}] Scanning {site_name} for {username}...")

                url = site_url.replace("USER", username)
                try:
                    r = requests.get(url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True)
                    if r.status_code == 200:
                        score = score_profile(r.text, username, keywords)
                        if score >= 7:
                            self.log_match(username, site_name, url)
                except requests.RequestException:
                    self.log_info(f"[!] {site_name}: Failed for {username}")

                time.sleep(random.uniform(*REQUEST_DELAY))

        self.log_info("\n[*] Scan complete.")
        self.start_button.config(state="normal")

    def log_info(self, text):
        lbl = tk.Label(self.scrollable_frame, text=text, anchor="w", justify="left")
        lbl.pack(fill="x")


if __name__ == "__main__":
    root = tk.Tk()
    app = SocialFinderGUI(root)
    root.mainloop()
