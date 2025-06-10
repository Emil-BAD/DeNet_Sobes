from web3 import Web3
import abi
from config import POLYGON_URL, TOKEN_ADDRESS
from models.TokenInfo import TokenInfo
from models.TransferEvent import TransferEvent
import time

web3 = Web3(Web3.HTTPProvider(POLYGON_URL))

if not web3.is_connected():
    raise ConnectionError("Не удалось подключиться к сети Polygon!")

contract = web3.eth.contract(address=Web3.to_checksum_address(TOKEN_ADDRESS), abi=abi.erc20_abi)

def get_token_info() -> TokenInfo:
    """
    Получение информации о токене (название, символ, десятичные знаки).
    
    Аргументы:
        Нет аргументов.
    
    Возвращается:
        TokenInfo: Объект с информацией о токене (название, символ, десятичные знаки, общее количество, если доступно).
    """
    try:
        name = contract.functions.name().call()
        symbol = contract.functions.symbol().call()
        decimals = contract.functions.decimals().call()
        total_supply = contract.functions.totalSupply().call() if 'totalSupply' in [func.fn_name for func in contract.functions] else None
        return TokenInfo(name=name, symbol=symbol, decimals=decimals, total_supply=total_supply)
    except Exception as e:
        print(f"Ошибка при получении информации о токене: {e}")
        return TokenInfo(name="Неизвестно", symbol="N/A", decimals=0)

def get_balance(address: str) -> float:
    """
    Получение баланса по одиночному адресу.
    
    Аргументы:
        address (str): Адрес кошелька для проверки.
    
    Возвращается:
        float: Баланс в удобочитаемом формате (разделенный на 10^18).
    """
    checksum_address = web3.to_checksum_address(address)
    balance = contract.functions.balanceOf(checksum_address).call()
    return balance / 10 ** 18

def get_balance_batch(wallets: list) -> list:
    """
    Получение баланса токенов для списка адресов.
 
    Аргументы:
        wallets (list): Список адресов кошельков.
 
    Возвращается:
        list: Список балансов в удобочитаемом формате.
    """
    return [get_balance(web3.to_checksum_address(addr)) for addr in wallets]