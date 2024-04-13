import asyncio
import aiohttp
import time
import requests
from moralis import evm_api
from config import *


async def coin_holds(wallet):
    try:
        url = f"https://deep-index.moralis.io/api/v2.2/wallets/{wallet}/tokens?chain=eth"

        headers = {
            "Accept": "application/json",
            "X-API-Key": f"{moralis_api_key}"
        }

        response = requests.request("GET", url, headers=headers)

        hold = response.json()['result']
        coin_hold = list()
        for coin in hold:
            coin_symbol = coin['symbol']
            coin_contract = coin['token_address']
            coin_value = round(float(coin['balance_formatted']), 4)
            if coin_contract == '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE':
                coin_hold.append(f"{coin_value} {coin_symbol}")
            else:
                coin_hold.append(f"{coin_value} [{coin_symbol}](https://etherscan.io/token/{coin_contract})")


        other_coins = list()
        count = 0
        for coin in coin_hold:
            if "ETH" in coin and count == 0:
                eth_hold = coin
                count += 1
            else:
                other_coins.append(coin)

        return eth_hold, other_coins
    except Exception as error:
        print("Error in coin_hold()")
        print(error)


async def last_month_trade(bought_tx, sold_tx, local_db):
    try:
        bought_summary = float(0)
        bought_template = list()

        for b_tx in bought_tx:
            if b_tx['hash'] in local_db:
                bought_template.append(f"[{b_tx['tokenSymbol']}](https://etherscan.io/tx/{b_tx['hash']}) - {round((int(b_tx['value']) / (10 ** int(b_tx['tokenDecimal']))) * float(local_db[b_tx['hash']]), 3)} ETH")
                bought_summary += round((int(b_tx['value']) / (10 ** int(b_tx['tokenDecimal']))) * float(local_db[b_tx['hash']]), 3)
            else:
                bought_template.append(f"[{b_tx['tokenSymbol']}](https://etherscan.io/tx/{b_tx['hash']}) - 0.0 ETH")

        sold_summary = float(0)
        sold_template = list()

        for s_tx in sold_tx:
            if s_tx['hash'] in local_db:
                sold_template.append(f"[{s_tx['tokenSymbol']}](https://etherscan.io/tx/{s_tx['hash']}) - {round((int(s_tx['value']) / (10 ** int(s_tx['tokenDecimal']))) * float(local_db[s_tx['hash']]), 3)} ETH")
                sold_summary += round((int(s_tx['value']) / (10 ** int(s_tx['tokenDecimal']))) * float(local_db[s_tx['hash']]), 3)
            else:
                sold_template.append(f"[{s_tx['tokenSymbol']}](https://etherscan.io/tx/{s_tx['hash']}) - 0.0 ETH")

        return round(bought_summary, 3), round(sold_summary, 3)
    except Exception as error:
        print("Error in last_month_trade()")
        print(error)


async def parse_txs(txs_list, wallet, block):
    try:
        bought_tx = list()
        sold_tx = list()
        contract_info = list()
        contract_list = list()

        bought_last_month = list()
        sold_last_month = list()

        count = 0
        for tx in txs_list[::-1]:
            if count <= 10:
                if tx['to'].lower() == wallet.lower():
                    bought_tx.append(tx)
                    if int(tx['blockNumber']) >= int(block):
                        bought_last_month.append(tx)
                elif tx['to'].lower() != wallet.lower():
                    sold_tx.append(tx)
                    if int(tx['blockNumber']) >= int(block):
                        sold_last_month.append(tx)

                contract_info.append((tx['hash'], tx['contractAddress'], tx['blockNumber']))

            count += 1


        contract_list = list()
        for contract in contract_info:
            contract_list.append(
                {
                    "token_address": contract[1],
                    "to_block": contract[2]
                }
            )


        old_prices = await check_token_prices(contract_list)

        local_db = dict()
        for hash, price in zip(contract_info, old_prices):
            local_db[f'{hash[0]}'] = int(price['nativePrice']['value']) / (10 ** price['nativePrice']['decimals'])

        local_db = {k: f"{v:.20f}" if v < 0.0001 else f"{v}" for k, v in local_db.items()}

        b_lst_m, s_las_m = await last_month_trade(bought_last_month, sold_last_month, local_db)

        pnl = round(float(s_las_m - b_lst_m), 3)

        bought_summary = float(0)
        bought_template = list()
        sold_summary = float(0)
        sold_template = list()


        for b_tx in bought_tx:
            if b_tx['hash'] in local_db:
                bought_template.append(f"[{b_tx['tokenSymbol']}](https://etherscan.io/tx/{b_tx['hash']}) - {round((int(b_tx['value']) / (10 ** int(b_tx['tokenDecimal']))) * float(local_db[b_tx['hash']]), 3)} ETH")
                bought_summary += round((int(b_tx['value']) / (10 ** int(b_tx['tokenDecimal']))) * float(local_db[b_tx['hash']]), 3)
            else:
                bought_template.append(f"[{b_tx['tokenSymbol']}](https://etherscan.io/tx/{b_tx['hash']}) - 0.0 ETH")

        for s_tx in sold_tx:
            if s_tx['hash'] in local_db:
                sold_template.append(f"[{s_tx['tokenSymbol']}](https://etherscan.io/tx/{s_tx['hash']}) - {round((int(s_tx['value']) / (10 ** int(s_tx['tokenDecimal']))) * float(local_db[s_tx['hash']]), 3)} ETH")
                sold_summary += round((int(s_tx['value']) / (10 ** int(s_tx['tokenDecimal']))) * float(local_db[s_tx['hash']]), 3)
            else:
                sold_template.append(f"[{s_tx['tokenSymbol']}](https://etherscan.io/tx/{s_tx['hash']}) - 0.0 ETH")


        eth_hold, other_coin_hold_list = await coin_holds(wallet)

        return bought_template, sold_template, pnl, eth_hold, other_coin_hold_list
    except Exception as error:
        print("Error in parse_txs()")
        print(error)


async def check_token_prices(contract_list):
    try:
        body = {
            "tokens": contract_list
        }

        params = {
            "chain": "eth",
        }

        result = evm_api.token.get_multiple_token_prices(
            api_key=moralis_api_key,
            body=body,
            params=params,
        )

        return result
    except Exception as error:
        print("Error in check_token_prices()")
        print(error)


async def check_transaction_hash(wallet):
    try:
        txs_url = f"https://api.etherscan.io/api?module=account&action=tokentx&address={wallet}&page=1&offset=10000&startblock=0&endblock=999999999&sort=asc&apikey={etherscan_api_key}"
        async with aiohttp.ClientSession() as session:
            async with session.get(txs_url) as response:
                if response.status == 200:
                    result = await response.json()
                    txs_list = result['result']

                    past_month_unix = int(time.time()) - (60 * 60 * 24 * 30)

                    block_url = f"https://api.etherscan.io/api?module=block&action=getblocknobytime&timestamp={past_month_unix}&closest=before&apikey={etherscan_api_key}"
                    async with aiohttp.ClientSession() as session:
                        async with session.get(block_url) as response:
                            if response.status == 200:
                                block_result = await response.json()
                                block = block_result['result']

                                return await parse_txs(txs_list, wallet, block)
    except Exception as error:
        print("Error in check_transaction_hash()")
        print(error)
