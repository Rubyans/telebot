from concurrent.futures.thread import _worker
from os import stat
from aiogram import types,Dispatcher
from cv2 import stereoRectify
from create_bot import dp,bot
from hendlers.client import logistadd
from keybords import buttonadmin
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from mybd import databasepy
from keybords import kblogist,kbwarehouse,kbdriver,kbadminreg,kbadmin,kbadminbd1,kbdemonstjob,kbcomp,kbwareadmin

class driverman(StatesGroup): #клас додавання даних про водія
    surname =State()
    name=State()
    middlename=State()
    email=State()
    phone=State()
    login=State()
    password=State()

class logist(StatesGroup): #клас додавання логіста
    surname=State()
    name=State()
    middlename=State()
    email=State()
    phone=State()
    login=State()
    password=State()
    ipp=State()

class warehouseman(StatesGroup): #клас додавання складальника
    surname=State()
    name=State()
    middlename=State()
    email=State()
    phone=State()
    login=State()
    password=State()
    address=State()

class deleletworker(StatesGroup): #клас видалення працівника
    surname=State()
    phone=State()

class company(StatesGroup): #клас додавання компанії(логіст)
    namecompany=State()
    numbertraty=State()
    EDRPOY=State()
    IPP=State()
    MFO=State()
    Phone=State()
    City=State()
    Street=State()
    Home=State()

class deletecompany(StatesGroup): #клас видалення складу
    IPP=State()

class warehouse(StatesGroup):#клас додавання складу
    area=State()
    staff=State()
    ipp=State()
    name=State()
    city=State()
    street=State()
    home=State()

class deletewarehouse(StatesGroup):
    codekey=State()
################################################база даних перехід##################################################################################
async def funcbd(message:types.Message): # початок перехід від меню в підменю
    await bot.send_message(message.chat.id,'Робота з базою даних розпочато',reply_markup=kbadminbd1)

async def regchoose(message:types.Message): # початок перехід від меню в підменю
    await bot.send_message(message.chat.id,'Оберіть кого ви бажаєте зареєструвати',reply_markup=kbadminreg)

##################################додавання даних про водія адміністратором##########################################################################################
async def adddriverman(message:types.Message): # початок машини додавання
    await driverman.surname.set()
    await bot.send_message(message.chat.id,'Введіть прізвище водія')

async def adddriverman1(message:types.Message,state=FSMContext):#машина стану додавання водія
    async with state.proxy() as drive:
        drive['surname']=message.text
    await driverman.next()
    await bot.send_message(message.chat.id,'Введіть ім`я водія')

async def adddriverman2(message:types.Message,state=FSMContext):#машина стану додавання водія
    async with state.proxy() as drive:
        drive['name']=message.text
    await driverman.next()
    await bot.send_message(message.chat.id,'Введіть по батькові водія')

async def adddriverman3(message:types.Message,state=FSMContext):#машина стану додавання водія
    async with state.proxy() as drive:
        drive['middlename']=message.text
    await driverman.next()
    await bot.send_message(message.chat.id,'Введіть електрону пошту водія')
  
async def adddriverman4(message:types.Message,state=FSMContext):#машина стану додавання водія
    async with state.proxy() as drive:
        drive['email']=message.text
    await driverman.next()
    await bot.send_message(message.chat.id,'Введіть номер телефона водія +38##########')

async def adddriverman5(message:types.Message,state=FSMContext):#машина стану додавання водія
    async with state.proxy() as drive:
        drive['phone']=message.text
    await driverman.next()
    await bot.send_message(message.chat.id,'Введіть майбутній логін водія')

async def adddriverman6(message:types.Message,state=FSMContext):#машина стану додавання водія
    async with state.proxy() as drive:
        drive['login']=message.text
    await driverman.next()
    await bot.send_message(message.chat.id,'Введіть майбутній пароль водія')

