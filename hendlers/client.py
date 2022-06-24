from email.message import Message
import io
from multiprocessing import Condition
import os
from pyzbar.pyzbar import decode
from PIL import Image
from io import BytesIO
from aiogram import types,Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from numpy import equal, sign
from create_bot import dp, bot
from mybd import databasepy
from aiogram.dispatcher.filters import Text
from keybords import kbautho,kbdriver,kblogist1,kblogist3,kblogist2,kblogist,kbdrive1,kbmenustart,kbdriwe,kbwareh,kbadmin1,kbmethodsave,kbwarehouse,kbtypecargo,kbqrcode,kblogist5,kbtypecar
#################################################складальник###################################################################
class savecargoo(StatesGroup):#клас для додавання(складальник)
    name=State()
    savemethod=State()
    countcargoo=State()
    namewarehouse=State()
    typecargo=State()
    photo=State()

class deletecargoo(StatesGroup):#клас видалення(складальник)
    deletecargoo=State()
class demonst(StatesGroup):
    key=State()

#################################################логіст###################################################################
class car(StatesGroup):# #клас додавання даних про автомобіль
    namecar=State()
    numbercar=State()
    typecar=State()

class delivery(StatesGroup): #клас додавання даних про доставку
    cityunload=State()
    time=State()
    Numbecar=State()
    Namecargo=State()

class deletenote(StatesGroup): #для виделення транспортної накладної
    codenote=State()

class demonstgeopoz(StatesGroup): #демострація геопозиції клас
    surname=State()

class logininprogramm(StatesGroup):#клас для індефікації в програмі логіста
    login=State()
    password=State()

class loginingdrive(StatesGroup):#клас для індефікації в програмі водія
    login=State()
    password=State()

class loginingwareh(StatesGroup):#клас для індефікації в програмі складальника
    login=State()
    password=State()

class loginingadmin(StatesGroup):#клас для індефікації в програмі адміністрнатора
    login=State()
    password=State()

class nakladna(StatesGroup):
    surname=State()

class nakladnaqr(StatesGroup):
    photo=State()

class naklandawarehouse(StatesGroup):
    key=State()

################################################функції входу####################################################################################
async def command_start(message:types.Message):#початок роботи з телеграм ботом
    try:
        await bot.send_message(message.from_user.id,'Вітаємо в Cargogood',reply_markup=kbmenustart)
    except:
        await message.reply('Діалог з ботом можливий тільки через особисте повідомлення:\n @Cargogoodbot')

async def menulogist(message:types.Message):
    await bot.send_message(message.from_user.id,'Увійдіть в особистий кабінет',reply_markup=kbautho)

async def menudriverman(message:types.Message):
    await bot.send_message(message.from_user.id,'Увійдіть в особистий кабінет',reply_markup=kbdriwe)

async def menuwarehouseman(message:types.Message):
    await bot.send_message(message.from_user.id,'Увійдіть в особистий кабінет',reply_markup=kbwareh)

async def menuadmin(message:types.Message):
    await bot.send_message(message.from_user.id,'Увійдіть в особистий кабінет',reply_markup=kbadmin1)

######################################вхід у програму логіста######################################################################
async def log_startlogist(message:types.Message):# запуск машини стану для входу в програму логіста
    await logininprogramm.login.set()
    await bot.send_message(message.chat.id,'Введіть логін')

async def load_loginlogist(message:types.Message,state=FSMContext):# введення даних логіну, машина стану логіста
    async with state.proxy() as autho:
        autho['login']=message.text
    await logininprogramm.next()
    await bot.send_message(message.chat.id,'Введіть пароль')
      

async def load_passwordlogist(message:types.Message,state=FSMContext):# введення даних паролю, машина стану логіста
    async with state.proxy() as passw:
        passw['password']=message.text
    await databasepy.sqllogist(state)
    await bot.send_message(message.chat.id,'Натисніть на кнопку ✅Підтвердити')
    await state.finish()

async def loadfinishcllogist(message:types.Message):#перенесення даних в хедер-файл БД логіста
    await databasepy.logistfinish(message)

#####################################вхід  у програму водія################################################################################################
async def log_startdriverman(message:types.Message):# запуск машини стану для входу в програму водія
    await loginingdrive.login.set()
    await bot.send_message(message.chat.id,'Введіть логін')

