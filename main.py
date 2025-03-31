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

from modules.payment import Payment
from modules.client import client_handlers
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
    client = client_handlers(db_instance, dp, pay)
    await client.main()
    #######
    
    
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    asyncio.run(main())
    
