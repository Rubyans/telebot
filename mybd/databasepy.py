from asyncio.windows_events import NULL
import code
import io
import os
import string
import qrcode
from traceback import print_tb
import turtle
from unittest import result
import cv2
from cv2 import circle
import pandas as pd
from io import BytesIO
import sqlite3 as sq
from PIL import Image
from pyzbar.pyzbar import decode
from create_bot import bot
from keybords import kbwarehouse,kblogist,kbdriver,kbadmin,kbwareh
def startfunc():
    global base1
    base1=sq.connect('fortelegram.db')
    cur1=base1.cursor()
    if base1:
        print('БД работает')
    base1.isolation_level = None
    base1.commit

########################################вхід користувача(логіст, водій, складальник, адміністратор)#########################################################################################
async def sqllogist(state):#знаходження відповідності при вході логіста
    cur1=base1.cursor()
    async with state.proxy() as data:
        global logist
        sql="SELECT Name FROM Logist WHERE Login=? and Password=?"
        result=cur1.execute(sql,(tuple(data.values())))
        logist=result.fetchone()
    cur1.close()

async def logistfinish(message): #допуск у власний кабінет логіста
    try:
        if logist[0]!=None:
            await bot.send_message(message.from_user.id,logist[0] + ', ви увійшли в свій особистий кабінет логіста',reply_markup=kblogist)
    except:
        await bot.send_message(message.from_user.id,'Ви ввели невірно дані або не натиснули кнопку Увійти. Спробуйте знову')

async def sqldriverman(state):#знаходження відповідності при вході водія
    cur1=base1.cursor()
    async with state.proxy() as data:
        global driver
        sql="SELECT Name,Surname,Codedriverman FROM Driverman WHERE Login=? and Password=?"
        result =cur1.execute(sql,(tuple(data.values())))
        driver=result.fetchone()
    cur1.close()

async def drivermanfinish(message): #допуск у власний кабінет логіста
    try:
        if driver[0]!=None:
            await bot.send_message(message.from_user.id,driver[0] + ', ви увійшли в свій особистий кабінет водія',reply_markup=kbdriver)
    except:
        await bot.send_message(message.from_user.id,'Ви ввели невірно дані або не натиснули кнопку Увійти. Спробуйте знову')

async def sqlwarehouseman(state):#знаходження відповідності при вході складальника
    cur1=base1.cursor()
    async with state.proxy() as data:
        global wareman
        sql="SELECT Name FROM Warehouseman WHERE Login=? and Password=?"
        result=cur1.execute(sql,(tuple(data.values())))
        wareman=result.fetchone()
    cur1.close()

async def warehousefinish(message): #допуск у власний кабінет складальника
    try:
        if wareman[0]!=None:
            await bot.send_message(message.from_user.id,wareman[0] + ', ви увійшли в свій особистий кабінет складальника',reply_markup=kbwarehouse)
    except:
        await bot.send_message(message.from_user.id,'Ви ввели невірно дані або не натиснули кнопку Увійти. Спробуйте знову')

async def sqladmin(state):#знаходження відповідності при вході адміністратора
    cur1=base1.cursor()
    async with state.proxy() as data:
        global admins
        sql="SELECT Name FROM Administrator WHERE Login=? and Password=?"
        result=cur1.execute(sql,(tuple(data.values())))
        admins=result.fetchone()
    cur1.close()

async def adminfinish(message): #допуск у власний кабінет адміністратора
    try:
        if admins[0]!=None:
            await bot.send_message(message.from_user.id,admins[0] + ', ви увійшли в свій особистий кабінет адміністратора',reply_markup=kbadmin)
    except:
        await bot.send_message(message.from_user.id,'Ви ввели невірно дані або не натиснули кнопку Увійти. Спробуйте знову')

########################################складальник#########################################################################################
async def warehousedemostrate(message,state):# демонстрація даних для складальника
    cur1=base1.cursor()
    async with state.proxy() as data:
        cur1.execute("SELECT Cargo.CodeCargo,Namecargo,savemethod,Generaltonnage,QRcipher,Namewarehouse,Typecargo FROM Cargo INNER JOIN Notewarehousewarehouse ON Cargo.CodeCargo=Notewarehousewarehouse.Codecargo INNER JOIN Warehouse ON Notewarehousewarehouse.Codewarehouse=Warehouse.Codewarehouse WHERE Notewarehousewarehouse.Codenotew=?",data['key'])
        demonst=cur1.fetchall()
        if(not demonst):
            await bot.send_message(message.chat.id,"За даним номером не існує склада або вантажа на складі немає. Спробуйте знову")
        else:
            for strone in demonst:
                str=strone
                await bot.send_message(message.from_user.id,"Порядковий номер вантажа: {0}. Назва вантажу: {1}. Спосіб зберігання: {2}. Тонажність: {3}. Тип вантажу: {6}. Місність вантажу: {4}.  Назва складу: {5}.".format(str[0],str[1],str[2],str[3],str[4],str[5],str[6]))
    cur1.close()
    
