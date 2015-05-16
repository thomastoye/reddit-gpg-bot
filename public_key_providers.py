#/usr/bin/env python3

import re
import requests

""" Extracts a public key that is embedded in plain text """
def public_key_embedded_in_text(text):
    pattern = '-----BEGIN PGP PUBLIC KEY BLOCK-----.*-----END PGP PUBLIC KEY BLOCK-----'
    flags = re.DOTALL | re.MULTILINE
    match = re.search(pattern, text, flags)
    
    if match:
        newlines_removed = '\n'.join([line for line in match.group(0).split('\n') if line.strip()])
        return newlines_removed
    else:
        return None

""" Extracts a private key that is embedded in plain text """
def private_key_embedded_in_text(text):
    pattern = '-----BEGIN PGP PRIVATE KEY BLOCK-----.*-----END PGP PRIVATE KEY BLOCK-----'
    flags = re.DOTALL | re.MULTILINE
    match = re.search(pattern, text, flags)
    
    if match:
        return match.group(0)
    else:
        return None

""" Looks for a pastebin link in the text, tries to retrieve a public key from there """
def link_to_pastebin(text):
    pattern = '(pastebin\.com/(.{8})(?=\s))|(pastebin\.com/(.{8}))'
    match = re.search(pattern, text)

    if match:
        id = match.group(0)[-8:]
        link_to_raw = 'http://pastebin.com/raw.php?i=%s' % id
        req = requests.get(link_to_raw)
        if req.status_code is 404:
            print('404 response for %s' % link_to_raw)
            return None
        else:
            return public_key_embedded_in_text(req.text)
    else:
        return None

def link_to_mit_keyserver(text):
    pattern = 'mit.edu'
    match = re.search(pattern, text)

    if match:
        return match.group(0)
        # Note: should make request to MIT keyserver here
    else:
        return None

""" Register any providers you create here """
all_providers = [
    public_key_embedded_in_text,
    link_to_pastebin,
    #link_to_mit_keyserver
]

""" These are for detecing if someone is doing something wrong. """
warning_providers = [private_key_embedded_in_text]

