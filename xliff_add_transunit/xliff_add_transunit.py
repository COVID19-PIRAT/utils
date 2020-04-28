#!/usr/bin/env python3

import argparse
import os
import cgi


def do_work(path, id, source_text, default_lang):
    source_text = cgi.escape(source_text)

    # Content for messages.xlf
    base_unit = """  <trans-unit id="{id}" datatype="html">
        <source>{source_text}</source>
      </trans-unit>""".format(id=id, source_text=source_text)

    # Content for messages.{default_lang}.xlf
    source_lang_unit = """  <trans-unit id="{id}" datatype="html">
        <source>{source_text}</source>
        <target state="translated">{source_text}</target>
      </trans-unit>""".format(id=id, source_text=source_text)

    # Content for messages.*.xlf
    translation_unit = """  <trans-unit id="{id}" datatype="html">
        <source>{source_text}</source>
        <target state="new"></target>
      </trans-unit>""".format(id=id, source_text=source_text)

    for filename in os.listdir(path):
        if not filename.startswith('messages.') or not filename.endswith('.xlf'):
            continue
        if filename == 'messages.xlf':
            new_unit = base_unit
        elif filename == 'messages.' + default_lang + '.xlf':
            new_unit = source_lang_unit
        else:
            new_unit = translation_unit
        with open(os.path.join(path, filename), 'r+') as f:
            new_file_content = f.read().replace('</body>', new_unit + '\n    </body>')
            f.seek(0)
            f.write(new_file_content)
            f.truncate()


def main():
    parser = argparse.ArgumentParser(description='This tool add a transunit block to a set of xliff message files.')
    parser.add_argument('path', help='the path to the directory with the messages files')
    parser.add_argument('--id', help='the id of the transunit', required=True)
    parser.add_argument('--source-text', help='the text in the source language', required=True)
    parser.add_argument('--default-lang', help='the language that is used as the source language for translations',
        default='en')

    args = parser.parse_args()
    do_work(args.path, args.id, args.source_text, args.default_lang)

main()
