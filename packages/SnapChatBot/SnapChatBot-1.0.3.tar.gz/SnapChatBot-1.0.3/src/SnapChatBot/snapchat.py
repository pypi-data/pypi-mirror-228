import os
import time
import shutil
import getpass
import threading
from queue import Queue

import selenium
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .snapfunctions import SnapFunctions, DoesExist
from .exceptions import ExitFunctionException


class SnapChat:
    def __init__(self):
        self.driver_list = []
        self.url = "https://web.snapchat.com"
        self.login_url = "https://accounts.snapchat.com/accounts/v2/login"

        self.root_path = os.path.join(os.getcwd(), "ChromeSaves")

        os.makedirs(self.root_path, exist_ok=True)

    def run(self, account_count: int = 1):  # , check_accounts: bool = True):
        # if check_accounts:
        account_list = self.check_accounts()
        # else:
        #     # if account_list is None:
        #     account_list = ["kochluca-1"]  # TODO: add list enter support for the argparse

        if len(account_list) < account_count:
            print(f"You do not have enough accounts. You have {len(account_list)} account/s. You want to launch {account_count} account/s.")
            account_count = len(account_list)

        thread_list = []
        is_running = True

        queue = Queue()
        lock = threading.Lock()

        for _ in range(account_count):
            username = account_list[0]
            account_list.pop(0)

            thread = threading.Thread(name=username, target=self._open_account,
                                      args=(webdriver.Chrome(options=self.get_chrome_options(username)), is_running, queue, lock))
            thread.daemon = True
            thread.start()

            thread_list.append(thread)

        thread_count_list = {}

        while is_running:
            value_dict = dict(queue.get())
            thread_count_list[list(value_dict.keys())[0]] = list(value_dict.values())[0]

            string = ""
            for key, value in thread_count_list.items():
                string += f"{key}: {value} - "
            string = string[:-3]

            # print(f"\nvalue-dict: {value_dict}\nthread-count-list: {thread_count_list}\nstring: {string}\n", end="\r")
            # print(string, end="\r")
            print(string)

        # at the end
        for thread in thread_list:
            thread.join()

    def _open_account(self, driver: webdriver.Chrome, is_running: bool, queue: Queue, lock: threading.Lock):
        while is_running:
            driver.get(self.url)
            WebDriverWait(driver, 10).until(EC.url_contains(self.url))

            snap_functions = SnapFunctions(driver)
            does_exist = DoesExist(driver)

            snap_score = 0
            loop_list = []

            # TODO: make the function more efficient
            while snap_score < 999 and is_running:
                fail_safe = False

                took_snap = False
                pressed_sent_to = False
                is_user_selected = False
                sent_snap = False

                loop_count = 0

                while is_running:  # not sendSnap
                    loop_count += 1
                    # with lock:
                    #     print(loop_count, end="\r")
                    if does_exist.xpath("/html/body/main/div[1]/div[2]/div/div/div/div/div[1]/div/div/div/div/div/div/div/div/button[1]") or fail_safe:
                        # Camera SVG (means camera is deactivated)
                        snap_functions.activate_camera()

                    if not took_snap and does_exist.xpath("/html/body/main/div[1]/div[2]/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div[1]/button[1]") or fail_safe:
                        # Take Snap Button
                        took_snap = snap_functions.take_snap()

                    if took_snap and not pressed_sent_to and does_exist.xpath("/html/body/main/div[1]/div[2]/div/div/div/div/div[1]/div/div/div/div/div[2]/div["
                                                                              "2]/button[2]") or fail_safe:
                        # Send To Button
                        pressed_sent_to = snap_functions.press_send_to()

                    if pressed_sent_to and not is_user_selected and does_exist.xpath("/html/body/main/div[1]/div[2]/div/div/div/div/div[1]/div/div/div/div/div["
                                                                                     "1]/div/form") or fail_safe:
                        # Select User - form

                        # check if already something was entered in the input
                        xpath = "/html/body/main/div[1]/div[2]/div/div/div/div/div[1]/div/div/div/div/div[1]/div/form/div/div[1]/div/div/div/svg"
                        xpath = "/html/body/main/div[1]/div[2]/div/div/div/div/div[1]/div/div/div/div/div[1]/div/form/div/div/div/div/div/svg"
                        # TODO: add a select_user_reset function to reset the input where you enter the name
                        if does_exist.xpath(xpath):
                            driver.find_element(By.XPATH, xpath).click()

                        is_user_selected = snap_functions.select_user("Luca Koch")

                    if is_user_selected and not sent_snap and does_exist.xpath("/html/body/main/div[1]/div[2]/div/div/div/div/div[1]/div/div/div/div/div["
                                                                               "1]/div/form/div[2]/button") or fail_safe:
                        # Send Snap to selected User button
                        sent_snap = snap_functions.send_snap()

                        if sent_snap:
                            snap_score += 1
                            # with lock:
                            #     print(f"{threading.current_thread().name} - {snap_score}")

                            loop_list.append(loop_count)

                            queue.put({threading.current_thread().name: snap_score})
                            break

                    if len(loop_list) > 0:

                        total_count = 0
                        for count in loop_list:
                            total_count += count

                        average_loop_count = round(total_count / len(loop_list), 2)

                        if loop_count > average_loop_count * 2:
                            fail_safe = True

    def add_account(self):
        username = input("Enter the username of the account: ")

        # check if account session already exists
        if username in self.list_root_path():
            while True:
                print(f"Session for username: \"{username}\" already got a session")
                response = input("Do you want to continue (Y/n)")
                if response.lower() == "y":
                    break
                elif response.lower() == "n":
                    raise ExitFunctionException

        # password = input ("Enter the password of the account: ")
        password = getpass.getpass("Enter the password of the account: ")

        driver = webdriver.Chrome(options=self.get_chrome_options(username))
        driver.get(self.login_url)
        WebDriverWait(driver, 10).until(EC.url_contains(self.login_url))

        time.sleep(0.5)

        try:
            # accept cookies
            driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[4]/div/section/div/section/div[2]/div/div/div/div[3]/button[2]").click()
        except selenium.common.exceptions.NoSuchElementException:
            print("No cookies were found")

        # enter username
        driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[3]/article/div[1]/div[3]/form/div[1]/input").send_keys(username)

        # wait for bot detection
        time.sleep(1)

        # click the Enter button
        driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[3]/article/div[1]/div[3]/form/div[3]/button").click()

        # TODO: maybe automate the anti robot puzzle with a third party solution
        # TODO: check for class: AccountIdentifier
        input("Press Enter if you solved the anti robot puzzle")

        # after puzzle address https://accounts.snapchat.com/accounts/v2/password?ai=a29jaGx1Y2EtMg%3D%3D&continue=%2Faccounts%2Fwelcome
        # TODO: add an await function

        # input the password
        driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[3]/article/div/div[3]/form/div[1]/div/input").send_keys(password)

        # wait for bot detection
        time.sleep(1)

        # press the Enter button
        driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[3]/article/div/div[3]/form/div[3]/button").click()

        # sometimes otp happens https://accounts.snapchat.com/accounts/v2/otp?ai=a29jaGx1Y2EtMg%3D%3D&continue=%2Faccounts%2Fwelcome&otpRequirement=
        # ChtCZXN0w6R0aWdlLCBkYXNzIGR1IGVzIGJpc3QSPkJpdHRlIGdpYiBkZW4gQ29kZSBlaW4sIGRlciBhbiArNDMgKioqLSoqKjkyNjYgZ2VzZW5kZXQgd3VyZGUuGAYiAQE%3D
        # TODO: add an await and human input function

        input("Sometimes an otp check happens. If you are on a welcome page press Enter")

        WebDriverWait(driver, 10).until(EC.url_contains("https://accounts.snapchat.com/accounts/welcome"))

        driver.get(self.url)

        # print("Finished login")

        # input("Press Enter if you logged in successfully")

        input("Press Enter if you finished")

        driver.close()

    def check_accounts(self):
        def f(account, logged_in):
            result = self.is_account_logged_in(account)
            if result:
                print(f"Account: {account} is logged in")
                logged_in.append(account)
            else:
                print(f"Account: {account} is NOT logged in")

        account_list = self.list_root_path()

        logged_in = []

        thread_list = []

        for account in account_list:  # TODO: add a max number of threads in the same time
            thread = threading.Thread(target=f, args=(account, logged_in))
            thread.daemon = True
            thread.start()

            thread_list.append(thread)

        for thread in thread_list:
            thread.join()

        return logged_in

    def remove_account(self, account: str):
        path = os.path.join(self.root_path, account)
        if account in self.list_root_path():
            shutil.rmtree(path)
        else:
            print(f"Account: {account} doesn't exist")

    def list_accounts(self):
        print(self.list_root_path())

    def open(self, account: str):
        driver = webdriver.Chrome(options=self.get_chrome_options(account))
        driver.get(self.url)

        input("Enter if you are done.")

        driver.close()

    def is_account_logged_in(self, account: str):
        if account not in self.list_root_path():
            raise Exception(f"Account: {account} isn't there")

        # options = webdriver.ChromeOptions()
        # options.add_argument(f"user-data-dir={self.get_user_data_dir(account)}")

        driver = webdriver.Chrome(options=self.get_chrome_options(account))
        driver.get(self.url)

        WebDriverWait(driver, 10).until(EC.url_contains(self.url))
        time.sleep(2)

        try:
            WebDriverWait(driver, 2).until(EC.url_contains(self.url))
            return True
        except selenium.common.exceptions.TimeoutException:
            try:
                WebDriverWait(driver, 2).until(EC.url_contains(self.login_url))
                return False
            except selenium.common.exceptions.TimeoutException:
                return None
        finally:
            driver.close()

    def get_chrome_options(self, user: str = None, user_data_dir: str = None):
        if user_data_dir is None:
            user_data_dir = self.get_user_data_dir(user)

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(f"user-data-dir={user_data_dir}")
        chrome_options.add_argument('--no-sandbox')

        chrome_options.add_argument("--enable-logging")
        chrome_options.add_argument("--v")

        chrome_options.add_argument('--disable-dev-shm-usage')
        # chrome_options.add_argument("--headless")
        return chrome_options

    def list_root_path(self):
        return os.listdir(self.root_path)

    def get_user_data_dir(self, user: str):
        return os.path.join(self.root_path, user)
