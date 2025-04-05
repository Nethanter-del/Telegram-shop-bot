# -*- coding: utf-8 -*-

# Developer: Nethanter-del
# Github: https://github.com/Nethanter-del
# Date Created: 2025-03-04
# Version: 1.0.0

# License: MIT License
#
# Copyright (c) 2025 Nethanter-del
class _message:

    def start_msg():
        return (
"""👋 Добро пожаловать в Test_market"""
        )
    def product_msg(details):
        return (
f"""💎 Товар: {details["product_name"]} 
|
├ Описание: {details["product_description"]}
╰ Цена {details["price"]} ₽"""
        )
    def buy_msg(details, user):
        return (
f"""🛒 Покупка 
├ Товар: {details["product_name"]} 
| 
├ Цена {details["price"]} ₽
╰ Ваш баланс: {user[0]["balance"]}"""
        )
    def buy_alt_msg(details):
        return (
f"""🛒 Покупка 
├ Товар: {details["product_name"]} 
| 
├ Цена {details["price"]} ₽
╰ На вашем балансе недостаточно средств!"""
        )
    def finish_buy_msg(details, user):
        return (
f"""🎉 Успешная покупка: 
├ Товар: {details["product_name"]} 
├ Цена: {details["price"]} ₽ 
├ Ваш баланс: {int(user[0]["balance"]-details["price"])} ₽ 
|
╰ Данные: {details["product"]}"""
        )
    def deposit_msg(invoice):
        return (
f"""💸 Пополнение баланса 
├ Платеж: #{invoice[0]} 
├ Статус: {invoice[1]} 
╰ Сумма: {invoice[2]} ₽"""
        )
    def deposit_paid_msg(invoice):
        return (
f"""🎊 Баланс пополнен
├ Платеж: #{invoice[0].invoice_id} 
├ Статус: {invoice[0].status}
╰ Сумма: {invoice[0].amount} ₽"""
        )
    def deposit_cancel_msg(invoice):
        return (
f"""❌ Пополнение отменено 
├ Платеж: #{invoice[0].invoice_id} 
├ Статус: cancel 
╰ Сумма: {invoice[0].amount} ₽"""
        )
    def profile_msg(user):
        return (
f"""🧑‍💻 Ваш профиль
├ Айди: {user[0]["user_id"]}
├ Баланс: {user[0]["balance"]} ₽
╰ Администратор: {user[0]["is_admin"]}"""
        )
    def faq_msg():
        return (
"""test faq"""
        )
    def s1tart_msg():
        return (
"""Добро пожаловать в -------"""
        )
    def st1art_msg():
        return (
"""Добро пожаловать в -------"""
        )