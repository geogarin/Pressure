import sqlite3
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

from Config import DATABASE_PATH,DATABASE_NAME

# Типы датчиков
SENSOR_TYPES = {"Differential":
                    {"Description"           : "HSCDRRD006MDSA3",
                    "SensorUnitOfMeasure"    : "mBar",
                    "SensorPressureMin"      : -6,
                    "SensorPressureMax"      : 6,
                    "DisplayUnitOfMeasure"   : "Па",
                    "Ratio"                  : 100,
                    "DisplayPressureMin"     : -600,
                    "DisplayPressureMax"     : 600,
                    "DigitalCounts10Percent" : 1638,
                    "DigitalCounts90Percent" : 14746,
                    "TemperatureMax"         : 2047
                    },
                "Absolute":
                    {"Description"           : "HSCDANN060PGSA3",
                    "SensorUnitOfMeasure"    : "psi",
                    "SensorPressureMin"      : 0,
                    "SensorPressureMax"      : 60,
                    "DisplayUnitOfMeasure"   : "мБар",
                    "Ratio"                  : 68.95,
                    "DisplayPressureMin"     : 0,
                    "DisplayPressureMax"     : 4137,
                    "DigitalCounts10Percent" : 1638,
                    "DigitalCounts90Percent" : 14746,
                    "TemperatureMax"         : 2047
                    }
                }

print('================')

CHANNELS = {
    "Канал 1":
        {"DifPin" : 477,
         "AbsPin" : 479,
         "Enabled": 1} ,
    "Канал 2":
        {"DifPin" : 476,
         "AbsPin" : 492,
         "Enabled": 1} ,
    "Канал 3":
        {"DifPin" : 483,
         "AbsPin" : 490,
         "Enabled": 1} ,
    "Канал 4":
        {"DifPin" : 480,
         "AbsPin" : 434,
         "Enabled": 1} ,
}
#a=CHANNELS.items()
#b=[(k,*v.values()) for k,v in a]
#a=list(zip(SENSOR_TYPES))

#[tuple(_.values()) for _ in list(SENSORS.values())]
#print(b)



"""
# Список датчиков
SENSORS = {
    "ABS_1":
        {"Type"    : "Absolute",
         "Name"    : "Abs 1",
         "PIN"     : 479,
         "Enabled" : 1},
    "ABS_2":
        {"Type"    : "Absolute",
         "Name"    : "Abs 2",
         "PIN"     : 492,
         "Enabled" : 1},
    "ABS_3":
        {"Type"    : "Absolute",
         "Name"    : "Abs 3",
         "PIN"     : 490,
         "Enabled" : 1},
    "ABS_4":
        {"Type"    : "Absolute",
         "Name"    : "Abs 4",
         "PIN"     : 434,
         "Enabled" : 1},

    "DIF_1":
        {"Type"    : "Differential",
         "Name"    : "Dif 1",
         "PIN"     : 477,
         "Enabled" : 1},

    "DIF_2":
        {"Type"    : "Differential",
         "Name"    : "Dif 2",
         "PIN"     : 476,
         "Enabled" : 1},

    "DIF_3":
        {"Type"    : "Differential",
         "Name"    : "Dif 3",
         "PIN"     : 483,
         "Enabled" : 1},

    "DIF_4":
        {"Type"    : "Differential",
         "Name"    : "Dif 4",
         "PIN"     : 480,
         "Enabled" : 1}         
} 
"""



connection = sqlite3.connect(DATABASE_PATH+DATABASE_NAME)
connection.row_factory = sqlite3.Row
connection.isolation_level = None
#connection.execute("PRAGMA foreign_keys = 1")
cursor = connection.cursor()
cursor.execute('drop table if exists SensorType')
cursor.execute('''create table if not exists SensorType (
                    Type text primary key not null,
                    Description text,
                    SensorUnitOfMeasure text,
                    SensorPressureMin decimal,
                    SensorPressureMax decimal,
                    Ratio decimal,
                    DisplayUnitOfMeasure text,
                    DisplayPressureMin decimal,
                    DisplayPressureMax decimal,
                    DigitalCounts10Percent integer,
                    DigitalCounts90Percent integer,
                    TemperatureMax integer)
               ''')

for sensorType,sensorParameters in SENSOR_TYPES.items():
    cursor.execute(f'select * from SensorType where Type="{sensorType}"')
    rec = cursor.fetchone()
    if rec is None:
        cursor.execute(f'insert into SensorType (Type) values ("{sensorType}")')
        
    cursor.execute('''update SensorType set 
                            Description=?,
                            SensorUnitOfMeasure=?,
                            SensorPressureMin=?,
                            SensorPressureMax=?,
                            Ratio=?,
                            DisplayUnitOfMeasure=?,
                            DisplayPressureMin=?,
                            DisplayPressureMax=?,
                            DigitalCounts10Percent=?,
                            DigitalCounts90Percent=?,
                            TemperatureMax=?
                        where Type=?
                    ''',
                    (sensorParameters["Description"],
                    sensorParameters["SensorUnitOfMeasure"],
                    sensorParameters["SensorPressureMin"],
                    sensorParameters["SensorPressureMax"],
                    sensorParameters["Ratio"],
                    sensorParameters["DisplayUnitOfMeasure"],
                    sensorParameters["DisplayPressureMin"],
                    sensorParameters["DisplayPressureMax"],
                    sensorParameters["DigitalCounts10Percent"],
                    sensorParameters["DigitalCounts90Percent"],
                    sensorParameters["TemperatureMax"],
                    sensorType))

connection.commit()
cursor.execute('drop table if exists Sensor')
"""
connection.execute("PRAGMA foreign_keys = 1")

cursor.execute('''create table if not exists Sensor (
                    Name text not null,
                    Type text not null references SensorType(Type),                   
                    Pin integer,
                    Enabled integer,
                    Primary key(Name,Type))
               ''')
connection.commit()
cursor.executemany('insert into Sensor (Type,Name,Pin,Enabled) values (?,?,?,?)',[tuple(_.values()) for _ in list(SENSORS.values())])
"""



cursor.execute('drop table if exists Channels')
cursor.execute('''create table if not exists Channels (
                    Name text primary key not null,
                    PinDif integer,
                    PinAbs integer,
                    Enabled integer)
               ''')
connection.commit()
cursor.executemany('insert into Channels (Name,PinDif,PinAbs,Enabled) values (?,?,?,?)',[(k,*v.values()) for k,v in CHANNELS.items()])

print('-------------')
cursor.execute(f'select * from SensorType')
res= [list(row) for row in cursor.fetchall()]
print(res)
print('-------------')
"""
cursor.execute(f'select * from Sensor')
res= [list(row) for row in cursor.fetchall()]
print(res)
"""

cursor.execute(f'select * from Channels')
res= [list(row) for row in cursor.fetchall()]
print(res)
print('-------------')


connection.commit()
connection.close()
