'''
Function:
    Generate ops_schema.py according to Genie Models in wiki.

Usage:
    1. Save each wiki page as html file to a folder manually.
    Make sure the name of html file is the same as ops name.
    For example:
    - htmls
        - Acl.htm
        - Arp.htm
        - Bgp.htm
        - ...

    2. Run script in command line
    python ops_schema_generator.py --html_path PATH_TO_HTML_FOLDER
    For example:
    python ops_schema_generator.py --html_path htmls
'''
import re
import os
import argparse
from bs4 import BeautifulSoup

IGNORE = ('AAA.htm', 'Template.htm')
DESTFILE = "ops_schema.py"  # path to the generated py file

def main():

    # parse argument
    parser = argparse.ArgumentParser()
    parser.add_argument('--html_path', required = True, help = "path to the folder of html files")

    args = parser.parse_args()
    HTMLPATH = args.html_path

    # compile patterns
    pattern_tab = re.compile(r'\t')
    pattern_comment = re.compile(r' *\#[\S ]+')
    pattern_corner1 = re.compile(r'\[[\S ]+\]: {')
    patter_key = re.compile(r'((?!\')\S)((?!\')[\S ])+: *{')
    pattern_corner2 = re.compile(r'\= *\n *{')
    pattern_corner3 = re.compile(r'(\} *(?!\,))')
    pattern_newline = re.compile(r'\n')
    pattern_self = re.compile(r' *self\.')
    pattern_colon = re.compile(r' *=')
    pattern_any = re.compile(r'(\: *(?!\{)\S+\,{0,1})')

    text = ["from genie.metaparser.util.schemaengine import Any\n\n",
            "class Ops_structure:\n\n    ops_schema = {\n    "]

    for filename in os.listdir(HTMLPATH):
        if filename in IGNORE:
            continue
        fread = os.path.join(HTMLPATH, filename)
        soup = BeautifulSoup(open(fread), "lxml")

        filename = filename.split('.')[0].lower()

        text.append("    \'")
        text.append(filename)
        text.append("\': {\n")

        for item in soup.select('.syntaxhighlighter-pre'):
            if item.get_text().lstrip().startswith('self'):
                ret = item.get_text()

                # replace tab with space. To solve inconsistent indent
                ret = pattern_tab.sub("    ", ret)

                # remove comments
                ret = pattern_comment.sub("", ret)

                # corner case 1: key is list with space
                ret = pattern_corner1.sub("Any(): {", ret)

                # replace those keys without quatation mark with Any()
                # corner case: nbr_af_name+" RD "+route_distinguisher: {
                ret = patter_key.sub("Any(): {", ret)

                # eg: 'self.* = \n {'
                ret = pattern_corner2.sub("= {", ret)

                # corner case: no ',' after '}'
                ret = pattern_corner3.sub("},", ret)

                # To solve indent, add space before each line
                ret = pattern_newline.sub("\n            ", ret)

                # eg: self.info = {
                # eg: self.chassis = chassis,
                ret = pattern_self.sub("            \'", ret)

                # = to colon
                ret = pattern_colon.sub("\':", ret)

                # replace type with Any()... some don't end with ,
                ret = pattern_any.sub(": Any(),", ret)

                text.append(ret)
                text.append("\n")

        text.append("        },\n\n    ")

    text[-1] = text[-1].rstrip()
    text.append("\n    }")
    
    result = ''.join(text)

    # write to .py file
    with open(DESTFILE, 'w') as f:
        f.write(result)


if __name__ == '__main__':
    main()