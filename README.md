# Selenium Automation Script - Login Flow

This script automates the login and registration flow for the Scanbo application.

## Prerequisites

1. **Python 3.7 or higher** installed on your system
2. **Google Chrome browser** installed
3. **Internet connection**

## Step-by-Step Setup and Execution

### Step 1: Install Python (if not already installed)

Check if Python is installed:
```bash
python3 --version
```

If not installed, install Python 3.7+ from [python.org](https://www.python.org/downloads/)

### Step 2: Navigate to Project Directory

```bash
cd /home/scalp8/RD_Project/new_Register_flow
```

### Step 3: Create Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 4: Install Required Packages

```bash
pip install -r requirements.txt
```

This will install:
- `selenium` - Web automation framework
- `webdriver-manager` - Automatically manages ChromeDriver

### Step 5: Update Selectors in Script

**IMPORTANT:** Before running, you need to update the element selectors in `login_automation.py` to match your actual website HTML.

To find the correct selectors:
1. Open Chrome browser
2. Navigate to `https://dev2.scanbo.com/authentication/login`
3. Press `F12` to open Developer Tools
4. Click the "Select Element" tool (or press `Ctrl+Shift+C`)
5. Click on each element (mobile input, checkbox, buttons, etc.)
6. In the Elements tab, right-click the highlighted HTML → Copy → Copy selector
7. Update the selectors in the script

Common selectors to update:
- Mobile number input field
- Disclaimer checkbox
- Disclaimer scrollable area
- Agree button
- OTP input field
- Verify OTP button
- Patient profile selection
- Registration step 1 indicator

### Step 6: Run the Script

```bash
python3 login_automation.py
```

### Step 7: Monitor Execution

The script will:
- Print progress messages for each step
- Keep the browser open if an error occurs (for debugging)
- Automatically close after successful completion (if uncommented)

## Testing Tips

### Test Individual Steps

Comment out steps you've already tested to focus on specific parts:

```python
# Comment out completed steps
# print("Step 1: Opening login page...")
# driver.get("https://dev2.scanbo.com/authentication/login")
```

### Debug Mode

The script keeps the browser open on errors. To manually close:
- Press `Ctrl+C` in terminal
- Or uncomment `driver.quit()` in the finally block

### Common Issues and Solutions

1. **ChromeDriver version mismatch**
   - Solution: `webdriver-manager` handles this automatically

2. **Element not found**
   - Solution: Update selectors using browser DevTools
   - Add more `time.sleep()` if page loads slowly

3. **Timeout errors**
   - Solution: Increase wait time: `WebDriverWait(driver, 30)`

4. **Popup/Modal not detected**
   - Solution: Add explicit wait for popup to appear before interacting

## Script Flow

1. ✅ Open login page
2. ✅ Enter mobile number (7575757676)
3. ✅ Open disclaimer popup (click checkbox)
4. ✅ Scroll disclaimer fully
5. ✅ Click Agree button
6. ✅ Wait for OTP field
7. ✅ Enter OTP (654320)
8. ✅ Click Verify OTP button
9. ✅ Select patient profile
10. ✅ Wait for registration step 1

## Notes

- The script includes `time.sleep()` calls for stability
- All selectors need to be updated based on actual website HTML
- Browser will stay open on errors for debugging
- Remove `time.sleep()` calls once selectors are correct and timing is stable