async def adddriverman7(message:types.Message,state=FSMContext):#машина стану додавання водія
    try:
        async with state.proxy() as drive:
            drive['password']=message.text
        await driverman.next()
        await databasepy.adddrivermanbd(message,state)
        await state.finish()
    except Exception as e:
        await bot.send_message(message.chat.id,"Даний логін вже використовується, введіть інший")

##################################додавання даних про логіста адміністратором##########################################################################################
async def addlogist(message:types.Message): # початок машини додавання
    await logist.surname.set()
    await bot.send_message(message.chat.id,'Введіть прізвище логіста')

async def addlogist1(message:types.Message,state=FSMContext):#машина стану додавання водія
    async with state.proxy() as drive:
        drive['surname']=message.text
    await logist.next()
    await bot.send_message(message.chat.id,'Введіть ім`я логіста')

async def addlogist2(message:types.Message,state=FSMContext):#машина стану додавання водія
    async with state.proxy() as drive:
        drive['name']=message.text
    await logist.next()
    await bot.send_message(message.chat.id,'Введіть по батькові логіста')

async def addlogist3(message:types.Message,state=FSMContext):#машина стану додавання водія
    async with state.proxy() as drive:
        drive['middlename']=message.text
    await logist.next()
    await bot.send_message(message.chat.id,'Введіть електрону пошту логіста')
  
async def addlogist4(message:types.Message,state=FSMContext):#машина стану додавання водія
    async with state.proxy() as drive:
        drive['email']=message.text
    await logist.next()
    await bot.send_message(message.chat.id,'Введіть номер телефона логіста +38###########')

async def addlogist5(message:types.Message,state=FSMContext):#машина стану додавання водія
    async with state.proxy() as drive:
        drive['phone']=message.text
    await logist.next()
    await bot.send_message(message.chat.id,'Введіть майбутній логін логіста')

async def addlogist6(message:types.Message,state=FSMContext):#машина стану додавання водія
    async with state.proxy() as drive:
        drive['login']=message.text
    await logist.next()
    await bot.send_message(message.chat.id,'Введіть майбутній пароль логіста')

async def addlogist7(message:types.Message,state=FSMContext):#машина стану додавання водія
    async with state.proxy() as drive:
        drive['password']=message.text
    await logist.next()
    await bot.send_message(message.chat.id,'ведіть IPP компанії')

async def addlogist8(message:types.Message,state=FSMContext):#машина стану додавання водія
    try:
        async with state.proxy() as drive:
            drive['IPP']=message.text
        await logist.next()
        await databasepy.addlogistbd(message,state)
        await state.finish()
    except Exception as e:
        await bot.send_message(message.chat.id,"Даний логін вже використовується")
        
##################################додавання даних про складальника адміністратором##########################################################################################
async def addwarehouseman(message:types.Message): # початок машини додавання
    await warehouseman.surname.set()
    await bot.send_message(message.chat.id,'Введіть прізвище складальника')

async def addwarehouseman1(message:types.Message,state=FSMContext):#машина стану додавання водія
    async with state.proxy() as drive:
        drive['surname']=message.text
    await warehouseman.next()
    await bot.send_message(message.chat.id,'Введіть ім`я складальника')

async def addwarehouseman2(message:types.Message,state=FSMContext):#машина стану додавання водія
    async with state.proxy() as drive:
        drive['name']=message.text
    await warehouseman.next()
    await bot.send_message(message.chat.id,'Введіть по батькові складальника')

async def addwarehouseman3(message:types.Message,state=FSMContext):#машина стану додавання водія
    async with state.proxy() as drive:
        drive['middlename']=message.text
    await warehouseman.next()
    await bot.send_message(message.chat.id,'Введіть електрону пошту складальника')
  
async def addwarehouseman4(message:types.Message,state=FSMContext):#машина стану додавання водія
    async with state.proxy() as drive:
        drive['email']=message.text
    await warehouseman.next()
    await bot.send_message(message.chat.id,'Введіть номер телефона складальника +38###########')

async def addwarehouseman5(message:types.Message,state=FSMContext):#машина стану додавання водія
    async with state.proxy() as drive:
        drive['phone']=message.text
    await warehouseman.next()
    await bot.send_message(message.chat.id,'Введіть майбутній логін складальника')