async def deletewarehousecargoo(message,state):
    try:
        cur1=base1.cursor()
        async with state.proxy() as data:
            res=cur1.execute('SELECT CodeCargo FROM Notewarehousewarehouse WHERE Codenotew = ?',(data['deletecargo'],))
            ccargo=sum(res.fetchone(),0)
            sql="Delete FROM Cargo WHERE CodeCargo="+str(ccargo)
            sql1="Delete From Notewarehousewarehouse WHERE Codenotew = "+str(data['deletecargo'])
        cur1.execute(sql)
        cur1.execute(sql1)
        base1.commit()
        await bot.send_message(message.chat.id,'Дані успішно видалено')
        cur1.close()
    except Exception as e:
        await bot.send_message(message.chat.id,"За номером накладної не існує вантажа або сталася помилка. Спробуйте знову")

async def dbsavecargo(state,message,file_info):#функція складальника вписання даних в бд
    try:
        global resultbd
        img = Image.open(file_info.file_path)
        qr= decode(img)
        for q in qr:
            resultbd=q.data.decode('utf-8')
    except Exception as e:
        await bot.send_message(message.chat.id,"Щось не так...Перевірте QR-code, програма не може його дешифрувати. Спробуйте знову")


async def dbsavecargo1(message,state):
    try:
        cur1=base1.cursor()
        async with state.proxy() as data:
            cur1.execute("SELECT Namecargo,savemethod,Generaltonnage,QRcipher,Namewarehouse,Warehouse.City,Warehouse.Street,Warehouse.Home,Namecompany,Phone,Typecargo FROM Notewarehousewarehouse INNER JOIN Cargo ON Notewarehousewarehouse.Codecargo=Cargo.CodeCargo INNER JOIN Warehouse ON Notewarehousewarehouse.Codewarehouse=Warehouse.Codewarehouse INNER JOIN Company ON Warehouse.CodeCompany=Company.Codecompany WHERE Notewarehousewarehouse.Codenotew = ?",resultbd)
        demonst=cur1.fetchone()
        await bot.send_message(message.from_user.id,"Вантаж: {0}, зберігається за допомогою: {1}, загальною тонажністю: {2} тон(а), маючи міцність: {3} та тип: {10}, розташован на складі: {4}, Місто: {5}, вулиця: {6}, будинок: {7}, компанії: {8}, контактний номер телефону компанії: {9}.".format(demonst[0],demonst[1],demonst[2],demonst[3],demonst[4],demonst[5],demonst[6],demonst[7],demonst[8],demonst[9],demonst[10]))
        cur1.close()
    except Exception as e:
        await bot.send_message(message.chat.id,"Накладної за даним номером не існує")




async def dbkbnext(message,state):
    cur1=base1.cursor()
    pk=maxcountsavecargo()
    async with state.proxy() as data:
        a=(pk,data['name'],data['savemethod'],data['countcargo'],data['typecargo'],data['photo'])    
        res=cur1.execute('SELECT Codewarehouse FROM Warehouse WHERE Namewarehouse = ?',(data['namewarehouse'],))
        codewarehouse=res.fetchone()
        if(codewarehouse!=None):
            keyone=maxcountnote()
            a1=(keyone,pk,sum(codewarehouse,0))
            cur1.execute('INSERT INTO Cargo VALUES (?,?,?,?,?,?)',tuple(a))
            cur1.execute('INSERT INTO Notewarehousewarehouse VALUES (?,?,?)',tuple(a1))
            base1.commit()
            number=firstkeynote(pk)

            img=qrcode.make(pk)
            strphoto='./photos/'+str(pk)+'.png'
            print(strphoto)
            img.save(strphoto)


            text="Дані успішно завантажені в БД. Накладна на вантаж у складі сформована №"+str(number)+"\nСтворений QR-code вантажу"
            await bot.send_message(message.from_user.id,text,reply_markup=kbwarehouse) 
            await bot.send_photo(message.from_user.id, open(strphoto, 'rb'))

        else:
            await bot.send_message(message.from_user.id,"Ве ввели невірно назву складу або його не існує",reply_markup=kbwarehouse) 

           # file_info = await bot.get_file(message.photo[len(message.photo)-1].file_id)
   #     downloaded_file = await bot.download_file(file_info.file_path)
    #    src=file_info.file_path
     #   with open(src, 'wb') as new_file:
      #      new_file.write(downloaded_file.getvalue())
       # await databasepy.dbsavecargo(state,message,file_info)
        #await databasepy.dbkbnext(message,state)
        #await state.finish()
    cur1.close()

def firstkeynote(pk):
    cur1=base1.cursor()
    key="SELECT Codenotew FROM Notewarehousewarehouse WHERE Codecargo="+str(pk)
    result=cur1.execute(key)
    key1=result.fetchone()
    cur1.close()
    return sum(key1,0)

def maxcountsavecargo():
    try:
        cur1=base1.cursor()
        result=cur1.execute('SELECT MAX(CodeCargo) FROM Cargo')
        pos=result.fetchone()
        cur1.close()
        return sum(pos,1)
    except Exception as e:
        return 1

def maxcountnote():
    try:
        cur1=base1.cursor()
        result=cur1.execute('SELECT MAX(Codenotew) FROM Notewarehousewarehouse')
        pos=result.fetchone()
        cur1.close()
        return sum(pos,1)
    except Exception as e:
        return 1

