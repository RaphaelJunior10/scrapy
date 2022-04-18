import os, sys, time, threading, itertools

try:
    import json
except:
    os.system('pip install jsonlib')
finally:
    import json

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
except:
    os.system('pip install selenium')
finally:
    from selenium import webdriver
    from selenium.webdriver.common.by import By

try:
    from webdriver_manager.chrome import ChromeDriverManager
except:
    os.system('pip install webdriver-manager')
finally:
    from webdriver_manager.chrome import ChromeDriverManager

try:
    import urllib.request
except:
    os.system('pip install urllib')
finally:
    import urllib.request


try:
    from pyquickhelper.filehelper import download, unzip_files
except:
    os.system('pip install pyquickhelper')
finally:
    from pyquickhelper.filehelper import download, unzip_files

try:
    import mysql.connector as mysql
except:
    os.system('pip install mysql-connector')
finally:
    import mysql.connector as mysql



def getDataToBDD(debut=0):
    print("Connexion a la base de donnee")
    try:
        db = mysql.connect(user='root', password='',
                       host='localhost', database='astreat',
                       auth_plugin='mysql_native_password')
    except:
        print("Impossible de se connecter a la base de donnee")
        sys.exit(1)

    print("Connexion a la base de donnee reussi - Recuperation des informations")
    cursor = db.cursor()
    query = "SELECT * FROM medicaments LIMIT "+str(debut)+",5217"
    cursor.execute(query)
    res = cursor.fetchall()
    tab = {}
    for re in res:
        tab['medoc' + str(re[0])] = re[1]
    print("Recuperation terminee : "+str(len(tab)) + "entree(s)")
    return tab


class Scrapy:
    def __init__(self):
        self.path_to_web_driver,self.url = "chromedriver",""
        self.class_name, self.attr, self.path = "Q4LuWd", "src", "path/"
        self.version, self.extension = "73.0.3683.68", '.jpg'
        self.url = "https://chromedriver.storage.googleapis.com/%s/" % self.version
        self.downloadChromeDriver()
        self.initBrowser()
        self.tab = []

    def downloadChromeDriver(self):
        print("Verification/Telechargement de chromeDriver")
        if "win" in sys.platform:
            if not os.path.exists("chromedriver_win32.zip"):
                d = download(self.url + "chromedriver_win32.zip")
            if not os.path.exists("chromedriver.exe"):
                unzip_files("chromedriver_win32.zip", where_to=".")
        elif sys.platform.startswith("linux"):
            if not os.path.exists("chromedriver_linux64.zip"):
                d = download(self.url + "chromedriver_linux64.zip")
            if not os.path.exists("chromedriver"):
                unzip_files("chromedriver_linux64.zip", where_to=".")
        elif sys.platform.startswith("darwin"):
            if not os.path.exists("chromedriver_mac64.zip"):
                d = download(self.url + "chromedriver_mac64.zip")
            if not os.path.exists("chromedriver"):
                unzip_files("chromedriver_mac64.zip", where_to=".")

    def initBrowser(self):
        print("Initialisation du browser")
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--verbose')

        self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    def download(self,search,name):
        try:
            self.url = "https://www.google.co.in/search?q="+search+"&source=lnms&tbm=isch"
            self.browser.get(self.url)
            #page = self.browser.find_elements_by_class_name(self.class_name)
            page = self.browser.find_elements(by=By.CLASS_NAME, value=self.class_name)
            link = page[0].get_attribute(self.attr)
            #print(link)
            path = self.path+name+self.extension
            urllib.request.urlretrieve(link, path)
        except:
            self.tab[name] = search
            self.setData(tab)

    def getData(self):
        with open('data.json') as mon_fichier:
            data = json.load(mon_fichier)
        return data

    def setData(self,data):
        with open('data.json', 'w') as mon_fichier:
            json.dump(data, mon_fichier)


class Downloading:
    def __init__(self):
        self.downloaded = 0
        print("---------- Debut du telechargement des images ---------------")

    def animate(self):
        for c in itertools.cycle(['|', '/', '-', '\\']):
            if int(self.downloaded) == 100:
                break
            sys.stdout.write('\rTelechargement '+str(self.downloaded)+'%  ' + c)
            sys.stdout.flush()
            time.sleep(0.1)
            #print("val " +str(self.pourcentage))
        sys.stdout.write('\rTelechargement termine!     ')



tab = getDataToBDD(103)

scrapy = Scrapy()
downloaded, index = 0, 0
total = len(tab)
downloaded = int((index / total) * 100)

downloadring = Downloading()
t = threading.Thread(target=downloadring.animate)
t.start()
for t in tab:
    scrapy.download(tab[t], t)
    index += 1
    downloaded = round((index / total) * 100, 4)
    downloadring.downloaded = downloaded



