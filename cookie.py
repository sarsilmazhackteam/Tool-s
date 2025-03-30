import sqlite3
import os
from datetime import datetime, timedelta

def get_chrome_cookies_formatted(domain=None):
    """Chrome çerezlerini belirtilen formatta getirir"""
    cookie_path = get_chrome_cookie_path()
    
    if not os.path.exists(cookie_path):
        raise FileNotFoundError("Chrome çerez dosyası bulunamadı")

    conn = sqlite3.connect(cookie_path)
    cursor = conn.cursor()

    query = "SELECT host_key, name, value, path, expires_utc, is_secure FROM cookies"
    if domain:
        query += f" WHERE host_key LIKE '%{domain}%'"

    cursor.execute(query)
    
    print("# Vulnerabil\n")
    print("## User ID:")
    print("- ID: 1")
    print("- First name: ad")
    print("- Surname: admin\n")
    
    print("## More info")
    print("http://www.security.com/item.wikipedia.org/wiki/More_Info\n")
    print("---\n")
    print("### Name")
    print("| Value    | P... | E... | S... | H... | S... |")
    print("|---|---|---|---|---|---|")

    for item in cursor.fetchall():
        host, name, value, path, expires, secure = item
        print(f"| {name} | {value[:15]}... | {path} | {convert_chrome_time(expires)} | {'Yes' if secure else 'No'} | {len(value)} |")

    print("\n---\n")
    print("### Source")
    print("- SQL Injection")
    print("- API Injection (BIL-A)")

    conn.close()

def get_chrome_cookie_path():
    """Chrome çerez dosya yolunu bulur"""
    system = platform.system()
    if system == "Windows":
        return os.path.join(os.getenv('LOCALAPPDATA'), 'Google', 'Chrome', 'User Data', 'Default', 'Network', 'Cookies')
    elif system == "Darwin":
        return os.path.expanduser('~/Library/Application Support/Google/Chrome/Default/Cookies')
    else:
        return os.path.expanduser('~/.config/google-chrome/Default/Cookies')

def convert_chrome_time(chrome_time):
    """Chrome zaman formatını dönüştürür"""
    if chrome_time == 0:
        return "Session"
    return (datetime(1601, 1, 1) + timedelta(microseconds=chrome_time)).strftime('%Y-%m-%d')

if __name__ == '__main__':
    import platform
    try:
        get_chrome_cookies_formatted()
    except Exception as e:
        print(f"Hata: {str(e)}")