async def demonstwareh(message):#демонстрація даних про склад
    try:
        cur1=base1.cursor()
        sql="SELECT Codewarehouse, Area, Staff,Namecompany,Namewarehouse,Warehouse.City,Warehouse.Street,Warehouse.Home FROM Warehouse INNER JOIN Company ON Warehouse.Codewarehouse=Company.Codecompany"
        cur1.execute(sql)
        demonst=cur1.fetchall()
        for strone in demonst:
            str=strone
            await bot.send_message(message.from_user.id,"Порядковий номер: {0}. Площа складу: {1}. Штат робітників: {2}. Назва компанії складу: {3}. Назва складу: {4}. Місто: {5}. Вулиця: {6}. Будинок: {7}.".format(str[0],str[1],str[2],str[3],str[4],str[5],str[6],str[7]))
        cur1.close()
    except Exception as e:
        await bot.send_message(message.from_user.id,"Даних в таблиці не існує, додайте дані!") 
#####################################################логіст#################################################
############################################дані про геопозицію в бд########################################

async def geodanbdprint(message,state):
    cur1=base1.cursor()
    async with state.proxy() as data:
        cur1.execute("SELECT Latitude,Longitude FROM driverman INNER JOIN Cardriverman ON driverman.Codedriverman=Cardriverman.Codedriverman INNER JOIN Car ON Cardriverman.CodeCar=Car.Codecar INNER JOIN Delivery ON Car.Codecar=Delivery.Codecar WHERE Codedelivery = ?",(data['g'],))
        
    demonst=cur1.fetchone()

    textt=str(demonst)
    print(textt[2])
    if(demonst==None):
         await bot.send_message(message.from_user.id,'Ви ввели невірно номер транспортної накладної або ії не існує')
    else:
        if(textt[2]=='1'):
            await bot.send_message(message.from_user.id,'Водій не додав координат')
        else:
            if(demonst!=None and textt!='1', '1'):
                await bot.send_message(message.from_user.id,'Вантаж розташований за даною геопозицією')
                await bot.send_location(message.from_user.id,textt[15:25],textt[2:12])
    cur1.close()
        
#########################################видалення транспортної накладної логіст################################################

async def deletenote(message,state):
    try:
        cur1=base1.cursor()
        async with state.proxy() as data:
            cur1.execute("SELECT Cityload FROM Delivery WHERE Codedelivery = ?",(data['codenote'],))
            demonst=cur1.fetchone()
            if(demonst==None):
                await bot.send_message(message.chat.id,'ТП накладної не існує')
            else:
                cur1.execute("DELETE FROM Delivery WHERE Codedelivery = ?",(data['codenote'],))
                base1.commit()
                await bot.send_message(message.chat.id,'Дані успішно видалено')
        cur1.close()
    except Exception as e:
        await bot.send_message(message.chat.id,"Щось не так...Перевірте чи правильно ви ввели номер транспортної накладної. Спробуйте знову")
##############################################################додавання даних########################################

async def addcompany(message,state): # додавання даних про компанію
    cur1=base1.cursor()
    pk=maxcountcompany()
    async with state.proxy() as data:
        if(data['EDRPOY'].isnumeric()==True):
            if(data['EDRPOY'].isnumeric()==True):
                if(len(data['EDRPOY'])==8):
                    if(data['IPP'].isnumeric()==True):
                        if(len(data['IPP'])==7):
                            if(data['MFO'].isnumeric()==True):
                                if(data['Phone'].isnumeric()==True):
                                    if(len(data['Phone'])==10):
                                        if(data['Phone'][0]=='0'):
                                            phone='+38'+data['Phone']
                                            a=(pk,data['namecompany'],data['numbertreaty'],data['EDRPOY'],data['IPP'],data['MFO'],phone,data['City'],data['Street'],data['Home'])    
                                            cur1.execute('INSERT INTO Company VALUES (?,?,?,?,?,?,?,?,?,?)',tuple(a))
                                            base1.commit()
                                            cur1.close()   
                                            await bot.send_message(message.from_user_id,"Дані успішно додано")   
                                        else:
                                            await bot.send_message(message.from_user.id,"Дані ввведено не вірно, перша цифра номеру повинна бути нуль") 
                                    else:
                                        await bot.send_message(message.from_user.id,"Дані ввведено не вірно, довжина номеру повинна бути 10")
                                else:
                                    await bot.send_message(message.from_user.id,"Дані ввведено не вірно, номер телефону не повинен бути з символами")
                            else:
                                await bot.send_message(message.from_user.id,"Дані ввведено не вірно, МФО код повинен бути з цифр")
                        else:
                            await bot.send_message(message.from_user.id,"Дані ввведено не вірно, довжина ІПП 7 цифр")
                    else:
                        await bot.send_message(message.from_user.id,"Дані ввведено не вірно, ІПП повинен бути з цифр")
                else:
                    await bot.send_message(message.from_user.id,"Дані ввведено не вірно, довжина ЄДРПОУ повинна бути 8")
            else:
                await bot.send_message(message.from_user.id,"Дані ввведено не вірно, договір складається лише з цифр")


def maxcountcompany():# пошук максимального числа рядків в таблиці
    try:
        cur1=base1.cursor()
        result=cur1.execute('SELECT MAX(Codecompany) FROM Company')
        pos=result.fetchone()
        cur1.close()
        return sum(pos,1)
    except Exception as e:
        return 1

