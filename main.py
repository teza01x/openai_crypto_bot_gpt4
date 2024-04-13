import asyncio
import time
import aiofiles
from telebot.async_telebot import AsyncTeleBot
from telebot.types import InlineKeyboardMarkup
from telebot import types
from datetime import datetime
from async_markdownv2 import *
from async_sqlite import *
from text_scripts import *
from async_funcs import *
from blockchain import *
from openai import *
from config import *


bot = AsyncTeleBot(telegram_token)


@bot.message_handler(commands=['start'])
async def start(message):
    try:
        user_id = message.from_user.id
        username = message.from_user.username

        chat_type = message.chat.type
        if chat_type == 'private':
            main_menu_text = text_dict['main_menu']

            main_menu_text = await escape(main_menu_text, flag=0)

            button_list1 = [
                types.InlineKeyboardButton("✨ Ask project question", callback_data="project_question"),
                types.InlineKeyboardButton("⭐️ Ask any question", callback_data="any_question"),
            ]

            button_list2 = [
                types.InlineKeyboardButton("🖼 Generate Image", callback_data="img_generate"),
                types.InlineKeyboardButton("🧾 Image Analysis", callback_data="img_analyze"),
            ]
            button_list3 = [
                types.InlineKeyboardButton("📊 Analyze Token", callback_data="token_analyze"),
                types.InlineKeyboardButton("📝 Analyze Wallet", callback_data="wallet_analyze"),
            ]
            button_list4 = [
                types.InlineKeyboardButton("📈 Technical Analysis", callback_data="coming_soon"),
                types.InlineKeyboardButton("🔎 Crypto News", callback_data="crypto_news"),
            ]
            button_list5 = [
                types.InlineKeyboardButton("🤖 AI Automated Trading Bot", callback_data="coming_soon"),
                types.InlineKeyboardButton("🤖 AI Automated Token Audit", callback_data="coming_soon"),
            ]
            reply_markup = types.InlineKeyboardMarkup([button_list1, button_list2, button_list3, button_list4, button_list5])
            await bot.send_message(message.chat.id, text=main_menu_text, reply_markup=reply_markup, parse_mode="MarkdownV2", disable_web_page_preview=True)

            if not await check_user_exists(user_id):
                try:
                    await add_user_to_db(user_id, username, START_MENU_STATUS)
                except Exception as error:
                    print(f"Error adding user to db error:\n{error}")
            else:
                await update_username(user_id, username)
    except Exception as e:
        print(f"Error in start message: {e}")


