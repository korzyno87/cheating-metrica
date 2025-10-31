#from fp.fp import FreeProxy
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