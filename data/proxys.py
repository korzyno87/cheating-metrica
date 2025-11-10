from proxybroker import Broker
from fp.fp import FreeProxy
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
        print('Формируем список актуальных proxy от proxybroker2 в количестве:',limit)
        proxys_list=[]    
        async def show(proxies):
            while True:
                proxy = await proxies.get()
                if proxy is None: break
                
                new_proxy=f'{proxy.host}:{proxy.port}'.split()[0]
                if new_proxy!= '':
                    proxys_list.append(new_proxy)
        
        proxies = asyncio.Queue()
        broker = Broker(proxies)
        tasks = asyncio.gather(
            broker.find(types=['HTTP','HTTPS'], limit=limit, countries=countries),
            show(proxies))

        loop = asyncio.get_event_loop()   
        try:
            loop.run_until_complete(asyncio.wait_for(tasks, 30))
        except asyncio.TimeoutError:
            print("RETRYING PROXIES ...")
        #loop = asyncio.get_event_loop()
        #loop.run_until_complete(tasks) 
        
        return proxys_list
    

    def get_proxys_list_FreeProxy(self, limit=10, rand=True, https=False, anonym=True, timeout=0.4):
        '''Функция возврощает список прокси. 
        limit - количество прокси (по умолчанию 10);
        rand - получение прокси случайным образом, возможны варианты: True, False;
        https - c поддержкой https, возможны варианты: True, False;
        anonym - анонимный, возможны варианты: True, False;
        timeout - время отклика не больше)
        '''
        #https://pypi.org/project/free-proxy/
        print('Формируем список актуальных proxy от FreeProxy в количестве:',limit)
        proxys_list=[] 
        counter=0
        while counter<limit:
            try:
                proxy = FreeProxy(rand=rand, https=https, anonym=anonym, timeout=timeout).get()
                counter+=1
                proxys_list.append(proxy)
            except:
                pass    
        return proxys_list
'''
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
    #app=Proxys().get_proxys_list_proxybroker2()
    app=Proxys().get_proxys_list_FreeProxy()
    print(app)
    print('='*50,'FINISH','='*50)