async def load_logindriverman(message:types.Message,state=FSMContext):# введення даних логіну, машина стану водія
    async with state.proxy() as autho:
        autho['login']=message.text
    await loginingdrive.next()
    await bot.send_message(message.chat.id,'Введіть пароль')
      

async def load_passworddriverman(message:types.Message,state=FSMContext):# введення даних паролю, машина стану водія
    async with state.proxy() as passw:
        passw['password']=message.text
    await databasepy.sqldriverman(state)
    await bot.send_message(message.chat.id,'Натисніть на кнопку ✔Підтвердити')
    await state.finish()

async def loadfinishcldriverman(message:types.Message):#перенесення даних в хедер-файл БД водія
    await databasepy.drivermanfinish(message)

#####################################вхід з у програму складальника################################################################################################
async def log_startwarehouseman(message:types.Message):# запуск машини стану для входу в програму складальника
    await loginingwareh.login.set()
    await bot.send_message(message.chat.id,'Введіть логін')

async def load_loginwarehouseman(message:types.Message,state=FSMContext):# введення даних логіну, машина стану складальника
    async with state.proxy() as autho:
        autho['login']=message.text
    await loginingwareh.next()
    await bot.send_message(message.chat.id,'Введіть пароль')
      

async def load_passwordwarehouseman(message:types.Message,state=FSMContext):# введення даних паролю, машина стану складальника
    async with state.proxy() as passw:
        passw['password']=message.text
    await databasepy.sqlwarehouseman(state)
    await bot.send_message(message.chat.id,'Натисніть на кнопку 🆗Підтвердити')
    await state.finish()

async def loadfinishclwarehouseman(message:types.Message):#перенесення даних в хедер-файл БД складальника
    await databasepy.warehousefinish(message)

#####################################вхід у програму адміністратора################################################################################################
async def log_startadmin(message:types.Message):# запуск машини стану для входу в програму адміністратора
    await loginingadmin.login.set()
    await bot.send_message(message.chat.id,'Введіть логін')

async def load_loginadmin(message:types.Message,state=FSMContext):# введення даних логіну, машина стану адміністратора
    async with state.proxy() as autho:
        autho['login']=message.text
    await loginingadmin.next()
    await bot.send_message(message.chat.id,'Введіть пароль')
      

async def load_passwordadmin(message:types.Message,state=FSMContext):# введення даних паролю, машина стану адміністратора
    async with state.proxy() as passw:
        passw['password']=message.text
    await databasepy.sqladmin(state)
    await bot.send_message(message.chat.id,'Натисніть на кнопку 👌Підтвердити')
    await state.finish()

async def loadfinishadmin(message:types.Message):#перенесення даних в хедер-файл БД адміністратора
    await databasepy.adminfinish(message)


###########################################додавання вантажу(складальника)######################################################################################
async def savecargostart(message:types.Message):#машину стану для складальника
    await savecargoo.name.set()
    await bot.send_message(message.chat.id,"Введіть назву вантажу")

async def savenamecargoo(message: types.Message,state=FSMContext):#машину стану для складальника(додавання)
    async with state.proxy() as data:
        data['name']=message.text
    await savecargoo.next()
    await bot.send_message(message.chat.id,"Оберіть спосіб зберігання",reply_markup=kbmethodsave)

async def savemethodcargo(message: types.Message,state=FSMContext):#машину стану для складальника(додавання)
    async with state.proxy() as data:
        data['savemethod']=message.text
    await savecargoo.next()
    await bot.send_message(message.chat.id,"Введіть тонажність вантажу",reply_markup=kbwarehouse)

async def savecargoocount(message: types.Message,state=FSMContext):#машину стану для складальника(додавання)
    async with state.proxy() as data:
        data['countcargo']=message.text
    await savecargoo.next()
    await bot.send_message(message.chat.id,"Введіть назву складу")   

async def savecargoowarecode(message: types.Message,state=FSMContext):#машину стану для складальника(додавання)
    async with state.proxy() as data:
        data['namewarehouse']=message.text
    await savecargoo.next()
    await bot.send_message(message.chat.id,"Оберіть тип продукції",reply_markup=kbtypecargo) 

