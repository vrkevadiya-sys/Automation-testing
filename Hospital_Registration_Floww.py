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

wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='tel']"))).send_keys("1122668878")

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
# I AM PAGE → SELECT hospital
# --------------------------------------------------
hospital_card = wait.until(EC.element_to_be_clickable(
    (By.XPATH, "//*[contains(text(),'Hospital')]")
))
hospital_card.click()

wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Next')]"))).click()
print("hospital profile selected")

# --------------------------------------------------
# STEP 1: HOSPITAL PROFILE
# --------------------------------------------------
HOSPITAL_NAME = "General Kalyan Hospital"
HOSPITAL_TYPE = "Specialty Hospitals"
HOSPITAL_REG_NO = "HOS1234"
GST_NO = "22AASDA0000A1Z5"
CONTACT_PERSON = "Scanbo test"
MOBILE_NO = "9765432134"
EMAIL = "scanbo@gmail.com"
#--------------------------------
def react_input(element, value):
    driver.execute_script("""
    let input = arguments[0];
    let value = arguments[1];
    input.focus();
    let setter = Object.getOwnPropertyDescriptor(
        window.HTMLInputElement.prototype, 'value'
    ).set;
    setter.call(input, value);
    input.dispatchEvent(new Event('input', { bubbles: true }));
    input.dispatchEvent(new Event('change', { bubbles: true }));
    input.dispatchEvent(new Event('blur', { bubbles: true }));
    """, element, value)
#---Hospital name -----------
hospital_name_input = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Hospital Name*']"))
)
react_input(hospital_name_input, HOSPITAL_NAME)
print("Hospital name entered")

#-------Select the hospital type ----------
hospital_type_select = wait.until(
    EC.presence_of_element_located((
        By.XPATH,
        "//div[contains(@class,'MuiSelect')]"
    ))
)

driver.execute_script("""
const el = arguments[0];
el.scrollIntoView({block:'center'});

// Real mouse sequence (MUI required)
['mousedown','mouseup','click'].forEach(type => {
  el.dispatchEvent(new MouseEvent(type, {
    view: window,
    bubbles: true,
    cancelable: true
  }));
});
""", hospital_type_select)

print("Hospital Type dropdown force-opened")
Specialty_option = WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((
        By.XPATH,
        "//li[normalize-space()='Specialty Hospitals']"
    ))
)
driver.execute_script("""
arguments[0].scrollIntoView({block:'center'});
arguments[0].click();
""", Specialty_option)

print("Hospital Type selected automatically")



#-------Hospital registration number-------------
reg_no_input = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Hospital Registration Number*']"))
)
react_input(reg_no_input, HOSPITAL_REG_NO)
print("Hospital registration number entered")



#----------Hospitla GST number---------------------
gst_input = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//input[contains(@placeholder,'GST')]"))
)
react_input(gst_input, GST_NO)
print("GST entered")

#----------Hospital Contact person name----------
contact_name_input = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Contact Person Name*']"))
)
react_input(contact_name_input, CONTACT_PERSON)
print("Contact person entered")

#----------Hospital contact mobile number------------------
mobile_input = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//input[@type='tel']"))
)

mobile_input.click()
mobile_input.send_keys(Keys.CONTROL, "a")
mobile_input.send_keys(Keys.BACKSPACE)

for digit in MOBILE_NO:
    mobile_input.send_keys(digit)
    time.sleep(0.2)

print("Mobile number entered")

#-------------hospital Email number-------------
email_input = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Contact Email Address*']"))
)
react_input(email_input, EMAIL)
print("Email entered")

#------------next button --------------
next_btn = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Next']"))
)

driver.execute_script("""
arguments[0].scrollIntoView({block:'center'});
arguments[0].click();
""", next_btn)

print("Hospital registration page completed Next clicked")


# --------------------------------------------------
# STEP 4: ADDRESS
# --------------------------------------------------
#wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Select Address')]"))).click()
#wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Clinic')]"))).click()

#driver.find_element(By.XPATH, "//input[contains(@placeholder,'Zip')]").send_keys("560001")
#driver.find_element(By.XPATH, "//input[contains(@placeholder,'Address 1')]").send_keys("Automation Clinic Address")

#driver.find_element(By.XPATH, "//button[contains(text(),'Submit')]").click()


ZIPCODE = "395009"
ADDRESS1 = "Surat, Mota Varaccha"


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
#wait.until(EC.presence_of_element_located(
 #   (By.XPATH, "//*[contains(text(),'Success') or contains(text(),'Dashboard')]")
#))

#print(" Hospital REGISTRATION COMPLETED")
#time.sleep(10)




print("Checking account activation status...")

# Give backend time to decide status
time.sleep(3)

# ---------- CASE 1: ACTIVE (Dashboard) ----------
if (
    "dashboard" in driver.current_url.lower()
    or driver.find_elements(By.XPATH, "//aside")
    or driver.find_elements(By.XPATH, "//header")
    or driver.find_elements(By.XPATH, "//*[contains(text(),'Logout')]")
):
    print("Hospital account ACTIVE  Dashboard opened")
    time.sleep(5)
    # continue automation here if needed

# ---------- CASE 2: INACTIVE / PENDING ----------
else:
    status_elements = driver.find_elements(
        By.XPATH,
        "//*[contains(text(),'Pending') or "
        "contains(text(),'Approval') or "
        "contains(text(),'Under Review') or "
        "contains(text(),'not active') or "
        "contains(text(),'Contact Admin')]"
    )

    if status_elements:
        print(" Hospital account NOT ACTIVE")
        print("Status message:", status_elements[0].text)
    else:
        print(" Account status unknown (no dashboard, no message)")

    time.sleep(5)
    driver.quit()
    exit()