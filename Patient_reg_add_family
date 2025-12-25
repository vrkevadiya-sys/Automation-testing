import os
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager


# ==================================================
# DRIVER SETUP
# ==================================================
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)
wait = WebDriverWait(driver, 40)


# ==================================================
# LOGIN + OTP
# ==================================================
driver.get("https://dev1.scanbo.com/authentication/login")

wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='tel']"))).send_keys("7878788189")

wait.until(EC.element_to_be_clickable((By.XPATH, "//label[contains(.,'Disclaimer')]"))).click()

wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']")))

driver.execute_script("""
let d=document.querySelector("[role='dialog']");
let s=[...d.querySelectorAll("*")].find(e=>e.scrollHeight>e.clientHeight);
if(s){s.scrollTop=s.scrollHeight;s.dispatchEvent(new Event('scroll'));}
""")

wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Agree')]"))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Send OTP')]"))).click()

otp_boxes = wait.until(
    EC.presence_of_all_elements_located(
        (By.XPATH, "//input[@inputmode='numeric' or @maxlength='1']")
    )
)

otp = os.getenv("TEST_OTP", "654320")
for i, d in enumerate(otp):
    otp_boxes[i].send_keys(d)

wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Verify')]"))).click()
time.sleep(8)

print("✅ Dashboard loaded")

# ==================================================
# CLICK FAMILY MEMBER (LEFT MENU)
# ==================================================
driver.find_element(By.XPATH, "//*[normalize-space()='Family Member']").click()
print("✅ Family Member menu clicked")

# ==================================================
# CLICK + ADD NEW (CENTER FAMILY MEMBERS PAGE)
# ==================================================

add_new_btn = wait.until(
    EC.element_to_be_clickable(
        (
            By.XPATH,
            "//button[.//text()[normalize-space()='Add New'] or normalize-space()='Add New']"
        )
    )
)
add_new_btn.click()
print("✅ + Add New clicked")

# # ==================================================
# # CLICK + ADD NEW (CENTER OF PAGE)
# # ==================================================

# add_new_btn = wait.until(
#     EC.element_to_be_clickable(
#         (
#             By.XPATH,
#             "//button[.//text()[normalize-space()='+ Add New']]"
#             " | //*[normalize-space()='+ Add New']"
#         )
#     )
# )
# add_new_btn.click()

# print("✅ + Add New clicked (center of page)")

# ==================================================
# WAIT FOR ADD FAMILY MEMBER – PROFILE PAGE
# ==================================================

wait.until(
    EC.visibility_of_element_located(
        (By.XPATH, "//*[normalize-space()='Profile']")
    )
)
print("✅ Profile page loaded")

# ==================================================
# ENTER MOBILE NUMBER
# ==================================================

mobile_input = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//input[@type='tel']"))
)
mobile_input.clear()
mobile_input.send_keys("9876545676")
print("✅ Mobile number entered")
time.sleep(3)

# ==================================================
# WAIT FOR OTP MODAL
# ==================================================

otp_modal = wait.until(
    EC.visibility_of_element_located(
        (By.XPATH, "//*[contains(text(),'Enter 6 digit number')]")
    )
)
print("✅ OTP modal displayed")

# ==================================================
# ENTER OTP DIGITS (ONE BY ONE)
# ==================================================

otp_digits = ["6", "5", "4", "3", "2", "0"]

otp_boxes = wait.until(
    EC.presence_of_all_elements_located(
        (By.XPATH, "//div[contains(@class,'MuiDialog')]//input[@type='tel' or @inputmode='numeric']")
    )
)

for i in range(6):
    otp_boxes[i].clear()
    otp_boxes[i].send_keys(otp_digits[i])

print("✅ OTP entered successfully")

# ==================================================
# WAIT FOR OTP ENTRY TO COMPLETE
# ==================================================
time.sleep(0.5)

# ==================================================
# CLICK VERIFY BUTTON
# ==================================================

verify_btn = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "//button[normalize-space()='Verify']")
    )
)
verify_btn.click()

time.sleep(3)

print("➡️ Verify clicked")

# ==================================================
# ENTER FIRST NAME
# ==================================================

first_name = driver.find_element(
    By.XPATH, "//input[contains(@placeholder,'First Name')]"
)
first_name.clear()
first_name.send_keys("viju")
print("✅ First name entered")

# ==================================================
# ENTER LAST NAME
# ==================================================

last_name = driver.find_element(
    By.XPATH, "//input[contains(@placeholder,'Last Name')]"
)
last_name.clear()
last_name.send_keys("Kevadiya")
print("✅ Last name entered")


