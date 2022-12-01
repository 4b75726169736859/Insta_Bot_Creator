###############################################
#   Python code written by 4b75726169736859
###############################################

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException, WebDriverException
import time
from faker import Faker
from fake_useragent import UserAgent
from proxylist import ProxyList
from mailtm import Email
import colorful as cf
from random_username.generate import generate_username

numberAccount = input("How many accounts do you want to create ? ")
counter = 0
intNumberAccount = int(numberAccount)
tableMail = []
tableProxy = []
tableUsername = []
codeInsta = None
trashProxy = []


def listener(message):
    global codeInsta
    codeInsta = message['subject'][0:5]
    print("code = " + codeInsta)


while counter < intNumberAccount:
    PROXY = None
    firefox_capabilities = None

    # Creation of fake name, username and email address
    fake = Faker()
    fakeName = fake.name()
    fakeUsername = generate_username(2)[0]

    email = Email()
    print("\nDomain: " + email.domain)
    email.register()
    print("Email Address: " + str(email.address))

    # Retrieving the proxy list
    pl = ProxyList()
    pl.load_file('http_proxies_residential.txt')
    pl.random()
    # Proxy setup
    firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
    firefox_capabilities['marionette'] = True

    while True:
        if PROXY is None or PROXY not in trashProxy:
            PROXY = pl.random().address()
            firefox_capabilities['proxy'] = {
                "proxyType": "MANUAL",
                "httpProxy": PROXY,
                "sslProxy": PROXY
            }

    # Create fake useragent
    useragent = UserAgent()
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override", useragent.random)

    # # Open a browser
    # driver = webdriver.Firefox(profile, capabilities=firefox_capabilities)       # with fake user-agent + a proxy
    # driver = webdriver.Firefox(capabilities=firefox_capabilities)        # with a proxy
    driver = webdriver.Firefox()        # No proxy or fake user-agent

    driver.maximize_window()
    try:
        driver.get('https://www.instagram.com/accounts/emailsignup/')
    except (NoSuchElementException, TimeoutException, WebDriverException) as e:
        if 'dnsNotFound' in str(e):
            print(cf.red('\n----- Error : DNS not found -----'))
        elif 'netTimeout' in str(e):
            print(cf.red('\n----- Error : Time Out'))
        elif 'connectionFailure' in str(e):
            print(cf.red('\n----- Error : Connection Failure'))
        else:
            print(cf.red('\n----- Error : Other Error -----'))
        driver.quit()
        continue
    time.sleep(2)
    try:
        driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[2]').click()
    except NoSuchElementException:
        driver.find_element(By.XPATH, '/html/body/div[4]/div/div/button[1]').click()
        print(cf.yellow('\nNo Cookie Accept'))
    try:
        driver.find_element(By.NAME, "emailOrPhone").send_keys(str(email.address))
        driver.find_element(By.NAME, "fullName").send_keys(fakeName)
        driver.find_element(By.NAME, "username").send_keys(fakeUsername)
        driver.find_element(By.NAME, "password").send_keys("456password123")
    except NoSuchElementException:
        driver.quit()
        continue
    time.sleep(2)
    try:
        driver.find_element(By.XPATH,
                            '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/div[7]/div/button').click()
    except (NoSuchElementException, ElementClickInterceptedException) as e:
        print(cf.red('\n----- Error -----'))
        driver.quit()
        continue
    time.sleep(5)
    try:
        driver.find_element(By.XPATH,
                            "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/div/div[1]/div/div[4]/div/div/span/span[3]/select").send_keys(
            "1999")
    except (NoSuchElementException, ElementClickInterceptedException) as e:
        print(cf.red('\n----- Error : Too Many request or Bad proxy -----'))
        if PROXY is not None:
            trashProxy.append(PROXY)
        driver.quit()
        continue
    time.sleep(2)

    driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/div/div[1]/div/div[6]/button').click()
    email.start(listener)
    print("\nWaiting for new emails...")

    while True:
        time.sleep(1)
        if codeInsta is not None:
            codeDeVerification = str(codeInsta)
            print("code = " + codeDeVerification)

            # Added verification code
            driver.switch_to.window(driver.window_handles[1])
            driver.find_element(By.XPATH,
                                '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[1]/input').send_keys(
                codeDeVerification)
            time.sleep(2)
            driver.find_element(By.XPATH,
                                '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[2]/button').click()

            time.sleep(35) # to adjust, this is the time it will take instagram to verify the code and display your account

            # Error management (XPATHs are probably bad)
            try:
                message = driver.find_element(By.XPATH,
                                              '/html/body/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[4]/div').text
                if 'Sorry ! A problem currently prevents us from verifying your code' in message:
                    print(cf.red("\n----- Error : Unable to verify code -----"))
                elif 'The IP address you are using has been reported' in message:
                    print(cf.red("\n----- Error : Proxy detect -----"))
                elif 'Unable to create your account.' in message:
                    print(cf.red("\n----- Error : Unable to create account -----"))
            except NoSuchElementException:
                try:
                    driver.find_element(By.XPATH, '/html/body/div[1]/section/main/div[2]/div/div/div[1]/div[1]/h2')
                    print(cf.red('\n----- Error : Request phone number -----'))
                except NoSuchElementException:
                    print(cf.green('\nAccount ' + fakeUsername + ' successfully created !'))
                    tableMail.append(str(email.address))
                    if PROXY is not None:
                        tableProxy.append(PROXY)
                    tableUsername.append(fakeUsername)
                    counter = counter + 1
                    with open('mailsInsta.txt', 'w') as f:
                        for line in tableMail:
                            f.write(line)
                            f.write('\n')
                    if PROXY is not None:
                        with open('proxyInsta.txt', 'w') as f:
                            for line in tableProxy:
                                f.write(line)
                                f.write('\n')
                    with open('userInsta.txt', 'w') as f:
                        for line in tableUsername:
                            f.write(line)
                            f.write('\n')
                    time.sleep(10)
        # Exit browser
        driver.quit()

print(cf.green('\n\nYour ' + numberAccount + ' account(s) successfully created !'))
