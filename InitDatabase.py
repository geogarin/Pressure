import sqlite3
from Config import DATABASE_NAME,DATABASE_PATH


# Типы датчиков
SENSOR_TYPES = {"Absolute":
                    {"Description"           : "HSCDANN060PGSA3",
                    "SensorUnitOfMeasure"    : "mBar",
                    "SensorPressureMin"      : -6,
                    "SensorPressureMax"      : 6,
                    "DisplayUnitOfMeasure"   : "Pa",
                    "Ratio"                  : 100,
                    "DisplayPressureMin"     : -600,
                    "DisplayPressureMax"     : 600,
                    "DigitalCounts10Percent" : 1638,
                    "DigitalCounts90Percent" : 14746,
                    "TemperatureMax"         : 2047
                    },
                "Differential":
                    {"Description"           : "HSCDRRD006MDSA3",
                    "SensorUnitOfMeasure"    : "psi",
                    "SensorPressureMin"      : 0,
                    "SensorPressureMax"      : 60,
                    "DisplayUnitOfMeasure"   : "mBar",
                    "Ratio"                  : 68.95,
                    "DisplayPressureMin"     : 0,
                    "DisplayPressureMax"     : 4137,
                    "DigitalCounts10Percent" : 1638,
                    "DigitalCounts90Percent" : 14746,
                    "TemperatureMax"         : 2047
                    }
                }
#a=SENSOR_TYPES.items()
#b=[(k,tuple(v.values())) for k,v in a]
#a=list(zip(SENSOR_TYPES))

#[tuple(_.values()) for _ in list(SENSORS.values())]
#print(a)
print('================')


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
         "PIN"     : 489,
         "Enabled" : 1},
    "ABS_4":
        {"Type"    : "Absolute",
         "Name"    : "Abs 4",
         "PIN"     : 488,
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


print('-------------')
cursor.execute(f'select * from SensorType')
res= [list(row) for row in cursor.fetchall()]
print(res)
print('-------------')
cursor.execute(f'select * from Sensor')
res= [list(row) for row in cursor.fetchall()]
print(res)



connection.commit()
connection.close()
