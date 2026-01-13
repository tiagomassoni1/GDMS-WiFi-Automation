import requests

jwt = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkYXRhIjp7ImNlbnRlcklkIjoxMzk1MjgsInN5c3RlbSI6IjAiLCJwbGF0Zm9ybVR5cGUiOiIwIiwiaXNBcHAiOiIwIiwiYWNjb3VudCI6InRpYWdvQGFmdGMuY28iLCJ0aW1lb3V0IjoxODAsIm11bHRpVGVybWluYWxMb2dpbiI6MX0sImlzcyI6ImdkbXMiLCJleHAiOjE3Njc3MzA2NTAsImlhdCI6MTc2NzcxOTg1MH0.Q1jj4aLEYYHH1iBL3P-WTYRYapmyEWaWVCiSNEAa1cU"
session = "YWQ0ZjI1MWItODU3Ni00NmYwLTg5NGYtZTQ4NzNmZjM2Yjk5"

payload = {
    "accessKey": [],
    "bindAllDevice": 0,
    "membership_macs": "EC:74:D7:9A:9E:DA",
    "removeAllDevices": 1,
    "removed_macs": "",
    "siteList": [690428],
    "ssid_ssid": "DEBUG-PERMISSION",
    "ssid_wpa_key": "test123456",
    "ssid_vlan": "20",
    "ssid_bridge_enable": "1",
    "ssid_new_ssid_band": "2",
    "ssid_enable": "1",
    "ssid_encryption": "3",
    "ssid_security_type": "1",
    "ssid_wpa_encryption": "0",
    "bandwidth_type": "",
    "device_site_type": "0",
    "filter": {"siteId": "all", "deviceType": "all", "search": ""},
    "os_filtering": "0",
    "ssid_11K": "0", "ssid_11R": "0", "ssid_11V": "0", "ssid_11W": "0",
    "ssid_ClientIPAssignment": "0", "ssid_bms": "0",
    "ssid_bonjour_forward": "0", "ssid_dtim_period": "1",
    "ssid_isolation": "0", "ssid_mac_auth": "0",
    "ssid_mac_filtering": "0", "ssid_mcast_to_ucast": "0",
    "ssid_portal_enable": "0", "ssid_proxyarp": "0",
    "ssid_remark": "", "ssid_schedule": "",
    "ssid_ssid_hidden": "0", "ssid_sta_idle_timeout": "300",
    "ssid_timed_client_policy": "", "ssid_twt_enable": "0",
    "ssid_uapsd": "1", "ssid_voice_enterprise": "0",
    "ssid_wifi_client_limit": "", "supportSite": 1
}

headers = {
    "Authorization": f"Bearer {jwt}",
    "X-Auth-Token": session,
    "Content-Type": "application/json",
    "Origin": "https://www.gdms.cloud",
    "Referer": "https://www.gdms.cloud/"
}

print("Testando criação de SSID...")
print(f"Network ID: 690428")
print(f"Account: tiago@aftc.co")

response = requests.post(
    "https://www.gwn.cloud/app/ssid/ssidEdit",
    json=payload,
    headers=headers
)

print(f"\nStatus: {response.status_code}")
print(f"Response completa:")
print(response.text)

try:
    result = response.json()
    print(f"\nretCode: {result.get('retCode')}")
    print(f"msg: {result.get('msg')}")
    print(f"data: {result.get('data')}")
except:
    print("Não conseguiu parsear JSON")