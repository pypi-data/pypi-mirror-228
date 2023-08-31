import selenium
import selenium.common.exceptions
from selenium.webdriver.common.by import By


class DoesExist:
    def __init__(self, driver):
        self.driver = driver

    def xpath(self, xpath):
        try:
            self.driver.find_element(By.XPATH, xpath)
        except selenium.common.exceptions.NoSuchElementException:
            return False
        return True


class SnapFunctions:
    def __init__(self, driver):
        self.driver = driver

    def activate_camera(self, xpath: str = "/html/body/main/div[1]/div[2]/div/div/div/div/div[1]/div/div/div/div/div/div/div/div/button[1]"):
        # when camera is deactivated activate it
        # try:
        #     self.driver.find_element(By.XPATH, "/html/body/main/div[1]/div[2]/div/div/div/div/div[1]/div/div/div/div/div/div/div/div/button[1]").click()
        # except selenium.common.exceptions.NoSuchElementException:
        #     print("Activate Camera. No such element")

        try:
            self.driver.find_element(By.XPATH, xpath).click()
            return True
        except selenium.common.exceptions.NoSuchElementException:
            print("Activate Camera. No such element")
        except selenium.common.exceptions.ElementNotInteractableException:
            print("Activate Camera. Element not interactable")
        return False

    def take_snap(self, xpath: str = "/html/body/main/div[1]/div[2]/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div[1]/button[1]"):
        # take picture
        try:
            self.driver.find_element(By.XPATH, xpath).click()
            return True
        except selenium.common.exceptions.NoSuchElementException:
            self.activate_camera()
            print("Take Picture. No such element")
        except selenium.common.exceptions.StaleElementReferenceException:
            self.take_snap()
        except selenium.common.exceptions.ElementClickInterceptedException:
            print("Take Picture. Element click intercepted")
        return False

    def press_send_to(self, xpath: str = "/html/body/main/div[1]/div[2]/div/div/div/div/div[1]/div/div/div/div/div[2]/div[2]/button[2]"):
        # Send To (select people)
        try:
            self.driver.find_element(By.XPATH, xpath).click()
            return True
        except selenium.common.exceptions.NoSuchElementException:
            print("Send to. No such element")
        except selenium.common.exceptions.ElementClickInterceptedException:
            # WebDriverWait(self.driver, 20).until(EC.invisibility_of_element((By.XPATH, x_path)))
            # self.press_send_to()
            print("Send to. Element Click intercepted")
        return False

    def select_user_to(self, nickname: str,
                       xpath: str = "/html/body/main/div[1]/div[2]/div/div/div/div/div[1]/div/div/div/div/div[1]/div/form/div/div/div/div/div/input"):
        try:
            self.driver.find_element(By.XPATH, xpath).send_keys(nickname)
            return True
        except selenium.common.exceptions.NoSuchElementException:
            print("Select User To. No such element")
        except selenium.common.exceptions.ElementNotInteractableException:
            print("Select User To. No such element")
        except selenium.common.exceptions.StaleElementReferenceException:
            self.select_user_to(nickname)
        return False

    def select_user(self, nickname: str, recent_position: int = 1):
        # select user to send the snap to

        self.select_user_to(nickname)

        try:
            self.driver.find_element(By.XPATH,
                                     f"/html/body/main/div[1]/div[2]/div/div/div/div/div[1]/div/div/div/div/div[1]/div/form/div/ul/li[{recent_position + 1}]/div").click()
            return True
        except selenium.common.exceptions.NoSuchElementException:
            print("Select User. No such element")
        except selenium.common.exceptions.ElementNotInteractableException:
            print("Select User. Element not intractable")
        except selenium.common.exceptions.StaleElementReferenceException:
            self.select_user(nickname)
        return False

    def send_snap(self, xpath: str = "/html/body/main/div[1]/div[2]/div/div/div/div/div[1]/div/div/div/div/div[1]/div/form/div[2]/button"):
        # send snap
        try:
            self.driver.find_element(By.XPATH, xpath).click()
            return True
        except selenium.common.exceptions.NoSuchElementException:
            print("Send Snap. No such element")
        except selenium.common.exceptions.StaleElementReferenceException:
            print("Send Snap. Stale element reference")
        return False
