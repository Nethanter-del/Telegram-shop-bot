
from aiogram import types
from aiogram.filters.command import Command
from aiogram import F
from aiogram.enums import ParseMode

from modules.constructs import Constructs
from modules.payment import Payment
from modules.keyboards import keyboards
from modules.messages import _message

class client_handlers:
    def __init__(self, db_instance, dp, pay):
        self.db_instance = db_instance
        self.dp = dp 
        self.pay = pay
    async def main(self):
        @self.dp.message(Command("start"))
        async def start(message: types.Message):
            user = await self.db_instance.get_user(message.from_user.id)
            if len(user) < 1:
                await self.db_instance.create_user(message.from_user.id, message.from_user.username)
            await message.answer(text=_message.start_msg(), reply_markup=await keyboards.main_kb())
        async def _category(callback_query):
            category = callback_query.data.split("_")
            await callback_query.message.edit_text(text=f"✨ Категория:  {category[1]}")
            products = await self.db_instance.get_products_by_category(category[1])
            await callback_query.message.edit_reply_markup(reply_markup=await keyboards.category_kb(products))
            
        async def _product(callback_query):
            product = callback_query.data.split("_")
            detailsr = await self.db_instance.get_product_by_id(product[1])
            details = detailsr[0]
            await callback_query.message.edit_text(text=_message.product_msg(details))
            await callback_query.message.edit_reply_markup(reply_markup=await keyboards.product_kb(product))
            
        async def _buy(callback_query):
            product = callback_query.data.split("_")
            user = await self.db_instance.get_user(callback_query.from_user.id)
            detailsr = await self.db_instance.get_product_by_id(product[1])
            details = detailsr[0]
            if user[0]["balance"] >= details["price"]:
                await callback_query.message.edit_text(text=_message.buy_msg(details,user))
            else: 
                await callback_query.message.edit_text(text=_message.buy_alt_msg(details))
            await callback_query.message.edit_reply_markup(reply_markup=await keyboards.buy_kb(user, details, product))
        async def _finishbuy(callback_query):
            product = callback_query.data.split("_")
            user = await self.db_instance.get_user(callback_query.from_user.id)
            detailsr = await self.db_instance.get_product_by_id(product[1])
            details = detailsr[0]
            await self.db_instance.update_balance(callback_query.from_user.id, balance=int(user[0]["balance"]-details["price"]))
            await callback_query.message.edit_text(text=_message.finish_buy_msg(details, user))
            await self.db_instance.del_product(product[1])
        async def _deposit(callback_query):
            product = callback_query.data.split("_")
            user = await self.db_instance.get_user(callback_query.from_user.id)
            detailsr = await self.db_instance.get_product_by_id(product[1])
            details = detailsr[0]
            amount = int(details["price"]-user[0]["balance"])
            invoice = await self.pay.create_invoice(amount=amount, fiat='RUB')
            await callback_query.message.edit_text(text=_message.deposit_msg(invoice))
            await callback_query.message.edit_reply_markup(reply_markup=await keyboards.deposit_kb(invoice, detailsr))
        async def _checkpayment(callback_query):
            invoiceid = callback_query.data.split("_")
            invoice = await self.pay.check_status(invoiceid[1])
            if invoice[0].status == "active":
                pass
            elif invoice[0].status == "paid":
                await callback_query.message.edit_text(text=_message.deposit_paid_msg(invoice))
                await self.db_instance.update_balance(callback_query.from_user.id, balance=int(invoice[0].amount))
                await callback_query.message.edit_reply_markup(reply_markup=await keyboards.check_payment_kb(invoiceid))
        async def _cancelpayment(callback_query):
            invoiceid = callback_query.data.split("_")
            invoice = await self.pay.check_status(invoiceid[1])
            if invoice[0].status == "active":
                await self.pay.del_invoice(invoiceid[1])
                await callback_query.message.edit_text(text=_message.deposit_cancel_msg(invoice))
        async def _back(callback_query):
            await callback_query.message.delete()
            await start(callback_query.message)
        @self.dp.message(F.text == "Каталог 📦")
        async def catalog(message: types.Message):
            products = await self.db_instance.get_products()
            categories = await Constructs.format_products1(products)
            await message.answer(text="📦 Каталог товаров: ", reply_markup=await keyboards.catalog_kb(categories))
        @self.dp.message(F.text == "Наличие ✅")
        async def list_goods(message: types.Message):
            products = await self.db_instance.get_products()
            text = await Constructs.format_products(products)
            await message.answer(text=text)
        @self.dp.message(F.text == "Мой профиль 👤")
        async def profile(message: types.Message):
            user = await self.db_instance.get_user(message.from_user.id)
            await message.answer(text=_message.profile_msg(user))
        @self.dp.message(F.text == "FAQ ❓")
        async def faq(message: types.Message):
            await message.answer(text=_message.faq_msg())
        @self.dp.callback_query()    
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