def maxcountcargo():# пошук максимального числа рядків в таблиці
    try:
        cur1=base1.cursor()
        result=cur1.execute('SELECT MAX(CodeCargo) FROM Cargo')
        pos=result.fetchone()
        cur1.close()
        return sum(pos,1)
    except Exception as e:
        return 1

async def addwarehouse(message,state): # додавання даних про компанію
    try:
                cur1=base1.cursor()
                pk=maxcountwarehouse()
                async with state.proxy() as data:
                    if(data['area'].isnumeric()==True):
                        if(data['staff'].isnumeric()==True):
                            resm=cur1.execute("SELECT Codecompany FROM Company WHERE IPP = ?",(data['ipp'],))
                            codecompany=resm.fetchone()
                            a=(pk,data['area'],data['staff'],sum(codecompany,0),data['name'],data['city'],data['street'],data['home'])    
                            cur1.execute('INSERT INTO Warehouse VALUES (?,?,?,?,?,?,?,?)',tuple(a))
                            base1.commit()
                            cur1.close()
                            await bot.send_message(message.from_user.id,"Дані успішно завантажені в БД") 
                        else:
                            await bot.send_message(message.from_user.id,"Кількість робітників складу не повинна мати символів")
                    else:
                        await bot.send_message(message.from_user.id,"Площа складу не повинна мати символів")
    except Exception as e:
        await bot.send_message(message.from_user.id,"Ви ввели не вірно дані. Спробуйте знову")

def maxcountwarehouse():# пошук максимального числа рядків в таблиці
    try:
        cur1=base1.cursor()
        result=cur1.execute('SELECT MAX(Codewarehouse) FROM Warehouse')
        pos=result.fetchone()
        cur1.close()
        return sum(pos,1)
    except Exception as e:
        return 1

######################################################додавання даних адміністратором(логіст,водія,складальник)###########################################################
######################################################додавання даних адміністратором водія ##############################################################################
async def adddrivermanbd(message,state):# додавання даних про водія
    cur1=base1.cursor()
    pk=maxcountdriverman()
    async with state.proxy() as data:
        if(len(data['phone'])==10):
            if(data['phone'][0]=='0'):
                phone='+38'+data['phone']
                a=(pk,data['surname'],data['name'],data['middlename'],data['email'],phone,data['login'],data['password'],1,1)
                cur1.execute('INSERT INTO Driverman VALUES (?,?,?,?,?,?,?,?,?,?)',tuple(a))
                base1.commit()
                await bot.send_message(message.from_user.id,"Водія зареєстровано успішно") 
                cur1.close()
            else:
                await bot.send_message(message.from_user.id,"Дані ввведено не вірно, перша цифра номеру повинна бути нуль") 
        else:
            await bot.send_message(message.from_user.id,"Дані ввведено не вірно, довжина номеру повинна бути 10")
   

def maxcountdriverman():# пошук максимального числа рядків в таблиці
    try:
        cur1=base1.cursor()
        result=cur1.execute('SELECT MAX(Codedriverman) FROM Driverman')
        pos=result.fetchone()
        return sum(pos,1)
        cur1.close()
    except Exception as e:
        return 1
######################################################додавання даних адміністратором логіста ############################################################################
async def addlogistbd(message,state):# додавання даних про водія
    cur1=base1.cursor()
    pk=maxcountlogist()
    codlc=maxcountoflc()
    async with state.proxy() as data:
        if(len(data['phone'])==10):
            if(data['phone'][0]=='0'):
                if(data['IPP'].isnumeric()==True):
                    if(len(data['IPP'])==7):
                        phone='+38'+data['phone']
                        company=cur1.execute('SELECT Codecompany FROM Company WHERE IPP = ?',(data['IPP'],))
                        companykey=company.fetchone()

                        a=(pk,data['surname'],data['name'],data['middlename'],data['email'],phone,data['login'],data['password'])    
                        a1=(codlc,pk,sum(companykey,0))
                        cur1.execute('INSERT INTO Logist VALUES (?,?,?,?,?,?,?,?)',tuple(a))
                        cur1.execute('INSERT INTO CompanyLogist VALUES (?,?,?)',tuple(a1))
                        base1.commit()
                        cur1.close()
                        await bot.send_message(message.from_user.id,"Логіста зареєстровано успішно") 
                    else:
                        await bot.send_message(message.from_user.id,"Дані введено не вірно, код ІПП повинен бути 7 циифр")
                else:
                    await bot.send_message(message.from_user.id,"Дані введено не вірно, код ІПП повинен бути без символів")    
            else:
                await bot.send_message(message.from_user.id,"Дані ввведено не вірно, перша цифра номеру повинна бути нуль") 
        else:
            await bot.send_message(message.from_user.id,"Дані ввведено не вірно, довжина номеру повинна бути 10")
    
def maxcountlogist():# пошук максимального числа рядків в таблиці логіст
    try:
        cur1=base1.cursor()
        result=cur1.execute('SELECT MAX(Codelogist) FROM Logist')
        pos=result.fetchone()
        cur1.close()
        return sum(pos,1)
    except Exception as e:
        return 1
