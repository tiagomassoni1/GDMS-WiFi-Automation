import streamlit as st
import requests
import pandas as pd
import time

st.set_page_config(page_title="GDMS Bulk SSID + Assignment", page_icon="📡", layout="wide")

st.title("📡 GDMS Bulk SSID with Device Assignment")

# Sidebar
with st.sidebar:
    st.header("🔐 Authentication")
    jwt = st.text_input("JWT Token", type="password", value="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkYXRhIjp7ImNlbnRlcklkIjoxMzk1MjgsInN5c3RlbSI6IjAiLCJwbGF0Zm9ybVR5cGUiOiIwIiwiaXNBcHAiOiIwIiwiYWNjb3VudCI6InRpYWdvQGFmdGMuY28iLCJ0aW1lb3V0IjoxODAsIm11bHRpVGVybWluYWxMb2dpbiI6MX0sImlzcyI6ImdkbXMiLCJleHAiOjE3Njc2NjY3ODUsImlhdCI6MTc2NzY1NTk4NX0.impuhy9vWJgFGdn9nJL_cPl_QwTxg46yI9RX7VLs0VE")
    session = st.text_input("Session Token", type="password", value="dc8616fc-1273-4feb-829d-75b92c8f4784")
    network_id = st.text_input("Network ID", value="274713")
    
    if jwt and session:
        st.success("🟢 Ready")

def create_ssid_assigned(ssid_name, password, vlan, mode, band, ap_mac, jwt, session):
    """Create SSID and assign to specific AP"""
    band_map = {"2.4GHz": "2", "5GHz": "5"}
    
    payload = {
        "accessKey": [],
        "bindAllDevice": 0,  # ← KEY: Don't bind to all
        "membership_macs": ap_mac,  # ← KEY: Specific AP only
        "removeAllDevices": 1,  # ← Remove from others
        "removed_macs": "",
        "siteList": [],  # ← Empty when assigning to device
        "device_site_type": "0",
        "filter": {"siteId": "all", "deviceType": "all", "search": ""},
        "os_filtering": "0",
        "bandwidth_type": "",
        
        # SSID Config
        "ssid_ssid": ssid_name,
        "ssid_wpa_key": password,
        "ssid_vlanid": str(vlan),
	"ssid_vlan": "1",
        "ssid_bridge_enable": "1" if mode == "bridge" else "0",
        "ssid_new_ssid_band": band_map[band],
        "ssid_enable": "1",
        "ssid_encryption": "3",
        "ssid_security_type": "1",
        "ssid_wpa_encryption": "0",
        
        # Defaults
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
    
    try:
        response = requests.post(
            "https://www.gwn.cloud/app/ssid/ssidEdit",
            json=payload,
            headers=headers,
            timeout=10
        )
        result = response.json()
        return result.get("retCode") == 0, result.get("msg", "Unknown error")
    except Exception as e:
        return False, str(e)

# Main
st.header("📊 Bulk SSID Creation with AP Assignment")

st.info("ℹ️ CSV must include AP_MAC column for device assignment")

# Sample CSV
if st.button("📥 Download Sample CSV with AP_MAC"):
    sample = pd.DataFrame({
        'Room_Number': ['0302A', '0302B', '0303A'],
        'AP_MAC': ['EC:74:D7:1C:66:A8', 'EC:74:D7:1C:66:B9', 'EC:74:D7:1C:66:C0'],
        'Password': ['1234567890', '2345678901', '3456789012'],
        'VLAN': [10, 10, 10],
        'Mode': ['bridge', 'bridge', 'bridge']
    })
    csv = sample.to_csv(index=False)
    st.download_button("💾 Download", csv, "trilogy_with_macs.csv", "text/csv")

# File upload
uploaded_file = st.file_uploader("Upload CSV with AP_MAC", type=['csv'])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    # Validate
    required = ['Room_Number', 'AP_MAC', 'Password', 'VLAN', 'Mode']
    missing = [col for col in required if col not in df.columns]
    
    if missing:
        st.error(f"❌ Missing columns: {missing}")
        st.stop()
    
    st.subheader("📋 Preview")
    st.dataframe(df.head(10), use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Rooms", len(df))
    with col2:
        st.metric("SSIDs to Create", len(df) * 2)
    with col3:
        st.metric("Device Assignment", "✅ Enabled")
    
    st.success("✅ Each SSID will be assigned ONLY to its specific AP")
    
    dry_run = st.checkbox("🧪 Dry Run", value=True)
    
    if st.button("🚀 CREATE & ASSIGN ALL", type="primary"):
        if not jwt or not session:
            st.error("❌ Enter tokens!")
        else:
            progress = st.progress(0)
            status = st.empty()
            
            results = []
            total = len(df) * 2
            current = 0
            
            for idx, row in df.iterrows():
                room = row['Room_Number']
                ap_mac = row['AP_MAC']
                password = row['Password']
                vlan = int(row['VLAN'])
                mode = row['Mode']
                
                # Create 2.4GHz
                ssid_2g = f"Trilogy U{room} 2.4G"
                status.text(f"🔄 [{current+1}/{total}] {ssid_2g} → {ap_mac}")
                
                if dry_run:
                    results.append({
                        'SSID': ssid_2g,
                        'AP': ap_mac,
                        'Status': '🧪 Would create & assign',
                        'Message': 'Dry run'
                    })
                else:
                    success, msg = create_ssid_assigned(
                        ssid_2g, password, vlan, mode, "2.4GHz",
                        ap_mac, jwt, session
                    )
                    results.append({
                        'SSID': ssid_2g,
                        'AP': ap_mac,
                        'Status': '✅ Created' if success else '❌ Failed',
                        'Message': msg
                    })
                    time.sleep(0.5)
                
                current += 1
                progress.progress(current / total)
                
                # Create 5GHz
                ssid_5g = f"Trilogy U{room} 5G"
                status.text(f"🔄 [{current+1}/{total}] {ssid_5g} → {ap_mac}")
                
                if dry_run:
                    results.append({
                        'SSID': ssid_5g,
                        'AP': ap_mac,
                        'Status': '🧪 Would create & assign',
                        'Message': 'Dry run'
                    })
                else:
                    success, msg = create_ssid_assigned(
                        ssid_5g, password, vlan, mode, "5GHz",
                        ap_mac, jwt, session
                    )
                    results.append({
                        'SSID': ssid_5g,
                        'AP': ap_mac,
                        'Status': '✅ Created' if success else '❌ Failed',
                        'Message': msg
                    })
                    time.sleep(0.5)
                
                current += 1
                progress.progress(current / total)
            
            status.text("✅ Complete!")
            
            results_df = pd.DataFrame(results)
            st.subheader("📊 Results")
            st.dataframe(results_df, use_container_width=True)
            
            # Summary
            success = len([r for r in results if '✅' in r['Status']])
            failed = len([r for r in results if '❌' in r['Status']])
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("✅ Success", success)
            with col2:
                st.metric("❌ Failed", failed)
            
            # Download
            csv = results_df.to_csv(index=False)
            st.download_button("📥 Download Results", csv, "results.csv", "text/csv")

st.markdown("---")
st.caption("🏨 Trilogy Hotel - AFT Deployment")