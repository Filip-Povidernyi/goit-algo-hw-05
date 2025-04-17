import timeit


def read_file(path: str, encod=None) -> str:

    with open(path, 'r', encoding=encod) as f:
        content = f.read()
        return content


def run_time_test(sort_func, data, substring):
    return timeit.timeit(lambda: sort_func(data, substring), number=1)


def compute_lps(substring):
    lps = [0] * len(substring)
    length = 0
    i = 1

    while i < len(substring):
        if substring[i] == substring[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps


def kmp_search(data, substring):
    M = len(substring)
    N = len(data)

    lps = compute_lps(substring)

    i = j = 0

    while i < N:
        if substring[j] == data[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j

    return -1


def build_shift_table(substring):

    table = {}
    length = len(substring)
    for index, char in enumerate(substring[:-1]):
        table[char] = length - index - 1
    table.setdefault(substring[-1], length)

    return table


def boyer_moore_search(data, substring):

    shift_table = build_shift_table(substring)
    i = 0

    while i <= len(data) - len(substring):
        j = len(substring) - 1
        while j >= 0 and data[i + j] == substring[j]:
            j -= 1

        if j < 0:
            return i

        i += shift_table.get(data[i + len(substring) - 1], len(substring))
    return -1


def polynomial_hash(substring, base=256, modulus=101):

    n = len(substring)
    hash_value = 0

    for i, char in enumerate(substring):
        power_of_base = pow(base, n - i - 1) % modulus
        hash_value = (hash_value + ord(char) * power_of_base) % modulus

    return hash_value


def rabin_karp_search(data, substring):

    substring_length = len(substring)
    main_string_length = len(data)
    base = 256
    modulus = 101
    substring_hash = polynomial_hash(substring, base, modulus)
    current_slice_hash = polynomial_hash(
        data[:substring_length], base, modulus)
    h_multiplier = pow(base, substring_length - 1) % modulus

    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if data[i:i+substring_length] == substring:
                return i

        if i < main_string_length - substring_length:
            current_slice_hash = (current_slice_hash -
                                  ord(data[i]) * h_multiplier) % modulus
            current_slice_hash = (
                current_slice_hash * base + ord(data[i + substring_length])) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus

    return -1


def main():
    text1 = read_file('text.txt')
    text2 = read_file('text2.txt', 'utf-8')
    substrings = ('алгоритм використовує',
                  'adgjearghksrasfhgj', 'кількість предметів')

    results = {
        "Boyer-Moore": [
            run_time_test(boyer_moore_search, text1, substrings[0]),
            run_time_test(boyer_moore_search, text1, substrings[1]),
            run_time_test(boyer_moore_search, text2, substrings[2]),
            run_time_test(boyer_moore_search, text2, substrings[1])
        ],
        "KMP": [
            run_time_test(kmp_search, text1, substrings[0]),
            run_time_test(kmp_search, text1, substrings[1]),
            run_time_test(kmp_search, text2, substrings[2]),
            run_time_test(kmp_search, text2, substrings[1])
        ],
        "Rabin-Karp": [
            run_time_test(rabin_karp_search, text1, substrings[0]),
            run_time_test(rabin_karp_search, text1, substrings[1]),
            run_time_test(rabin_karp_search, text2, substrings[2]),
            run_time_test(rabin_karp_search, text2, substrings[1])
        ]
    }

    print("\n| Алгоритм      |     Article 1     |     Article 2     |")
    print("|               | (real)  |  (fake) | (real)  |  (fake) |")
    print("|---------------|---------|---------|---------|---------|")

    for algo, times in results.items():
        row = f"| {algo:<14}| " + " | ".join(f"{t:.5f}" for t in times) + " |"
        print(row)


if __name__ == '__main__':
    main()
