Quick Start (5 Steps)
Step 1: Download the Project
Get the code from: [GitHub Link Here]
bash# Download and extract, then navigate to folder:
cd gdms-automation
Files you'll need:

gdms_bulk_assigned.py (main script)
requirements.txt (dependencies)
Your CSV file with network data


Step 2: Install Dependencies
Make sure Python is installed:
bashpython --version

If you don't have Python:

Download from: https://python.org
⚠️ During installation: CHECK "Add Python to PATH"

Install required packages:
bashpip install streamlit pandas requests openpyxl
```

---

### **Step 3: Get GDMS Authentication Tokens**

#### **3.1 - Select Correct Network**
```
1. Login to GDMS: www.gdms.cloud
2. TOP LEFT corner - verify network name:
   ┌─────────────────────────────┐
   │ ▼ Your Hotel/Company Name   │  ← Make sure this is correct!
   └─────────────────────────────┘
3. If managing multiple networks, SELECT the right one first!
```

#### **3.2 - Extract Tokens**
```
1. Press F12 (opens Developer Tools)
2. Click "Network" tab
3. In GDMS: Go to Settings → Wi-Fi → Click ANY existing network
4. In DevTools: Find request named "ssidEdit"
5. Click on it → "Headers" tab → "Request Headers" section
6. Copy these TWO values:

   Authorization: Bearer eyJ0eXAiOiJKV1Q...
                        └─────┬─────┘
                           JWT Token (copy everything after "Bearer ")

   Cookie: SESSION=YWQ0ZjI1MWIt...
                   └────┬────┘
                   Session Token (copy value after "SESSION=")
```

**Visual guide:**
```
DevTools → Network → ssidEdit → Headers → Request Headers:

Authorization: Bearer [COPY_THIS_LONG_STRING]
Cookie: SESSION=[COPY_THIS_VALUE]; other_cookies...
```

---

### **Step 4: Get Network ID**

**Choose ONE method:**

#### **Method A: From URL (Easiest)**
```
After selecting your network, look at browser address bar:

https://www.gdms.cloud/dashboard/network/690428/overview
                                        ^^^^^^
                                    Network ID = 690428
```

#### **Method B: From DevTools**
```
Same "ssidEdit" request → "Payload" tab → Look for:

{
  "siteList": [690428],    ← Network ID
  ...
}
```

#### **Method C: Decode JWT Token**
```
1. Go to: https://jwt.io
2. Paste your JWT token
3. Look at decoded "Payload" section
4. Find: "centerId": 690428 ← Might be Network ID
```

**⚠️ Common Mistake:**
```
❌ Wrong: Get Network ID while viewing different network
✅ Right: Select YOUR network FIRST, then get Network ID

Step 5: Run the Application
bash# From project folder:
streamlit run gdms_bulk_assigned.py
```

**Browser opens automatically at:** `http://localhost:8501`

---

## **🖥️ Using the Interface**

### **1. Enter Authentication (Left Sidebar)**
```
┌─────────────────────────────┐
│ JWT Token                   │
│ [paste JWT here]            │
│                             │
│ Session Token               │
│ [paste Session here]        │
│                             │
│ Network ID                  │
│ [enter Network ID]          │
│                             │
│ Status: 🟢 Ready            │
└─────────────────────────────┘
2. Upload CSV File
Your CSV format:
csvRoom_Number,AP_MAC,Password,VLAN,Mode
0302A,EC:74:D7:9A:9E:DA,3091456218,20,bridge
0302B,EC:74:D7:9A:8A:BB,7936484653,20,bridge
```

**Required columns:**
- `Room_Number` - Room/unit identifier
- `AP_MAC` - Access Point MAC address (format: `AA:BB:CC:DD:EE:FF`)
- `Password` - WiFi password (8+ characters)
- `VLAN` - VLAN ID number
- `Mode` - Use `bridge` (or `nat`)

**After upload, verify preview shows your data correctly**

### **3. Test with Dry Run**
```
✅ Check: "🧪 Dry Run" 
Click: "CREATE & ASSIGN ALL"

This shows what WILL happen without actually creating anything!

Review output:
🔄 [1/10] Would create: Network-Name-2.4G → MAC:AA:BB:CC:DD:EE:FF
🔄 [2/10] Would create: Network-Name-5G → MAC:AA:BB:CC:DD:EE:FF
...
✅ Dry Run Complete! (Nothing created)
```

