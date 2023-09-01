from time                         import sleep
from selenium.webdriver.common.by import By

class NavChrome:
    def waitObject(driver, object):
        a = 0
        while len(driver.find_elements_by_id(object)) == 0 and len(driver.find_elements_by_name(object)) == 0 and len(driver.find_elements_by_xpath(object)) == 0 and a < 20:
            sleep(1)
            a = a + 1
        
        if a < 20:
            pass
        else:
            "Erro: Tempo limite de espera atingido (120s)"

        sleep(1)
    
    def waitObjectClose(driver, object):
        while len(driver.find_elements_by_id(object)) == 0 and len(driver.find_elements_by_name(object)) == 0 and len(driver.find_elements_by_xpath(object)) > 0:
            sleep(1)
        sleep(1)

    def getUrl(driver, url):
        print('[Navegação] Realizando o acesso ao URL!')

        driver.get(url)

    def switchFrame(driver, frame):
        NavChrome.waitObject(driver, frame)

        try:
            driver.switch_to.frame(driver.find_element_by_id(frame))
        except:
            try:
                driver.switch_to.frame(driver.find_element_by_name(frame))
            except:
                try:
                    driver.switch_to.frame(driver.find_element_by_xpath(frame))
                except:
                    "Frame não localizado"
    
    def switchParentFrame(driver):
        driver.switch_to.parent_frame()

    def executeScript(driver, script):
        driver.execute_script(script)
    
    def alterWindowChrome(driver):
        JanelaOriginal = driver.current_window_handle
    
        for window_handle in driver.window_handles:
            if window_handle != JanelaOriginal:
                driver.switch_to.window(window_handle)
                break
    
    