async def savecargoowaretype(message: types.Message,state=FSMContext):#машину стану для складальника(додавання)
    async with state.proxy() as data:
        data['typecargo']=message.text
    await savecargoo.next()
    await bot.send_message(message.chat.id,"Оберіть тип місцності вантажу",reply_markup=kbqrcode) 

    
async def savecargoqr(message: types.Message,state=FSMContext):#машину стану для складальника(додавання)
    try:
        async with state.proxy() as data:
            data['photo']=message.text #у разі потреби використання масиву 
        await databasepy.dbkbnext(message,state)
        await state.finish()

    except Exception as e:
        await bot.send_message(message.chat.id,"Щось не так...Перевірте правельність вводу назви складу")


#######################################видалення вантажу(складальника)#####################################################################
async def deletecargowarehousestart(message:types.Message):#машину стану для складальника(видалення)
    await deletecargoo.deletecargoo.set()
    await bot.send_message(message.chat.id,"Введіть номер накладної")

async def deletecargowarehouse(message: types.Message,state=FSMContext):#машину стану для складальника(видалення)
    async with state.proxy() as data:
        data['deletecargo']=message.text
    await databasepy.deletewarehousecargoo(message,state)
    await state.finish()

##########################################демострація вантажу(складальник)####################################################################################
async def kbdemonst(message:types.Message):
    await demonst.key.set()
    await bot.send_message(message.chat.id,"Введіть порядковий номер накладної складу")

async def kbdemonst1(message: types.Message,state=FSMContext):
    try:
        async with state.proxy() as data:
            data['key']=message.text
        await databasepy.warehousedemostrate(message,state)   
        await state.finish()
    except Exception as e:
        await bot.send_message(message.chat.id,"Вантажу за даною накладною не існує або не існує накладної")

##########################################демострація даних складу(складальник)####################################################################################

async def waredemonst(message:types.Message):
    await databasepy.demonstwareh(message)

############################################логіст########################################################################################################

async def logistdemonstratiom(message:types.Message):#підключення головного меню
    await bot.send_message(message.from_user.id,'Оберіть потрібну кнопку',reply_markup=kblogist1)

async def logistdemonstratiom2(message:types.Message):#підключення меню демонстрації
    await bot.send_message(message.from_user.id,'Оберіть потрібну кнопку',reply_markup=kblogist3)
async def logistadd(message:types.Message):#підключення меню додавання
    await bot.send_message(message.from_user.id,'Оберіть потрібну кнопку',reply_markup=kblogist2)

##################################додавання даних про автомобіль##########################################################################################
async def addcar(message:types.Message): # початок машини додавання
    await car.namecar.set()
    await bot.send_message(message.chat.id,'Введіть марку автомобіля')

async def addcar1(message:types.Message,state=FSMContext):#машина стану додавання автомобіля
    async with state.proxy() as carr:
        carr['namecar']=message.text
    await car.next()
    await bot.send_message(message.chat.id,'Введіть номер автомобіля')

async def addcar2(message:types.Message,state=FSMContext):#машина стану додавання автомобіля
    async with state.proxy() as carr:
        carr['numbercar']=message.text
    await car.next()
    await bot.send_message(message.chat.id,'Оберіть тип автомобіля',reply_markup=kbtypecar)

async def addcar3(message:types.Message,state=FSMContext):#машина стану додавання автомобіля
    try:
        async with state.proxy() as carr:
            carr['typecar']=message.text
        await car.next()
        await databasepy.addcarbd(message,state)
        await state.finish()
    except Exception as e:
        await bot.send_message(message.chat.id,"Ви ввели неправильно дані, спробуйте знову",reply_markup=kbdriver)

##################################додавання даних про маршрут##########################################################################################

async def addroute(message:types.Message): # початок машини додавання
    await delivery.cityunload.set()
    await bot.send_message(message.chat.id,'Введіть ЄДРПОУ компанії вивантаження')

async def addroute1(message:types.Message,state=FSMContext):
    async with state.proxy() as rout:
        rout['ippload']=message.text
    await delivery.next()
    await bot.send_message(message.chat.id,'Введіть час прибуття вантажу (наприклад 22.02.2022)')

