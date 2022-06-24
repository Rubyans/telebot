from aiogram.utils import executor
from create_bot import dp
from mybd import databasepy

async def on_startup(_):  #додав бд для логіну и паролю
    print('Бот вышел в онлайн')
    databasepy.startfunc()

from hendlers import client,admin,other

client.registet_hand_clients(dp)
admin.registet_hand_clients(dp)


executor.start_polling(dp,skip_updates=True,on_startup=on_startup)