def maxcountoflc():# пошук максимального числа рядків в таблиці логісткомпанія
    try:
        cur1=base1.cursor()
        result=cur1.execute('SELECT MAX(CodeCL) FROM CompanyLogist')
        pos=result.fetchone()
        cur1.close()
        return sum(pos,1)
    except Exception as e:
        return 1
######################################################додавання даних адміністратором складальника ############################################################################
async def addwarehouseman(message,state):# додавання даних про водія
    cur1=base1.cursor()
    pk=maxcountwarehouseman()
    codww=maxcoutwarehouseandman()
    async with state.proxy() as data:
        if(len(data['phone'])==10):
            if(data['phone'][0]=='0'):
                phone='+38'+data['phone']
                a=(pk,data['surname'],data['name'],data['middlename'],data['email'],phone,data['login'],data['password'])    
                a1=(codww,data['address'],pk)
                cur1.execute('INSERT INTO Warehouseman VALUES (?,?,?,?,?,?,?,?)',tuple(a))
                cur1.execute('INSERT INTO WarehouseWarehouseman VALUES (?,?,?)',tuple(a1))
                base1.commit()
                await bot.send_message(message.from_user.id,"Складальника зареєстровано успішно")
                cur1.close()
            else:
                await bot.send_message(message.from_user.id,"Дані ввведено не вірно, перша цифра номеру повинна бути нуль") 
        else:
            await bot.send_message(message.from_user.id,"Дані ввведено не вірно, довжина номеру повинна бути 10")
        

def maxcountwarehouseman():# пошук максимального числа рядків в таблиці
    try:
        cur1=base1.cursor()
        result=cur1.execute('SELECT MAX(Codewman) FROM Warehouseman')
        pos=result.fetchone()
        cur1.close()
        return sum(pos,1)
    except Exception as e:
        return 1
def maxcoutwarehouseandman():# пошук максимального числа рядків в таблиці складускладальника
    try:
        cur1=base1.cursor()
        result=cur1.execute('SELECT MAX(CodeWW) FROM WarehouseWarehouseman')
        pos=result.fetchone()
        cur1.close()
        return sum(pos,1)
    except Exception as e:
        return 1
    
################################################################################################################################################################################
async def addcarbd(message,state):# додавання даних про автомобіль
    cur1=base1.cursor()
    pk=maxcountcar()
    pkkey=maxcoutcardriverman()
    async with state.proxy() as data:
        a=(pk,data['namecar'],data['numbercar'],data['typecar'])    
        a1=(pkkey,pk,driver[2])
    cur1.execute('INSERT INTO Car VALUES (?,?,?,?)',tuple(a))
    base1.commit()
    cur1.execute('INSERT INTO Cardriverman VALUES (?,?,?)',tuple(a1))
    base1.commit()
    await bot.send_message(message.from_user.id,"Дані успішно завантажені в базу даних",reply_markup=kbdriver)
    cur1.close()

def maxcountcar():# пошук максимального числа рядків в таблиці
    try:
        cur1=base1.cursor()
        result=cur1.execute('SELECT MAX(Codecar) FROM Car')
        pos=result.fetchone()
        cur1.close()
        return sum(pos,1)
    except Exception as e:
        return 1
def maxcoutcardriverman():
    try:
        cur1=base1.cursor()
        result=cur1.execute('SELECT MAX(Codecardriver) FROM Cardriverman')
        pos=result.fetchone()
        cur1.close()
        return sum(pos,1)
    except Exception as e:
        return 1

async def addrout(message,state):# додавання даних про автомобіль
    cur1=base1.cursor()
    pk=maxdel()
    async with state.proxy() as data:

        car=cur1.execute('SELECT Codecar FROM Car WHERE Numbercar = ?',(data['Numbercar'],))
        codecar=car.fetchone()

        load=cur1.execute('SELECT Company.Codecompany,Company.City FROM Company INNER JOIN Warehouse ON Company.Codecompany=Warehouse.CodeCompany INNER JOIN Notewarehousewarehouse ON Warehouse.Codewarehouse=Notewarehousewarehouse.Codewarehouse WHERE Notewarehousewarehouse.Codenotew = ?',(data['numbernaklanda'],))
        loadcity=load.fetchone()
        
        unload=cur1.execute('SELECT City FROM Company WHERE Code_EDRPOY = ?',(data['ippload'],))
        unloadcity=unload.fetchone()

        cargo=cur1.execute('SELECT Cargo.Codecargo FROM Cargo INNER JOIN Notewarehousewarehouse ON Cargo.CodeCargo=Notewarehousewarehouse.Codecargo WHERE Codenotew = ?',(data['numbernaklanda'],))
        numbercargo=cargo.fetchone()

        a=(pk,loadcity[1],unloadcity[0],data['time'],loadcity[0],sum(codecar,0), sum(numbercargo,0))
        
    cur1.execute('INSERT INTO Delivery VALUES (?,?,?,?,?,?,?)',tuple(a))
    base1.commit()
    await bot.send_message(message.from_user.id,"Створено накладну за номером №"+str(pk)) 
    cur1.close()

def funccodecompany(name):
    cur1=base1.cursor()
    sql="SELECT Codecompany FROM Company WHERE Namecompany="+str(name)
    cur1.execute(sql)
    demonst=cur1.fetchall()
    cur1.close()
    return demonst

