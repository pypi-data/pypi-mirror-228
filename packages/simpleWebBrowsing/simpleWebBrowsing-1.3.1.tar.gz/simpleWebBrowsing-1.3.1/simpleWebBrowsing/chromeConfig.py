from selenium                           import webdriver
from selenium.webdriver.chrome.service  import Service
from webdriver_manager.chrome           import ChromeDriverManager
from selenium.webdriver.support.ui      import WebDriverWait

import os 
import shutil
import getpass

class ConexaoChrome:
    def setupDownload(rotina):
        print('[Chrome] Realizando a configuração da pasta de download!')

        diretorioOrigem         = os.path.dirname(os.path.realpath(__file__))
        direcionamentoDownload  = diretorioOrigem + '\\' + rotina
        
        try: 
            try:
                shutil.rmtree(direcionamentoDownload)
            except:
                pass
            try: 
                os.rmdir(direcionamentoDownload)
            except:
                pass
            os.mkdir(direcionamentoDownload)
        except:
            try:
                os.mkdir(direcionamentoDownload)
            except:
                pass
        
        return direcionamentoDownload
    
    def setupChrome(diretorioDownload, diretorioUserChrome):
        print('[Chrome] Realizando a configuração do driver no chrome!')
        print('')

        user = getpass.getuser()

        download = {'download.default_directory' : diretorioDownload}

        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option('prefs', download)
        options.add_argument("--start-maximized")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), chrome_options=options)
    
        return driver
    
    def setupChromeDir(diretorioDownload, diretorioUserChrome):
        print('[Chrome] Realizando a configuração do driver no chrome!')
        print('')

        user = getpass.getuser()

        download = {'download.default_directory' : diretorioDownload}

        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option('prefs', download)
        options.add_argument("user-data-dir=C:\\Users\\" + user + "\\AppData\\Local\\Google\\Chrome\\User Data\\" + diretorioUserChrome)
        options.add_argument("--start-maximized")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), chrome_options=options)
    
        return driver
    
    def setupChromeNew(download_directory, process_name, chromedriver_automatico, chromedriver_directory):
        print('[Chrome] Realizando a configuração do driver no chrome!')
        print('')

        user = getpass.getuser()
        chrome_user_data_dir = f"C:\\Users\\{user}\\AppData\\Local\\Google\\Chrome\\User Data\\{process_name}"

        download = {'download.default_directory' : download_directory}

        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option('prefs', download)
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-popup-blocking")
        options.add_argument(f"user-data-dir={chrome_user_data_dir}")
        options.add_argument("--start-maximized")

        if chromedriver_automatico == "N":
            service  = Service(executable_path = chromedriver_directory + "\\chromedriver.exe")
            driver = webdriver.Chrome(service=service , options=options)
        else:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), chrome_options=options)
    
        return driver
    
    def closeChromeNew(driver, process_name):
        user = getpass.getuser()
        chrome_user_data_dir = f"C:\\Users\\{user}\\AppData\\Local\\Google\\Chrome\\User Data\\{process_name}"

        print('')
        print('[Chrome] Encerrando o navegador Web')
        print('')

        driver.close()
        driver.quit()

        try:
            os.remove(chrome_user_data_dir)
        except:
            pass

    def closeChrome(driver):
        print('')
        print('[Chrome] Encerrando o navegador Web')
        print('')

        driver.close()
        driver.quit()
    
    def verificaDownloadsCompletosChrome(driver):
        if not driver.current_url.startswith("chrome://downloads"):
            driver.get("chrome://downloads/")
        return driver.execute_script("""
            var items = document.querySelector('downloads-manager')
                .shadowRoot.getElementById('downloadsList').items;
            if (items.every(e => e.state === "COMPLETE"))
                return items.map(e => e.fileUrl || e.file_url);
            """)

    def aguardaFinalizacaoDownload(driver):
        WebDriverWait(driver, 120, 1).until(ConexaoChrome.verificaDownloadsCompletosChrome)