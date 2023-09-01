from simpleWebBrowsing.seleniumNew.chromeNav    import NavChrome
from time                                       import sleep
from selenium.webdriver.common.by               import By

class ElementsManipulate:
    def fillDirectObject(driver, object, data, sleepTime, maxAttempts):
        NavChrome.waitObject(driver, object)
        a = 0 

        while a <= int(maxAttempts):
            try:
                driver.find_element(By.ID, object).send_keys(data)
                sleep(int(sleepTime))
                a = 9999
                break
            except:
                try:
                    driver.find_element(By.NAME, object).send_keys(data)
                    sleep(int(sleepTime))
                    a = 9999
                    break
                except:
                    try:
                        driver.find_element(By.XPATH, object).send_keys(data)
                        sleep(int(sleepTime))
                        a = 9999
                        break
                    except:
                        print('Erro: Elemento não localizado!')
                        a = a + 1
                        sleep(int(sleepTime))
    
    def fillIndexObject(driver, object, position, data, sleepTime, maxAttempts):
        NavChrome.waitObject(driver, object)
        a = 0 

        while a <= int(maxAttempts):
            try:
                driver.find_elements(By.ID, object)[position].send_keys(data)
                sleep(int(sleepTime))
                a = 9999
                break
            except:
                try:
                    driver.find_elements(By.NAME, object)[position].send_keys(data)
                    sleep(int(sleepTime))
                    a = 9999
                    break
                except:
                    try:
                        driver.find_elements(By.XPATH, object)[position].send_keys(data)
                        sleep(int(sleepTime))
                        a = 9999
                        break
                    except:
                        print('Erro: Elemento não localizado!')
                        a = a + 1
                        sleep(int(sleepTime))

    def clickDirectObject(driver, object, sleepTime, maxAttempts):
        NavChrome.waitObject(driver, object)
        a = 0 

        while a <= int(maxAttempts):
            try:
                driver.find_element(By.ID, object).click()
                sleep(int(sleepTime))
                a = 9999
                break
            except:
                try:
                    driver.find_element(By.NAME, object).click()
                    sleep(int(sleepTime))
                    a = 9999
                    break
                except:
                    try:
                        driver.find_element(By.XPATH, object).click()
                        sleep(int(sleepTime))
                        a = 9999
                        break
                    except:
                        print('Erro: Elemento não localizado!')
                        a = a + 1
                        sleep(int(sleepTime))
    
    def clickIndexObject(driver, object, position, sleepTime, maxAttempts):
        NavChrome.waitObject(driver, object)
        a = 0 

        while a <= int(maxAttempts):
            try:
                driver.find_elements(By.ID, object)[position].click()
                sleep(int(sleepTime))
                a = 9999
                break
            except:
                try:
                    driver.find_elements(By.NAME, object)[position].click()
                    sleep(int(sleepTime))
                    a = 9999
                    break
                except:
                    try:
                        driver.find_elements(By.XPATH, object)[position].click()
                        sleep(int(sleepTime))
                        a = 9999
                        break
                    except:
                        print('Erro: Elemento não localizado!')
                        a = a + 1
                        sleep(int(sleepTime))

    def clickMultiplesObject(driver, object, sleepTime, maxAttempts):
        NavChrome.waitObject(driver, object)
        a = 0 

        while a <= int(maxAttempts):
            try:
                driver.find_elements(By.ID, object).click()
                sleep(int(sleepTime))
                a = 9999
                break
            except:
                try:
                    driver.find_elements(By.NAME, object).click()
                    sleep(int(sleepTime))
                    a = 9999
                    break
                except:
                    try:
                        driver.find_elements(By.XPATH, object).click()
                        sleep(int(sleepTime))
                        a = 9999
                        break
                    except:
                        print('Erro: Elemento não localizado!')
                        a = a + 1
                        sleep(int(sleepTime))

    def clearDirectObject(driver, object, sleepTime, maxAttempts):
        NavChrome.waitObject(driver, object)
        a = 0 

        while a <= int(maxAttempts):
            try:
                driver.find_element(By.ID, object).clear()
                sleep(int(sleepTime))
                a = 9999
                break
            except:
                try:
                    driver.find_element(By.NAME, object).clear()
                    sleep(int(sleepTime))
                    a = 9999
                    break
                except:
                    try:
                        driver.find_element(By.XPATH, object).clear()
                        sleep(int(sleepTime))
                        a = 9999
                        break
                    except:
                        print('Erro: Elemento não localizado!')
                        a = a + 1
                        sleep(int(sleepTime))
    
    def clearIndexObject(driver, object, position, sleepTime, maxAttempts):
        NavChrome.waitObject(driver, object)
        a = 0 

        while a <= int(maxAttempts):
            try:
                driver.find_elements(By.ID, object)[position].clear()
                sleep(int(sleepTime))
                a = 9999
                break
            except:
                try:
                    driver.find_elements(By.NAME, object)[position].clear()
                    sleep(int(sleepTime))
                    a = 9999
                    break
                except:
                    try:
                        driver.find_elements(By.XPATH, object)[position].clear()
                        sleep(int(sleepTime))
                        a = 9999
                        break
                    except:
                        print('Erro: Elemento não localizado!')
                        a = a + 1
                        sleep(int(sleepTime))

    def findElements(driver, object):
        xpath = ''
        id    = ''
        name  = ''

        try:
            xpath = driver.find_elements(By.XPATH, object)
        except:
            try:
                id = driver.find_elements(By.ID, object)
            except:
                try:
                    name = driver.find_elements(By.NAME, object)
                except:
                    "Nenhum elemento localizado!"
        
        return xpath, id, name
    
    def findElement(driver, object):
        try:
            element = driver.find_element(By.XPATH, object)
        except:
            try:
                element = driver.find_element(By.ID, object)
            except:
                try:
                    element = driver.find_element(By.NAME, object)
                except:
                    "Nenhum elemento localizado!"
        
        return element

    def findAtributeElement(driver, object, atribute):
        try:
            atribute = driver.find_element(By.XPATH, object).get_attribute(atribute)
        except:
            try:
                atribute = driver.find_element(By.ID, object).get_attribute(atribute)
            except:
                try:
                    atribute = driver.find_element(By.NAME, object).get_attribute(atribute)
                except:
                    "Nenhum elemento localizado!"
        
        return atribute