from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time

# --------------------------------------------------
# CHROME SETUP
# --------------------------------------------------
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)
wait = WebDriverWait(driver, 30)

# --------------------------------------------------
# LOGIN PAGE
# --------------------------------------------------
driver.get("https://dev2.scanbo.com/authentication/login")

wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='tel']"))).send_keys("7878784344")

# STEP 3: CLICK DISCLAIMER CHECKBOX
# --------------------------------------------------
label = wait.until(
    EC.element_to_be_clickable((
        By.XPATH,
        "//label[contains(.,'Disclaimer') or contains(.,'agree')]"
    ))
)
driver.execute_script("arguments[0].click();", label)
print("Disclaimer clicked")

# --------------------------------------------------
# STEP 4: WAIT FOR DISCLAIMER POPUP
# --------------------------------------------------
popup = wait.until(
    EC.presence_of_element_located((
        By.XPATH, "//div[@role='dialog' or contains(@class,'modal')]"
    ))
)
print("Disclaimer popup opened")

# --------------------------------------------------
# STEP 5: SCROLL DISCLAIMER
# --------------------------------------------------
scrollable = driver.execute_script("""
let modal = arguments[0];
for (let el of modal.querySelectorAll('*')) {
  if (el.scrollHeight > el.clientHeight) return el;
}
return null;
""", popup)

driver.execute_script("""
let el = arguments[0];
let y = 0;
let timer = setInterval(() => {
  el.scrollTop = y;
  el.dispatchEvent(new Event('scroll'));
  y += 150;
  if (y >= el.scrollHeight) {
    clearInterval(timer);
    el.scrollTop = el.scrollHeight;
    el.dispatchEvent(new Event('scroll'));
  }
}, 80);
""", scrollable)

time.sleep(1)
print("Disclaimer scrolled")

# --------------------------------------------------
# STEP 6: CLICK AGREE
# --------------------------------------------------
agree = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Agree')]"))
)
driver.execute_script("arguments[0].click();", agree)
print("Agree clicked")

# --------------------------------------------------
send_otp = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Send')]")))
driver.execute_script("arguments[0].click();", send_otp)
print("Send OTP clicked")

# ---------- WAIT FOR PAGE TRANSITION ----------
time.sleep(3)  # React route change safety

# ---------- RE-BIND ACTIVE WINDOW ----------
driver.switch_to.window(driver.window_handles[-1])
#wait.until(
EC.presence_of_element_located(
        (By.XPATH, "//*[contains(text(),'6 Digit Code') or contains(text(),'OTP')]")
    )

print("OTP screen loaded")

# ---------- FIND OTP BOXES (ROBUST) ----------
otp_inputs = wait.until(
    EC.presence_of_all_elements_located(
        (By.XPATH, "//input[@inputmode='numeric' or @maxlength='1']")
    )
)

print("OTP boxes found:", len(otp_inputs))

# ---------- ENTER OTP ----------
OTP = "654320"   # test OTP

for i, box in enumerate(otp_inputs):
    box.clear()
    box.send_keys(OTP[i])

print("OTP entered automatically")

# ---------- VERIFY ----------
verify_btn = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Verify')]"))
)
driver.execute_script("arguments[0].click();", verify_btn)
print("Verify clicked")
#------------------------------------------------------
# --------------------------------------------------
# CHECK: EXISTING USER OR NEW USER
# --------------------------------------------------
time.sleep(2)  # allow React route decision

try:
    # DASHBOARD DETECTION (existing user)
    WebDriverWait(driver, 8).until(
        EC.any_of(
            EC.url_contains("dashboard"),
            EC.presence_of_element_located((By.XPATH, "//aside")),
            EC.presence_of_element_located((By.XPATH, "//header")),
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Logout')]"))
        )
    )
    print(" Existing user detected  Dashboard opened")
    # STOP REGISTRATION FLOW
    time.sleep(5)
    driver.quit()
    exit()

except TimeoutException:
    print(" New user detected  Continue registration flow")



# --------------------------------------------------
# I AM PAGE → SELECT DOCTOR
# --------------------------------------------------
doctor_card = wait.until(EC.element_to_be_clickable(
    (By.XPATH, "//*[contains(text(),'Doctor')]")
))
doctor_card.click()

wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Next')]"))).click()
print("Doctor profile selected")

# --------------------------------------------------
# STEP 1: DOCTOR PROFILE
# --------------------------------------------------
FIRST_NAME = "scanbo"
LAST_NAME = "new test"
first_name = wait.until(
    EC.visibility_of_element_located(
        (By.XPATH, "//input[@placeholder='First Name*' or contains(@placeholder,'First')]")
    )
)

