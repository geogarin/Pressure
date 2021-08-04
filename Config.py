
# База данных
DATABASE_NAME = 'data.db'
DATABASE_PATH = '/home/gga/Pressure/Data/'     #'./Data/' так не работает в kiosk mode!

# Точность округления показаний давления (знаков после запятой)
ABS_PRESSURE_ROUNDING_PRECISION = 0
DIF_PRESSURE_ROUNDING_PRECISION = 0

ABS_MASTER_MODE_PRESSURE_ROUNDING_PRECISION = 2
DIF_MASTER_MODE_PRESSURE_ROUNDING_PRECISION = 2



# Период опроса датчиков (мс)
SENSORS_REQUEST_PERIOD = 25

# Период срабатывания таймера простоя (мс)
IDLE_TIMER_PERIOD = 10000

# Допустимый период простоя
IDLE_PERIOD = 60000

# Период обновления контрола прохождения теста (мс)
DURATION_TIMER_STEP = 100

# Пауза между шагами теста (мс)
DELAY_BETWEEN_STEPS = 1000

# Длительность обнуления датчиков (мс). Складывается из двух чисел: ожидания стабилизации после открытия клапанов и самого обнуления
SENSOR_WAIT_PERIOD = 1000
SENSORS_INIT_PERIOD = 2000

# обнуление датчиков, как нулевой шаг теста
RC_ZERO_SENSORS = 'Инициализация'

# Период проверки вставленных флешек (мс)
USB_CHECK_PERIOD = 5000

# i2c адрес модуля, управляющего фитингами
FITTING_MODULE_ADDRESS = 0x15 

# Максимальное давление по диф. датчику, при котором клапан2 может быть закрыт (-500..500 Па). При превышении-клапан принудительно открывается 
MAX_PRESSURE_VALVE2_CLOSED = 500

# дополнительно подаваемое давление (мБар)
ADDITIONAL_PRESSURE = 10

# допустимый перепад давления при стабилизации (Па)
ALLOWED_PRESSURE_DELTA = 5  # -5..5

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
SETUP_DIALOG_SHOW_RESULTS = 'Результаты'

SETUP_DIALOG_LINE_EDIT_FIELD_WIDTH = 200

# Форма настройки рецепта
RC_STRENGTH_TEST = 'Тест прочности'
RC_SEALED_TEST = 'Тест герметичности'
RC_TESTING = 'Тестирование'

RC_NAME = 'Название'
RC_VOLUME = 'Объем изделия, куб.см.'
RC_ENABLED = 'Разрешен'
RC_CONNECTION_DURATION = 'Стыковка'
RC_INFLATING_DURATION = 'Напуск'
RC_STABILIZATION_DURATION = 'Стабилизация'

RC_STRENGTH_TEST_PRESSURE = 'Давление теста прочности'
RC_STRENGTH_TEST_PRESSURE_UNIT_OF_MEASURE = 'мБар'
RC_STRENGTH_TEST_DURATION = 'Длительность теста прочности'

RC_SEALED_TEST_PRESSURE = 'Давление теста герметичности'
RC_SEALED_TEST_PRESSURE_UNIT_OF_MEASURE = 'мБар'
RC_SEALED_TEST_DELTA_THRESHOLD = 'Порог течи теста герметичности'
RC_SEALED_TEST_DELTA_THRESHOLD_UNIT_OF_MEASURE = 'Па'
RC_SEALED_TEST_DURATION = 'Длительность теста герметичности'

RC_SAVE = 'Сохранить'
RC_DELETE = 'Удалить'
RC_NEW = 'Создать'

RC_DIALOG_NAME = 'Настройка рецепта'
RC_DIALOG_RECEIPT_EXISTS = 'Рецепт с таким названием уже существует.\nПерезаписать?'

RC_DURATION_UNIT_OF_MEASURE = 'сек'

RC_VOLUME_MIN = 0
RC_VOLUME_MAX = 100000

