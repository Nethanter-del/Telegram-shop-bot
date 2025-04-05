# -*- coding: utf-8 -*-

# Developer: Nethanter-del
# Github: https://github.com/Nethanter-del
# Date Created: 2025-25-03
# Version: 1.0.0

# License: MIT License
#
# Copyright (c) 2025 Nethanter-del
from aiocryptopay import AioCryptoPay, Networks


class Payment:
    def __init__(self, token):
        self.crypto = AioCryptoPay(token=token, network=Networks.MAIN_NET)
    
    async def get(self):
        profile = await self.crypto.get_me()
        balance = await self.crypto.get_balance()

    async def create_invoice(self, amount, fiat='USD'):
        invoice = await self.crypto.create_invoice(amount=amount, fiat=fiat, currency_type='fiat')
       
        return invoice.invoice_id, invoice.status, invoice.amount, invoice.bot_invoice_url
    
    async def check_status(self, invoice_id):
        
        invoice = await self.crypto.get_invoices(invoice_ids=invoice_id)
        
        return invoice
    async def del_invoice(self, invoice_id):
        invoice = await self.crypto.delete_invoice(invoice_id=invoice_id)

        
