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
driver.get("https://dev2.scanbo.com/authentication/login")

wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='tel']"))).send_keys("8787646453")

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

# --------------------------------------------------
# SELECT CHW ROLE
# --------------------------------------------------
chw_card = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "//*[contains(text(),'Community') or contains(text(),'CHW')]")
    )
)
driver.execute_script("arguments[0].click();", chw_card)
print("CHW role selected")

# --------------------------------------------------
# WAIT FOR CHW REGISTRATION FORM
# --------------------------------------------------
wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//input | //select | //textarea")
    )
)
print("CHW Registration form loaded")

# --------------------------------------------------
# FILL CHW REGISTRATION FORM 
# --------------------------------------------------


first_name = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//input[contains(@placeholder,'First')]")
    )
)
first_name.clear()
first_name.send_keys("Test")

last_name = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//input[contains(@placeholder,'Last')]")
    )
)
last_name.clear()
last_name.send_keys("CHW")

# --------------------------------------------------
# CLICK ADD BUTTON (QUALIFICATION)
# --------------------------------------------------
add_btn = wait.until(
    EC.element_to_be_clickable((
        By.XPATH, "//button[normalize-space()='Add']"
    ))
)
driver.execute_script("arguments[0].click();", add_btn)
print("Add button clicked")

# --------------------------------------------------
# WAIT FOR QUALIFICATION POPUP
# --------------------------------------------------
qualification_popup = wait.until(
    EC.presence_of_element_located((
        By.XPATH, "//div[@role='dialog' or contains(@class,'modal')]"
    ))
)
print("Qualification popup opened")

qualification_input = qualification_popup.find_element(
    By.XPATH,
    ".//label[contains(text(),'Qualification')]/following::input[1]"
)
qualification_input.clear()
qualification_input.send_keys("ANM")
print("Qualification entered")

#qualification caleder
year_input = qualification_popup.find_element(
    By.XPATH,
    ".//label[contains(text(),'Year of Completion')]/following::input[1]"
)

driver.execute_script("""
const input = arguments[0];
const nativeSetter = Object.getOwnPropertyDescriptor(
    window.HTMLInputElement.prototype, 'value'
).set;

nativeSetter.call(input, 'December 2020');

input.dispatchEvent(new Event('input', { bubbles: true }));
input.dispatchEvent(new Event('change', { bubbles: true }));
""", year_input)

print("Year of Completion displayed as December 2020")


# issuer field
issuer_input = qualification_popup.find_element(
    By.XPATH,
    ".//label[contains(text(),'Issuer')]/following::input[1]"
)

driver.execute_script("document.activeElement.blur();")
issuer_input.clear()
issuer_input.send_keys("State Medical Board")
print("Issuer entered")


# Wait for the Save button inside the qualification popup
save_button = qualification_popup.find_element(
    By.XPATH, ".//button[contains(., 'Save') or contains(@class,'save')]"
)

# Make sure the button is clickable and click it
wait.until(EC.element_to_be_clickable(save_button))
driver.execute_script("arguments[0].click();", save_button)
print("Save button clicked")

# Wait for the popup to close
wait.until(EC.invisibility_of_element(qualification_popup))
print("Qualification popup closed and data saved")

Registration= wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//input[contains(@placeholder,'Registration')]")
    )
)
Registration.clear()
Registration.send_keys("123456")



# --------------------------------------------------
# CLICK "Are you working with any organization?" TOGGLE
# --------------------------------------------------

org_toggle = wait.until(
    EC.presence_of_element_located((
        By.CSS_SELECTOR,
        "input.MuiSwitch-input"
    ))
)

driver.execute_script("arguments[0].scrollIntoView({block:'center'});", org_toggle)

# Click via JS (input is hidden)
driver.execute_script("arguments[0].click();", org_toggle)

print("Organization toggle clicked")

add_org_popup = wait.until(
    EC.visibility_of_element_located((
        By.XPATH,
        "//div[@role='dialog' and .//*[contains(text(),'Organization')]]"
    ))
)

print("Add Organization popup opened")

# Fill Organization Form 

inputs = wait.until(
    EC.presence_of_all_elements_located((
        By.CSS_SELECTOR,
        "div[role='dialog'] input"
    ))
)

print("Total inputs found in popup:", len(inputs))

# Organization popup always has:
# 0 = Organization Name
# 1 = Registration Number


org_name = inputs[0]
reg_no = inputs[1]

# Scroll & fill
driver.execute_script("arguments[0].scrollIntoView({block:'center'});", org_name)

org_name.clear()
org_name.send_keys("smily")

reg_no.clear()
reg_no.send_keys("12345")

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


print("Organization details entered")

# --------------------------------------------------
# Fill Contact Person Name, Contact, and Email
# --------------------------------------------------

CONTACT_PERSON = "Nilam"
CONTACT_NO = "9876543210"
EMAIL = "nilam@example.com"

# Contact Person Name
contact_input = wait.until(
    EC.presence_of_element_located((
        By.XPATH, "//input[contains(@placeholder,'Contact Person') or @name='contactPerson']"
    ))
)
contact_input.clear()
contact_input.send_keys(CONTACT_PERSON)

