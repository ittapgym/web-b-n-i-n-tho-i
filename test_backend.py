import urllib.request
import json

url = "https://peach-store-backend.onrender.com/san-pham/danh-muc/iphone"

try:
    with urllib.request.urlopen(url) as response:
        html = response.read().decode('utf-8')
        print("Success:", html)
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}:")
    try:
        error_body = e.read().decode('utf-8')
        print(error_body)
    except Exception as ex:
        print("Could not read error body:", ex)
except Exception as e:
    print("Error:", e)
