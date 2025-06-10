import requests
from web3 import Web3
from config import MORALIS_API_KEY, TOKEN_ADDRESS
from models.ResponseTopWithTransfer import ResponseTransfer

if not MORALIS_API_KEY or not TOKEN_ADDRESS:
    raise ValueError("Отсутствует MORALIS_API_KEY или TOKEN_ADDRESS в файле .env!")

token_address = Web3.to_checksum_address(TOKEN_ADDRESS)
url = f"https://deep-index.moralis.io/api/v2.2/erc20/{token_address}/owners?chain=polygon&limit=5"
url_data_tranfers = f"https://deep-index.moralis.io/api/v2.2/{token_address}/erc20/transfers"
headers = {"X-API-Key": MORALIS_API_KEY}

def get_transfer_history(wallet_address: str, limit: int = 10) -> list[ResponseTransfer]:
    """
Получение истории трансферов для указанного адреса.

Аргументы:
wallet_address (str): Адрес кошелька для проверки.
limit (int, optional): Максимальное количество трансферов для возврата. По умолчанию 10.

Возвращается:
list[ResponseTransfer]: Список объектов трансферов, связанных с адресом.
"""
    try:
        params = {
            "chain": "polygon",
            "order": "DESC",
            "address": wallet_address,
            "limit": limit
        }
        response = requests.get(url_data_tranfers, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data.get("result"):
            transfers = [ResponseTransfer(**item) for item in data["result"]]
            return transfers
        print("Нет данных о трансферах для данного адреса.")
        return []
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса к Moralis API (transfers): {e}")
        return []
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
        return []

def get_top(num):
    """
    Получить топ N держателей токена через API Moralis.

    Аргументы:
    num (int): Количество топовых держателей для возврата.

    Возвращает:
    list: Список кортежей (address, balance) для топовых держателей.

    Вызывает исключения:
    requests.exceptions.RequestException: Если запрос к API завершится неудачно.
    KeyError: Если в ответе API отсутствует поле 'result'.
    """
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        top = []
        for item in data['result']:
            address = item["owner_address"]
            balance = int(item["balance"]) / 10**18
            top.append((address, balance))
        
        return top[:num]
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса к Moralis API: {e}")
        return []
    except KeyError:
        print("Ошибка: данные в ответе API не содержат поля 'result'")
        return []
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
        return []

def get_with_transfer_single(wallet_address: str) -> ResponseTransfer:
    """
    Получить информаци о трансфере переданного держателя токена.

    Аргументы:
    wallet_address (str): Адрес держателя

    Возвращает:
    ResponseTransfer: Модель валидирующая данные ответа.

    Вызывает исключения:
    requests.exceptions.RequestException: Если запрос к API завершится неудачно.
    KeyError: Если в ответе API отсутствует поле 'result'.
    """
    try:
        params = {
        "chain": "polygon",
        "contract_addresses": [
            "0x1a9b54a3075119f1546c52ca0940551a6ce5d2d0"
        ],
        "order": "DESC",
        "address": wallet_address
        }
        response = requests.get(url_data_tranfers, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        transfer = ResponseTransfer(**data["result"][0])
        return transfer
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса трансфера: {e}")
        return None
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
        return None

def get_top_with_transfer(num: int) -> list:
    """
    Получить топ N держателей токена с информацией о последнем трансфере.

    Аргументы:
    num (int): Количество топовых держателей для возврата.

    Возвращает:
    list: Список кортежей (address, balance, ResponseTransfer) для топовых держателей.
    """
    top_with_transfer = []
    top = get_top(num)
    for address, balance in top:
        transfer = get_with_transfer_single(address)
        top_with_transfer.append((address, balance, transfer))
    return top_with_transfer