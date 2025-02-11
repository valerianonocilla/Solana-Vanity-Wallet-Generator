# Solana Vanity Wallet Generator

This script generates Solana wallets with a specified prefix, using multiprocessing to accelerate the search.

## Requirements

*   Python 3.6+
*   Libraries: `base58`, `solders`, `colorama`

    Install: `pip install base58 solders colorama`

## Installation

1.  Clone: `git clone [YOUR_REPOSITORY_URL]` and `cd [REPOSITORY_DIRECTORY]`
2.  Create virtual environment (recommended): `python -m venv venv`
3.  Activate virtual environment:
    *   **Windows:** `venv\Scripts\activate`
    *   **macOS/Linux:** `source venv/bin/activate`

## Usage

1.  Run: `python WalletFinder.py`
2.  Enter desired prefixes (space-separated) when prompted.
3.  Found wallets (public and private keys) are saved to `wallets.txt`.
4.  **Important:** Once you find a wallet you like, press `Ctrl+C` to stop the process. This will ensure the found wallet is saved to `wallets.txt`.

## Configuration

*   **Number of Processes:**  Set the `processes` variable (default: 24) in `WalletFinder.py` to match your CPU core count. Find your core count:
    *   **Windows:** Task Manager (Performance tab)
    *   **macOS:** `sysctl -n hw.ncpu` (Terminal)
    *   **Linux:** `nproc` (Terminal)
    Experiment for optimal performance; avoid exceeding your core count to prevent slowdowns.
*   **Prefixes:** Input prefixes when running the script.
*   **Output File:**  `wallets.txt` (configurable in `save_results` function).

## Security Notes

*   **Secure your private keys!** The `wallets.txt` file is sensitive.
*   Keys are generated locally. Keep the script and your system secure.
*   Use at your own risk.
*   Consider generating keys offline for maximum security.

## How It Works

The script:

1.  Takes prefixes as input.
2.  Expands prefixes using `letters_dict` for variations (e.g., "E" -> "E", "e", "3").
3.  Generates random Solana keypairs.
4.  Checks if the public key starts with the specified prefix.
5.  Saves matching wallets to `wallets.txt`.
6.  Uses multiprocessing for faster searching.
7.  Supports leet speak (I=1, E=3, S=5, O=0, T=7, L=1).

## Contributing

Submit pull requests for improvements.

## License

[MIT License](LICENSE)
