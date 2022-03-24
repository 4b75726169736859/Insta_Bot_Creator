from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import TimeoutException
import time
from faker import Faker
from fake_useragent import UserAgent
from proxylist import ProxyList
import colorful as cf

emailDisabled = "britted.com"
numberAccount = input("Combien de compte voulez vous créé ? ")
compteur = 0
intNumberAccount = int(numberAccount)
tableMail = []
tableProxy = []
tableUsername = []

while compteur < intNumberAccount :
    #Creation faux nom
    fake = Faker()
    fakeName = fake.name()

    #Récuperation de la proxy list
    pl = ProxyList()
    pl.load_file('http_proxies.txt')
    pl.random()

    #configuration du proxy
    firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
    firefox_capabilities['marionette'] = True
    PROXY = pl.random().address()

    #firefox_capabilities['proxy'] = {
        #"proxyType": "MANUAL",
        #"httpProxy": PROXY,
        #"sslProxy": PROXY
    #}

    #Creation faux useragent
    #useragent = UserAgent()
    #profile = webdriver.FirefoxProfile()
    #profile.set_preference("general.useragent.override", useragent.random)

    #ouvrir un navigateur
    #driver = webdriver.Firefox(profile, capabilities=firefox_capabilities, executable_path=r"C:\Users\ZxFic\Documents\geckodriver\geckodriver.exe")
    #driver = webdriver.Firefox(capabilities=firefox_capabilities, executable_path=r"C:\Users\ZxFic\Documents\geckodriver\geckodriver.exe")
    driver = webdriver.Firefox(executable_path=r"C:\Users\ZxFic\Documents\geckodriver\geckodriver.exe")
    
    driver.maximize_window()

    #Creation mail jettable
    try :
        #driver.get("http://httpbin.org/ip")
        driver.get("https://www.crazymailing.com")
    except (NoSuchElementException, TimeoutException, WebDriverException) as e :
        #print('Erreur : '+str(e))
        if 'dnsNotFound' in str(e) :
            print(cf.red('\n----- Error : DNS not found -----'))
        elif 'netTimeout' in str(e):
            print(cf.red('\n----- Error : Time Out'))
        elif 'connectionFailure' in str(e):
            print(cf.red('\n----- Error : Connection Failure'))
        else :
            print(cf.red('\n----- Error : Other Error -----'))
        driver.quit()
        continue

    time.sleep(4)
    try :
        emailJettable = driver.find_element_by_xpath('//*[@id="email_addr"]').text
    except NoSuchElementException :
        print(cf.red('\n----- Error : Access denied -----'))
        driver.quit()
        continue
    fakeUsername = 'xavier'+emailJettable[0:5]

    #Verification mail
    if emailDisabled in emailJettable:
        print(cf.red("\n----- Error : Bad mail -----"))
    else:
        #ouverture d'un nouvelle onglet
        driver.execute_script("window.open('');") 
        driver.switch_to.window(driver.window_handles[1])
        try :
            driver.get('https://www.instagram.com/accounts/emailsignup/') 
        except (NoSuchElementException, TimeoutException, WebDriverException) as e :
            #print('Erreur : '+str(e))
            if 'dnsNotFound' in str(e) :
                print(cf.red('\n----- Error : DNS not found -----'))
            elif 'netTimeout' in str(e):
                print(cf.red('\n----- Error : Time Out'))
            elif 'connectionFailure' in str(e):
                print(cf.red('\n----- Error : Connection Failure'))
            else :
                print(cf.red('\n----- Error : Other Error -----'))
            driver.quit()
            continue
        #Gestion onglet Instagram
        time.sleep(2)
        try :
            driver.find_element_by_xpath('/html/body/div[4]/div/div/button[1]').click()
            
        except NoSuchElementException :
            print(cf.yellow('\nNo Cookie Accept'))
        try :
            driver.find_element_by_name("emailOrPhone").send_keys(emailJettable)
            driver.find_element_by_name("fullName").send_keys(fakeName)
            driver.find_element_by_name("username").send_keys(fakeUsername)
            driver.find_element_by_name("password").send_keys("IsayevN2")
        except NoSuchElementException :
            driver.quit()
            continue
        time.sleep(2)
        try :
            driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div[1]/div/form/div[7]/div/button').click()
        except (NoSuchElementException, ElementClickInterceptedException) as e :
            #print('error '+e)
            print(cf.red('\n----- Error : Bad proxy -----'))
            driver.quit()
            continue
        time.sleep(5)
        try :
            driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div/div[1]/div/div[4]/div/div/span/span[3]/select").send_keys("1999")
        except (NoSuchElementException, ElementClickInterceptedException) as e :
            #print('error '+e)
            print(cf.red('\n----- Error : Bad proxy -----'))
            driver.quit()
            continue
        time.sleep(2)
        try :
            driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div[1]/div/div[6]/button').click()
        except NoSuchElementException :
            driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/div[6]/button').click()

        #Changer d'onglet
        driver.switch_to.window(driver.window_handles[0]) 
        time.sleep(2)

        #Recuperation du code de verification

        emailRecu = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[3]/div/div/div/div[2]/table/tbody/tr[1]/td[1]/div[2]/strong').text
        codeDeVerification = emailRecu[0:6]
        
        badTime = 0
        while 'Welc' in codeDeVerification :
            badTime = badTime + 1
            if badTime == 30:
                print(cf.red('\n----- Error : Email non recu -----'))
                driver.quit()
                continue
            time.sleep(1)
            emailRecu = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[3]/div/div/div/div[2]/table/tbody/tr[1]/td[1]/div[2]/strong').text
            codeDeVerification = emailRecu[0:6]

        #Ajout du code de verification
        driver.switch_to.window(driver.window_handles[1])
        driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[1]/input').send_keys(codeDeVerification)
        time.sleep(2)
        driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[2]').click()
        time.sleep(35)

        #Gestion des erreurs
        try:
            message = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[4]/div').text
            if 'Désolé ! Un problème nous empêche actuellement de vérifier votre code' in message :
                print(cf.red("\n----- Error : Impossible de verifier le code -----"))
            elif 'L’adresse IP que vous utilisez a été signalée' in message :
                print(cf.red("\n----- Error : Proxy detecter -----"))
            elif 'Impossible de créer votre compte. Veu' in message :
                print(cf.red("\n----- Error : Impossible de crée le compte -----"))
        except NoSuchElementException:
            try:
                driver.find_element_by_xpath('/html/body/div[1]/section/main/div[2]/div/div/div[1]/div[1]/h2')
                print(cf.red('\n----- Error : Demande numero de telephone -----'))
            except NoSuchElementException :
                print(cf.green('\nCompte '+fakeUsername+' crée avec succes !'))
                tableMail.append(emailJettable)
                tableProxy.append(PROXY)
                tableUsername.append(fakeUsername)
                compteur = compteur + 1
                with open('mailsInsta.txt', 'w') as f:
                    for line in tableMail:
                        f.write(line)
                        f.write('\n')
                with open('proxyInsta.txt', 'w') as f:
                    for line in tableProxy:
                        f.write(line)
                        f.write('\n')
                with open('userInsta.txt', 'w') as f:
                    for line in tableUsername:
                        f.write(line)
                        f.write('\n')
                time.sleep(10)

    #Quitter le navigateur
    driver.quit()

print(cf.green('\n\nVos '+ numberAccount +' compte(s) on bien été créé !'))