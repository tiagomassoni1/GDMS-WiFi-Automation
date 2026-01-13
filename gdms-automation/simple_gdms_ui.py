import streamlit as st
import requests
import pandas as pd
import time

st.set_page_config(page_title="GDMS Bulk SSID", page_icon="📡", layout="wide")

st.title("📡 GDMS Bulk SSID Creator")

# Sidebar
with st.sidebar:
    st.header("🔐 Authentication")
    jwt = st.text_input("JWT Token", type="password", value="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkYXRhIjp7ImNlbnRlcklkIjoxMzk1MjgsInN5c3RlbSI6IjAiLCJwbGF0Zm9ybVR5cGUiOiIwIiwiaXNBcHAiOiIwIiwiYWNjb3VudCI6InRpYWdvQGFmdGMuY28iLCJ0aW1lb3V0IjoxODAsIm11bHRpVGVybWluYWxMb2dpbiI6MX0sImlzcyI6ImdkbXMiLCJleHAiOjE3Njc2NjY3ODUsImlhdCI6MTc2NzY1NTk4NX0.impuhy9vWJgFGdn9nJL_cPl_QwTxg46yI9RX7VLs0VE")
    session = st.text_input("Session Token", type="password", value="dc8616fc-1273-4feb-829d-75b92c8f4784")
    network_id = st.text_input("Network ID", value="274713")
    
    if jwt and session:
        st.success("🟢 Ready")

def create_ssid(ssid_name, password, vlan, mode, band, network_id, jwt, session):
    """Create a single SSID"""
    band_map = {"2.4GHz": "0", "5GHz": "1"}
    
    payload = {
        "accessKey": [],
        "bindAllDevice": 1,
        "siteList": [int(network_id)],
        "ssid_ssid": ssid_name,
        "ssid_wpa_key": password,
        "ssid_vlan": str(vlan),
        "ssid_bridge_enable": "1" if mode == "bridge" else "0",
        "ssid_new_ssid_band": band_map[band],
        "ssid_enable": "1",
        "ssid_encryption": "3",
        "ssid_security_type": "1",
        "ssid_wpa_encryption": "0",
        "bandwidth_type": "",
        "bindAllButUncheckedMacs": [],
        "device_site_type": "0",
        "filter": {"siteId": "all", "deviceType": "all", "search": ""},
        "os_filtering": "0",
        "removeAllDevices": 0,
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

# Main content
st.header("📊 Bulk SSID Creation")

# Sample CSV download
if st.button("📥 Download Sample CSV"):
    sample = pd.DataFrame({
        'Room_Number': ['101', '102', '103', '104', '105'],
        'Password': ['guest101', 'guest102', 'guest103', 'guest104', 'guest105'],
        'VLAN': [10, 10, 10, 10, 10],
        'Mode': ['bridge', 'bridge', 'bridge', 'bridge', 'bridge']
    })
    csv = sample.to_csv(index=False)
    st.download_button("💾 Download", csv, "rooms.csv", "text/csv")

# File upload
uploaded_file = st.file_uploader("Upload CSV", type=['csv'])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    st.subheader("📋 Preview")
    st.dataframe(df, use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Rooms", len(df))
    with col2:
        st.metric("SSIDs to Create", len(df) * 2)
    with col3:
        st.metric("Bands", "2.4G + 5G")
    
    st.info("ℹ️ Each room will get 2 SSIDs: Room-XXX-2.4G and Room-XXX-5G")
    
    dry_run = st.checkbox("🧪 Dry Run (test mode)", value=True)
    
    if st.button("🚀 START PROCESSING", type="primary"):
        if not jwt or not session:
            st.error("❌ Enter tokens in sidebar!")
        else:
            progress_bar = st.progress(0)
            status = st.empty()
            
            results = []
            total = len(df) * 2  # 2 SSIDs per room
            current = 0
            
            for idx, row in df.iterrows():
                room = str(row['Room_Number']).zfill(3)
                password = row['Password']
                vlan = int(row['VLAN'])
                mode = row['Mode']
                
                # Create 2.4GHz SSID
                ssid_2g = f"Room-{room}-2.4G"
                status.text(f"🔄 [{current+1}/{total}] Creating {ssid_2g}...")
                
                if dry_run:
                    results.append({
                        'SSID': ssid_2g,
                        'Band': '2.4GHz',
                        'Status': '🧪 Dry run - would create',
                        'Message': 'Simulation'
                    })
                    time.sleep(0.1)  # Small delay for realism
                else:
                    success, msg = create_ssid(
                        ssid_2g, password, vlan, mode, "2.4GHz",
                        network_id, jwt, session
                    )
                    results.append({
                        'SSID': ssid_2g,
                        'Band': '2.4GHz',
                        'Status': '✅ Created' if success else '❌ Failed',
                        'Message': msg
                    })
                    time.sleep(0.5)  # Avoid rate limiting
                
                current += 1
                progress_bar.progress(current / total)
                
                # Create 5GHz SSID
                ssid_5g = f"Room-{room}-5G"
                status.text(f"🔄 [{current+1}/{total}] Creating {ssid_5g}...")
                
                if dry_run:
                    results.append({
                        'SSID': ssid_5g,
                        'Band': '5GHz',
                        'Status': '🧪 Dry run - would create',
                        'Message': 'Simulation'
                    })
                    time.sleep(0.1)
                else:
                    success, msg = create_ssid(
                        ssid_5g, password, vlan, mode, "5GHz",
                        network_id, jwt, session
                    )
                    results.append({
                        'SSID': ssid_5g,
                        'Band': '5GHz',
                        'Status': '✅ Created' if success else '❌ Failed',
                        'Message': msg
                    })
                    time.sleep(0.5)
                
                current += 1
                progress_bar.progress(current / total)
            
            # Summary
            status.text("✅ Processing complete!")
            
            results_df = pd.DataFrame(results)
            
            st.subheader("📊 Results")
            st.dataframe(results_df, use_container_width=True)
            
            # Metrics
            success_count = len([r for r in results if '✅' in r['Status']])
            failed_count = len([r for r in results if '❌' in r['Status']])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("✅ Success", success_count)
            with col2:
                st.metric("❌ Failed", failed_count)
            with col3:
                st.metric("📊 Total", len(results))
            
            # Download results
            csv_results = results_df.to_csv(index=False)
            st.download_button(
                "📥 Download Results",
                csv_results,
                "ssid_creation_results.csv",
                "text/csv"
            )

st.markdown("---")
st.caption("🏨 AFT - Bulk SSID Automation")