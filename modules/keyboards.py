# -*- coding: utf-8 -*-

# Developer: Nethanter-del
# Github: https://github.com/Nethanter-del
# Date Created: 2025-12-03
# Version: 1.0.0

# License: MIT License
#
# Copyright (c) 2025 Nethanter-del
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, KeyboardBuilder, ReplyKeyboardBuilder
from aiogram import types
class keyboards:
    async def main_kb():
        builder = ReplyKeyboardBuilder()
        button_catalog = types.KeyboardButton(text="Каталог 📦")
        button_list = types.KeyboardButton(text="Наличие ✅")
        button_profile = types.KeyboardButton(text="Мой профиль 👤")
        button_faq = types.KeyboardButton(text="FAQ ❓")
        builder.add(button_catalog, button_list, button_profile, button_faq)
        return builder.as_markup(resize_keyboard=True)
    async def catalog_kb(categories):
        builder = InlineKeyboardBuilder()
        for category in categories:
            button = InlineKeyboardButton(text = category, callback_data = f"category_{category}")
            builder.add(button)
        return builder.as_markup()
    async def category_kb(products):
        builder = InlineKeyboardBuilder()
        for item in products:
            button = InlineKeyboardButton(text = item["product_name"], callback_data = f"product_{item["product_id"]}")
            builder.row(button)
        return builder.as_markup()
    async def product_kb(product):
        builder = InlineKeyboardBuilder()
        button_buy = InlineKeyboardButton(text = "Купить", callback_data = f"buy_{product[1]}")
        button_cancel = InlineKeyboardButton(text = "Отмена", callback_data = f"back")
        builder.add(button_buy, button_cancel)
        return builder.as_markup()
    async def deposit_kb(invoice, detailsr):
        builder = InlineKeyboardBuilder()
        buttonpay = InlineKeyboardButton(text ='Оплатить', url=invoice[3])
        button_checkpay = InlineKeyboardButton(text ='Я оплатил', callback_data=f"checkpayment_{invoice[0]}_{detailsr[0]["product_id"]}")
        button_cancelpay = InlineKeyboardButton(text ='Отмена', callback_data=f"cancelpayment_{invoice[0]}")
        builder.add(buttonpay, button_checkpay, button_cancelpay)
        return builder.as_markup()
    async def check_payment_kb(invoiceid):
        builder = InlineKeyboardBuilder()
        button_backToProd = InlineKeyboardButton(text ='Вернуться к покупке', callback_data=f"buy_{invoiceid[2]}")
        builder.add(button_backToProd)
        return builder.as_markup()
    async def buy_kb(user, details, product):
        builder = InlineKeyboardBuilder()
        if user[0]["balance"] >= details["price"]:
            button_finishbuy = InlineKeyboardButton(text = "Потдвердить покупку", callback_data = f"finishbuy_{product[1]}")
            button_cancel = InlineKeyboardButton(text = "Отмена", callback_data = f"back")
            builder.add(button_finishbuy, button_cancel)
        else: 
            button_deposit = InlineKeyboardButton(text = "Пополнить баланс", callback_data = f"deposit_{product[1]}")
            button_cancel = InlineKeyboardButton(text = "Отмена", callback_data = f"back")
            builder.add(button_deposit, button_cancel)
        return builder.as_markup()