@bot.callback_query_handler(func=lambda call: True)
async def callback_query(call):
    user_id = call.message.chat.id
    if call.data == "project_question":
        await bot.answer_callback_query(call.id)
        await change_menu_status(user_id, ASK_PROJECT_STATUS)

        text = text_dict['project_question'] + project_signature
        text = await escape(text, flag=0)

        button_list1 = [
            types.InlineKeyboardButton("🔙 Back", callback_data="main_menu"),
        ]
        reply_markup = types.InlineKeyboardMarkup([button_list1])

        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=reply_markup, parse_mode="MarkdownV2")

    elif call.data == "any_question":
        await bot.answer_callback_query(call.id)
        await change_menu_status(user_id, ASK_ANY_STATUS)

        text = text_dict['any_question'] + project_signature
        text = await escape(text, flag=0)

        button_list1 = [
            types.InlineKeyboardButton("🔙 Back", callback_data="main_menu"),
        ]
        reply_markup = types.InlineKeyboardMarkup([button_list1])

        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=reply_markup, parse_mode="MarkdownV2")

    elif call.data == "img_generate":
        await bot.answer_callback_query(call.id)
        await change_menu_status(user_id, GENERATE_IMAGE)

        text = text_dict['img_generate'] + project_signature
        text = await escape(text, flag=0)

        button_list1 = [
            types.InlineKeyboardButton("🔙 Back", callback_data="main_menu"),
        ]
        reply_markup = types.InlineKeyboardMarkup([button_list1])

        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=reply_markup, parse_mode="MarkdownV2")

    elif call.data == "img_generate_new":
        await bot.answer_callback_query(call.id)
        await change_menu_status(user_id, GENERATE_IMAGE)

        text = text_dict['img_generate'] + project_signature
        text = await escape(text, flag=0)

        button_list1 = [
            types.InlineKeyboardButton("🔙 Back", callback_data="main_menu"),
        ]
        reply_markup = types.InlineKeyboardMarkup([button_list1])

        await bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=reply_markup, parse_mode="MarkdownV2")

    elif call.data == "img_analyze":
        await bot.answer_callback_query(call.id)
        await change_menu_status(user_id, ANALYZE_IMAGE)

        text = text_dict['img_analyze'] + project_signature
        text = await escape(text, flag=0)

        button_list1 = [
            types.InlineKeyboardButton("🔙 Back", callback_data="main_menu"),
        ]
        reply_markup = types.InlineKeyboardMarkup([button_list1])

        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=reply_markup, parse_mode="MarkdownV2")

    elif call.data == "crypto_news":
        await bot.answer_callback_query(call.id)
        news = await scrap_binance()

        try:
            text = "🆕 **Latest News** 🆕\n\n" + "\n\n".join(news) + project_signature
            text = await escape(text, flag=0)
        except:
            text = "Technical problems, please try again later." + project_signature
            text = await escape(text, flag=0)


        button_list1 = [
            types.InlineKeyboardButton("🔙 Back", callback_data="main_menu"),
        ]
        reply_markup = types.InlineKeyboardMarkup([button_list1])

        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=reply_markup, parse_mode="MarkdownV2")

    elif call.data == "wallet_analyze":
        await bot.answer_callback_query(call.id)
        await change_menu_status(user_id, ANALYZE_WALLET)

        text = text_dict['wallet_analyze'] + project_signature
        text = await escape(text, flag=0)

        button_list1 = [
            types.InlineKeyboardButton("🔙 Back", callback_data="main_menu"),
        ]
        reply_markup = types.InlineKeyboardMarkup([button_list1])

        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=reply_markup, parse_mode="MarkdownV2")

    elif call.data == "wallet_analyze_new":
        await bot.answer_callback_query(call.id)
        await change_menu_status(user_id, ANALYZE_WALLET)

        text = text_dict['wallet_analyze'] + project_signature
        text = await escape(text, flag=0)

        button_list1 = [
            types.InlineKeyboardButton("🔙 Back", callback_data="main_menu"),
        ]
        reply_markup = types.InlineKeyboardMarkup([button_list1])

        await bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=reply_markup, parse_mode="MarkdownV2")

    elif call.data == "token_analyze":
        await bot.answer_callback_query(call.id)
        await change_menu_status(user_id, ANALYZE_TOKEN)

        text = text_dict['token_analyze'] + project_signature
        text = await escape(text, flag=0)

        button_list1 = [
            types.InlineKeyboardButton("🔙 Back", callback_data="main_menu"),
        ]
        reply_markup = types.InlineKeyboardMarkup([button_list1])

        await bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=reply_markup, parse_mode="MarkdownV2")


    elif call.data == "main_menu":
        await bot.answer_callback_query(call.id)
        text = text_dict['main_menu'] + project_signature
        text = await escape(text, flag=0)
        await change_menu_status(user_id, START_MENU_STATUS)

        button_list1 = [
            types.InlineKeyboardButton("✨ Ask project question", callback_data="project_question"),
            types.InlineKeyboardButton("⭐️ Ask any question", callback_data="any_question"),
        ]
        button_list2 = [
            types.InlineKeyboardButton("🖼 Generate Image", callback_data="img_generate"),
            types.InlineKeyboardButton("🧾 Image Analysis", callback_data="img_analyze"),
        ]
        button_list3 = [
            types.InlineKeyboardButton("📊 Analyze Token", callback_data="token_analyze"),
            types.InlineKeyboardButton("📝 Analyze Wallet", callback_data="wallet_analyze"),
        ]
        button_list4 = [
            types.InlineKeyboardButton("📈 Technical Analysis", callback_data="coming_soon"),
            types.InlineKeyboardButton("🔎 Crypto News", callback_data="crypto_news"),
        ]
        button_list5 = [
            types.InlineKeyboardButton("🤖 AI Automated Trading Bot", callback_data="coming_soon"),
            types.InlineKeyboardButton("🤖 AI Automated Token Audit", callback_data="coming_soon"),
        ]
        reply_markup = types.InlineKeyboardMarkup([button_list1, button_list2, button_list3, button_list4, button_list5])
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=reply_markup, parse_mode="MarkdownV2")

    elif call.data == "main_menu_new":
        await bot.answer_callback_query(call.id)
        text = text_dict['main_menu'] + project_signature
        text = await escape(text, flag=0)
        await change_menu_status(user_id, START_MENU_STATUS)

        button_list1 = [
            types.InlineKeyboardButton("✨ Ask project question", callback_data="project_question"),
            types.InlineKeyboardButton("⭐️ Ask any question", callback_data="any_question"),
        ]
        button_list2 = [
            types.InlineKeyboardButton("🖼 Generate Image", callback_data="img_generate"),
            types.InlineKeyboardButton("🧾 Image Analysis", callback_data="img_analyze"),
        ]
        button_list3 = [
            types.InlineKeyboardButton("📊 Analyze Token", callback_data="token_analyze"),
            types.InlineKeyboardButton("📝 Analyze Wallet", callback_data="wallet_analyze"),
        ]
        button_list4 = [
            types.InlineKeyboardButton("📈 Technical Analysis", callback_data="coming_soon"),
            types.InlineKeyboardButton("🔎 Crypto News", callback_data="crypto_news"),
        ]
        button_list5 = [
            types.InlineKeyboardButton("🤖 AI Automated Trading Bot", callback_data="coming_soon"),
            types.InlineKeyboardButton("🤖 AI Automated Token Audit", callback_data="coming_soon"),
        ]
        reply_markup = types.InlineKeyboardMarkup([button_list1, button_list2, button_list3, button_list4, button_list5])
        await bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=reply_markup, parse_mode="MarkdownV2")

    elif call.data == "coming_soon":
        await bot.answer_callback_query(call.id)

        text = text_dict['coming_soon'] + project_signature
        text = await escape(text, flag=0)

        button_list1 = [
            types.InlineKeyboardButton("🔙 Back", callback_data="main_menu"),
        ]
        reply_markup = types.InlineKeyboardMarkup([button_list1])

        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=reply_markup, parse_mode="MarkdownV2")


