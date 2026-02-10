#!/usr/bin/env python3

#---------------------------------------------------------------
#
# CMPUT 331 Student Submission License
# Version 1.0
# Copyright 2025 Louis Lam
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
#---------------------------------------------------------------

"""
Enhanced substitution cipher solver
February 2025
Author: Louis Lam
"""

import re
import simpleSubHacker as ssh

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def hackSimpleSub(message: str):
    """
    Simple substitution cipher hacker.
    First runs the textbook program to get an initial, potentially incomplete decipherment.
    Then uses regular expressions and a dictionary to decipher additional letters.
    """
    # Get initial mapping from textbook hacker
    letterMapping = ssh.hackSimpleSub(message)

    # Initial partial decrypt (unknown show up as '_')
    plaintext = ssh.decryptWithCipherletterMapping(message, letterMapping)

    # Load dictionary (uppercase)
    with open("dictionary.txt", "r", encoding="utf-8") as f:
        dict_words = [w.strip().upper() for w in f.read().splitlines() if w.strip()]

    # Stop when no changes are made in a full pass
    changed = True
    while changed:
        changed = False

        # Recompute plaintext each round from current mapping
        plaintext = ssh.decryptWithCipherletterMapping(message, letterMapping)

        cipher_words = re.findall(r"[A-Z]+", message.upper())
        plain_words  = re.findall(r"[A-Z_]+", plaintext.upper())

        # If alignment ever breaks return best
        if len(cipher_words) != len(plain_words):
            return plaintext

        # Build solved maps (cipher->plain and plain->cipher) from current map
        solved_c2p = {}
        solved_p2c = {}
        for c in LETTERS:
            if len(letterMapping[c]) == 1:
                p = letterMapping[c][0]
                solved_c2p[c] = p
                solved_p2c[p] = c

        # For each word with blanks find dictionary candidates that fit
        for cw, pw in zip(cipher_words, plain_words):
            if "_" not in pw:
                continue  # already fully solved word
            if len(cw) != len(pw):
                continue

            # Regex pattern from partially-decrypted word
            pat = "^" + pw.replace("_", ".") + "$"

            # Pre-filter by length first (fast)
            candidates = [w for w in dict_words if len(w) == len(pw)]
            candidates = [w for w in candidates if re.match(pat, w) is not None]

            if not candidates:
                continue

            # Filter candidates by respecting current one-to-one solved constraints
            filtered = []
            for cand in candidates:
                ok = True
                for i in range(len(cw)):
                    c = cw[i]
                    p = cand[i]

                    # if cipher letter already solved, it must match
                    if c in solved_c2p and solved_c2p[c] != p:
                        ok = False
                        break

                    # if plaintext letter already assigned to a different cipher, reject
                    if p in solved_p2c and solved_p2c[p] != c:
                        ok = False
                        break

                if ok:
                    filtered.append(cand)

            if not filtered:
                continue

            # If exactly one candidate, we can force all letters for this word
            if len(filtered) == 1:
                cand = filtered[0]
                for i in range(len(cw)):
                    c = cw[i]
                    p = cand[i]
                    if len(letterMapping[c]) != 1:
                        # lock it
                        letterMapping[c] = [p]
                        changed = True
                # propagate solved letters (removes solved letters from other lists)
                letterMapping = ssh.removeSolvedLettersFromMapping(letterMapping)

                # refresh solved maps for later checks this round
                solved_c2p = {}
                solved_p2c = {}
                for c2 in LETTERS:
                    if len(letterMapping[c2]) == 1:
                        p2 = letterMapping[c2][0]
                        solved_c2p[c2] = p2
                        solved_p2c[p2] = c2

            else:
                # Multiple candidates: intersect possibilities position-wise.
                # If for some cipherletter, all candidates agree on the plaintext letter, lock it.
                for i in range(len(cw)):
                    c = cw[i]
                    if len(letterMapping[c]) == 1:
                        continue
                    letters_here = set(cand[i] for cand in filtered)
                    if len(letters_here) == 1:
                        p = next(iter(letters_here))
                        letterMapping[c] = [p]
                        changed = True
                if changed:
                    letterMapping = ssh.removeSolvedLettersFromMapping(letterMapping)

        # End for each word

        # If solved fully, stop early
        plaintext = ssh.decryptWithCipherletterMapping(message, letterMapping)
        if "_" not in plaintext:
            return plaintext

    # Return best
    return plaintext


def test():
    # Provided test.
    message = 'Sy l nlx sr pyyacao l ylwj eiswi upar lulsxrj isr sxrjsxwjr, ia esmm rwctjsxsza sj wmpramh, lxo txmarr jia aqsoaxwa sr pqaceiamnsxu, ia esmm caytra jp famsaqa sj. Sy, px jia pjiac ilxo, ia sr pyyacao rpnajisxu eiswi lyypcor l calrpx ypc lwjsxu sx lwwpcolxwa jp isr sxrjsxwjr, ia esmm lwwabj sj aqax px jia rmsuijarj aqsoaxwa. Jia pcsusx py nhjir sr agbmlsxao sx jisr elh. -Facjclxo Ctrramm'
    assert(hackSimpleSub(message)=="If a man is offered a fact which goes against his instincts, he will scrutinize it closely, and unless the evidence is overwhelming, he will refuse to believe it. If, on the other hand, he is offered something which affords a reason for acting in accordance to his instincts, he will accept it even on the slightest evidence. The origin of myths is explained in this way. -Bertrand Russell")
    # End of provided test.
    

if __name__ == '__main__':
    test()
