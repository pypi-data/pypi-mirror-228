from simpleWebBrowsing.seleniumOld.chromeNav    import NavChrome
from time                                       import sleep
from selenium.webdriver.common.by               import By

class ElementsManipulate:
    def fillDirectObject(driver, object, data, sleepTime, maxAttempts):
        NavChrome.waitObject(driver, object)
        a = 0 

        while a <= int(maxAttempts):
            try:
                driver.find_element_by_id(object).send_keys(data)
                sleep(int(sleepTime))
                a = 9999
                break
            except:
                try:
                    driver.find_element_by_name(object).send_keys(data)
                    sleep(int(sleepTime))
                    a = 9999
                    break
                except:
                    try:
                        driver.find_element_by_xpath(object).send_keys(data)
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
                driver.find_elements_by_id(object)[position].send_keys(data)
                sleep(int(sleepTime))
                a = 9999
                break
            except:
                try:
                    driver.find_elements_by_name(object)[position].send_keys(data)
                    sleep(int(sleepTime))
                    a = 9999
                    break
                except:
                    try:
                        driver.find_elements_by_xpath(object)[position].send_keys(data)
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
                driver.find_element_by_id(object).click()
                sleep(int(sleepTime))
                a = 9999
                break
            except:
                try:
                    driver.find_element_by_name(object).click()
                    sleep(int(sleepTime))
                    a = 9999
                    break
                except:
                    try:
                        driver.find_elements_by_xpath(object).click()
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
                driver.find_elements_by_id(object)[position].click()
                sleep(int(sleepTime))
                a = 9999
                break
            except:
                try:
                    driver.find_elements_by_name(object)[position].click()
                    sleep(int(sleepTime))
                    a = 9999
                    break
                except:
                    try:
                        driver.find_elements_by_xpath(object)[position].click()
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
                driver.find_elements_by_id(object).click()
                sleep(int(sleepTime))
                a = 9999
                break
            except:
                try:
                    driver.find_elements_by_name(object).click()
                    sleep(int(sleepTime))
                    a = 9999
                    break
                except:
                    try:
                        driver.find_elements_by_xpath(object).click()
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
                driver.find_element_by_id(object).clear()
                sleep(int(sleepTime))
                a = 9999
                break
            except:
                try:
                    driver.find_element_by_name(object).clear()
                    sleep(int(sleepTime))
                    a = 9999
                    break
                except:
                    try:
                        driver.find_element_by_xpath(object).clear()
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
                driver.find_elements_by_id(object)[position].clear()
                sleep(int(sleepTime))
                a = 9999
                break
            except:
                try:
                    driver.find_elements_by_name(object)[position].clear()
                    sleep(int(sleepTime))
                    a = 9999
                    break
                except:
                    try:
                        driver.find_elements_by_xpath(object)[position].clear()
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
            xpath = driver.find_elements_by_xpath(object)
        except:
            try:
                id = driver.find_elements_by_id(object)
            except:
                try:
                    name = driver.find_elements_by_name(object)
                except:
                    "Nenhum elemento localizado!"
        
        return xpath, id, name
    
    def findElement(driver, object):
        try:
            element = driver.find_element_by_xpath(object)
        except:
            try:
                element = driver.find_element_by_id(object)
            except:
                try:
                    element = driver.find_element_by_name(object)
                except:
                    "Nenhum elemento localizado!"
        
        return element

    def findAtributeElement(driver, object, atribute):
        try:
            atribute = driver.find_element_by_xpath(object).get_attribute(atribute)
        except:
            try:
                atribute = driver.find_element_by_id(object).get_attribute(atribute)
            except:
                try:
                    atribute = driver.find_element_by_name(object).get_attribute(atribute)
                except:
                    "Nenhum elemento localizado!"
        
        return atribute