@bot.message_handler(func=lambda message: True, content_types=['text'])
async def handle_text(message):
    chat_type = message.chat.type
    if chat_type == 'private':
        user_id = message.chat.id
        user_status = await get_user_status(user_id)

        if user_status == ASK_PROJECT_STATUS:
            user_question = message.text
            ai_answer = await fetch_openai_completion(openai_prompt['project_question_prompt'], user_question)
            text = "🤖 **AI Assistant** 🤖\n\n" + ai_answer + project_signature
            text = await escape(text, flag=0)

            button_list0 = [
                types.InlineKeyboardButton("🔄 Try Again", callback_data="project_question"),
            ]
            button_list1 = [
                types.InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu"),
            ]
            reply_markup = types.InlineKeyboardMarkup([button_list0, button_list1])

            await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=reply_markup, parse_mode="MarkdownV2")
            await change_menu_status(user_id, START_MENU_STATUS)

        elif user_status == ASK_ANY_STATUS:
            user_question = message.text
            ai_answer = await fetch_openai_completion(openai_prompt['any_question_prompt'], user_question)
            text = "🤖 **AI Assistant** 🤖\n\n" + ai_answer + project_signature
            text = await escape(text, flag=0)

            button_list0 = [
                types.InlineKeyboardButton("🔄 Try Again", callback_data="any_question"),
            ]
            button_list1 = [
                types.InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu"),
            ]
            reply_markup = types.InlineKeyboardMarkup([button_list0, button_list1])

            await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=reply_markup, parse_mode="MarkdownV2")
            await change_menu_status(user_id, START_MENU_STATUS)

        elif user_status == GENERATE_IMAGE:
            user_img_prompt = message.text
            await bot.send_message(chat_id=message.chat.id, text='⚡️ Please wait a few seconds, the image is being generated ⚡️')
            img_text, img_name = await img_openai_generation(user_img_prompt)
            text = await escape(img_text, flag=0)

            button_list0 = [
                types.InlineKeyboardButton("🔄 Try Again", callback_data="img_generate_new"),
            ]
            button_list1 = [
                types.InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu_new"),
            ]
            reply_markup = types.InlineKeyboardMarkup([button_list0, button_list1])

            with open(image_dir_path + img_name, 'rb') as image:
                await bot.send_photo(chat_id=message.chat.id, photo=image, caption=text + project_signature, reply_markup=reply_markup, parse_mode="MarkdownV2")
            await change_menu_status(user_id, START_MENU_STATUS)

        elif user_status == ANALYZE_WALLET:
            wallet = message.text
            await bot.send_message(chat_id=message.chat.id, text='⚡️ Please wait a few seconds, information on your wallet is collecting... ⚡️')
            try:
                bought_template, sold_template, pnl, eth_hold, other_coin_hold_list = await check_transaction_hash(wallet)

                if len(bought_template) == 0:
                    bought_template = ["No purchases in the last 10 trades."]
                if len(sold_template) == 0:
                    sold_template = ["There are no sales in the last 10 trades."]
                if len(other_coin_hold_list) > 5:
                    holdings = "\n - ".join(other_coin_hold_list[:5]) + f"\n\n **➕ also {len(other_coin_hold_list)-5} more coins**\n"
                else:
                    holdings = "\n - ".join(other_coin_hold_list[:5])

                text = text_dict['wallet_analyze_template'].format(wallet, wallet, eth_hold, pnl, holdings, "\n - ".join(bought_template), "\n - ".join(sold_template))
            except:
                text = "Technical problems, please try again later."
            text = await escape(text, flag=0)

            button_list0 = [
                types.InlineKeyboardButton("🔄 Try Again", callback_data="wallet_analyze_new"),
            ]
            button_list1 = [
                types.InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu_new"),
            ]
            reply_markup = types.InlineKeyboardMarkup([button_list0, button_list1])

            await bot.send_message(chat_id=message.chat.id, text=text + project_signature, reply_markup=reply_markup, parse_mode="MarkdownV2", disable_web_page_preview=True)
            await change_menu_status(user_id, START_MENU_STATUS)

        elif user_status == ANALYZE_TOKEN:
            contract_address = message.text
            await bot.send_message(chat_id=message.chat.id, text='⚡️ Please wait a few seconds, information on contract address is collecting... ⚡️')




