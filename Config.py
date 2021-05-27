
# База данных
DATABASE_NAME = 'data.db'
DATABASE_PATH = './Data/'

# Период опроса датчиков (мс)
SENSORS_REQUEST_PERIOD = 5

# Названия контролов
BUTTON_START_TEST = 'Старт'
BUTTON_STOP_TEST = 'Стоп'

BUTTON_VALUE_ON = 'Вкл'
BUTTON_VALUE_OFF = 'Выкл'

BUTTON_SETUP = 'Настройки'
BUTTON_MANUAL = 'Сервис'

CHECKBOX_STRENGTH_TEST = 'Прочность'
CHECKBOX_SEALED_TEST = 'Герметичность'

# Форма настроек 
SETUP_DIALOG_NAME = 'Настройка' 
SETUP_DIALOG_COMMON = 'Общие'
SETUP_DIALOG_RECEIPTS = 'Рецепты'

SD_FILTER_DEPTH = 'Глубина фильтра'
SD_KEYBOARD_BUTTON_SIZE='Размер кнопки на клавиатуре'

SETUP_DIALOG_SAVE_CHANGED = 'Cохранить измененные настройки?'
SETUP_DIALOG_SAVE = 'Сохранить'
SETUP_DIALOG_CLOSE = 'Закрыть'

SETUP_DIALOG_LINE_EDIT_FIELD_WIDTH = 200
# Символы клавиатуры
KEYBOARD_CHARS=['1234567890-+',
                'йцукенгшщзхъ',
                'фывапролджэ ',
                'ячсмитьбю., ']

#KEYBOARD_CHARS_ENG='1234567890qwertyuiopasdfghjkl zxcvbnm,. ' # 4 ряда по 10 символов (недостающие дополнены пробелами)
KEYBOARD_BUTTON_DELETE='Del'
KEYBOARD_BUTTON_DONE='Enter'
KEYBOARD_BUTTON_DELETE_DIGIT='<='

# Кол-во отсчетов для усреднения
MAX_SAMPLES_QUANTITY = 1000
MIN_KB_BUTTON_SIZE = 50
MAX_KB_BUTTON_SIZE = 100

# Точность округления показаний давления (знаков после запятой)
ABS_PRESSURE_ROUNDING_PRECISION = 2
DIF_PRESSURE_ROUNDING_PRECISION = 2

if __name__=='__main__':
    #print(f'{len(KEYBOARD_CHARS)}  {KEYBOARD_CHARS[38]}')
    #positions = [(i, j) for i in range(4) for j in range(10)]
    p = [((i, j),KEYBOARD_CHARS[i][j]) for i in range(4) for j in range(12)]
    print(p)

    m = len(KEYBOARD_CHARS)
    print(f'{KEYBOARD_CHARS[0][3]} {m}') 
    for position, name in p:
        print(f'{position} = {name}')
    #for i in range(4):