async def addwarehouseman6(message:types.Message,state=FSMContext):#машина стану додавання водія
    async with state.proxy() as drive:
        drive['login']=message.text
    await warehouseman.next()
    await bot.send_message(message.chat.id,'Введіть майбутній пароль складальника')

async def addwarehouseman7(message:types.Message,state=FSMContext):#машина стану додавання водія
    async with state.proxy() as drive:
        drive['password']=message.text
    await warehouseman.next()
    await bot.send_message(message.chat.id,'Введіть порядковий номер складу на якому складальник буде працювати')

async def addwarehouseman8(message:types.Message,state=FSMContext):#машина стану додавання водія
   # try:
        async with state.proxy() as drive:
            drive['IPP']=message.text
        await warehouseman.next()
        await databasepy.addwarehouseman(message,state)
        await state.finish()
   # except Exception as e:
     #   await bot.send_message(message.chat.id,"Даний логін вже використовується, введіть інший або ви ввели невірно дані")

########################################################################################################################################
async def demonstlogist(message:types.Message):
    await bot.send_message(message.chat.id,"Інтерфейс логіста",reply_markup=kblogist)

async def demonstvodiy(message:types.Message):
    await bot.send_message(message.chat.id,"Інтерфейс водія",reply_markup=kbdriver)

async def demonstwarehouse1(message:types.Message):
    await bot.send_message(message.chat.id,"Інтерфейс складальника",reply_markup=kbwarehouse)

async def demonstrrob(message:types.Message):
    await bot.send_message(message.chat.id,"Оберіть професію",reply_markup=kbdemonstjob)

async def viewlogist(message:types.Message):
    await databasepy.demonstlogistdb(message)

async def viewdriver(message:types.Message):
    await databasepy.demonstdrivermandb(message)

async def viewwarehouseman(message:types.Message):
    await databasepy.demonstwarehousemandb(message)

##################################додавання даних про компанію##########################################################################################
async def addcompany(message:types.Message):# початок машини додавання(компанія)
    await company.namecompany.set()
    await bot.send_message(message.chat.id,'Введіть назву компанії')

async def addcompany1(message:types.Message,state=FSMContext): #машина стану додавання компанії
    async with state.proxy() as compan:
        compan['namecompany']=message.text
    await company.next()
    await bot.send_message(message.chat.id,'Введіть номер договору')

async def addcompany2(message:types.Message,state=FSMContext):#машина стану додавання компанії
    async with state.proxy() as compan:
        compan['numbertreaty']=message.text
    await company.next()
    await bot.send_message(message.chat.id,'Введіть код ЄДРПОУ')

async def addcompany3(message:types.Message,state=FSMContext):#машина стану додавання компанії
    async with state.proxy() as compan:
        compan['EDRPOY']=message.text
    await company.next()
    await bot.send_message(message.chat.id,'Введіть код ІПП')

async def addcompany4(message:types.Message,state=FSMContext):#машина стану додавання компанії
    async with state.proxy() as compan:
        compan['IPP']=message.text
    await company.next()
    await bot.send_message(message.chat.id,'Введіть код МФО')

async def addcompany5(message:types.Message,state=FSMContext):#машина стану додавання компанії
    async with state.proxy() as compan:
        compan['MFO']=message.text
    await company.next()
    await bot.send_message(message.chat.id,'Введіть номер телефону +38##########')

async def addcompany6(message:types.Message,state=FSMContext):#машина стану додавання компанії
    async with state.proxy() as compan:
        compan['Phone']=message.text
    await company.next()
    await bot.send_message(message.chat.id,'Введіть місто компанії')

async def addcompany7(message:types.Message,state=FSMContext):#машина стану додавання компанії
    async with state.proxy() as compan:
        compan['City']=message.text
    await company.next()
    await bot.send_message(message.chat.id,'Введіть вулицю компанії')

