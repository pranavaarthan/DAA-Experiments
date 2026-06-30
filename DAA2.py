import random
import string


def naive_search(text, pattern):
    n = len(text)
    m = len(pattern)
    matches = []
    comparisons = 0

    for i in range(n - m + 1):
        j = 0
        while j < m:
            comparisons += 1
            if text[i + j] != pattern[j]:
                break
            j += 1

        if j == m:
            matches.append(i)

    return matches, comparisons


def compute_lps(pattern):
    m = len(pattern)
    lps = [0] * m

    length = 0
    i = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length != 0:
            length = lps[length - 1]
        else:
            lps[i] = 0
            i += 1

    return lps


def kmp_search(text, pattern):
    n = len(text)
    m = len(pattern)

    lps = compute_lps(pattern)

    matches = []
    comparisons = 0

    i = 0
    j = 0

    while i < n:
        comparisons += 1

        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == m:
            matches.append(i - j)
            j = lps[j - 1]

        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return matches, comparisons


def rabin_karp(text, pattern, q=101):
    n = len(text)
    m = len(pattern)

    d = 256
    h = pow(d, m - 1, q)

    p_hash = 0
    t_hash = 0

    matches = []
    comparisons = 0

    for i in range(m):
        p_hash = (d * p_hash + ord(pattern[i])) % q
        t_hash = (d * t_hash + ord(text[i])) % q

    for s in range(n - m + 1):

        if p_hash == t_hash:
            match = True

            for k in range(m):
                comparisons += 1
                if text[s + k] != pattern[k]:
                    match = False
                    break

            if match:
                matches.append(s)

        if s < n - m:
            t_hash = (d * (t_hash - ord(text[s]) * h) + ord(text[s + m])) % q

            if t_hash < 0:
                t_hash += q

    return matches, comparisons


text = "AABAACAADAABAABA"
pattern = "AABA"

naive_matches, naive_comp = naive_search(text, pattern)
kmp_matches, kmp_comp = kmp_search(text, pattern)
rk_matches, rk_comp = rabin_karp(text, pattern)

print("Sample Test")
print("-------------------------")
print("Text    :", text)
print("Pattern :", pattern)

print("\nNaive -> Matches at:", naive_matches, ", Comparisons:", naive_comp)
print("KMP    -> Matches at:", kmp_matches, ", Comparisons:", kmp_comp)
print("RK     -> Matches at:", rk_matches, ", Comparisons:", rk_comp)

print("\nPerformance Comparison")
print("-" * 60)

random.seed(42)
text = ''.join(random.choices(string.ascii_uppercase, k=10000))

pattern_lengths = [5, 10, 20, 50]

print("{:<10}{:<15}{:<15}{:<15}".format("Length", "Naive", "KMP", "RK"))

for length in pattern_lengths:

    start = random.randint(0, 10000 - length)
    pattern = text[start:start + length]

    _, naive_comp = naive_search(text, pattern)
    _, kmp_comp = kmp_search(text, pattern)
    _, rk_comp = rabin_karp(text, pattern)

    print("{:<10}{:<15}{:<15}{:<15}".format(
        length,
        naive_comp,
        kmp_comp,
        rk_comp
    ))