# Contact Number
contact_no_input = wait.until(
    EC.presence_of_element_located((
        By.XPATH, "//input[@type='tel' or @name='contactNumber']"
    ))
)
contact_no_input.clear()
contact_no_input.send_keys("9999999999")
print("Contact number entered")

# Email Address
email_input = wait.until(
    EC.presence_of_element_located((
        By.XPATH, "//input[contains(@placeholder,'Email') or @name='email']"
    ))
)
email_input.clear()
email_input.send_keys(EMAIL)

print("Contact person, number, and email entered")

ORG_TYPE = "Private"  # or "Government"

# --------------------------------------------------
# Click on the dropdown
# --------------------------------------------------
org_type_dropdown = wait.until(
    EC.element_to_be_clickable((
        By.XPATH, "//label[contains(text(),'Select Organization Type')]/following-sibling::div"
    ))
)
org_type_dropdown.click()
print("Organization Type dropdown clicked/opened")

# --------------------------------------------------
# Wait a short time for React/MUI options to render
# --------------------------------------------------
time.sleep(0.5)  

# --------------------------------------------------
# Locate the option 
# --------------------------------------------------
org_option = wait.until(
    EC.presence_of_element_located((
        By.XPATH, f"//li[contains(@class,'MuiMenuItem') and normalize-space(text())='{ORG_TYPE}']"
    ))
)

# --------------------------------------------------
# Click using JavaScript 
# --------------------------------------------------
driver.execute_script("arguments[0].scrollIntoView(true); arguments[0].click();", org_option)
print(f"Organization Type selected as {ORG_TYPE}")

ENTITY_TYPE = "For-Profit"  # or "Non-Profit"

# --------------------------------------------------
# Click on the dropdown
# --------------------------------------------------
entity_type_dropdown = wait.until(
    EC.element_to_be_clickable((
        By.XPATH, "//label[contains(text(),'Select Entity Type')]/following-sibling::div"
    ))
)
entity_type_dropdown.click()
print("Entity Type dropdown clicked/opened")

# --------------------------------------------------
# Wait a short time 
# --------------------------------------------------
time.sleep(0.5)  # small delay 

# --------------------------------------------------
# Locate the option globally (React portal)
# --------------------------------------------------
entity_option = wait.until(
    EC.presence_of_element_located((
        By.XPATH, f"//li[contains(@class,'MuiMenuItem') and normalize-space(text())='{ENTITY_TYPE}']"
    ))
)

# --------------------------------------------------
# Click using JavaScript 
# --------------------------------------------------
driver.execute_script("arguments[0].scrollIntoView(true); arguments[0].click();", entity_option)
print(f"Entity Type selected as {ENTITY_TYPE}")


# --------------------------------------------------
# Wait until the Save button is clickable
# --------------------------------------------------
save_btn = wait.until(
    EC.element_to_be_clickable((
        By.XPATH, "//button[normalize-space()='Save']"
    ))
)

# --------------------------------------------------
# Scroll into view and click using JavaScript 
# --------------------------------------------------
driver.execute_script("arguments[0].scrollIntoView(true); arguments[0].click();", save_btn)
print("Save button clicked, all information submitted.")

# Wait for the Next button to be present and clickable
next_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Next')]"))
)

# Click using JS to avoid overlay/animation issues
driver.execute_script("arguments[0].click();", next_button)
print("Next button clicked")


# Gender selection page 
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
# AGE FIELD 
# --------------------------------------------------

age_input = wait.until(
    EC.visibility_of_element_located((
        By.XPATH, "//label[text()='Age']/following-sibling::div//input"
    ))
)
driver.execute_script("arguments[0].scrollIntoView(true);", age_input)
age_input.click()
age_input.clear()
age_input.send_keys("29")

print(" Age entered successfully")

next_btn = wait.until(
    EC.element_to_be_clickable((
        By.XPATH, "//button[normalize-space()='Next']"
    ))
)
driver.execute_script("arguments[0].click();", next_btn)
print("Next button clicked after age selection")

#Address page
Select_ADDRESS_TYPE = "Primary"
ZIPCODE = "395009"
ADDRESS1 = "Surat, Mota Varaccha"
wait.until(
    EC.presence_of_element_located((
        By.XPATH, "//h2[contains(text(),'Clinic Address')] | //button[normalize-space()='Submit']"
    ))
)
print("Clinic Address page loaded")
address_type_dropdown = wait.until(
    EC.element_to_be_clickable((
        By.XPATH, "//div[contains(@class,'MuiSelect') or contains(@class,'select')]"
    ))
)
driver.execute_script("arguments[0].click();", address_type_dropdown)
print("Address type dropdown opened")
# WAIT FOR DROPDOWN OPTIONS TO RENDER
# --------------------------------------------------
# ADDRESS TYPE — FORCE OPEN DROPDOWN (MUI SAFE)
# --------------------------------------------------
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
submit = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Submit')]"))
)
driver.execute_script("arguments[0].click();", submit)
print(" REGISTRATION COMPLETED SUCCESSFULLY")


time.sleep(10)
