import time, datetime, os, random
from selenium import webdriver
from fake_useragent import UserAgent
import asyncio
import data.settings as SETTINFS_FILE #подключаем файл считывания настроек

class MAIN():
    def __init__(self):
        '''Основной класс работы программы'''
        #переменная для обращения к настройкам
        self.SETTINGS=SETTINFS_FILE.Settings()
        self.LINKS=self.links_list()
        pass

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
        И возвращает путь сохранения скриншота'''
        now = datetime.datetime.now()

        #путь к местурасположения программы
        dir_path = os.path.dirname(os.path.realpath(__file__))
        time_file=str(now.time()).split('.')[0]

        year=str(now.year)
        if now.month<10: month=f'0{now.month}'
        else: month=str(now.month)
        if now.day<10: day=f'0{now.day}'
        else: day=str(now.day)
        directory=f'{dir_path}/{self.SETTINGS.get("DIRECTORY_LOGS")}'
        if not os.path.isdir(directory):
            os.mkdir(directory)
        directory=f'{dir_path}/{self.SETTINGS.get("DIRECTORY_LOGS")}/{year}-{month}-{day}'
        #print('директория определена')
        if not os.path.isdir(directory):
            os.mkdir(directory)
        #print('директория создана')
        file_name=f'{day}.{month}.{year}.txt'
        with open(os.path.join(directory, file_name), 'a') as log:
            log.write(f'{time_file} - {url} - {proxy} - {agent}\n')
        return f'{directory}/{time_file}-{str(url).split("//")[1].split("/")[0]}.png'

    def get_chromedriver(self, proxy=None, agent=None):
        chrome_options = webdriver.ChromeOptions()
        if agent!=None:  chrome_options.add_argument(f'user-agent={agent}')
        if proxy!=None:  chrome_options.add_argument(f'--proxy-server={proxy}')
        driver = webdriver.Chrome(options=chrome_options)
        return driver

    def main(self):
        '''Оснавная функция '''
        limit_proxy=25
        useragent = UserAgent().random
        #proxys_list = get_proxys_list(limit=limit_proxy)
        #Счетчики:
        counter = 1 # счетчик попыток
        counter_good=0 # условно удачных посещений
        counter_list = 1 # счетчик по списку (один для списка)
        counter_proxy=0 # счетчик для работы со списком прокси
        while counter_list<3:
        #    proxy = proxys_list[counter]
           
            for url in self.links_list():
                #driver = get_chromedriver(proxy=proxy, agent=useragent)
                driver = self.get_chromedriver(agent=useragent)
                print(f'Попытка №{counter} для списка {counter_list} - {url}',end=' ')
                try:
                    driver.get(url=url)
                    time.sleep(int(self.SETTINGS.get('TIME_PRE_SITE')))#поменять в настройках на 10
                    #driver.save_screenshot(self.save_log(url,proxy,useragent))
                    
                    driver.save_screenshot(self.save_log(url,useragent))

                    time.sleep(int(self.SETTINGS.get('TIME_IN_SITE')))#поменять в настройках на 2
                    counter_good+=1
                    print('GOOD!',end='')
                except Exception as ex:
                    print('BAD', end='')#,proxy)
                finally:
                    driver.quit()
                    print()
                
                counter+=1
            print(f'УДАЧНЫХ посещений - {counter_good}')
            useragent = UserAgent().random    

            counter_list+=1
            counter_proxy+=1
            if counter_proxy==limit_proxy:
                counter_proxy=0
                #proxys_list = get_proxys_list(limit=limit_proxy)


if __name__ == "__main__":
    print('-'*50,'START','-'*50)
    #print()
    app=MAIN().main()
    print('='*50,'FINISH','='*50)