time.sleep(.3)

# ==================================================
# SELECT RELATIONSHIP → SON
# ==================================================

# Click Relationship dropdown
relationship_dropdown = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "//*[normalize-space()='Relationship']/following::*[contains(@class,'MuiInputBase') or contains(@class,'MuiOutlinedInput')][1]")
    )
)
relationship_dropdown.click()
print("✅ Relationship dropdown clicked")

# Select "Son" from list
son_option = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "//*[normalize-space()='Son']")
    )
)
son_option.click()
print("✅ Relationship selected: Son")


driver.find_element(By.XPATH, "//button[normalize-space()='Next']").click()
print("➡️ Next clicked")

time.sleep(3)

# ==================================================
# ✅ ADDRESS PAGE
# ==================================================
wait.until(EC.presence_of_element_located((By.XPATH, "//*[normalize-space()='Address']")))
print("✅ Address page loaded")



address_dropdown = wait.until(
    EC.presence_of_element_located((
        By.XPATH,
        "//div[contains(@class,'MuiSelect') or contains(text(),'Select Address')]"
    ))
)

driver.execute_script("""
arguments[0].scrollIntoView({block:'center'});
arguments[0].click();
arguments[0].dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
arguments[0].dispatchEvent(new MouseEvent('mouseup', { bubbles: true }));
""", address_dropdown)

print("Address type dropdown opened")

time.sleep(1)

# --------------------------------------------------
# SELECT "Primary"
# --------------------------------------------------
primary_option = wait.until(
    EC.presence_of_element_located((
        By.XPATH,
        "//li[normalize-space()='Primary']"
    ))
)

driver.execute_script("""
arguments[0].scrollIntoView({block:'center'});
arguments[0].click();
""", primary_option)

print("Primary address selected")

# --------------------------------------------------
# ZIPCODE — REACT CONTROLLED INPUT FIX
# --------------------------------------------------
from selenium.webdriver.common.keys import Keys

ZIPCODE = "395009"

zip_input = wait.until(
    EC.element_to_be_clickable((
        By.XPATH, "//input[contains(@placeholder,'Zip')]"
    ))
)

zip_input.click()
zip_input.send_keys(Keys.CONTROL, "a")
zip_input.send_keys(Keys.DELETE)

for digit in ZIPCODE:
    zip_input.send_keys(digit)
    time.sleep(0.3)   # VERY IMPORTANT (React debounce)

print("Zipcode typed like human")

# Wait for city/state API binding
time.sleep(3)
ADDRESS1 = "Surat, Mota Varachha"

address1_input = wait.until(
    EC.presence_of_element_located((
        By.XPATH, "//input[@name='address1' or contains(@placeholder,'Address')]"
    ))
)

driver.execute_script("""
let input = arguments[0];
let value = arguments[1];

// focus
input.focus();

// React value setter
let setter = Object.getOwnPropertyDescriptor(
    window.HTMLInputElement.prototype,
    'value'
).set;

// set value
setter.call(input, value);

// dispatch real events (React needs this)
input.dispatchEvent(new Event('input', { bubbles: true }));
input.dispatchEvent(new Event('change', { bubbles: true }));
input.dispatchEvent(new Event('blur', { bubbles: true }));
""", address1_input, ADDRESS1)

time.sleep(1)

print(" Address 1 filled and locked")


time.sleep(1)

next_btn = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "//button[normalize-space()='Next' and not(@disabled)]")
    )
)
driver.execute_script("arguments[0].click();", next_btn)

print("✅ Address step completed successfully")

# ==================================================
# I AM PATIENT / Gender selection
# ==================================================

# --------------------------------------------------
# STEP 2: GENDER
# --------------------------------------------------
GENDER = "Male"   # "Male" | "Female" | "Other"
# --------------------------------------------------
# SELECT GENDER
# --------------------------------------------------
gender_btn = wait.until(
    EC.element_to_be_clickable((
        By.XPATH, f"//button[normalize-space()='{GENDER}']"
    ))
)

driver.execute_script("arguments[0].scrollIntoView({block:'center'});", gender_btn)
time.sleep(0.3)

driver.execute_script("arguments[0].click();", gender_btn)
print("Gender selected:", GENDER)

time.sleep(0.5)

# --------------------------------------------------
# CLICK NEXT BUTTON
# --------------------------------------------------
next_btn = wait.until(
    EC.element_to_be_clickable((
        By.XPATH, "//button[normalize-space()='Next']"
    ))
)

driver.execute_script("arguments[0].click();", next_btn)
print("Next button clicked after gender selection")


