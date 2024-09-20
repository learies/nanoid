from math import ceil, log
from secrets import token_bytes
from typing import Callable

ALPHABET = "_-0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
DEFAULT_SIZE = 21


def calculate_mask(alphabet_length: int) -> int:
    """Calculate the bit mask to limit random byte values to alphabet size."""
    if alphabet_length > 1:
        return (2 << int(log(alphabet_length - 1) / log(2))) - 1
    return 1


def calculate_step(mask: int, size: int, alphabet_length: int) -> int:
    """Calculate random bytes we need to generate on each iteration."""
    return int(ceil(1.6 * mask * size / alphabet_length))


def generate_random_bytes(
    algorithm: Callable[[int], bytes], step: int
) -> bytes:
    """Generate random bytes using the provided algorithm."""
    return algorithm(step)


def generate_unique_id(
    algorithm: Callable[[int], bytes], alphabet: str, size: int
) -> str:
    """Generate a unique ID of a given size."""
    alphabet_length: int = len(alphabet)
    mask: int = calculate_mask(alphabet_length)
    step: int = calculate_step(mask, size, alphabet_length)

    unique_id: list = []
    while len(unique_id) < size:
        random_bytes: bytes = generate_random_bytes(algorithm, step)

        for random_byte in random_bytes:
            index: int = random_byte & mask
            if index >= alphabet_length:
                continue

            unique_id.append(alphabet[index])
            if len(unique_id) == size:
                break

    return "".join(unique_id)


def algorithm_generate(random_bytes: int) -> bytes:
    """Generate random bytes using urandom."""
    return bytes(token_bytes(random_bytes))


def generate(alphabet: str = ALPHABET, size: int = DEFAULT_SIZE) -> str:
    """Generate a unique ID using the given alphabet and size."""
    if not alphabet:
        raise ValueError("Alphabet must be non-empty.")

    if size <= 0:
        raise ValueError("Size must be greater than 0.")

    return generate_unique_id(algorithm_generate, alphabet, size)


if __name__ == "__main__":
    print(generate())
