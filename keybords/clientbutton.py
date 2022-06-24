from cmath import log10
from aiogram.types import ReplyKeyboardMarkup,KeyboardButton
from cv2 import log, resize
b1=KeyboardButton('🇺🇦Вантаж на карті') 
b2=KeyboardButton('📋Накладна транспортна')
b3=KeyboardButton('📋Накладна складу')
b4=KeyboardButton('✒Додати автомобіль')
b5=KeyboardButton('❌Вийти')
kbdriver=ReplyKeyboardMarkup(resize_keyboard=True).add(b1,b2,b3,b4,b5)

bb1=KeyboardButton('Передача місцерозташування',request_location=True)
kbdrive1=ReplyKeyboardMarkup(resize_keyboard=True).add(bb1)

l1=KeyboardButton('🗃База даних')
l2=KeyboardButton('📋Накладна транспортна')
l3=KeyboardButton('📋Накладна складу')
l4=KeyboardButton('❌Вийти')
kblogist=ReplyKeyboardMarkup(resize_keyboard=True).add(l1,l2,l3,l4)

l11=KeyboardButton('💻Демонстрація')
l12=KeyboardButton('📌Додати ТН')
l13=KeyboardButton('🗑Видалити ТН')
l14=KeyboardButton('🇺🇦Місцерозташування вантажа')
l15=KeyboardButton('👩‍💼Назад')
kblogist1=ReplyKeyboardMarkup(resize_keyboard=True).add(l11,l12,l13,l14,l15)

lo1=KeyboardButton('✒Додати накладну')
lo2=KeyboardButton('✒Додати водія')
lo3=KeyboardButton('👨‍💼Назад')
kblogist2=ReplyKeyboardMarkup(resize_keyboard=True).add(lo1,lo2,lo3)

ldem1=KeyboardButton('📺Компанії')
ldem2=KeyboardButton('📺Вантажі')
ldem3=KeyboardButton('📺Водії')
ldem4=KeyboardButton('📺Автомобілі')
ldem5=KeyboardButton('👨‍💼Назад')
kblogist3=ReplyKeyboardMarkup(resize_keyboard=True).add(ldem1,ldem2,ldem3,ldem4,ldem5)

ldel1=KeyboardButton('🗑Видалити компанію')
ldel2=KeyboardButton('🗑Видалити вантаж')
ldel3=KeyboardButton('🗑Видалити маршрут')
ldel4=KeyboardButton('🗑Видалити водія')
ldel5=KeyboardButton('🗑Видалити автомобіль')
ldel6=KeyboardButton('👨‍💼Назад')
kblogist4=ReplyKeyboardMarkup(resize_keyboard=True).add(ldel1,ldel2,ldel3,ldel4,ldel5,ldel6)


nak1=KeyboardButton('⌨Ввести порядковий номер')
nak2=KeyboardButton('📷Відправити QR-code')
nak3=KeyboardButton('👩‍💼Назад')


kblogist5=ReplyKeyboardMarkup(resize_keyboard=True).add(nak1,nak2,nak3)
################################################################################################################

##########################################складальник##########################################################
w1=KeyboardButton('🖊Додати вантаж')
w2=KeyboardButton('🗑Видалити вантаж')
w3=KeyboardButton('📺Перегляд вантажу')
w4=KeyboardButton('📺Перегляд складів')
w5=KeyboardButton('📋Накладна складу')
w6=KeyboardButton('❌Вийти')
kbwarehouse=ReplyKeyboardMarkup(resize_keyboard=True).add(w1,w2,w3,w4,w5,w6)# головне меню для складальника

save1=KeyboardButton('Палети')
save2=KeyboardButton('Діжки')
save3=KeyboardButton('Мішки')
kbmethodsave=ReplyKeyboardMarkup(resize_keyboard=True).add(save1,save2,save3)


type1=KeyboardButton('Споживча продукція')
type2=KeyboardButton('Металопродукція')
type3=KeyboardButton('Нафтопродукція')
type4=KeyboardButton('Лісопродукція')
type5=KeyboardButton('Газопродукція')
type6=KeyboardButton('Радіоактивна продукція')

kbtypecargo=ReplyKeyboardMarkup(resize_keyboard=True).add(type1,type2,type3,type4,type5,type6)


typecar1=KeyboardButton('Рефрижиратор')
typecar2=KeyboardButton('Сцепка')
typecar3=KeyboardButton('Термічний')

kbtypecar=ReplyKeyboardMarkup(resize_keyboard=True).add(typecar1,typecar2,typecar3)