RC_CONNECTION_DURATION_MIN = 1
RC_CONNECTION_DURATION_MAX = 30

RC_INFLATING_DURATION_MIN = 1
RC_INFLATING_DURATION_MAX = 30

RC_STABILIZATION_DURATION_MIN = 1
RC_STABILIZATION_DURATION_MAX = 30 

RC_STRENGTH_TEST_PRESSURE_MIN = 500
RC_STRENGTH_TEST_PRESSURE_MAX = 900

RC_STRENGTH_TEST_DURATION_MIN = 5
RC_STRENGTH_TEST_DURATION_MAX = 30

RC_SEALED_TEST_PRESSURE_MIN = 100
RC_SEALED_TEST_PRESSURE_MAX = 400

RC_SEALED_TEST_DELTA_THRESHOLD_MIN = 20
RC_SEALED_TEST_DELTA_THRESHOLD_MAX = 100

RC_SEALED_TEST_DURATION_MIN = 5
RC_SEALED_TEST_DURATION_MAX = 30 

RC_LIST_WIDTH=300 # Ширина списка рецептов

# форма сервиса
SVC_SERVICE_NAME = 'Сервис'

SVC_VALVE1_NAME = 'Клапан 1'
SVC_VALVE2_NAME = 'Клапан 2'
SVC_VALVE3_NAME = 'Клапан 3'
SVC_VALVE4_NAME = 'Клапан 4'
SVC_VALVE5_NAME = 'Клапан фитинга'
SVC_VALVE_CLOSED = 'Закр'
SVC_VALVE_OPEN = 'Откр'
SVC_ZERO_SENSOR = 'Обнулить'
SVC_RESET_ZERO_SENSOR = 'Удалить обнуление'


# Символы клавиатуры
KEYBOARD_CHARS=['1234567890-+',
                'йцукенгшщзхъ',
                'фывапролджэ ',
                'ячсмитьбю., ']

KEYBOARD_BUTTON_DELETE='Del'
KEYBOARD_BUTTON_DONE='Enter'
KEYBOARD_BUTTON_DELETE_DIGIT='<='

# Кол-во отсчетов для усреднения
MAX_SAMPLES_QUANTITY = 1000
MIN_KB_BUTTON_SIZE = 50
MAX_KB_BUTTON_SIZE = 100

# Результаты
RES_YES = 'Да'
RES_NO = 'Нет'

RES_TEST_OK = 'Успех'
RES_TEST_FAILED = 'Неудача'
RES_TEST_OFF = 'Не проводился'
RES_TEST_CANCELED = 'Отменен'

RES_PRESSURE_TOO_LOW = 'Давление слишком мало'

RES_UNSTABLE_PARAMETRES = 'Нестабильные параметры'
RES_LEAK_OUT_OF_DIAGNOSTIC = 'Течь вне диагностики'

RES_LEAK_MORE_ALLOWED = 'Течь выше допустимой'
RES_LEAK_DIAMETER = 'Сопоставимый D течи, мкм'
RES_MKM = 'мкм'

RES_ROUNDING_PRECISION = 3

RES_EXPORT_RESULT = 'Количество тестов для выгрузки в Excel'
RES_EXPORT_BUTTON = 'Выгрузить'
RES_EXPORT_INIT_USB = 'Инициализация USB'

RES_COLUMN_NAMES = [
    
    "Дата",
    "Канал",
    "Тест",
    "Объем продукта, см3",
    "Тест прочности разрешен",
    "Результат",
    "Комментарий",
    "Длительность план., сек",
    "Давление плановое, мБар",
    "Давление фактическое, мБар",
    "Тест герметичности разрешен",
    "Результат",
    "Комментарий",
    "Длительность план., сек",
    "Давление плановое, мБар",
    "Давление фактическое, мБар",
    "Макс. план. перепад давления, Па",
    "Факт. перепад давления, Па",
    "Величина течи, мБар*см3/сек",
    "Площадь сечения течи,мкм2",
    "Диаметр течи, мкм"
]





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
