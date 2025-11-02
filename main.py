import time, datetime, os, platform
from selenium import webdriver
from fake_useragent import UserAgent
import data.settings as SETTINFS_FILE #подключаем файл считывания настроек
import data.proxys as PROXYS # Подключаем файл для работы с прокси

class MAIN():
    def __init__(self):
        '''Основной класс работы программы'''
        #переменная для обращения к настройкам
        self.get_platform()
        self.SETTINGS=SETTINFS_FILE.Settings()
        self.PROXYS=PROXYS.Proxys()
        self.LINKS=self.links_list()
   
    def get_platform(self):
        self.SYMBOL='/'
        if platform.system() == 'Windows': 
            self.SYMBOL='\\'


    def links_list(self):
        '''Функция возвращает список ссылок считанных из файла'''
        file=open('data/settings/links_list.txt')
        links=file.readlines()
        for i in range(len(links)):
            links[i]=str(links[i]).split('\n')[0]
        return links

    def save_log(self,url,proxy=None,agent=None):
        '''Фукция создает директорию для сохранения скриншотов в зависимости от даты. 
        В ней файл с датой в котором будут прописываться попытки подключения. 
        И возвращает путь сохранения скриншота !!! На Windows скриншот не сохраняеться!'''
        now = datetime.datetime.now()

        #путь к местурасположения программы
        dir_path = os.path.dirname(os.path.realpath(__file__))
        time_file=str(now.time()).split('.')[0]

        year=str(now.year)
        if now.month<10: month=f'0{str(now.month)}'
        else: month=str(now.month)
        if now.day<10: day=f'0{str(now.day)}'
        else: day=str(now.day)
        #directory=f'{dir_path}/{self.SETTINGS.get("DIRECTORY_LOGS")}'
        directory=f'{dir_path}{self.SYMBOL}{self.SETTINGS.get("DIRECTORY_LOGS")}'
        if not os.path.isdir(directory):
            os.mkdir(directory)
        #directory=f'{dir_path}/{self.SETTINGS.get("DIRECTORY_LOGS")}/{year}-{month}-{day}'
        directory=f'{dir_path}{self.SYMBOL}{self.SETTINGS.get("DIRECTORY_LOGS")}{self.SYMBOL}{year}-{month}-{day}'    
        #print('директория определена')
        if not os.path.isdir(directory):
            os.mkdir(directory)
        #print('директория создана')
        file_name=f'{day}.{month}.{year}.txt'
        with open(os.path.join(directory, file_name), 'a') as log:
            log.write(f'{time_file} - {url} - {proxy} - {agent}\n')
        return f'{directory}{self.SYMBOL}{time_file.split(":")[0]}.{time_file.split(":")[1]}.{time_file.split(":")[2]}-{str(url).split("//")[1].split("/")[0]}.png'


    def get_chromedriver(self, proxy=None, agent=None):
        chrome_options = webdriver.ChromeOptions()
        if agent!=None:  chrome_options.add_argument(f'user-agent={agent}')
        if proxy!=None:  chrome_options.add_argument(f'--proxy-server={proxy}')
        driver = webdriver.Chrome(options=chrome_options)
        return driver

    def new_proxy_list(self):
        if self.SETTINGS.get('DEFAULT_PROXY') == 'proxybroker2':
           proxys_list = self.PROXYS.get_proxys_list_proxybroker2(limit=self.SETTINGS.get("LENGHT_PROXYS_LIST"))
           #попробовать передалать в f строку
           #proxys_list =f'self.PROXYS.get_proxys_list_{self.SETTINGS.get('DEFAULT_PROXY')}(limit={self.SETTINGS.get("LENGHT_PROXYS_LIST")})'
           #f''get_proxys_list(limit=limit_proxy)
        #print(proxys_list)
        return proxys_list
    
    def main(self):
        '''Оснавная функция '''
        useragent = UserAgent().random
        proxys_list = self.new_proxy_list()
        #Счетчики:
        counter = 1 # счетчик попыток
        counter_good=0 # условно удачных посещений
        counter_list = 1 # счетчик по списку (один для списка)
        counter_proxy=0 # счетчик для работы со списком прокси
        while True:#counter_list<3:
            for url in self.links_list():
                proxy = proxys_list[counter_proxy]
                driver = self.get_chromedriver(proxy=proxy, agent=useragent)
                print(f'Попытка №{counter} для списка {counter_list} - {url}',end=' ')
                try:
                    driver.get(url=url)
                    time.sleep(int(self.SETTINGS.get('TIME_PRE_SITE')))#поменять в настройках на 10
                    driver.save_screenshot(self.save_log(url,proxy, useragent))
                    time.sleep(int(self.SETTINGS.get('TIME_IN_SITE')))#поменять в настройках на 2
                    counter_good+=1
                    print('GOOD!',end='')
                except Exception as ex:
                    print('BAD', ',PROXY =',proxy, end='')
                    counter_proxy+=1
                finally:
                    driver.quit()
                    print()
                counter+=1
                if counter_proxy==self.SETTINGS.get('LENGHT_PROXYS_LIST'):
                    counter_proxy=0
                    self.new_proxy_list()
            print(f'УДАЧНЫХ посещений - {counter_good}')
            useragent = UserAgent().random    
            counter_list+=1
            counter_proxy+=1

if __name__ == "__main__":
    print('-'*50,'START','-'*50)
    app=MAIN().main()
    print('='*50,'FINISH','='*50)