#!/usr/bin/env python

import re
import json

import argparse
import locale

import urllib2 as request
from urllib import quote

string_pattern = r"\"(([^\"\\]|\\.)*)\""
match_string =re.compile(
                        r"\,?\["
                        + string_pattern + r"\,"
                        + string_pattern + r"\,"
                             + string_pattern + r"\,"
                             + string_pattern
                             +r"\]")

def _get_json5_from_google(from_lang, to_lang, source):
    escaped_source = quote(source, '')
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.168 Safari/535.19'}
    req = request.Request(
                          url="http://translate.google.com/translate_a/t?client=t&ie=UTF-8&oe=UTF-8"
                          +"&sl=%s&tl=%s&text=%s" % (from_lang, to_lang, escaped_source)
                          , headers = headers)
    r = request.urlopen(req)
    return r.read().decode('utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('texts', metavar='text', nargs='+',
                        help='a string to translate(use "" when it\'s a sentence)')
    parser.add_argument('-t', '--to', dest='to_lang', type=str, default='zh',
                        help='To language (e.g. zh, zh-TW, en, ja, ko). Default is zh.')
    parser.add_argument('-f', '--from', dest='from_lang', type=str, default='auto',
                        help='From language (e.g. zh, zh-TW, en, ja, ko). Default is auto.')
    args = parser.parse_args()
    
    text = str(args.texts[0])
    from_lang = args.from_lang
    to_lang = args.to_lang
    
    json_format = _get_json5_from_google(from_lang, to_lang, text)    
    fi_result = match_string.match(json_format, 2).group(1)

    res = fi_result.encode(locale.getpreferredencoding())
    translation = json.loads('"%s"' % res)
    
    print translation
    
if __name__ == "__main__":
    main()
