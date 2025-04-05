from aiogram import types
from aiogram.filters.command import Command
from aiogram import F
from aiogram.enums import ParseMode

from modules.constructs import Constructs
from modules.payment import Payment
from modules.keyboards import keyboards
from modules.messages import _message

class admin_handlers:
    def __init__(self, dp, bd, bot):
        self.dp = dp
        self.bd = bd
        self.bot = bot
    async def main(self):
        @self.dp.message(Command("admins"))
        async def admins(message: types.Message):
            ss = await self.bd.get_user(message.from_user.id)
            if ss[0]["is_admin"] == True:
                adminlist = 'Список администраторов:\n\n'
                admins = await self.bd.select_admins()
                for admin in admins:
                    userAdmin = await self.bot.get_chat(admin["user_id"])
                    text = f"🔹 {admin["user_id"]} | {userAdmin.username} | {userAdmin.full_name}\n"
                    adminlist= adminlist + text
                text1 = '\n/grant_admin [id] - Добавить амиинистратора \n/ungrant_admin [id] - Убрать администратора'
                adminlist = adminlist + text1
                await message.answer(text=adminlist)
        @self.dp.message(Command("ungrant_admin"))
        async def ungrantadmin(message: types.Message):
            ss = await self.bd.get_user(message.from_user.id)
            if ss[0]["is_admin"] == True:
                args = message.text.split()[1:]
                if args:
                    if len(args) == 1:
                        user = await self.bd.get_user(int(args[0]))
                        if user:
                            if user[0]["is_admin"] == True:
                                await self.bd.admin_ungrant(args[0])
                                await self.bot.send_message(args[0], "Вас сняли с роли администратора")
                                await message.answer(text=f"Вы убрали админ права у {args[0]}")
                            else:
                                await message.answer(text=f"У пользователя с id: {args[0]} нету админ прав")
                            
                        else:
                            await message.answer(text=f"Пользователя с id: {args[0]} не существует")
                else:
                    await message.answer(text="Отствуют аргументы [id]")

        @self.dp.message(Command("grant_admin"))
        async def grant_admin(message: types.Message):
            ss = await self.bd.get_user(message.from_user.id)
            if ss[0]["is_admin"] == True:
                args = message.text.split()[1:]
                if args:
                    if len(args) == 1:
                        user = await self.bd.get_user(int(args[0]))
                        print(user)
                        if user:
                            if user[0]["is_admin"] == False:
                                await self.bd.admin_grant(int(args[0]))
                                await message.answer(text=f"Вы выдали админ права для {args[0]}")
                                await self.bot.send_message(args[0], "Вас повысили до администратора.")
                            else:
                                await message.answer(text=f"Пользователь {args[0]} уже является администратором")
                        else:
                            await message.answer(text=f"Пользователя с id: {args[0]} не существует")
                else:
                    await message.answer(text="Отствуют аргументы [id]")

        @self.dp.message(Command("add_money"))
        async def add_money(message: types.Message):
            ss = await self.bd.get_user(message.from_user.id)
            if ss[0]["is_admin"] == True:
                args = message.text.split()[1:]
                if args:
                    if len(args) == 2:
                        user = await self.bd.get_user(int(args[0]))
                        if user:
                            await self.bd.add_balance(int(args[0]), int(args[1]))
                            await message.answer(text=f"Баланс пополнен id: {args[0]} сумма: {args[1]} ₽")
                            
                            await self.bot.send_message(chat_id=int(args[0]), text=f"Баланс пополнен сумма: {args[1]} ₽")
                        else:
                            await message.answer(text=f"Пользователя с id: {args[0]} не существует")
                    else:
                        await message.answer(text="Недостаточно аргументов или их слишком много аргументов, [id] [Сумма]")
                else:
                    await message.answer(text="Отствуют аргументы [id] [Сумма]")
        @self.dp.message(Command("create_product"))
        async def add_money(message: types.Message):
            ss = await self.bd.get_user(message.from_user.id)
            if ss[0]["is_admin"] == True:
                args = message.text.split()[1:]
                if args:
                    if len(args) == 5:
                        
                        await self.bd.add_product(str(args[0]), str(args[1]), str(args[2]), int(args[3]), str(args[4]))
                        await message.answer(text=f"Товар создан {str(args[0]), str(args[1]), str(args[2]), int(args[3]), str(args[4])}")
                        
                    else:
                        await message.answer(text="Недостаточно аргументов или их слишком много аргументов, [Категория] [Название] [Описание] [Цена] [Товар]")
                else:
                    await message.answer(text="Отствуют аргументы [Категория] [Название] [Описание] [Цена] [Товар]")
       