def funccodecargo(ncargo):
    cur1=base1.cursor()
    sql="SELECT CodeCargo FROM Cargo WHERE Namecargo="+str(ncargo)
    cur1.execute(sql)
    demonst=cur1.fetchall()
    cur1.close()
    return sum(demonst,0)

def maxdel():# пошук максимального числа рядків в таблиці
    try:
        cur1=base1.cursor()
        result=cur1.execute('SELECT MAX(Codedelivery) FROM Delivery')
        pos=result.fetchone()
        cur1.close()
        return sum(pos,1)
    except Exception as e:
        return 1
###########################виведення інформації логіст########################################

async def demonstrcompany(message):# демонстрація даних компанії
    try:
        cur1=base1.cursor()
        sql="SELECT CodeCompany,Namecompany,Numbertreaty,Code_EDRPOY,IPP,MFO,Phone,City,Street,Home FROM Company"
        cur1.execute(sql)
        demonst=cur1.fetchall()
        for strone in demonst:
            str=strone
            await bot.send_message(message.from_user.id,"Порядковий номер: {0}. Назва компанії: {1}. Номер договору: {2}. Код ЄДРПОУ: {3}. код ІПП: {4}. Код МФО: {5}. Номер телефону: {6}.  Місто: {7}. Вулиця: {8}. Будинок: {9}.".format(str[0],str[1],str[2],str[3],str[4],str[5],str[6],str[7],str[8],str[9]))
        cur1.close()
    except Exception as e:
        await bot.send_message(message.from_user.id,"Даних в таблиці не існує, додайте дані!") 
  
async def demonstrcargo(message): #демонстрація даних вантажу
    try:
        cur1=base1.cursor()
        sql="SELECT CodeCargo, Namecargo,savemethod,Generaltonnage,QRcipher FROM Cargo"
        cur1.execute(sql)
        demonst=cur1.fetchall()
        for strone in demonst:
            str=strone
            await bot.send_message(message.from_user.id,"Порядковий номер: {0}. Назва вантажу: {1}. Метод зберігання: {2}. Загальна тонажність: {3}. Місність вантажу: {4}. ".format(str[0],str[1],str[2],str[3],str[4]))
        cur1.close()
    except Exception as e:
        await bot.send_message(message.from_user.id,"Даних в таблиці не існує, додайте дані!") 

async def demonstrcar(message): #демонстрація даних автомобіля
    try:
        cur1=base1.cursor()
        sql="SELECT Codecar,Namecar, Numbercar,Typecar FROM Car"
        cur1.execute(sql)
        demonst=cur1.fetchall()
        for strone in demonst:
            str=strone
            await bot.send_message(message.from_user.id,"Порядковий номер: {0}. Назва автомобіля: {1}. Номер автомобіля: {2}. Тип автомобіля: {3}.".format(str[0],str[1],str[2],str[3]))
        cur1.close()
    except Exception as e:
        await bot.send_message(message.from_user.id,"Даних в таблиці не існує, додайте дані!") 
    
async def demonstrdriverman(message): #демонстрація даних водія
    try:
        cur1=base1.cursor()
        sql="SELECT Codedriverman,Surname,Name,Middlename,Email,Phone FROM driverman"
        cur1.execute(sql)
        demonst=cur1.fetchall()
        for strone in demonst:
            str=strone
            await bot.send_message(message.from_user.id,"Порядковий номер: {0}. Прізвище водія: {1}. Ім'я водія: {2}. По батькові: {3}. Електрона скринька: {4}. Телефонний номер: {5}.".format(str[0],str[1],str[2],str[3],str[4],str[5]))
        cur1.close()
    except Exception as e:
        await bot.send_message(message.from_user.id,"Даних в таблиці не існує, додайте дані!") 

######################################водій################################################################
async def geodanbd(message):# додавання геопозиції в БД
    try:
        cur1=base1.cursor()
        a=(message.location.longitude,message.location.latitude,driver[1])
        cur1.execute('UPDATE driverman SET latitude=?,longitude=? WHERE driverman.Surname=?',tuple(a))
        base1.commit()
        await bot.send_message(message.from_user.id,"Дані успішно передані логісту. Дякую, що користуєтесь нашою системою",reply_markup=kbdriver)
        cur1.close()
    except:
        await bot.send_message(message.from_user.id,"Помилка. Перезайдіть в особистий кабінет")
 
        
async def reportvoidy(message,state):
    try:
        cur1=base1.cursor()
        async with state.proxy() as data:#накладна транспортування
            cur1.execute("SELECT Driverman.Surname,Driverman.Name,Driverman.Middlename,Namecargo,Cityload,Cityunload,Generaltonnage,Namecar,Numbercar,Typecar,data,Namecompany,Company.Phone,Driverman.Phone FROM Delivery INNER JOIN Car ON Delivery.Codecar=Car.Codecar INNER JOIN Cardriverman ON Car.CodeCar=Cardriverman.CodeCar INNER JOIN Driverman ON Cardriverman.Codedriverman=Driverman.Codedriverman INNER JOIN Company ON Delivery.Codecompany=Company.Codecompany INNER JOIN Cargo ON Delivery.CodeCargo=Cargo.CodeCargo WHERE Delivery.Codedelivery=?",(data['g'],))
        demonst=cur1.fetchone()
        await bot.send_message(message.from_user.id,"Водій: {0} {1} {2} перевозить вантаж: {3} з міста: {4} до міста: {5}, масою: {6} тон(а) на автомобілі: {7} з номерами: {8}, використовуючи прицеп: {9}. Орієнтований час доставлення: {10}. Назва компанії: {11}.\nКонтактний номер компанії: {12}.\nКонтактний номер водія: {13}".format(demonst[0],demonst[1],demonst[2],demonst[3],demonst[4],demonst[5],demonst[6],demonst[7],demonst[8],demonst[9],demonst[10],demonst[11],demonst[12],demonst[13]))
        cur1.close()
    except Exception as e:
        await bot.send_message(message.from_user.id,"Накладної за даним номером не існує, спробуйте знову")