async def addcompany8(message:types.Message,state=FSMContext):#машина стану додавання компанії
    async with state.proxy() as compan:
        compan['Street']=message.text
    await company.next()
    await bot.send_message(message.chat.id,'Введіть номер будинка компанії')

async def addcompany9(message:types.Message,state=FSMContext):#машина стану додавання компанії
    try:
        async with state.proxy() as compan:
            compan['Home']=message.text
        await company.next()
        await databasepy.addcompany(message,state)
        await state.finish()
    except Exception as e:
        await bot.send_message(message.chat.id,"Щось не так...Перевірте правельність вводу та спробуйте знову")

################################################видалення працівника##################################################################################
async def deleteworker(message:types.Message):
    await deleletworker.surname.set()
    await bot.send_message(message.chat.id,"Введіть прізвище працівника")

async def deleteworker1(message:types.Message,state=FSMContext):
    async with state.proxy() as work:
        work['surname']=message.text
    await deleletworker.next()
    await bot.send_message(message.chat.id,'Введіть номер телефону працівника')
       
async def deleteworker2(message:types.Message,state=FSMContext):
    try:
        async with state.proxy() as work:
            work['phone']=message.text
        await databasepy.deleteworker(message,state)
        await state.finish()
    except Exception as e:
        await bot.send_message(message.chat.id,"Щось не так...Перевірте правельність вводу та спробуйте знову") 

################################################видалення компанії##################################################################################
async def deletecompany1(message:types.Message):
    await deletecompany.IPP.set()
    await bot.send_message(message.chat.id,"Введіть ІPP компанії")

async def deletecompany2(message:types.Message,state=FSMContext):
    try:
        async with state.proxy() as work:
            work['IPP']=message.text
        await databasepy.deletecompany(message,state)
        await state.finish()
    except Exception as e:
        await bot.send_message(message.chat.id,"Ви ввели невірно ІPP або даної компанії не існує") 

################################################перехід від меню##################################################################################
async def backmainmanu(message:types.Message):# повернення до головного меню
    await bot.send_message(message.from_user.id,'Назад',reply_markup=kbadmin) #з підменю в меню

async def backmenu(message:types.Message):# повернення до головного меню
    await bot.send_message(message.from_user.id,'Назад',reply_markup=kbadminbd1) #з підменю в меню(яке є також підменю)

async def funccompany(message:types.Message):
    await bot.send_message(message.from_user.id,'Робота з компанією',reply_markup=kbcomp)

async def funcwarehouse(message:types.Message):
    await bot.send_message(message.from_user.id,'Робота зі складом',reply_markup=kbwareadmin)

##################################додавання даних про склад адміністратором##########################################################################################
async def addwarehouse1(message:types.Message):# початок машини додавання(компанія)
    await warehouse.area.set()
    await bot.send_message(message.chat.id,'Введіть площу складу')

async def addwarehouse2(message:types.Message,state=FSMContext): #машина стану додавання компанії
    async with state.proxy() as compan:
        compan['area']=message.text
    await warehouse.next()
    await bot.send_message(message.chat.id,'Введіть штат працівників')

async def addwarehouse3(message:types.Message,state=FSMContext):#машина стану додавання компанії
    async with state.proxy() as compan:
        compan['staff']=message.text
    await warehouse.next()
    await bot.send_message(message.chat.id,'Введіть код ІПП компанії складу')

async def addwarehouse4(message:types.Message,state=FSMContext):#машина стану додавання компанії
    async with state.proxy() as compan:
        compan['ipp']=message.text
    await warehouse.next()
    await bot.send_message(message.chat.id,'Введіть назву складу')

async def addwarehouse5(message:types.Message,state=FSMContext):#машина стану додавання компанії
    async with state.proxy() as compan:
        compan['name']=message.text
    await warehouse.next()
    await bot.send_message(message.chat.id,'Введіть місто, де розташован склад')

async def addwarehouse6(message:types.Message,state=FSMContext):#машина стану додавання компанії
    async with state.proxy() as compan:
        compan['city']=message.text
    await warehouse.next()
    await bot.send_message(message.chat.id,'Введіть вулицю, де розташован склад')