### **4. Execute Creation**

**If dry run looks good:**
```
☐ Uncheck: "Dry Run"
Click: "CREATE & ASSIGN ALL"

Progress bar shows:
[████████████░░░] 420/432 (97%)
⏱️ Estimated: 45 seconds remaining
```

### **5. Download Results**
```
✅ Complete!

Success: 432
Failed: 0
Time: 8m 15s

[Download Results] ← Click to save CSV report
```

---

## **⚠️ Troubleshooting**

### **"Unauthorized" Error**
```
Problem: Tokens expired (last ~3 hours)
Fix: Get fresh tokens (repeat Step 3)
```

### **"Permission Denied"**
```
Problem: Account lacks admin access
Fix: Use account with Admin/Owner role
Test: Can you manually create SSIDs in GDMS UI?
```

### **"Device not found"**
```
Problem: AP MAC address incorrect or AP not adopted
Fix: 
  1. Verify MAC in GDMS: Devices → Access Points
  2. Check CSV format: AA:BB:CC:DD:EE:FF (colons, uppercase)
```

### **Can't Start Program**
```
Error: 'streamlit' is not recognized
Fix: 
  pip install --upgrade streamlit
  # Or:
  python -m streamlit run gdms_bulk_assigned.py
```

### **CSV Upload Error**
```
Problem: Wrong column names or format
Fix: Verify EXACT column names (case-sensitive):
  Room_Number,AP_MAC,Password,VLAN,Mode
```

---

## **📋 Pre-Flight Checklist**

**Before running:**
```
□ Python installed (3.8+)
□ Dependencies installed (streamlit, pandas, requests, openpyxl)
□ GDMS login credentials available
□ Correct network selected in GDMS
□ Fresh tokens extracted (< 3 hours old)
□ Network ID confirmed
□ CSV file prepared and validated
□ Tested with Dry Run first
```

---

## **💡 Best Practices**

1. **Always use Dry Run first** - Preview before executing
2. **Test small batch** - Try 5-10 SSIDs before full deployment
3. **Keep tokens fresh** - Refresh every 2-3 hours
4. **Verify in GDMS** - Spot-check created SSIDs manually
5. **Save results** - Download CSV log for records
6. **Document settings** - Note VLAN, passwords, configurations

---

## **📊 What Gets Created**

**For each room in CSV:**
- 2 SSIDs (one 2.4GHz + one 5GHz)
- Same password for both bands
- Assigned to specific Access Point
- Configured with your VLAN and mode

**Example:**
```
Room: 0302A
  → Creates: Network-0302A-2.4G (on AP: AA:BB:CC:DD:EE:FF)
  → Creates: Network-0302A-5G   (on AP: AA:BB:CC:DD:EE:FF)
  Password: 3091456218 (same for both)
  VLAN: 20
  Mode: Bridge
```

---

## **🆘 Getting Help**

**Can't find Network ID?**

Send AI assistant:
1. Screenshot of GDMS page (showing selected network name)
2. Screenshot of browser URL
3. Screenshot of DevTools → ssidEdit → Payload tab

**Other issues?**

Check logs in terminal/console for error messages and share them.

---

## **📦 Project Files Structure**
```
gdms-automation/
├── gdms_bulk_assigned.py          # Main script
├── requirements.txt                # Dependencies list
├── your_data.csv                   # Your network data
└── README.md                       # This guide

🎯 Quick Commands
bash# Install
pip install streamlit pandas requests openpyxl

# Navigate to project
cd gdms-automation

# Run
streamlit run gdms_bulk_assigned.py

# Stop (if needed)
Press Ctrl+C in terminal
```

---

## **⏱️ Expected Timeline**
```
Setup: 10-15 minutes (first time only)
Token extraction: 2-3 minutes
CSV preparation: 5-10 minutes
Execution: ~1 second per SSID (432 SSIDs ≈ 7-10 minutes)

Total: ~30 minutes (vs 36 hours manual!)
```

---

## **✅ Success Checklist**

**After completion, verify:**
```
□ All SSIDs visible in GDMS → Settings → Wi-Fi
□ SSID names match expected format
□ Passwords match CSV
□ VLAN configured correctly
□ Each SSID assigned to correct AP only
□ Both 2.4GHz and 5GHz created per room
□ Results CSV downloaded and saved

🎉 That's it! You're ready to automate WiFi deployment!
