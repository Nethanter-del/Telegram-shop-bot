# -*- coding: utf-8 -*-

# Developer: Nethanter-del
# Github: https://github.com/Nethanter-del
# Date Created: 2025-12-03
# Version: 1.0.0

# License: MIT License
#
# Copyright (c) 2025 Nethanter-del

import asyncpg

class bd:
    def __init__(self, host, user, password, database, owner):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.owner = owner
        self.conn = None

    async def init_db(self):
        try:
            self.conn = await asyncpg.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            await self.create_tables()
        except Exception:
            print(f"CRITICAL:-Connection to {self.database} corrupted")
            exit()
    async def create_tables(self):
        tables = '''CREATE TABLE IF NOT EXISTS public.products
(
    product_id SERIAL NOT NULL,
    category text COLLATE pg_catalog."default",
    product_name text COLLATE pg_catalog."default" NOT NULL,
    product_description text COLLATE pg_catalog."default",
    price bigint NOT NULL,
    product text COLLATE pg_catalog."default",
    CONSTRAINT products_pkey PRIMARY KEY (product_id)
)

TABLESPACE pg_default;

CREATE TABLE IF NOT EXISTS public.users
(
    id SERIAL NOT NULL,
    user_id bigint NOT NULL,
    username text COLLATE pg_catalog."default",
    is_admin boolean NOT NULL,
    state text COLLATE pg_catalog."default",
    balance bigint,
    purchase bigint,
    CONSTRAINT users_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;'''
        await self.conn.execute(tables)
    # unformated response to dictionary        
    async def format_response(self, values):
        return  [dict(record) for record in values]
    # create user
    async def create_user(self, user_id, username):
        is_admin = False
        if str(user_id) == str(self.owner):
            is_admin = True
        await self.conn.execute("INSERT INTO users (user_id, username, is_admin, balance) VALUES ($1, $2, $3, $4)", user_id, username, is_admin, 0)
    # fetch user info   
    async def get_user(self, user_id):
        values = await self.conn.fetch(f"SELECT * FROM users WHERE user_id = {user_id}")
        return await self.format_response(values)
    
    # check admin status True|False
    async def check_admin(self, user_id):
        values = await self.conn.fetch(f"SELECT * FROM users WHERE user_id = {user_id} AND is_admin = true")
        if len(values) > 0:
            return True
        else:
            return False
    # fetch all admins 
    async def select_admins(self):
        values = await self.conn.fetch(f"SELECT user_id FROM users WHERE is_admin = True")
        return await self.format_response(values)
    # get user state polling|waiting|free
    async def get_state(self, user_id):
        values = await self.conn.fetch(f"SELECT state FROM users WHERE user_id = {user_id}")
        return await self.format_response(values)
    # set user state polling|waiting|free
    async def set_state(self, user_id, state):
        await self.conn.execute("UPDATE users SET state = $1 WHERE user_id = $2", state, user_id)
    async def update_balance(self, user_id, balance): 
        await self.conn.execute("UPDATE users SET balance = $1 WHERE user_id = $2", balance, user_id)
    async def get_products(self):
        values = await self.conn.fetch(f"SELECT * FROM products")
        return await self.format_response(values)
    async def get_products_by_category(self, category):
        values = await self.conn.fetch(f"SELECT * FROM products WHERE category = $1", (category))
        return await self.format_response(values)
    async def get_product_by_id(self, id):
        values = await self.conn.fetch(f"SELECT * FROM products WHERE product_id = $1", (int(id)))
        return await self.format_response(values)