qrtext=KeyboardButton('Звичайний')
qrtext1=KeyboardButton('Крихкий')
qrtext2=KeyboardButton('Вологонестійкий')
qrtext3=KeyboardButton('Сонценестійкий')
qrtext4=KeyboardButton('Морозонестійкий')

kbqrcode=ReplyKeyboardMarkup(resize_keyboard=True).add(qrtext,qrtext2,qrtext3,qrtext4)
###########################################адміністратор########################################################################
a1=KeyboardButton('📁База даних')
a2=KeyboardButton('📊Інтерфейс логіста')
a3=KeyboardButton('🚚Інтерфейс водія')
a4=KeyboardButton('👷‍♂️Інтерфейс складальника')
a5=KeyboardButton('❌Вийти')
kbadmin=ReplyKeyboardMarkup(resize_keyboard=True).add(a1,a2,a3,a4,a5)# головне меню для логіста

bdadmin=KeyboardButton('📌Додати користувача')
bdadmin1=KeyboardButton('🗑Видалити працівника')
bdadmin2=KeyboardButton('📄Дані про працівників')
bdadmin3=KeyboardButton('🏢Робота з компанією')
bdadmin4=KeyboardButton('🏚Робота зі складом')
bdadmin5=KeyboardButton('⬅Назад')
kbadminbd1=ReplyKeyboardMarkup(resize_keyboard=True).add(bdadmin,bdadmin1,bdadmin2,bdadmin3,bdadmin4,bdadmin5)
c1=KeyboardButton('📺Компанії')
c2=KeyboardButton('✒Додати компанію')
c3=KeyboardButton('🗑Видалити компанію')
c4=KeyboardButton('🔙Назад')
kbcomp=ReplyKeyboardMarkup(resize_keyboard=True).add(c1,c2,c3,c4)

aw1=KeyboardButton('📺Склади')
aw2=KeyboardButton('✒Додати склад')
aw3=KeyboardButton('🗑Видалити склад')
aw4=KeyboardButton('🔙Назад')
kbwareadmin=ReplyKeyboardMarkup(resize_keyboard=True).add(aw1,aw2,aw3,aw4)

wh1=KeyboardButton('Додати склад')
wh2=KeyboardButton('Видалити склад')
wh3=KeyboardButton('📺Склад')
wh4=KeyboardButton('📺🔙Назад')
kbwadnin=ReplyKeyboardMarkup(resize_keyboard=True).add(wh1,wh2,wh3,wh4)

logist=KeyboardButton('🦸‍♂️Дані логістів')
driveman=KeyboardButton('🚛Дані водіїв')
warehouseman=KeyboardButton('📦Дані складальників')
back=KeyboardButton('🔙Назад')
kbdemonstjob=ReplyKeyboardMarkup(resize_keyboard=True).add(logist,driveman,warehouseman,back)

reg1=KeyboardButton('📌Додати логіста')
reg2=KeyboardButton('📌Додати водія')
reg3=KeyboardButton('📌Додати складальника')
reg4=KeyboardButton('🔙Назад')
kbadminreg=ReplyKeyboardMarkup(resize_keyboard=True).add(reg1,reg2,reg3,reg4)#регістрація водія,логіста,складальника

###########################################система входу########################################################################
logman=KeyboardButton('🦸‍♂️Кабінет логіста')
wareman=KeyboardButton('📦Кабінет складальника')
driverman=KeyboardButton('🚛Кабінет водія')
admin=KeyboardButton('🧝Кабінет адміністратора')
kbmenustart=ReplyKeyboardMarkup(resize_keyboard=True).add(logman,wareman,driverman,admin)# меню вибору інтерфейса на початку

autho=KeyboardButton('🔑Увійти') 
autho1=KeyboardButton('✅Підтвердити')
kbautho=ReplyKeyboardMarkup(resize_keyboard=True).add(autho,autho1) # логіста

driwe=KeyboardButton('🗝Увійти') 
driwe1=KeyboardButton('✔Підтвердити')
kbdriwe=ReplyKeyboardMarkup(resize_keyboard=True).add(driwe,driwe1) # водія

wareh=KeyboardButton('🔧Увійти') 
wareh1=KeyboardButton('🆗Підтвердити')
kbwareh=ReplyKeyboardMarkup(resize_keyboard=True).add(wareh,wareh1) # складальника

admin=KeyboardButton('🔐Увійти') 
admin1=KeyboardButton('👌Підтвердити')
kbadmin1=ReplyKeyboardMarkup(resize_keyboard=True).add(admin,admin1) # адміністратора