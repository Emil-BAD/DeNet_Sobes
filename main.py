from contract import get_balance, get_balance_batch, get_token_info
from utils import print_balance, print_balance_table, print_top_holders, print_top_holders_with_transfer, print_token_info, print_transfer_history
from moralesAPI import get_top, get_top_with_transfer, get_transfer_history
from colorama import Fore, Style

if __name__ == "__main__":
    try:
        single_address = "0x51f1774249Fc2B0C2603542Ac6184Ae1d048351d"
        balance = get_balance(single_address)
        print_balance(single_address, balance)

        batch_addresses = [
            "0x51f1774249Fc2B0C2603542Ac6184Ae1d048351d",
            "0x4830AF4aB9cd9E381602aE50f71AE481a7727f7C"
        ]
        balances = get_balance_batch(batch_addresses)
        print_balance_table(batch_addresses, balances)
        
        top_holders = get_top(5)
        print_top_holders(top_holders)
        
        top_holders_with_transfer = get_top_with_transfer(5)
        print_top_holders_with_transfer(top_holders_with_transfer)
        
        token_info = get_token_info()
        print_token_info(token_info)

        wallet_address = "0x51f1774249Fc2B0C2603542Ac6184Ae1d048351d"
        transfers = get_transfer_history(wallet_address, limit=5)
        print_transfer_history(transfers)

    except Exception as e:
        print(f"{Fore.RED}Ошибка: {e}{Style.RESET_ALL}")