first_name.clear()
first_name.send_keys(FIRST_NAME)

print("First Name filled automatically:", FIRST_NAME)
last_name = wait.until(
    EC.visibility_of_element_located(
        (By.XPATH, "//input[@placeholder='Last Name*' or contains(@placeholder,'Last')]")
    )
)

last_name.clear()
last_name.send_keys(LAST_NAME)

print("Last Name filled automatically:", LAST_NAME)

 



# Add Qualification
#driver.find_element(By.XPATH, "//button[contains(text(),'Add')]").click()
#wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder,'Qualification')]"))).send_keys("MBBS")
#driver.find_element(By.XPATH, "//input[contains(@placeholder,'YYYY')]").send_keys("2020")
#driver.find_element(By.XPATH, "//input[contains(@placeholder,'Issuer')]").send_keys("Medical Council")
#driver.find_element(By.XPATH, "//button[contains(text(),'Save')]").click()

#driver.find_element(By.XPATH, "//input[contains(@placeholder,'Medical')]").send_keys("MED12345")
#driver.find_element(By.XPATH, "//input[contains(@placeholder,'Experience')]").send_keys("5")

#driver.find_element(By.XPATH, "//button[contains(text(),'Next')]").click()
#print("Doctor Profile completed")
QUALIFICATION = "MBBS"
COMPLETION_MONTH = "January"
COMPLETION_YEAR = "2003"
ISSUER = "Medical Certificate"
add_btn = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Add']"))
)
driver.execute_script("arguments[0].click();", add_btn)
print("Add button clicked")
popup = wait.until(
    EC.visibility_of_element_located((By.XPATH, "//div[@role='dialog']"))
)

time.sleep(1.5)  # React animation settle
print("Qualification popup visible")

popup_inputs = wait.until(
    lambda d: popup.find_elements(By.XPATH, ".//input")
)

print("Popup inputs loaded:", len(popup_inputs))

actions = ActionChains(driver)

# --------------------------------------------------
# WAIT FOR QUALIFICATION POPUP INPUTS
# --------------------------------------------------
popup_inputs = wait.until(
    EC.presence_of_all_elements_located(
        (By.XPATH, "//div[@role='dialog']//input")
    )
)

print("Popup inputs loaded:", len(popup_inputs))

# --------------------------------------------------
#  QUALIFICATION
# --------------------------------------------------
popup_inputs[0].click()
popup_inputs[0].clear()
popup_inputs[0].send_keys(QUALIFICATION)
time.sleep(1)

# --------------------------------------------------
#  COMPLETION DATE (MONTH + YEAR) — CALENDAR SAFE
# --------------------------------------------------
# --------------------------------------------------
# YEAR OF COMPLETION (MONTH + YEAR) — REACT SAFE
# --------------------------------------------------
# --------------------------------------------------
# YEAR OF COMPLETION — UI SELECTION (REACT SAFE)
# --------------------------------------------------

#  Open calendar

# --------------------------------------------------
# YEAR OF COMPLETION — KEYBOARD SAFE (WORKING)
# --------------------------------------------------

completion_input = wait.until(
    EC.element_to_be_clickable((
        By.XPATH, "//input[contains(@placeholder,'YYYY')]"
    ))
)

completion_input.click()
time.sleep(0.5)

# CLEAR PROPERLY
completion_input.send_keys(Keys.CONTROL, "a")
completion_input.send_keys(Keys.BACKSPACE)
time.sleep(0.5)

# TYPE MONTH + YEAR EXACT FORMAT
completion_input.send_keys(COMPLETION_MONTH)
time.sleep(0.3)
completion_input.send_keys(" ")
completion_input.send_keys(COMPLETION_YEAR)

#  VERY IMPORTANT — LOCK VALUE
completion_input.send_keys(Keys.TAB)

time.sleep(1)

print("Month & Year entered and locked:", COMPLETION_MONTH, COMPLETION_YEAR)



# --------------------------------------------------
#  ISSUER
# --------------------------------------------------
popup_inputs[2].click()
popup_inputs[2].clear()
popup_inputs[2].send_keys(ISSUER)
time.sleep(1)

# --------------------------------------------------
# SAVE QUALIFICATION
# --------------------------------------------------
save_btn = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(text(),'Save')]")
    )
)
driver.execute_script("arguments[0].click();", save_btn)