async def reportwarehouse(message,state):# накладна складу
    try:
        cur1=base1.cursor()
        async with state.proxy() as data:
            cur1.execute("SELECT Namecargo,savemethod,Generaltonnage,QRcipher,Namewarehouse,Warehouse.City,Warehouse.Street,Warehouse.Home,Namecompany,Phone,Typecargo FROM Notewarehousewarehouse INNER JOIN Cargo ON Notewarehousewarehouse.Codecargo=Cargo.CodeCargo INNER JOIN Warehouse ON Notewarehousewarehouse.Codewarehouse=Warehouse.Codewarehouse INNER JOIN Company ON Warehouse.CodeCompany=Company.Codecompany WHERE Notewarehousewarehouse.Codenotew = ?",(data['g'],))
        demonst=cur1.fetchone()
        await bot.send_message(message.from_user.id,"Вантаж: {0}, зберігається за допомогою: {1}, загальною тонажністю: {2} тон(а), маючи міцність: {3} та тип: {10}, розташован на складі: {4}, Місто: {5}, вулиця: {6}, будинок: {7}, компанії: {8}, контактний номер телефону компанії: {9}.".format(demonst[0],demonst[1],demonst[2],demonst[3],demonst[4],demonst[5],demonst[6],demonst[7],demonst[8],demonst[9],demonst[10]))
        cur1.close()
    except Exception as e:
        await bot.send_message(message.from_user.id,"Накладної за даним номером не існує, спробуйте знову")

######################################адміністратор################################################################
async def addjob(message,state):# додавання даних про водія
    cur1=base1.cursor()
    pk=maxwoker()
    async with state.proxy() as data:
        a=(pk,data['surname'],data['name'],data['middlename'],data['email'],data['phone'],data['login'],data['password'],data['codcompany'],data['pos'])    
    cur1.execute('INSERT INTO Worker VALUES (?,?,?,?,?,?,?,?,?,?)',tuple(a))
    base1.commit()
    cur1.close()
    await bot.send_message(message.from_user.id,"Дані успішно завантажені в БД") 

def maxwoker():# пошук максимального числа рядків в таблиці
    try:
        cur1=base1.cursor()
        result=cur1.execute('SELECT MAX(Codeworker) FROM Worker')
        pos=result.fetchone()
        cur1.close()
        return sum(pos,1)
    except Exception as e:
        return 1

async def demonstlogistdb(message): #для адміна демонстрація логістів
    try:
        cur1=base1.cursor()
        sql="SELECT Logist.Codelogist,Surname,Name,Middlename,Email,Logist.Phone,Login,Password,Namecompany FROM Logist INNER JOIN CompanyLogist ON Logist.Codelogist=CompanyLogist.Codelogist INNER JOIN Company ON CompanyLogist.CodeCompany=Company.Codecompany"
        cur1.execute(sql)
        demonst=cur1.fetchall()
        for strone in demonst:
            str=strone
            await bot.send_message(message.from_user.id,"Порядковий номер: {0}. Прізвище: {1}. Ім'я: {2}. По батькові: {3}. Електрона адреса: {4}. Номер телефону: {5}. Логін: {6}. Пароль: {7}. Назва компанії з якою працює: {8}".format(str[0],str[1],str[2],str[3],str[4],str[5],str[6],str[7],str[8]))
        cur1.close()
    except Exception as e:
        await bot.send_message(message.from_user.id,"Даних про логістів не існує")

async def demonstdrivermandb(message): #для адміна демонстрація водіїв
    try:
        cur1=base1.cursor()
        await bot.send_message(message.from_user.id,"Підказка:якщо дані працівника не виведено на екран, зачекайте водій прив'язує до себе автомобіль")
        sql="SELECT Driverman.Codedriverman,Surname,Name,Middlename,Email,Driverman.Phone,Login,Password,Namecar,Numbercar,Typecar FROM Driverman INNER JOIN Cardriverman ON Driverman.Codedriverman=Cardriverman.Codedriverman INNER JOIN Car ON Cardriverman.CodeCar=Car.CodeCar"
        cur1.execute(sql)
        demonst=cur1.fetchall()
        print(demonst)
        for strone in demonst:
            str=strone
            await bot.send_message(message.from_user.id,"Порядковий номер: {0}. Прізвище: {1}. Ім'я: {2}. По батькові: {3}. Електрона адреса: {4}. Номер телефону: {5}. Логін: {6}. Пароль: {7}. Назва автомобіля з яким працює: {8}. Номер автомобіля: {9}. Тип автомобіля: {10}.".format(str[0],str[1],str[2],str[3],str[4],str[5],str[6],str[7],str[8],str[9],str[10]))
        cur1.close()
    except Exception as e:
        await bot.send_message(message.from_user.id,"Даних про водіїв не існує або водій не прив'язав автомобіль")

