""" This generates a series of Markdown files (for use with Pelican) from a single specialized
BibTeX file with custom fields. """

import re
from pyparsing import nestedExpr

BIBTEX_FILE_PATH = "cv/publications.bib"
MARKDOWN_DIR_PATH = "pelican/content/publications"
KNOWN_RECORD_TYPES = {'inproceedings', 'article', 'report', 'incollection'}
IGNORE_KEYWORDS = {"impact", "brown"}
print("CHECK FOR EMPTY KEYWORDS")
print("CHECK FOR EMPTY DOI OR URL")
print("ADD MORE IGNORED KEYWORDS")
print("ADD AUTHORS TO TAGS AS WELL AS KEYWORDS")

def tokens_to_dict(token_list):
    """ Create a dictionary of fields """
    entries = {}
    field_name = None
    field_values = []
    for token in token_list:
        try:
            token = token.strip()
            if token[-1] == "=":
                if field_name:
                    entries[field_name] = field_values
                    field_values = []
                field_name = token[:-1]
            else:
                field_values.append(token)
        except TypeError:
            field_values.append(token)
    return entries

def flatten_list(input_list):
    output_list = [item for sublist in input_list for item in sublist]
    while True:
        try:
            output_list.remove(",")
        except ValueError:
            break
    return output_list

class Record:
    """ BibTeX record """
    def __init__(self, label, token_list):
        """ Initialize with the record label """
        self.label = label
        field_dict = tokens_to_dict(token_list)
        self.parse_field_dict(field_dict)
    def parse_field_dict(self, field_dict):
        """ Parse a dictionary of fields associated with an entry """
        for name, value in field_dict.items():
            value = flatten_list(value)
            if name == "year":
                year_string = " ".join(value)
                self.year = year_string
            elif name == "keywords":
                for keyword in IGNORE_KEYWORDS:
                    try:
                        value.remove(keyword)
                    except ValueError:
                        pass
                self.keywords = value
            elif name == "pmid":
                self.pmid = " ".join(value)
            elif name == "journal":
                self.journal = " ".join(value)
            elif name == "title":
                self.title = "".join(value)
                self.title = self.title.replace("{", "").replace("}", "").replace("\"", "")
            elif name == "url":
                self.url = " ".join(value)
            elif name == "author":
                print("***", value)
            elif name == "doi":
                self.doi = " ".join(value)
            elif name == "volume":
                self.volume = " ".join(value)
            elif name == "number":
                pass
            elif name == "publisher":
                pass
            elif name == "pages":
                self.pages = "".join(value).replace("--", "-")
            elif name == "booktitle":
                self.booktitle = " ".join(value)
            elif name == "type":
                self.type = " ".join(value)
                print(self.type)
            elif name == "pdf":
                self.pdf = "".join(value)
            else:
                errstr = "Unknown article field: %s" % name
                raise ValueError(errstr)
        print(self.__dict__)

class Article(Record):
    """ BibTeX article """
    def __str__(self):
        return "%s" % self.__dict__

class InCollection(Record):
    """ BibTeX collection """
    def __str__(self):
        return "%s" % self.__dict__

class Report(Record):
    """ BibTeX report """
    def __str__(self):
        return "%s" % self.__dict__

class InProceedings(Record):
    """ BibTeX proceedings """
    def __str__(self):
        return "%s" % self.__dict__

def test_record_types(record_types):
    """ Takes record type set as input and raises error if it is invalid """
    unknown_records = record_types - KNOWN_RECORD_TYPES
    if len(unknown_records) > 0:
        errstr = "Unknown record types: %s" % unknown_records
        raise ValueError(errstr)

def parse_record(record_string):
    """ Parse a single record """
    type_search_string = "@.*{"
    type_re = re.compile(type_search_string)
    type_match = type_re.match(record_string)
    record_type = record_string[type_match.start()+1:type_match.end()-1]
    record_string = record_string[type_match.end()-1:]
    test_record_types({record_type})
    nested_ex = nestedExpr("{", "}")
    token_list = nested_ex.parseString(record_string)[0]
    label = token_list.pop(0)
    print("Parsing %s..." % label)
    if record_type == "article":
        return Article(label, token_list)
    elif record_type == "report":
        return Report(label, token_list)
    elif record_type == "incollection":
        return InCollection(label, token_list)
    elif record_type == "inproceedings":
        return InProceedings(label, token_list)
    else:
        errstr = "Unknown record type:  %s" % record_type
        raise ValueError(errstr)

def parse_bibtex(bibfile):
    """ Parse a BibTeX file into a list of dictionaries """
    records = {}
    bibdata = bibfile.read()
    type_search_string = "@.*{"
    type_re = re.compile(type_search_string)
    record_spans = [match.span() for match in type_re.finditer(bibdata)]
    record_strings = []
    for irecord, span in enumerate(record_spans[:-1]):
        start = span[0]
        end = record_spans[irecord+1][0]
        record_strings.append(bibdata[start:end])
    record_strings.append(bibdata[record_spans[-1][0]:])
    for record_string in record_strings:
        parse_record(record_string)
    return records

def main():
    """ Main routine """
    with open(BIBTEX_FILE_PATH, "rt") as bibfile:
        records = parse_bibtex(bibfile)

if __name__ == "__main__":
    main()
