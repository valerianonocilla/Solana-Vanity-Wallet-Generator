import base58
import multiprocessing
from solders.keypair import Keypair
import time
import re
from colorama import init, Fore, Style

# Initialize colorama for colored terminal output
init(autoreset=True)

# Dictionary for expanding prefixes to include common variations (e.g., 'E' -> ['E', 'e', '3'])
letters_dict = {
    "A": ["A", "a"],
    "B": ["B", "b"],
    "C": ["C", "c"],
    "D": ["D", "d"],
    "E": ["E", "e", "3"],
    "F": ["F", "f"],
    "G": ["G", "g"],
    "H": ["H", "h"],
    "I": ["I", "i", "1"],
    "J": ["J", "j"],
    "K": ["K", "k"],
    "L": ["L", "l", "1"],
    "M": ["M", "m"],
    "N": ["N", "n"],
    "O": ["O", "o", "0"],
    "P": ["P", "p"],
    "Q": ["Q", "q"],
    "R": ["R", "r"],
    "S": ["S", "s", "5"],
    "T": ["T", "t", "7"],
    "U": ["U", "u"],
    "V": ["V", "v"],
    "W": ["W", "w"],
    "X": ["X", "x"],
    "Y": ["Y", "y"],
    "Z": ["Z", "z"]
}

def expand_prefijo(prefijo):
    """Generates all possible combinations of a prefix, considering letter variations."""
    if not prefijo:
        return [""]
    
    first_char = prefijo[0].upper()
    rest_of_prefijo = prefijo[1:]
    expanded_chars = letters_dict.get(first_char, [first_char])

    expanded_rest = expand_prefijo(rest_of_prefijo)

    return [char + rest for char in expanded_chars for rest in expanded_rest]


def worker(prefix_queue, results_queue):
    """Worker process to generate Solana keypairs and check for the desired prefix."""
    while True:
        prefix = prefix_queue.get()
        if prefix is None:  # Sentinel value to signal the worker to stop
            break

        while True:
            keypair = Keypair()
            private_key = bytes(keypair)
            private_key_base58 = base58.b58encode(private_key).decode()
            public_key = keypair.pubkey()
            public_key_bytes = bytes(public_key)
            public_key_base58 = base58.b58encode(public_key_bytes).decode()

            if public_key_base58.lower().startswith(prefix.lower()):
                results_queue.put((public_key_base58, private_key_base58))
                break

def save_results(results_queue, filename="wallets.txt"):
    """Saves found wallets (public and private keys) to a file."""
    with open(filename, "a") as f:
        while True:
            result = results_queue.get()
            if result is None:  # Sentinel value to signal the saver to stop
                break
            public_key, private_key = result
            f.write(f"Wallet found: {public_key}\n")
            f.write(f"Private key: {private_key}\n\n")
            print(f"{Fore.GREEN}Wallet found and saved: {public_key}{Style.RESET_ALL}")
            results_queue.task_done()

def buscar_wallets(prefixes, processes):
    """Main function to manage wallet generation and searching using multiprocessing."""
    prefix_queue = multiprocessing.Queue()
    results_queue = multiprocessing.JoinableQueue()

    # Populate the prefix queue with all prefixes
    for prefix in prefixes:
        for expanded_prefix in expand_prefijo(prefix):
            prefix_queue.put(expanded_prefix)

    # Create and start worker processes
    workers = [multiprocessing.Process(target=worker, args=(prefix_queue, results_queue)) for _ in range(processes)]
    for w in workers:
        w.start()

    # Create and start a saver process
    saver = multiprocessing.Process(target=save_results, args=(results_queue,))
    saver.start()

    # Signal workers to stop by adding None values to the queue
    for _ in range(processes):
        prefix_queue.put(None)

    # Wait for all workers to finish
    for w in workers:
        w.join()

    # Signal the saver to stop and wait for it to finish
    results_queue.put(None)
    results_queue.join()
    saver.join()


if __name__ == "__main__":
    print(f"{Fore.CYAN}{Style.BRIGHT}Let's create a personalized Solana wallet!{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Enter the desired prefixes, separated by spaces.{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}The program will search for all possible combinations.{Style.RESET_ALL}\n")

    prefix_str = input(f"{Fore.GREEN}Enter prefixes: {Style.RESET_ALL}").strip()
    prefixes = re.split(r'\s+', prefix_str)  # Split by spaces
    prefixes = [prefix for prefix in prefixes if prefix] # Remove empty prefixes

    if not prefixes:
        print(f"{Fore.RED}No prefixes entered.{Style.RESET_ALL}")
        exit()

    processes = 24 # Number of processes to use

    print(f"{Fore.MAGENTA}Using {processes} processes to search for wallets.{Style.RESET_ALL}")
    start_time = time.time()
    buscar_wallets(prefixes, processes)
    end_time = time.time()

    print(f"\n{Fore.GREEN}Search completed.{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Total execution time: {end_time - start_time:.2f} seconds.{Style.RESET_ALL}")
