import json

class Settings:
    def __init__(self,file_settings='data\settings\settings.json'):
        ''' Класс настроек, используеться для получения настроек'''
        self.SETTINGS = json.load(open(file_settings))

    def get(self, key):
        '''Функция которая возвращает значение настроек'''
        return self.SETTINGS[key]

if __name__ == "__main__":
    '''
    #для проверки
    set=Settings()
    print(set.get(key='TIME_IN_SITE'))
    '''
    pass