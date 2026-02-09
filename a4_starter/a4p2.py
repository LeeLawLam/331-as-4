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
#---------------------------------------------------------------

"""
Nomenclator cipher
February 2025
Author: <<Insert your name here>>
"""

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def translateMessage(key: str, message: str, codebook: dict, mode: str):
    """
    Encrypt or decrypt using a nomenclator.
    Takes a substitution cipher key, a message (plaintext or ciphertext),
    a codebook dictionary, and a mode string ('encrypt' or 'decrypt')
    specifying the action to be taken. Returns a string containing the
    ciphertext (if encrypting) or plaintext (if decrypting).
    """
    raise NotImplementedError()


def encryptMessage(key: str, message: str, codebook: dict):
    return translateMessage(key, message, codebook, 'encrypt')


def decryptMessage(key: str, message: str, codebook: dict):
    return translateMessage(key, message, codebook, 'decrypt')


def test():
    # Provided tests.
    key = 'LFWOAYUISVKMNXPBDCRJTQEGHZ'
    plaintext = "X-ray machines cannot be brought here, as -ray* are very dangerous. Hello;ray! ray;"
    codebook = {'ray':['1']}
    ciphertext = encryptMessage(key, plaintext, codebook)
    assert ciphertext=="G-clh nlwisxar wlxxpj fa fcptuij iaca, lr -1* lca qach olxuacptr. Iammp;clh! 1;"
    # End of provided tests.

if __name__ == '__main__':
    test()