print(" Qualification saved automatically")
MEDICAL_REG_NO = "MED123456"
EXPERIENCE_YEARS = "5"
# --------------------------------------------------
# MEDICAL REGISTRATION NUMBER
# --------------------------------------------------
med_reg_input = wait.until(
    EC.element_to_be_clickable((
        By.XPATH,
        "//input[contains(@placeholder,'Medical') or contains(@name,'registration')]"
    ))
)

med_reg_input.click()
time.sleep(0.3)
med_reg_input.send_keys(Keys.CONTROL, "a")
med_reg_input.send_keys(Keys.BACKSPACE)
med_reg_input.send_keys(MEDICAL_REG_NO)
med_reg_input.send_keys(Keys.TAB)

time.sleep(0.5)
print("Medical Registration Number entered:", MEDICAL_REG_NO)

# --------------------------------------------------
# EXPERIENCE (IN YEARS)
# --------------------------------------------------
experience_input = wait.until(
    EC.element_to_be_clickable((
        By.XPATH,
        "//input[contains(@placeholder,'Experience') or contains(@name,'experience')]"
    ))
)

experience_input.click()
time.sleep(0.3)
experience_input.send_keys(Keys.CONTROL, "a")
experience_input.send_keys(Keys.BACKSPACE)
experience_input.send_keys(EXPERIENCE_YEARS)
experience_input.send_keys(Keys.TAB)

time.sleep(0.5)
print("Experience entered:", EXPERIENCE_YEARS, "years")
# --------------------------------------------------
# CLICK NEXT BUTTON (AFTER EXPERIENCE)
# --------------------------------------------------
next_btn = wait.until(
    EC.element_to_be_clickable((
        By.XPATH, "//button[normalize-space()='Next']"
    ))
)

driver.execute_script("arguments[0].scrollIntoView({block:'center'});", next_btn)
time.sleep(0.5)

driver.execute_script("arguments[0].click();", next_btn)
print("Next button clicked successfully")


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
DOB_VALUE = "22/12/1990"   # DD/MM/YYYY format


# --------------------------------------------------
# DATE OF BIRTH
# --------------------------------------------------

# --------------------------------------------------
# DOB INPUT (AUTO → AGE AUTO UPDATE)
# --------------------------------------------------
# --------------------------------------------------
# DOB (REACT SAFE — AUTO AGE)
# --------------------------------------------------
#AGE_VALUE = "25"
#   EC.element_to_be_clickable((
 #       By.XPATH,
  #      "//label[contains(text(),'Age')]/following::input[1]"
    #))
#)

#age_input.click()
#time.sleep(0.5)

#ge_input.send_keys(Keys.CONTROL + "a")
#age_input.send_keys(Keys.BACKSPACE)

# Slow typing (important)
#for ch in AGE_VALUE:
 #   age_input.send_keys(ch)
  #  time.sleep(0.2)

# Force React state update
#driver.execute_script("""
#arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
#arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
#arguments[0].blur();
#""", age_input)

#print("Age entered:", AGE_VALUE)
#time.sleep(2)
#dob_input = wait.until(
#    EC.presence_of_element_located((
 #       By.XPATH,
  #      "//label[contains(text(),'Birth')]/following::input[1]"
   # ))
#)

#dob_value = dob_input.get_attribute("value")
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
#time.sleep(2)

#next_btn = wait.until(
 #   EC.presence_of_element_located((
  #      By.XPATH, "//button[normalize-space()='Next']"
   # ))
#)

#driver.execute_script("""
#arguments[0].scrollIntoView({block:'center'});
#arguments[0].disabled = false;
#arguments[0].removeAttribute('disabled');
#arguments[0].click();
#""", next_btn)

#print("Next button clicked automatically – moved to Address page")

next_btn = wait.until(
    EC.element_to_be_clickable((
        By.XPATH, "//button[normalize-space()='Next']"
    ))
)

driver.execute_script("arguments[0].click();", next_btn)
print("Next button clicked after Age ")


# --------------------------------------------------
# STEP 4: ADDRESS
# --------------------------------------------------
#wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Select Address')]"))).click()
#wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Clinic')]"))).click()

#driver.find_element(By.XPATH, "//input[contains(@placeholder,'Zip')]").send_keys("560001")
#driver.find_element(By.XPATH, "//input[contains(@placeholder,'Address 1')]").send_keys("Automation Clinic Address")

#driver.find_element(By.XPATH, "//button[contains(text(),'Submit')]").click()
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








# --------------------------------------------------
# SUCCESS
# --------------------------------------------------
wait.until(EC.presence_of_element_located(
    (By.XPATH, "//*[contains(text(),'Success') or contains(text(),'Dashboard')]")
))

print(" DOCTOR REGISTRATION COMPLETED")
time.sleep(10)
