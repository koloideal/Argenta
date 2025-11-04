import polib
import deepl
import getopt
import sys
import re

DEEPL_API_TOKEN = 'ADD YOUR API KEY HERE!'

global argv
global opts
global args

argv = sys.argv[1:]
opts, args = getopt.getopt(argv, "f:l:")

def translate(text, lang):
    # Define a dictionary to hold the mappings of tokens to placeholders
    placeholders = {}

    # Use a regular expression to find all the tokens
    tokens = re.findall(r'%\((.*?)\)s', text)

    # Replace each token with a unique placeholder
    for i, token in enumerate(tokens):
        placeholder = f'__PLACEHOLDER_{i}__'
        placeholders[placeholder] = f'%({token})s'
        text = text.replace(f'%({token})s', placeholder)

    # Perform the translation
    translator = deepl.Translator(DEEPL_API_TOKEN)
    translated_text = str(translator.translate_text(text, target_lang=lang))

    # Replace the placeholders back with the original tokens
    for placeholder, token in placeholders.items():
        translated_text = translated_text.replace(placeholder, token)

    return translated_text

def get_filename():
    # read arguments from command line
    for opt, arg in opts:
        if opt in ['-f']:
            filename = arg
    if not filename:
            print('Please enter the filename of the PO file e.g. /directory/django.po:')
            filename = input()
    return filename

def get_target_language():
    # read arguments from command line
    for opt, arg in opts:
        if opt in ['-l']:
            lang = arg
    if not lang:
            print('Please enter two letter ISO language code e.g. DE:')
            lang = input()
    return lang

def process_file(filename, lang):
    po = polib.pofile(filename)
    for entry in po.untranslated_entries():
        if not entry.msgstr:
            print(entry.msgid)
            print('translating...')
            entry.msgstr = translate(entry.msgid, lang)
            print(entry.msgstr)
            print('\n')
        po.save(filename)

if __name__ == '__main__':
    process_file(get_filename(), get_target_language())