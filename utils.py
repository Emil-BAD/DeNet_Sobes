from tabulate import tabulate
from models.TokenInfo import TokenInfo
from models.ResponseTopWithTransfer import ResponseTransfer
import colorama
from colorama import Fore, Style

colorama.init()

def print_balance(address: str, balance: float, token_symbol: str = "TBY"):
    print(f"{Fore.GREEN}Адрес: {address}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Баланс: {balance:.6f} {token_symbol}{Style.RESET_ALL}\n")

def print_balance_table(addresses: list, balances: list, token_symbol: str = "TBY"):
    data = [[addr, f"{bal:.6f} {token_symbol}"] for addr, bal in zip(addresses, balances)]
    print(tabulate(data, headers=[Fore.YELLOW + "Адрес" + Style.RESET_ALL, Fore.YELLOW + "Баланс" + Style.RESET_ALL], tablefmt="pretty"))
    
def print_top_holders(holders: list, token_symbol: str = "TBY"):
    if not holders:
        print(f"{Fore.RED}Нет данных о держателях.{Style.RESET_ALL}")
        return
    
    data = [[addr, f"{bal:.6f} {token_symbol}"] for addr, bal in holders]
    print(f"\n{Fore.YELLOW}Топ держателей токена:{Style.RESET_ALL}")
    print(tabulate(data, headers=[Fore.CYAN + "Адрес" + Style.RESET_ALL, Fore.CYAN + "Баланс" + Style.RESET_ALL], tablefmt="pretty"))

def print_top_holders_with_transfer(holders: list, token_symbol: str = "TBY"):
    if not holders:
        print(f"{Fore.RED}Нет данных о держателях.{Style.RESET_ALL}")
        return

    data = []
    for address, balance, transfer in holders:
        transfer_info = (
            f"{transfer.token_name} | {transfer.block_timestamp.strftime('%Y-%m-%d %H:%M')} | "
            f"{transfer.transaction_hash[:10]}... | Spam: {transfer.possible_spam}"
            if transfer else "Нет данных"
        )
        data.append([address, f"{balance:.6f} {token_symbol}", transfer_info])

    print(f"\n{Fore.YELLOW}Топ держателей токена с трансферами:{Style.RESET_ALL}")
    print(tabulate(
        data,
        headers=[Fore.CYAN + "Адрес" + Style.RESET_ALL, Fore.CYAN + "Баланс" + Style.RESET_ALL, Fore.CYAN + "Последний трансфер" + Style.RESET_ALL],
        tablefmt="pretty"
    ))
    
def print_token_info(token_info: TokenInfo):
    print(f"\n{Fore.YELLOW}Информация о токене:{Style.RESET_ALL}")
    data = [
        ["Название", token_info.name],
        ["Символ", token_info.symbol],
        ["Десятичные знаки", str(token_info.decimals)],
        ["Общее количество", f"{token_info.total_supply / 10**token_info.decimals:.2f} {token_info.symbol}" if token_info.total_supply else "Неизвестно"]
    ]
    print(tabulate(data, tablefmt="pretty", colalign=("left", "left")))

def print_transfer_history(transfers: list[ResponseTransfer], token_symbol: str = "TBY"):
    if not transfers:
        print(f"{Fore.RED}Нет истории трансферов.{Style.RESET_ALL}")
        return
    print(f"\n{Fore.YELLOW}История трансферов для адреса:{Style.RESET_ALL}")
    data = [
        [
            t.from_address,
            t.to_address,
            f"{t.value:.6f} {token_symbol}",
            t.block_timestamp.strftime('%Y-%m-%d %H:%M'),
            t.transaction_hash[:10] + "..." if t.transaction_hash else "N/A",
            "Да" if t.possible_spam else "Нет"
        ]
        for t in transfers
    ]
    print(tabulate(
        data,
        headers=[
            Fore.CYAN + "От" + Style.RESET_ALL,
            Fore.CYAN + "К" + Style.RESET_ALL,
            Fore.CYAN + "Значение" + Style.RESET_ALL,
            Fore.CYAN + "Время" + Style.RESET_ALL,
            Fore.CYAN + "Хэш" + Style.RESET_ALL,
            Fore.CYAN + "Спам?" + Style.RESET_ALL
        ],
        tablefmt="pretty"
    ))
    