async def addroute2(message:types.Message,state=FSMContext):
    async with state.proxy() as rout:
        rout['time']=message.text
    await delivery.next()
    await bot.send_message(message.chat.id,'Введіть номер автомобіля')

async def addroute3(message:types.Message,state=FSMContext):
    async with state.proxy() as rout:
        rout['Numbercar']=message.text
    await delivery.next()
    await bot.send_message(message.chat.id,'Введіть номер накладної на вантаж')

async def addroute4(message:types.Message,state=FSMContext):
    try:
        async with state.proxy() as rout:
            rout['numbernaklanda']=message.text
        await delivery.next()
        await databasepy.addrout(message,state)
        await state.finish()
    except Exception as e:
        await bot.send_message(message.chat.id,"Щось не так...Перевірте правельність вводу даних та спробуйте знову")

#################################################Видалення транспортної накладної логіст###########################################################################################################
async def delnote(message:types.Message): # початок машини додавання
    await deletenote.codenote.set()
    await bot.send_message(message.chat.id,'Введіть номер накладної')

async def delnote1(message:types.Message,state=FSMContext):
    try:
        async with state.proxy() as rout:
            rout['codenote']=message.text
        await deletenote.next()
        await databasepy.deletenote(message,state)
        await state.finish()
    except Exception as e:
        await bot.send_message(message.chat.id,"Щось не так...Перевірте правельність вводу номеру накладноїта спробуйте знову")

##################################демонстарція даних логіст##########################################################################################
async def logistdemostrcompany(message:types.Message):#демонстрація даних компанії
    await databasepy.demonstrcompany(message)

async def logistdemostrcargoo(message:types.Message):#демонстрація даних вантажу
    await databasepy.demonstrcargo(message)

async def logistdemostrcar(message:types.Message):#демонстрація даних автомобіля
    await databasepy.demonstrcar(message)

async def logistdemostrdriverman(message:types.Message):#демонстрація даних логіста
    await databasepy.demonstrdriverman(message)

async def logistdemonstgeopoz(message:types.Message):#демонстрація даних геопозиції
    await demonstgeopoz.surname.set()
    await bot.send_message(message.chat.id,'Введіть номер транспортної накладної.')

async def logistdemonstgeopoz1(message:types.Message,state=FSMContext):#демонстрація даних геопозиції
    async with state.proxy() as demonst:
        demonst['g']=message.text
    await databasepy.geodanbdprint(message,state)
    await state.finish()

##################################повернення з підменю логіст в меню##########################################################################################
async def backout1(message:types.Message):
    await bot.send_message(message.from_user.id,'Назад',reply_markup=kblogist1) #з підменю в меню


#############################################################вихід з інтерфейсу програми###############################################################################################
async def backout(message:types.Message):
    await bot.send_message(message.from_user.id,'Дякую, що користуєтесь нашим додатком',reply_markup=kblogist)#вихід з програми


#################################################геопозиція логіст##########################################################################################################
async def geopoz1(message:types.Message,state=FSMContext):
    await bot.send_message(message.from_user.id,"Натисніть на кнопку Передача місцерозташування",reply_markup=kbdrive1)

async def geopoz2(message): #відправлення даних в БД
    await databasepy.geodanbd(message)


#############################################накладна вантажу/накладна транспортування########################################################

async def rep(message:types.Message):
    await bot.send_message(message.chat.id,'Оберіть спосіб',reply_markup=kblogist5)


async def repqr(message:types.Message): #накладна транспортування
    await nakladnaqr.photo.set()
    await bot.send_message(message.chat.id,'Надішліть QR-код накладної')


async def repqr1(message:types.Message,state=FSMContext): #продовження накладної транспортування
    async with state.proxy() as data:
        data['phototext']=message.text #у разі потреби використання масиву 
        file_info = await bot.get_file(message.photo[len(message.photo)-1].file_id)
        downloaded_file = await bot.download_file(file_info.file_path)
        src=file_info.file_path
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file.getvalue())
        await databasepy.dbsavecargo(state,message,file_info)
        await databasepy.dbsavecargo1(message,state)
        await state.finish()




