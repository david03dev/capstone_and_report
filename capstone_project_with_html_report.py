
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
import pytest

# Locators and Configurations for OrangeHRM
class OrangeHRM_Locators:
    username = "username"
    password = "password"
    submit_button = "//button[@type='submit']"
    url = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
    dashboard_url = "https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index"
    excel_file = "D:\Guvi - Automation testing\Capstone projects\test_data.xlsx"
    sheet_number = "Sheet1"
    pass_data = "TEST PASS"
    fail_data = "TEST FAILED"

# Page Object for Login Page
class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.username_input = (By.NAME, OrangeHRM_Locators.username)
        self.password_input = (By.NAME, OrangeHRM_Locators.password)
        self.login_button = (By.XPATH, OrangeHRM_Locators.submit_button)

    def enter_username(self, username):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.username_input)
            ).send_keys(username)
        except TimeoutException:
            print("Username field not found or took too long to appear.")
        except WebDriverException as e:
            print(f"An error occurred: {str(e)}")

    def enter_password(self, password):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.password_input)
            ).send_keys(password)
        except TimeoutException:
            print("Password field not found or took too long to appear.")
        except WebDriverException as e:
            print(f"An error occurred: {str(e)}")

    def click_login(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.login_button)
            ).click()
        except TimeoutException:
            print("Login button not clickable or took too long to appear.")
        except WebDriverException as e:
            print(f"An error occurred: {str(e)}")

# Page Object for PIM Page
class PIMPage:
    def __init__(self, driver):
        self.driver = driver
        self.pim_menu = (By.ID, "menu_pim_viewPimModule")
        self.add_employee_button = (By.ID, "btnAdd")
        self.first_name_input = (By.ID, "firstName")
        self.last_name_input = (By.ID, "lastName")
        self.save_button = (By.ID, "btnSave")
        self.edit_employee_button = (By.ID, "btnEdit")
        self.delete_employee_button = (By.ID, "btnDelete")
        self.confirm_delete_button = (By.ID, "dialogDeleteBtn")

    def go_to_pim(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.pim_menu)
            ).click()
        except TimeoutException:
            print("PIM menu not clickable or took too long to appear.")
        except WebDriverException as e:
            print(f"An error occurred: {str(e)}")

    def add_employee(self, first_name, last_name):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.add_employee_button)
            ).click()

            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.first_name_input)
            ).send_keys(first_name)

            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.last_name_input)
            ).send_keys(last_name)

            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.save_button)
            ).click()
        except TimeoutException:
            print("Employee form took too long to load or the button is not clickable.")
        except WebDriverException as e:
            print(f"An error occurred: {str(e)}")

    def edit_employee(self, first_name, last_name):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.edit_employee_button)
            ).click()

            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.first_name_input)
            ).clear()
            self.driver.find_element(*self.first_name_input).send_keys(first_name)

            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.last_name_input)
            ).clear()
            self.driver.find_element(*self.last_name_input).send_keys(last_name)

            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.save_button)
            ).click()
        except TimeoutException:
            print("Edit form took too long to load.")
        except WebDriverException as e:
            print(f"An error occurred: {str(e)}")

    def delete_employee(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.delete_employee_button)
            ).click()

            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.confirm_delete_button)
            ).click()
        except TimeoutException:
            print("Delete button not clickable or took too long to appear.")
        except WebDriverException as e:
            print(f"An error occurred: {str(e)}")

# Test cases for OrangeHRM using pytest
@pytest.fixture(scope="function")
def setup():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(OrangeHRM_Locators.url)
    yield driver
    driver.quit()

def test_valid_login(setup):
    driver = setup
    login = LoginPage(driver)
    login.enter_username("Admin")
    login.enter_password("admin123")
    login.click_login()
    WebDriverWait(driver, 10).until(EC.url_contains(OrangeHRM_Locators.dashboard_url))
    assert "dashboard" in driver.current_url

def test_invalid_login(setup):
    driver = setup
    login = LoginPage(driver)
    login.enter_username("Admin")
    login.enter_password("InvalidPassword")
    login.click_login()
    error_message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//p[contains(text(),'Invalid credentials')]"))
    ).text
    assert error_message == "Invalid credentials"

def test_add_employee(setup):
    driver = setup
    login = LoginPage(driver)
    login.enter_username("Admin")
    login.enter_password("admin123")
    login.click_login()
    pim = PIMPage(driver)
    pim.go_to_pim()
    pim.add_employee("David", "Selvaraj")
    success_message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@class='message success fadable']"))
    ).text
    assert "Successfully Saved" in success_message

def test_edit_employee(setup):
    driver = setup
    login = LoginPage(driver)
    login.enter_username("Admin")
    login.enter_password("admin123")
    login.click_login()
    pim = PIMPage(driver)
    pim.go_to_pim()
    pim.edit_employee("John", "Doe")
    # Add assertion to check if employee edit was successful

def test_delete_employee(setup):
    driver = setup
    login = LoginPage(driver)
    login.enter_username("Admin")
    login.enter_password("admin123")
    login.click_login()
    pim = PIMPage(driver)
    pim.go_to_pim()
    pim.delete_employee()
    # Add assertion to check if employee was deleted successfully

if __name__ == "__main__":
    pytest.main(["--html=report.html", "--self-contained-html"])
