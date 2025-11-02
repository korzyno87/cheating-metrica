#from fp.fp import FreeProxy
from proxybroker import Broker
import asyncio

class Proxys():
    def __init__(self):
        '''Класс для работы с различными прокси. В файле настроек settings.json ключь
          "DEFAULT_PROXY" может принимать значение которая сводится к названию библиотеки,
            через которую получаем прокси. По умолчанию proxybroker2'''
        pass
    
    def get_proxys_list_proxybroker2(self, limit=10, countries=None):
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
                   # print('\t',new_proxy)
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


if __name__ == "__main__":
    print('-'*50,'START','-'*50)
    app=Proxys().get_proxys_list_proxybroker2()
    print(app)
    print('='*50,'FINISH','='*50)