async def report(message:types.Message): #накладна транспортування
    await nakladna.surname.set()
    await bot.send_message(message.chat.id,'Введіть номер транспортної накладної')

async def report1(message:types.Message,state=FSMContext): #продовження накладної транспортування
    async with state.proxy() as rep:
        rep['g']=message.text
    await databasepy.reportvoidy(message,state)
    await state.finish()

async def report2(message:types.Message): #накладна вантажу
    await naklandawarehouse.key.set()
    await bot.send_message(message.chat.id,'Введіть номер накладної вантажу на складі')

async def report2_2(message:types.Message,state=FSMContext): #продовження накладної вантажу
    async with state.proxy() as rep:
        rep['g']=message.text
    await databasepy.reportwarehouse(message,state)
    await state.finish()

#####################################регістрація хендлерів###################################################
def registet_hand_clients(dp:Dispatcher):

#####################################вхід в програму###################################################
    dp.register_message_handler(command_start,commands=['start','Вийти','Назад'])

    dp.register_message_handler(menulogist,Text(equals='🦸‍♂️Кабінет логіста'),state=None) #
    dp.register_message_handler(log_startlogist,Text(equals='🔑Увійти'),state=None)#######       функції аунтифікації для логіста
    dp.register_message_handler(load_loginlogist,content_types='text',state=logininprogramm.login)##
    dp.register_message_handler(load_passwordlogist,content_types='text',state=logininprogramm.password)##
    dp.register_message_handler(loadfinishcllogist,Text(equals='✅Підтвердити'))##

    dp.register_message_handler(menudriverman,Text(equals='🚛Кабінет водія'),state=None) #
    dp.register_message_handler(log_startdriverman,Text(equals='🗝Увійти'),state=None)#######       функції аунтифікації для водія
    dp.register_message_handler(load_logindriverman,content_types='text',state=loginingdrive.login)##
    dp.register_message_handler(load_passworddriverman,content_types='text',state=loginingdrive.password)##
    dp.register_message_handler(loadfinishcldriverman,Text(equals='✔Підтвердити'))##


    dp.register_message_handler(menuwarehouseman,Text(equals='📦Кабінет складальника'),state=None) #
    dp.register_message_handler(log_startwarehouseman,Text(equals='🔧Увійти'),state=None)#######       функції аунтифікації для складальника
    dp.register_message_handler(load_loginwarehouseman,content_types='text',state=loginingwareh.login)##
    dp.register_message_handler(load_passwordwarehouseman,content_types='text',state=loginingwareh.password)##
    dp.register_message_handler(loadfinishclwarehouseman,Text(equals='🆗Підтвердити'))##


    dp.register_message_handler(menuadmin,Text(equals='🧝Кабінет адміністратора'),state=None) #
    dp.register_message_handler(log_startadmin,Text(equals='🔐Увійти'),state=None)#######       функції аунтифікації для адміністратора
    dp.register_message_handler(load_loginadmin,content_types='text',state=loginingadmin.login)##
    dp.register_message_handler(load_passwordadmin,content_types='text',state=loginingadmin.password)##
    dp.register_message_handler(loadfinishadmin,Text(equals='👌Підтвердити'))##


#####################################складальник###################################################
    dp.register_message_handler(kbdemonst,Text(equals='📺Перегляд вантажу'),State=None)# перегляд даних про вантаж на складі
    dp.register_message_handler(kbdemonst1,content_types='text',state=demonst.key)# перегляд даних про вантаж на складі

    dp.register_message_handler(savecargostart,Text(equals='🖊Додати вантаж'),State=None)# машина стану додавання
    dp.register_message_handler(savenamecargoo,content_types='text',state=savecargoo.name)#
    dp.register_message_handler(savecargoocount,content_types='text',state=savecargoo.countcargoo)#
    dp.register_message_handler(savemethodcargo,content_types='text',state=savecargoo.savemethod)#
    dp.register_message_handler(savecargoowarecode,content_types='text',state=savecargoo.namewarehouse)#
    dp.register_message_handler(savecargoowaretype,content_types='text',state=savecargoo.typecargo)#

    dp.register_message_handler(savecargoqr,content_types='text',state=savecargoo.photo)#


    dp.register_message_handler(deletecargowarehousestart,Text(equals='🗑Видалити вантаж'),State=None)# машина стану видалення
    dp.register_message_handler(deletecargowarehouse,content_types='text',state=deletecargoo.deletecargoo)#

    dp.register_message_handler(waredemonst,Text(equals='📺Перегляд складів'))# перегляд даних про склад