@bot.message_handler(func=lambda message: True, content_types=["photo"])
async def handle_photo(message):
    chat_type = message.chat.type
    if chat_type == 'private':
        user_id = message.chat.id
        user_status = await get_user_status(user_id)

        if user_status == ANALYZE_IMAGE:
            file_id = message.photo[-1].file_id
            file_info = await bot.get_file(file_id)

            file_url = f'https://api.telegram.org/file/bot{telegram_token}/{file_info.file_path}'
            file_path = image_dir_path + f"{file_id}.jpg"

            async with aiohttp.ClientSession() as session:
                async with session.get(file_url) as response:
                    if response.status == 200:
                        async with aiofiles.open(file_path, 'wb') as f:
                            await f.write(await response.read())

            image_text = await image_to_text_openai(file_path)
            text = await escape(image_text, flag=0)


            button_list0 = [
                types.InlineKeyboardButton("🔄 Try Again", callback_data="img_analyze"),
            ]
            button_list1 = [
                types.InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu"),
            ]
            reply_markup = types.InlineKeyboardMarkup([button_list0, button_list1])


            await bot.send_message(chat_id=message.chat.id, text="🤖 **AI Generated** 🤖\n\n" + text + project_signature, reply_markup=reply_markup, parse_mode="MarkdownV2")


async def main():
    try:
        bot_task = asyncio.create_task(bot.polling(non_stop=True, request_timeout=500))
        await asyncio.gather(bot_task)
    except Exception as error:
        print(error)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
