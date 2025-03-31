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

from modules.constructs import Constructs
from modules.payment import Payment
from modules.keyboards import keyboards
async def main():
    logging.basicConfig(level=logging.INFO) 
    config =  dotenv_values(".env") 
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
        
        await message.answer(text="Добро пожаловать в Sasi_market:", reply_markup=await keyboards.main_kb())
    
    
    async def _category(callback_query):
        category = callback_query.data.split("_")
        await callback_query.message.edit_text(text=category[1])
        products = await db_instance.get_products_by_category(category[1])
        await callback_query.message.edit_reply_markup(reply_markup=await keyboards.category_kb(products))
        
    async def _product(callback_query):
        product = callback_query.data.split("_")
        detailsr = await db_instance.get_product_by_id(product[1])
        details = detailsr[0]
        await callback_query.message.edit_text(text=f"Товар: {details["product_name"]} описание: {details["product_description"]}, цена {details["price"]}")
        await callback_query.message.edit_reply_markup(reply_markup=await keyboards.product_kb(product))
        
    async def _buy(callback_query):
        product = callback_query.data.split("_")
        user = await db_instance.get_user(callback_query.from_user.id)
        detailsr = await db_instance.get_product_by_id(product[1])
        details = detailsr[0]
        if user[0]["balance"] >= details["price"]:
            await callback_query.message.edit_text(text=f"Покупка Товар: {details["product_name"]} за {details["price"]} ваш баланс: {user[0]["balance"]}")
        else: 
            await callback_query.message.edit_text(text=f"Покупка Товар: {details["product_name"]} за {details["price"]} ваш баланс: на вашем балансе недостаточно средств!")
        await callback_query.message.edit_reply_markup(reply_markup=await keyboards.buy_kb(user, details, product))
    async def _finishbuy(callback_query):
        product = callback_query.data.split("_")
        user = await db_instance.get_user(callback_query.from_user.id)
        detailsr = await db_instance.get_product_by_id(product[1])
        details = detailsr[0]
        await db_instance.update_balance(callback_query.from_user.id, balance=int(user[0]["balance"]-details["price"]))
        await callback_query.message.edit_text(text=f"Успешная покупка: {details["product_name"]} за {details["price"]} ваш баланс: {int(user[0]["balance"]-details["price"])}, данные: {details["product"]}")
    async def _deposit(callback_query):
        product = callback_query.data.split("_")
        user = await db_instance.get_user(callback_query.from_user.id)
        detailsr = await db_instance.get_product_by_id(product[1])
        details = detailsr[0]
        amount = int(details["price"]-user[0]["balance"])
        invoice = await pay.create_invoice(amount=amount, fiat='RUB')
        await callback_query.message.edit_text(text=f"Пополнение баланса платеж #{invoice[0]} статус: {invoice[1]} сумма: {invoice[2]}")
        await callback_query.message.edit_reply_markup(reply_markup=await keyboards.deposit_kb(invoice, detailsr))
    async def _checkpayment(callback_query):
        invoiceid = callback_query.data.split("_")
        invoice = await pay.check_status(invoiceid[1])
        if invoice[0].status == "active":
            pass
        elif invoice[0].status == "paid":
            await callback_query.message.edit_text(text=f"Баланс пополнен платеж #{invoice[0].invoice_id} статус: {invoice[0].status} сумма: {invoice[0].amount}")
            await db_instance.update_balance(callback_query.from_user.id, balance=int(invoice[0].amount))
            await callback_query.message.edit_reply_markup(reply_markup=await keyboards.check_payment_kb(invoiceid))
    async def _cancelpayment(callback_query):
        invoiceid = callback_query.data.split("_")
        invoice = await pay.check_status(invoiceid[1])
        if invoice[0].status == "active":
            await pay.del_invoice(invoiceid[1])
            await callback_query.message.edit_text(text=f"Пополнение отменено платеж #{invoice[0].invoice_id} статус: cancel сумма: {invoice[0].amount}")
    async def _back(callback_query):
        await callback_query.message.delete()
        await start(callback_query.message)
    @dp.message(F.text == "Каталог 📦")
    async def catalog(message: types.Message):
        products = await db_instance.get_products()
        categories = await Constructs.format_products1(products)
        await message.answer(text="Каталог", reply_markup=await keyboards.catalog_kb(categories))
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
            if callback_query.data == "*":
                pass
            
            elif callback_query.data.startswith("category"):
                await _category(callback_query)
                
            elif callback_query.data.startswith("product"):
                await _product(callback_query)
                
            elif callback_query.data.startswith("buy"): 
                await _buy(callback_query)
                
            elif callback_query.data.startswith("finishbuy"): 
                await _finishbuy(callback_query)
            
            elif callback_query.data.startswith("deposit"):
                await _deposit(callback_query)
            
            elif callback_query.data.startswith("checkpayment"):
                await _checkpayment(callback_query)
                    
            elif callback_query.data.startswith("cancelpayment"):
                await _cancelpayment(callback_query)
                
            elif callback_query.data == "back":
                await _back(callback_query)
           

    
    
    
    #######
    
    
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    asyncio.run(main())
    
