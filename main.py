# -*- coding: utf-8 -*-

# Developer: Nethanter-del
# Github: https://github.com/Nethanter-del
# Date Created: 2025-12-03
# Version: 1.0.0

# License: MIT License
#
# Copyright (c) 2025 Nethanter-del
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

from aiogram import Bot, Dispatcher
from dotenv import dotenv_values
from modules.bd_handler import bd

import asyncio
import logging


from aiogram import types
from aiogram.filters.command import Command
from aiogram import F
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, KeyboardBuilder, ReplyKeyboardBuilder
from modules.constructs import Constructs
from modules.payment import Payment
async def main():
    logging.basicConfig(level=logging.INFO) 
    config =  dotenv_values("config.env") 
    bot = Bot(token=config["TG_TOKEN"]) 
    dp = Dispatcher()
    bot.edit_message_reply_markup
    db_instance = bd(host=config["PG_HOST"],user=config["PG_USER"],password=config["PG_PASSWORD"],database=config["PG_DATABASE"],owner=config["OWNER_ID"])
    await db_instance.init_db()
    pay = Payment(token=config["CB_TOKEN"])
    #######
    
    @dp.message(Command("start"))
    async def start(message: types.Message):
        user = await db_instance.get_user(message.from_user.id)
        if len(user) < 1:
            await db_instance.create_user(message.from_user.id, message.from_user.username)
        builder = ReplyKeyboardBuilder()
        button_catalog = types.KeyboardButton(text="Каталог 📦")
        button_list = types.KeyboardButton(text="Наличие ✅")
        button_profile = types.KeyboardButton(text="Мой профиль 👤")
        button_faq = types.KeyboardButton(text="FAQ ❓")
        builder.add(button_catalog, button_list, button_profile, button_faq)
        await message.answer(text="Добро пожаловать в Sasi_market:", reply_markup=builder.as_markup(resize_keyboard=True))
    
            
    @dp.message(F.text == "Каталог 📦")
    async def catalog(message: types.Message):
        await message.answer(text="Каталог")
        products = await db_instance.get_products()
        categories = await Constructs.format_products1(products)
        builder = InlineKeyboardBuilder()
        for category in categories:
            button = InlineKeyboardButton(text = category, callback_data = f"category_{category}")
            builder.add(button)
        await message.answer(text="Каталог", reply_markup=builder.as_markup())
    @dp.message(F.text == "Наличие ✅")
    async def list_goods(message: types.Message):
        products = await db_instance.get_products()
        text = await Constructs.format_products(products)
        await message.answer(text=text)
    @dp.message(F.text == "Мой профиль 👤")
    async def profile(message: types.Message):
        await message.answer(text="профиль")
    @dp.message(F.text == "FAQ ❓")
    async def faq(message: types.Message):
        await message.answer(text="FAQ")
    @dp.callback_query()    
    async def process_callback(callback_query: types.CallbackQuery):
            if callback_query.data == "create_ticket":
                pass
            elif callback_query.data.startswith("category"):
                category = callback_query.data.split("_")
                await callback_query.message.edit_text(text=category[1])
                builder = InlineKeyboardBuilder()
                products = await db_instance.get_products_by_category(category[1])
                for item in products:
                    button = InlineKeyboardButton(text = item["product_name"], callback_data = f"product_{item["product_id"]}")
                    builder.row(button)
                await callback_query.message.edit_reply_markup(reply_markup=builder.as_markup())
            elif callback_query.data.startswith("product"):
                product = callback_query.data.split("_")
                detailsr = await db_instance.get_product_by_id(product[1])
                details = detailsr[0]
                await callback_query.message.edit_text(text=f"Товар: {details["product_name"]} описание: {details["product_description"]}, цена {details["price"]}")
                builder = InlineKeyboardBuilder()
                button_buy = InlineKeyboardButton(text = "Купить", callback_data = f"buy_{product[1]}")
                button_cancel = InlineKeyboardButton(text = "Отмена", callback_data = f"back")
                builder.add(button_buy, button_cancel)
                await callback_query.message.edit_reply_markup(reply_markup=builder.as_markup())
            elif callback_query.data.startswith("buy"): 
                product = callback_query.data.split("_")
                user = await db_instance.get_user(callback_query.from_user.id)
                detailsr = await db_instance.get_product_by_id(product[1])
                details = detailsr[0]
                builder = InlineKeyboardBuilder()
                if user[0]["balance"] >= details["price"]:
                    await callback_query.message.edit_text(text=f"Покупка Товар: {details["product_name"]} за {details["price"]} ваш баланс: {user[0]["balance"]}")
                    button_finishbuy = InlineKeyboardButton(text = "Потдвердить покупку", callback_data = f"finishbuy_{product[1]}")
                    button_cancel = InlineKeyboardButton(text = "Отмена", callback_data = f"back")
                    builder.add(button_finishbuy, button_cancel)
                    
                else: 
                    await callback_query.message.edit_text(text=f"Покупка Товар: {details["product_name"]} за {details["price"]} ваш баланс: на вашем балансе недостаточно средств!")
                    button_deposit = InlineKeyboardButton(text = "Пополнить баланс", callback_data = f"deposit_{product[1]}")
                    button_cancel = InlineKeyboardButton(text = "Отмена", callback_data = f"back")
                    builder.add(button_deposit, button_cancel)
                await callback_query.message.edit_reply_markup(reply_markup=builder.as_markup())
            elif callback_query.data.startswith("finishbuy"): 
                product = callback_query.data.split("_")
                user = await db_instance.get_user(callback_query.from_user.id)
                detailsr = await db_instance.get_product_by_id(product[1])
                details = detailsr[0]
                await db_instance.update_balance(callback_query.from_user.id, balance=int(user[0]["balance"]-details["price"]))
                await callback_query.message.edit_text(text=f"Успешная покупка: {details["product_name"]} за {details["price"]} ваш баланс: {int(user[0]["balance"]-details["price"])}, данные: {details["product"]}")
            elif callback_query.data.startswith("deposit"):
                product = callback_query.data.split("_")
                user = await db_instance.get_user(callback_query.from_user.id)
                detailsr = await db_instance.get_product_by_id(product[1])
                details = detailsr[0]
                amount = int(details["price"]-user[0]["balance"])
                invoice = await pay.create_invoice(amount=amount, fiat='RUB')
                await callback_query.message.edit_text(text=f"Пополнение баланса платеж #{invoice[0]} статус: {invoice[1]} сумма: {invoice[2]}")
                builder = InlineKeyboardBuilder()
                buttonpay = InlineKeyboardButton(text ='Оплатить', url=invoice[3])
                button_checkpay = InlineKeyboardButton(text ='Я оплатил', callback_data=f"checkpayment_{invoice[0]}_{detailsr[0]["product_id"]}")
                button_cancelpay = InlineKeyboardButton(text ='Отмена', callback_data=f"cancelpayment_{invoice[0]}")
                builder.add(buttonpay, button_checkpay, button_cancelpay)
                await callback_query.message.edit_reply_markup(reply_markup=builder.as_markup())
            elif callback_query.data.startswith("checkpayment"):
                invoiceid = callback_query.data.split("_")
                invoice = await pay.check_status(invoiceid[1])
                if invoice[0].status == "active":
                    pass
                elif invoice[0].status == "paid":
                    await callback_query.message.edit_text(text=f"Баланс пополнен платеж #{invoice[0].invoice_id} статус: {invoice[0].status} сумма: {invoice[0].amount}")
                    await db_instance.update_balance(callback_query.from_user.id, balance=int(invoice[0].amount))
                    builder = InlineKeyboardBuilder()
                    button_backToProd = InlineKeyboardButton(text ='Вернуться к покупке', callback_data=f"buy_{invoiceid[2]}")
                    builder.add(button_backToProd)
                    await callback_query.message.edit_reply_markup(reply_markup=builder.as_markup())
            elif callback_query.data.startswith("cancelpayment"):
                invoiceid = callback_query.data.split("_")
                invoice = await pay.check_status(invoiceid[1])
                if invoice[0].status == "active":
                    await pay.del_invoice(invoiceid[1])
                    await callback_query.message.edit_text(text=f"Пополнение отменено платеж #{invoice[0].invoice_id} статус: cancel сумма: {invoice[0].amount}")
            elif callback_query.data == "back":
                pass

    
    
    
    #######
    
    
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    asyncio.run(main())
    