async def addwarehouse7(message:types.Message,state=FSMContext):#машина стану додавання компанії
    async with state.proxy() as compan:
        compan['street']=message.text
    await warehouse.next()
    await bot.send_message(message.chat.id,'Введіть номер будинка, де розташован склад')

async def addwarehouse8(message:types.Message,state=FSMContext):#машина стану додавання компанії
    async with state.proxy() as compan:
        compan['home']=message.text
    await databasepy.addwarehouse(message,state)
    await state.finish()

################################################демонстрація складу адміністратор##################################################################################
async def demonstwarehouse(message:types.Message):#демонстрація складу
    await databasepy.demonstwarehouse(message)

################################################видалення складу адміністратором##################################################################################
async def deletewarehouse1(message:types.Message):
    await deletewarehouse.codekey.set()
    await bot.send_message(message.chat.id,"Введіть порядковий номер складу")

async def deletewarehouse2(message:types.Message,state=FSMContext):
    try:
        async with state.proxy() as work:
            work['codekey']=message.text
        await databasepy.deletewarehouse(message,state)
        await state.finish()
    except Exception as e:
        await bot.send_message(message.chat.id,"Ви ввели невірно порядковий номер або дані складів відсутні") 
################################################прив'язка працівника##################################################################################
def registet_hand_clients(dp:Dispatcher):

    dp.register_message_handler(regchoose,Text(equals='📌Додати користувача'))# реєстрація користувача
    dp.register_message_handler(funcbd,Text(equals='📁База даних'))# повернення з підменю в меню

    dp.register_message_handler(adddriverman,Text(equals='📌Додати водія'),State=None)# машина стану додавання водія
    dp.register_message_handler(adddriverman1,content_types='text',state=driverman.surname)#
    dp.register_message_handler(adddriverman2,content_types='text',state=driverman.name)#
    dp.register_message_handler(adddriverman3,content_types='text',state=driverman.middlename)#
    dp.register_message_handler(adddriverman4,content_types='text',state=driverman.email)#
    dp.register_message_handler(adddriverman5,content_types='text',state=driverman.phone)#
    dp.register_message_handler(adddriverman6,content_types='text',state=driverman.login)#    
    dp.register_message_handler(adddriverman7,content_types='text',state=driverman.password)#   

    dp.register_message_handler(addlogist,Text(equals='📌Додати логіста'),State=None)# машина стану додавання логіста
    dp.register_message_handler(addlogist1,content_types='text',state=logist.surname)#
    dp.register_message_handler(addlogist2,content_types='text',state=logist.name)#
    dp.register_message_handler(addlogist3,content_types='text',state=logist.middlename)#
    dp.register_message_handler(addlogist4,content_types='text',state=logist.email)#
    dp.register_message_handler(addlogist5,content_types='text',state=logist.phone)#
    dp.register_message_handler(addlogist6,content_types='text',state=logist.login)#    
    dp.register_message_handler(addlogist7,content_types='text',state=logist.password)#   
    dp.register_message_handler(addlogist8,content_types='text',state=logist.ipp)#   

    dp.register_message_handler(addwarehouseman,Text(equals='📌Додати складальника'),State=None)# машина стану додавання складальника
    dp.register_message_handler(addwarehouseman1,content_types='text',state=warehouseman.surname)#
    dp.register_message_handler(addwarehouseman2,content_types='text',state=warehouseman.name)#
    dp.register_message_handler(addwarehouseman3,content_types='text',state=warehouseman.middlename)#
    dp.register_message_handler(addwarehouseman4,content_types='text',state=warehouseman.email)#
    dp.register_message_handler(addwarehouseman5,content_types='text',state=warehouseman.phone)#
    dp.register_message_handler(addwarehouseman6,content_types='text',state=warehouseman.login)#    
    dp.register_message_handler(addwarehouseman7,content_types='text',state=warehouseman.password)#  
    dp.register_message_handler(addwarehouseman8,content_types='text',state=warehouseman.address)#  

    dp.register_message_handler(funccompany,Text(equals='🏢Робота з компанією'))# в меню компанії

    dp.register_message_handler(addcompany,Text(equals='✒Додати компанію'),State=None)# машина стану додавання
    dp.register_message_handler(addcompany1,content_types='text',state=company.namecompany)#
    dp.register_message_handler(addcompany2,content_types='text',state=company.numbertraty)#
    dp.register_message_handler(addcompany3,content_types='text',state=company.EDRPOY)#
    dp.register_message_handler(addcompany4,content_types='text',state=company.IPP)#
    dp.register_message_handler(addcompany5,content_types='text',state=company.MFO)#
    dp.register_message_handler(addcompany6,content_types='text',state=company.Phone)#
    dp.register_message_handler(addcompany7,content_types='text',state=company.City)#
    dp.register_message_handler(addcompany8,content_types='text',state=company.Street)#
    dp.register_message_handler(addcompany9,content_types='text',state=company.Home)#

    dp.register_message_handler(funcwarehouse,Text(equals='🏚Робота зі складом'))# в меню складу

    dp.register_message_handler(addwarehouse1,Text(equals='✒Додати склад'),State=None)# машина стану додавання
    dp.register_message_handler(addwarehouse2,content_types='text',state=warehouse.area)#
    dp.register_message_handler(addwarehouse3,content_types='text',state=warehouse.staff)#
    dp.register_message_handler(addwarehouse4,content_types='text',state=warehouse.ipp)#
    dp.register_message_handler(addwarehouse5,content_types='text',state=warehouse.name)#
    dp.register_message_handler(addwarehouse6,content_types='text',state=warehouse.city)#
    dp.register_message_handler(addwarehouse7,content_types='text',state=warehouse.street)#
    dp.register_message_handler(addwarehouse8,content_types='text',state=warehouse.home)#

    dp.register_message_handler(demonstwarehouse,Text(equals='📺Склади'))#перегляд складів

    dp.register_message_handler(deleteworker,Text(equals='🗑Видалити працівника'),State=None)# машина стану видалення робітника
    dp.register_message_handler(deleteworker1,content_types='text',state=deleletworker.surname)# машина стану видалення робітника
    dp.register_message_handler(deleteworker2,content_types='text',state=deleletworker.phone)# машина стану видалення робітника

    dp.register_message_handler(deletecompany1,Text(equals='🗑Видалити компанію'),State=None)# машина стану видалення компанії
    dp.register_message_handler(deletecompany2,content_types='text',state=deletecompany.IPP)# машина стану видалення компанії

    dp.register_message_handler(deletewarehouse1,Text(equals='🗑Видалити склад'),State=None)# машина стану видалення складу
    dp.register_message_handler(deletewarehouse2,content_types='text',state=deletewarehouse.codekey)# машина стану видалення складу

    dp.register_message_handler(demonstlogist,Text(equals='📊Інтерфейс логіста'))# інтерфейс логіста
    dp.register_message_handler(demonstvodiy,Text(equals='🚚Інтерфейс водія'))# інтерфейс водія
    dp.register_message_handler(demonstwarehouse1,Text(equals='👷‍♂️Інтерфейс складальника'))# інтерфейс складальника

    dp.register_message_handler(demonstrrob,Text(equals='📄Дані про працівників'))# інтерфейс складальника

    dp.register_message_handler(viewlogist,Text(equals='🦸‍♂️Дані логістів'))# інтерфейс складальника
    dp.register_message_handler(viewdriver,Text(equals='🚛Дані водіїв'))# інтерфейс складальника
    dp.register_message_handler(viewwarehouseman,Text(equals='📦Дані складальників'))# інтерфейс складальника

    dp.register_message_handler(backmainmanu,Text(equals='⬅Назад'))# повернення з підменю в меню
    dp.register_message_handler(backmenu,Text(equals='🔙Назад'))# повернення з підменю в меню

    