async def demonstwarehousemandb(message): #для адміна демонстрація складальників
    try:
        cur1=base1.cursor()
        sql="SELECT Warehouseman.Codewman,Surname,Name,Middlename,Email,Phone,Login,Password,Namewarehouse,City,Street,Home FROM Warehouseman INNER JOIN WarehouseWarehouseman ON Warehouseman.Codewman=WarehouseWarehouseman.Codewarehouseman INNER JOIN Warehouse ON WarehouseWarehouseman.Codewarehouse=Warehouse.Codewarehouse"
        cur1.execute(sql)
        demonst=cur1.fetchall()
        for strone in demonst:
            str=strone
            await bot.send_message(message.from_user.id,"Порядковий номер: {0}. Прізвище: {1}. Ім'я: {2}. По батькові: {3}. Електрона адреса: {4}. Номер телефону: {5}. Логін: {6}. Пароль: {7}. Назва складу на якому працює: {8}. Адреса складу. Місто {9}. Вулиця {10}. Будинок {11}.".format(str[0],str[1],str[2],str[3],str[4],str[5],str[6],str[7],str[8],str[9],str[10],str[11]))
        cur1.close()
    except Exception as e:
        await bot.send_message(message.from_user.id,"Даних про складальників не існує")

async def demonstwarehouse(message): #для адміна демонстрація складів
    try:
        cur1=base1.cursor()
        sql="SELECT Codewarehouse,Area,Staff,Namecompany,Namewarehouse,Warehouse.City,Warehouse.Street,Warehouse.Home FROM Warehouse INNER JOIN Company ON Warehouse.CodeCompany=Company.Codecompany"
        cur1.execute(sql)
        demonst=cur1.fetchall()
        for strone in demonst:
            str=strone
            await bot.send_message(message.from_user.id,"Порядковий номер: {0}. Площа складу: {1}. Штат робітників складу: {2}. Компанія, якій належить склад: {3}. Назва складу: {4}. Адреса. Місто: {5}. Вулиця: {6}. Будинок: {7}.".format(str[0],str[1],str[2],str[3],str[4],str[5],str[6],str[7]))
        cur1.close()
    except Exception as e:
        await bot.send_message(message.from_user.id,"Даних про склад не існує")

async def deleteworker(message,state):
    cur1=base1.cursor()
    async with state.proxy() as data:
        driverman=cur1.execute('SELECT Codedriverman FROM Driverman WHERE Surname=? and Phone=?',(tuple(data.values())))
        drivermannew=driverman.fetchone()
            
        logist=cur1.execute('SELECT Codelogist FROM Logist WHERE Surname=? and Phone=?',(tuple(data.values())))
        logistnew=logist.fetchone()

        warehouseman=cur1.execute('SELECT Codewman FROM Warehouseman WHERE Surname = ? and Phone=?',(tuple(data.values())))
        warehousemannew=warehouseman.fetchone()

    if(drivermannew!=None):
        sql="Delete FROM Driverman WHERE Codedriverman="+str(sum(drivermannew,0))
        cur1.execute(sql)
        base1.commit
        await bot.send_message(message.chat.id,"Водія видалено з системи")
    else:
        if(logistnew!=None):
            sql1="Delete FROM Logist WHERE Codelogist="+str(sum(logistnew,0))
            cur1.execute(sql1)
            base1.commit
            await bot.send_message(message.chat.id,"Логіста видалено з системи")
        else:
            if(warehousemannew!=None):
                sql2="Delete FROM Warehouseman WHERE Codewman="+str(sum(warehousemannew,0))
                cur1.execute(sql2)
                base1.commit
                await bot.send_message(message.chat.id,"Складальника видалено з системи")
            else:
                await bot.send_message(message.chat.id,"Працівника за вашими даними не існує")
    cur1.close()
        
async def deletecompany(message,state):
    try:
        cur1=base1.cursor()
        async with state.proxy() as data:
            if(data['IPP']==None):
                await bot.send_message(message.chat.id,"Ви ввели невірно IPP або дані відсутні") 
            else:
                sql="Delete FROM Company WHERE IPP="+data['IPP']
                cur1.execute(sql)
                base1.commit
                await bot.send_message(message.chat.id,"Компанію успішно видалено")
        cur1.close()
    except Exception as e:
        await bot.send_message(message.from_user.id,"Дані відстуні за даним кодом ІПП")
    

async def deletewarehouse(message,state):
    cur1=base1.cursor()
    async with state.proxy() as data:
        if(data['codekey']==None):
            await bot.send_message(message.chat.id,"Ви ввели невірно порядковий номер або дані складів відсутні") 
        else:
            sql="Delete FROM Warehouse WHERE Codewarehouse="+data['codekey']
            cur1.execute(sql)
            base1.commit
            await bot.send_message(message.chat.id,"Склад успішно видалено")
    cur1.close()
       
       
    












    
   