#####################################логіст##################################################################
    dp.register_message_handler(logistdemonstratiom,Text(equals='🗃База даних'))# машина стану видалення
    dp.register_message_handler(logistdemonstratiom2,Text(equals='💻Демонстрація'))# демонстрація даних (усіх меню)
    dp.register_message_handler(logistdemostrcompany,Text(equals='📺Компанії'))# демонстрація даних компанії
    dp.register_message_handler(logistdemostrcargoo,Text(equals='📺Вантажі'))# демонстарція даних вантажу
    dp.register_message_handler(logistdemostrcar,Text(equals='📺Автомобілі'))# демонстрація даних маршруту
    dp.register_message_handler(logistdemostrdriverman,Text(equals='📺Водії'))# демонстрація даних маршруту

    dp.register_message_handler(logistdemonstgeopoz,Text(equals='🇺🇦Місцерозташування вантажа'),State=None)# перегляд водія на карті для голіста
    dp.register_message_handler(logistdemonstgeopoz1,content_types='text',state=demonstgeopoz.surname)#перегляд водія на карті для голіста

    dp.register_message_handler(delnote,Text(equals='🗑Видалити ТН'),State=None)# додавання даних логіст
    dp.register_message_handler(delnote1,content_types='text',state=deletenote.codenote)# додавання даних логіст

    dp.register_message_handler(logistadd,Text(equals='📌Додати дані'))# додавання даних логіст

    dp.register_message_handler(addcar,Text(equals='✒Додати автомобіль'),State=None)# машина стану додавання автомобіля водієм
    dp.register_message_handler(addcar1,content_types='text',state=car.namecar)#
    dp.register_message_handler(addcar2,content_types='text',state=car.numbercar)#
    dp.register_message_handler(addcar3,content_types='text',state=car.typecar)#

    dp.register_message_handler(addroute,Text(equals='📌Додати ТН'),State=None)# машина стану додавання
    dp.register_message_handler(addroute1,content_types='text',state=delivery.cityunload)#
    dp.register_message_handler(addroute2,content_types='text',state=delivery.time)#
    dp.register_message_handler(addroute3,content_types='text',state=delivery.Numbecar)#
    dp.register_message_handler(addroute4,content_types='text',state=delivery.Namecargo)#

####################################функції для геопозиції(водій)##############################################
    dp.register_message_handler(geopoz1,Text(equals='🇺🇦Вантаж на карті'),State=None)#початоk роботи з геопозицією
    dp.register_message_handler(geopoz2,content_types=['location'])#передача даних в бд

####################################функції для накладної(водій)##############################################
    
    dp.register_message_handler(rep,Text(equals='📋Накладна складу'))#перехід з меню в підменю

    dp.register_message_handler(repqr,Text(equals='📷Відправити QR-code'),State=None)#перехід з меню в підменю
    dp.register_message_handler(repqr1,content_types='photo',state=nakladnaqr.photo)#передача даних в бд



    dp.register_message_handler(report,Text(equals='📋Накладна транспортна'),State=None)#передача даних в бд
    dp.register_message_handler(report1,content_types='text',state=nakladna.surname)#передача даних в бд

    dp.register_message_handler(report2,Text(equals='⌨Ввести порядковий номер'),State=None)#передача даних в бд
    dp.register_message_handler(report2_2,content_types='text',state=naklandawarehouse.key)#передача даних в бд

####################################функції для повернення користувача з підменю в меню або вихід з додатку######################################
    dp.register_message_handler(backout1,Text(equals='👨‍💼Назад'))# повернення з підменю в меню логіста
    dp.register_message_handler(backout,Text(equals='👩‍💼Назад'))# повернення з підменю в меню логіста

####################################функція для виходу з системи######################################
    dp.register_message_handler(command_start,Text(equals='❌Вийти'))# вихід з будь-якого інтерфейсу програми


