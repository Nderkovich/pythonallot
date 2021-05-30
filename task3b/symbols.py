from typing import List, Optional


my_symbols = ["a", "b", "c", "d", "c"]


def get_repeating(symbols: List[str]) -> Optional[str]:
    non_repeated = set()
    for symbol in symbols:
        if symbol in non_repeated:
            return symbol
        non_repeated.add(symbol)


print(get_repeating(my_symbols))
