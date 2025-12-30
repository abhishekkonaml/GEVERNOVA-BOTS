import requests
from requests.exceptions import RequestException, SSLError
 
# Configuration
app_id = "Intelligeni"
safe = "1801_00_NMG_SN_VN-NET-OPS"
#username = "504018887"
username ="504020320"
ccp1_url = "alpcts000000240.rd.ds.ge.com"
ccp2_url = "CGHCTS000000118.rd.ds.ge.com"
cert = ("/etc/pki/tls/certs/intelligeni.gevernova.net.crt", "/etc/pki/tls/private/bots.intelligeni.gevernova.net.key")  # Replace with your actual paths

proxies={
    "http": '',
    "https": ''
}

# Target API path
endpoint_path = "/AIMWebService/api/Accounts"
 
# Prepare request parameters
params = {
    "AppID": app_id,
    "Safe": safe,
    "username": username
}
 
headers = {
    "Content-Type": "application/json"
}
 
# Function to try a URL
def fetch_secrets_from_url(base_url):
    url = f"https://{base_url}{endpoint_path}"
    try:
        print(f"Trying: {url}")
        response = requests.get(url, params=params, headers=headers, cert=cert, timeout=10,proxies=proxies)
        response.raise_for_status()
        return response.json()
    except (RequestException, SSLError) as e:
        print(f"Failed to connect to {base_url}: {e}")
        return None
 
# Try primary first, fallback to secondary if needed
secrets = fetch_secrets_from_url(ccp1_url)
if not secrets:
    secrets = fetch_secrets_from_url(ccp2_url)


print(secrets)
 
# Handle result
if secrets:
    user = secrets.get("UserName")
    pswd = secrets.get("Content")
    print("-----------------------------------------------------------------------------")
    print(f"Account Information from CyberArk:\nUsername = {user}\nPassword = {pswd}")
    print("-----------------------------------------------------------------------------")
else:
    print("Failed to retrieve secrets from both endpoints.")