# --------------------------------------------------
# STEP 3: AGE
# --------------------------------------------------
DOB_VALUE = "10/11/1995"   # DD/MM/YYYY format


#print("Auto calculated DOB:", dob_value)
dob_input = wait.until(
    EC.element_to_be_clickable((
        By.XPATH,
        "//label[contains(text(),'Birth')]/following::input[1]"
    ))
)

# Click and clear
dob_input.click()
time.sleep(0.5)
dob_input.send_keys(Keys.CONTROL + "a")
dob_input.send_keys(Keys.BACKSPACE)

# Type DOB slowly (React requirement)
for ch in DOB_VALUE:
    dob_input.send_keys(ch)
    time.sleep(0.15)

# Force React state update
driver.execute_script("""
arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
arguments[0].blur();
""", dob_input)

time.sleep(2)
print("DOB entered and React accepted it")


# --------------------------------------------------
# VERIFY AGE AUTO CALCULATED (READ ONLY)
# --------------------------------------------------
#age_input = wait.until(
 #   EC.presence_of_element_located((
  #      By.XPATH, "//input[contains(@placeholder,'Age') or contains(@class,'age')]"
   # ))
#)

#print("Auto calculated Age:", age_input.get_attribute("value"))
# --------------------------------------------------
# NEXT BUTTON
# --------------------------------------------------
# give UI time to auto-calculate age
time.sleep(2)

next_btn = wait.until(
    EC.presence_of_element_located((
        By.XPATH, "//button[normalize-space()='Next']"
    ))
)

driver.execute_script("""
arguments[0].scrollIntoView({block:'center'});
arguments[0].disabled = false;
arguments[0].removeAttribute('disabled');
arguments[0].click();
""", next_btn)

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 15)
time.sleep(0.5)


# ==================================================
# WEIGHT (KG) PAGE
# ==================================================

# Wait for Weight input (KG page)
kg_input = wait.until(
    EC.element_to_be_clickable(
        (
            By.XPATH,
            "//div[.//*[contains(normalize-space(),'Weight') or contains(normalize-space(),'KG')]]"
            "//input[@type='number' or @type='text']"
        )
    )
)
print("✅ Weight page detected")

# Enter Weight
driver.execute_script(
    "arguments[0].scrollIntoView({block:'center'}); arguments[0].click();",
    kg_input
)
kg_input.clear()
kg_input.send_keys("25")
print("✅ Weight entered: 25 KG")

time.sleep(0.5)

# Click Next on Weight page
weight_next_btn = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Next']"))
)
driver.execute_script("arguments[0].click();", weight_next_btn)
print("➡️ Next clicked on Weight page")

# ==================================================
# HEIGHT (CM) PAGE
# ==================================================

# Ensure Weight input is no longer active
wait.until(
    EC.invisibility_of_element_located(
        (
            By.XPATH,
            "//div[.//*[contains(normalize-space(),'Weight') or contains(normalize-space(),'KG')]]"
            "//input"
        )
    )
)

# Wait for Height page
wait.until(
    EC.visibility_of_element_located(
        (By.XPATH, "//*[normalize-space()='Height']")
    )
)
print("✅ Height page detected")

# Locate Height input ONLY
height_input = wait.until(
    EC.element_to_be_clickable(
        (
            By.XPATH,
            "//div[.//*[normalize-space()='Height']]"
            "//input[@type='number' or @type='text']"
        )
    )
)

# Enter Height
driver.execute_script(
    "arguments[0].scrollIntoView({block:'center'}); arguments[0].click();",
    height_input
)
height_input.clear()
height_input.send_keys("35")
print("✅ Height entered: 35 CM")

time.sleep(0.5)

# Click Next on Height page
height_next_btn = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Next']"))
)
driver.execute_script("arguments[0].click();", height_next_btn)
print("➡️ Next clicked on Height page")

# Optional wait to observe next page
time.sleep(3)


# ==================================================
# BLOOD GROUP PAGE (CLEAN)
# ==================================================

# Wait for Blood Group page
wait.until(
    EC.visibility_of_element_located((By.XPATH, "//*[normalize-space()='Blood Group']"))
)
print("✅ Blood Group page loaded")

# Click O+ option (human-like click on visible text)
driver.find_element(By.XPATH, "//*[normalize-space()='O+']").click()
time.sleep(0.3)
print("✅ O+ selected")

# Click Submit button
driver.find_element(By.XPATH, "//button[normalize-space()='Submit']").click()
print("➡️ Submit clicked")


time.sleep(10)  