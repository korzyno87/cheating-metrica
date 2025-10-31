import time, datetime, os, random
from selenium import webdriver
#from fake_useragent import UserAgent
import asyncio
#from proxybroker2 import Broker
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

    def save_log(self,url,proxy,agent):
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
    


def get_chromedriver(proxy=None, agent=None):
    chrome_options = webdriver.ChromeOptions()
    if agent!=None:  chrome_options.add_argument(f'user-agent={agent}')
    if proxy!=None:  chrome_options.add_argument(f'--proxy-server={proxy}')
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def get_proxys_list(limit=10, countries=None):
    '''Функция возврощает список прокси. 
    limit - количество прокси (по умолчанию 10)
    countries - страна  по умолчанию None, возможны варианты: US,JP,SG,FR,BN,BR,RU)
    
    '''
    pass
    '''
    print('Формируем список актуальных proxy в количестве:',limit)
    proxys_list=[]    
    async def show(proxies):
        while True:
            proxy = await proxies.get()
            if proxy is None: break
            #print('Found proxy: %s' % proxy)
            #print(f'{proxy.host}:{proxy.port}')
            
            new_proxy=f'{proxy.host}:{proxy.port}'.split()[0]
            if new_proxy!= '':
                #print('\t',new_proxy)
                proxys_list.append(new_proxy)

    proxies = asyncio.Queue()
    broker = Broker(proxies)
    tasks = asyncio.gather(
        broker.find(types=['HTTP','HTTPS'], limit=limit, countries=countries),
        show(proxies))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(tasks) 
    return proxys_list
    '''
def main(visit=5):
    ''''''
    '''
     limit_proxy=25
    useragent = UserAgent().random
    proxys_list = get_proxys_list(limit=limit_proxy)

    counter=0
    visit_counter=0
    while visit_counter<visit:
        proxy = proxys_list[counter]
        driver = get_chromedriver(proxy=proxy, agent=useragent)
        try:

            driver.get(url=url)
            time.sleep(10)
            driver.save_screenshot(save_log(url,proxy,useragent))
            time .sleep(2)
            counter+=1
            visit_counter+=1
        except Exception as ex:
            #print(ex)
            print(f'Отказ proxy #{counter}:',proxy)
            counter+=1
        finally:
            driver.quit()
            useragent = UserAgent().random
        if counter==limit_proxy:
            counter=0
            proxys_list = get_proxys_list(limit=limit_proxy)
    '''
    pass    


if __name__ == "__main__":
    print('-'*50,'START','-'*50)
    #print()
    app=MAIN()  
    print('='*50,'FINISH','='*50)
