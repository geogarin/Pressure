from datetime import date, datetime
import sqlite3
from datetime import datetime
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
         "I2CAddres" : 17,
         "Enabled": 1} ,
    "Канал 2":
        {"DifPin" : 476,
         "AbsPin" : 492,
         "I2CAddres" : 18,
         "Enabled": 1} ,
    "Канал 3":
        {"DifPin" : 483,
         "AbsPin" : 490,
         "I2CAddres" : 19,
         "Enabled": 1} ,
    "Канал 4":
        {"DifPin" : 480,
         "AbsPin" : 434,
         "I2CAddres" : 20,
         "Enabled": 1} ,
}
#a=CHANNELS.items()
#b=[(k,*v.values()) for k,v in a]
#a=list(zip(SENSOR_TYPES))

#[tuple(_.values()) for _ in list(SENSORS.values())]
#print(b)

connection = sqlite3.connect(DATABASE_PATH+DATABASE_NAME)
connection.row_factory = sqlite3.Row
connection.isolation_level = None
#connection.execute("PRAGMA foreign_keys = 1")
cursor = connection.cursor()
"""
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


"""
cursor.execute('drop table if exists Channels')
cursor.execute('''create table if not exists Channels (
                    Name text primary key not null,
                    PinDif integer,
                    PinAbs integer,
                    I2CAddress integer,
                    Enabled integer)
               ''')
connection.commit()
cursor.executemany('insert into Channels (Name,PinDif,PinAbs,I2CAddress,Enabled) values (?,?,?,?,?)',[(k,*v.values()) for k,v in CHANNELS.items()])
"""
"""
cursor.execute('drop table if exists Setup')
cursor.execute('''create table if not exists Setup (
                    Entry integer primary key not null,
                    FilterDepth integer,
                    KeyboardButtonSize integer
                    )
               ''')
connection.commit()
cursor.execute('insert into Setup (Entry,FilterDepth,KeyboardButtonSize) values (?,?,?)',(0,50,70))
connection.commit()
"""
"""
cursor.execute('drop table if exists Receipts')
cursor.execute('''create table if not exists Receipts (
                    Name text primary key not null,
                    Volume integer,
                    ConnectionDuration integer,
                    InflatingDuration integer,
                    StabilizationDuration integer,
                    StrengthTestPressure integer,
                    StrengthTestDuration integer,
                    SealedTestPressure integer,
                    SealedTestDeltaThreshold integer,
                    SealedTestDuration integer,
                    Enabled integer)
               ''')
connection.commit()
"""
"""
cursor.execute('drop table if exists TestResult')
cursor.execute('''create table if not exists TestResult (
                    Entry integer primary key not null,
                    TestDate datetime,
                    ChannelNumber integer,
                    TestName text,
                    ProductVolume integer,
                    StrengthTestEnabled integer,
                    StrengthTestPassed integer,
                    StrengthTestResult text,
                    StrengthTestDuration integer,
                    StrengthTestPlanPressure integer,
                    StrengthTestFactPressure integer,
                    SealedTestEnabled integer,
                    SealedTestPassed integer,
                    SealedTestResult text,
                    SealedTestDuration integer,
                    SealedTestPlanPressure integer,
                    SealedTestFactPressure integer,
                    SealedTestMaxDeltaThreshold integer,
                    SealedTestFactDeltaThreshold integer,
                    SealedTestMaxAllowedLeak decimal,
                    SealedTestVolumeOfLeak decimal,
                    SealedTestCrossSecAreaLeak decimal,
                    SealedTestLeakDiameter decimal
                                        
                    )
               ''')
connection.commit()
"""
#cursor.execute('insert into Receipts (Name,Enabled) values(?,?)',('test1',1))
#cursor.execute('insert into Receipts (Name,Enabled) values(?,?)',('test2',1))
#cursor.execute('insert into Receipts (Name,Enabled) values(?,?)',('test3',1))


#cursor.execute('drop table if exists FlashDrives')
#cursor.execute('create table FlashDrives (Serial text primary key not null, Setup integer,Master integer)')

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


print('-------------')
cursor.execute(f'select * from Receipts')
res= [list(row) for row in cursor.fetchall()]
print(res)
print('-------------')

print('-------------')
cursor.execute(f'select * from FlashDrives')
res= [list(row) for row in cursor.fetchall()]
print(res)
print('-------------')
print('-------------')
t=datetime.now()
cursor.execute(f'select * from TestResult')
res= [list(row) for row in cursor.fetchall()]
print(res)
dt=datetime.now()
print(f'select={dt-t}')
print('-------------')
print('-------------')
res=cursor.execute(f'select count(*) from TestResult').fetchone()

print(res[0])
print('-------------')

connection.commit()
connection.close()
