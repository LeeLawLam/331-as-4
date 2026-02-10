#!/usr/bin/env python3

#---------------------------------------------------------------
#
# CMPUT 331 Student Submission License
# Version 1.0
# Copyright 2025 <<Insert your name here>>
#
# Redistribution is forbidden in all circumstances. Use of this software
# without explicit authorization from the author is prohibited.
#
# This software was produced as a solution for an assignment in the course
# CMPUT 331 - Computational Cryptography at the University of
# Alberta, Canada. This solution is confidential and remains confidential 
# after it is submitted for grading.
#
# Copying any part of this solution without including this copyright notice
# is illegal.
#
# If any portion of this software is included in a solution submitted for
# grading at an educational institution, the submitter will be subject to
# the sanctions for plagiarism at that institution.
#
# If this software is found in any public website or public repository, the
# person finding it is kindly requested to immediately report, including 
# the URL or other repository locating information, to the following email
# address:
#
#          gkondrak <at> ualberta.ca
#
#----------------------------------------------------------------

#-------------------- START ASSIGNMENT HERE ---------------------
"""
General decryption program
February 2025
Author: <<Insert your name here>>
"""

from detectEnglish import isEnglish
from itertools import permutations

import detectEnglish

def hack(ciphertype: str, ciphertext: str):
    """
    Decrypt a given ciphertext with either of these algorithm: caesar, transposition, or affine.
        Input: a line from `ciphers.txt`.
        Output: the decrypted message (or plaintext).
    """
    t = ciphertype.strip().lower()
    ct = ciphertext.rstrip("\n")

    # Caesar
    if t in ("c", "caesar"):
        LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        last_candidate = ct

        for key in range(26):
            pt_chars = []
            for ch in ct:
                if ch.upper() in LETTERS:
                    idx = LETTERS.find(ch.upper())
                    pidx = (idx - key) % 26
                    out = LETTERS[pidx]
                    pt_chars.append(out if ch.isupper() else out.lower())
                else:
                    pt_chars.append(ch)

            candidate = "".join(pt_chars)
            last_candidate = candidate

            if detectEnglish.isEnglish(candidate, wordPercentage=30, letterPercentage=70):
                return candidate

        return last_candidate

    # Transposition
    if t in ("t", "transposition", "columnar"):
        L = len(ct)
        best_candidate = ct
        best_score = -1.0

        for n in range(2, 10):
            if n > L:
                break

            for perm in permutations(range(n)):
                num_rows = (L + n - 1) // n
                shaded = (n * num_rows) - L

                col_lens = [num_rows] * n
                for col in range(n - shaded, n):
                    if 0 <= col < n:
                        col_lens[col] = num_rows - 1

                cols = [""] * n
                pos = 0
                for col_index in perm:
                    clen = col_lens[col_index]
                    cols[col_index] = ct[pos:pos + clen]
                    pos += clen

                pt_chars = []
                for r in range(num_rows):
                    for c in range(n):
                        if r < len(cols[c]):
                            pt_chars.append(cols[c][r])

                candidate = "".join(pt_chars)

                score = detectEnglish.getEnglishCount(candidate)
                if score > best_score:
                    best_score = score
                    best_candidate = candidate

        return best_candidate

    # Affine
    if t in ("a", "affine"):
        # Try A–Z first (spaces/punct unchanged) then try the larger set
        symbol_sets = [
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 !?.'\",;:-)"
        ]

        best_overall = ct
        best_overall_score = -1.0

        for SYMBOLS in symbol_sets:
            m = len(SYMBOLS)
            best_candidate = ct
            best_score = -1.0

            for a in range(m):
                # gcd(a, m)
                x, y = a, m
                while x != 0:
                    x, y = y % x, x
                if y != 1:
                    continue

                # mod inverse of a mod m
                u1, u2, u3 = 1, 0, a
                v1, v2, v3 = 0, 1, m
                while v3 != 0:
                    q = u3 // v3
                    v1, v2, v3, u1, u2, u3 = (
                        u1 - q * v1,
                        u2 - q * v2,
                        u3 - q * v3,
                        v1,
                        v2,
                        v3,
                    )
                inva = u1 % m

                for b in range(m):
                    pt_chars = []
                    for ch in ct:
                        idx = SYMBOLS.find(ch)
                        if idx == -1:
                            pt_chars.append(ch)
                        else:
                            pidx = (inva * (idx - b)) % m
                            pt_chars.append(SYMBOLS[pidx])

                    candidate = "".join(pt_chars)

                    if detectEnglish.isEnglish(candidate, wordPercentage=30, letterPercentage=70):
                        return candidate

                    score = detectEnglish.getEnglishCount(candidate)
                    if score > best_score:
                        best_score = score
                        best_candidate = candidate

            if best_score > best_overall_score:
                best_overall_score = best_score
                best_overall = best_candidate

        return best_overall

    return ct

def processing():
    # Add the processing steps here like reading form ciphers.txt, calling the hack function, writing to decrypted.txt, etc.
    plaintexts = []
    with open("ciphers.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            if ";" not in line:
                raise ValueError(f"Bad line (missing ';'): {line!r}")

            ctype, ct = line.split(";", 1)
            ct = ct.lstrip()
            plaintexts.append(hack(ctype, ct))

    with open("decrypted.txt", "w", encoding="utf-8") as out:
        for p in plaintexts:
            out.write(p + "\n")


    with open("decrypted.txt", "w", encoding="utf-8") as out:
        for p in plaintexts:
            out.write(p + "\n")

def test():
    # Test cases for the hack function. You can add more tests as needed.
    assert hack("caesar", "GHGIQ") == "ABACK", "Caesar hack failed"
    assert hack("transposition", "IS HAUCREERNP F") == "CIPHERS ARE FUN", "Transposition hack failed"
    assert hack("affine", "IHHWVC SWFRCP") == "AFFINE CIPHER", "Affine hack failed"

if __name__ == '__main__':
    test()
    processing()
