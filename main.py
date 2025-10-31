import time, datetime, os, random
from selenium import webdriver
from fake_useragent import UserAgent
#from fp.fp import FreeProxy
import asyncio
from proxybroker2 import Broker

def save_log(url,proxy,agent):
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
    directory=f'{dir_path}/Logs'
    if not os.path.isdir(directory):
        os.mkdir(directory)
    directory=f'{dir_path}/Logs/{year}-{month}-{day}'
    #print('директория определена')
    if not os.path.isdir(directory):
        os.mkdir(directory)
    #print('директория создана')
    file_name=f'{day}.{month}.{year}.txt'
    with open(os.path.join(directory, file_name), 'a') as log:
        log.write(f'{time_file} - {url} - {proxy} - {agent}\n')
    return f'{directory}/{time_file}-{str(url).split("//")[1].split("/")[0]}.png'
'''
def give_proxy():
    #https://pypi.org/project/free-proxy/
    print('Получаем прокси')
    proxy=''
    counter_proxy=0
    while proxy=='':
        try:
            proxy = FreeProxy(rand=True, https=False, anonym=True, timeout=0.4).get()
            #proxy = FreeProxy().get()
            print('\t',proxy)
        except:
            counter_proxy+=1
            print(f'\t{counter_proxy} попытка получения прокси завершилась неудачно')
            pass
    return str(proxy).split('//')[1]

def give_proxy_list(index):
    
    with open('Settings/proxy', 'r') as file_proxy:
        proxy_list = file_proxy.readlines()
    #print(proxy_list)   
    if index<len(proxy_list):
        print('Читаем прокси из файла')
        proxy = proxy_list[index]
    else:
        proxy=give_proxy()
    return proxy

def brouser(url):
    useragent = UserAgent()
    options = webdriver.ChromeOptions()
    counter=0
    while counter<150:
        #proxy=give_proxy_list(counter)
        proxy=give_proxy()
        options.add_argument(f'user-agent={useragent.random}')
        
        options.add_argument(f'--proxy-server={proxy}')
        driver = webdriver.Chrome(options=options)
        try:
            driver.get(url=url)
            time.sleep(5)
            driver.save_screenshot(test_time(url,proxy,useragent))
            time .sleep(2)
            print(f'Посетили сайт: {counter+1}')
            counter+=1
        except Exception as ex:
            print(counter,'отказ')
            counter+=1
            print(ex)
        finally:
            #print('x')
            driver.close()
            driver.quit()
'''
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

def main(visit=5):
    ''''''
    limit_proxy=25
    useragent = UserAgent().random
    proxys_list = get_proxys_list(limit=limit_proxy)

    
    counter=0
    visit_counter=0
    while visit_counter<visit:
        proxy = proxys_list[counter]
        driver = get_chromedriver(proxy=proxy, agent=useragent)
        try:

            url = 'https://2ip.ru/'
            url = 'https://kor-cbs.ru/'
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
        


if __name__ == "__main__":
    print('-'*100)
    url = 'https://2ip.ru/'
    main(100)

    #url = 'https://kor-cbs.ru/'
    #url = 'https://korcbs.biblioteka29.ru/'
    print('='*100)
