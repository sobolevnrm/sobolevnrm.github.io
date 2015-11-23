""" This generates a series of Markdown files (for use with Pelican) from a single specialized
BibTeX file with custom fields. """

# TODO - increase robustness of this script; e.g., to spaces around equals signs

import re
from io import StringIO
from pyparsing import nestedExpr
import logging

BIBTEX_FILE_PATH = "cv/publications.bib"
MARKDOWN_DIR_PATH = "pelican/content/publications"
KNOWN_RECORD_TYPES = {'inproceedings', 'article', 'report', 'incollection'}
IGNORE_KEYWORDS = {"impact", "fullonly", "fullmath", "longmath"}

_LOGGER = logging.getLogger("b2m")
logging.basicConfig(level=logging.INFO)

def tokens_to_dict(token_list):
    """ Create a dictionary of fields """
    entries = {}
    field_name = None
    field_values = []
    for token in token_list:
        _LOGGER.debug("Parsing token: %s", token)
        try:
            token = token.strip()
            # TODO - the next line appears to be the source of the equals signs parsing problems
            if token[-1] == "=":
                if field_name:
                    entries[field_name] = field_values
                    field_values = []
                field_name = token[:-1]
            else:
                field_values.append(token)
        except TypeError:
            field_values.append(token)
    entries[field_name] = field_values
    return entries

def flatten_list(input_list):
    output_list = [item for sublist in input_list for item in sublist]
    while True:
        try:
            output_list.remove(",")
        except ValueError:
            break
    clean_list = []
    for item in output_list:
        if type(item) == type("foo"):
            clean_list.append(item)
        else:
            clean_list = clean_list + item.asList()
    return clean_list

class Record:
    """ BibTeX record """
    def __init__(self, label, token_list):
        """ Initialize with the record label """
        self.label = label
        field_dict = tokens_to_dict(token_list)
        self.parse_field_dict(field_dict)
    def get_links(self):
        """ Return links as string """
        link_strings = []
        for attr in ["url", "pmid", "doi"]:
            try:
                value = getattr(self, attr)
                link_strings.append("* %s: [%s](%s)" % (attr, value, value))
            except AttributeError:
                pass
        try:
            link_strings.append("* [pdf](http://sobolevnrm.github.io/papers/%s)" % self.pdf)
        except AttributeError:
            pass
        return "\n".join(link_strings)
    def get_string_attr(self, attrname):
        lines = getattr(self, attrname).splitlines()
        return " ".join(lines)
    def get_short_citation(self):
        """ Return a short citation string """
        _LOGGER.info(self.__dict__)
        raise NotImplementedError()
    def get_date(self, default_month="01", default_day="01"):
        """ Return date as string, filling in with default values as needed """
        date_values = [self.year]
        try:
            date_values.append(self.month)
        except AttributeError:
            _LOGGER.error("%s is missing month" % self.label)
            date_values.append(default_month)
        try:
            date_values.append(self.day)
        except AttributeError:
            _LOGGER.error("%s is missing day" % self.label)
            date_values.append(default_day)
        return "-".join(date_values)
    def get_keywords(self, ignore_keywords=IGNORE_KEYWORDS):
        """ Return tags as a string, ignoring the specified tags """
        if len(self.keywords) == 0:
            raise IndexError("No keywords!")
        return ", ".join(self.keywords)
    def get_author_lastnames(self):
        """ Return authors' last names as string """
        authors = []
        for author in self.authors:
            authors.append(author[0])
        return ", ".join(authors)
    def get_short_authors(self):
        """ Return authors in short form as string """
        authors = []
        for author in self.authors:
            author_string = author[0] + " "
            for name in author[1:]:
                author_string = author_string + name[0]
            authors.append(author_string)
        return ", ".join(authors)
    def markdown(self):
        """ Return a Markdown document as a string """
        with StringIO() as f:
            f.write("Title: %s\n" % self.get_string_attr("title"))
            f.write("Date: %s\n" % self.get_date())
            f.write("Category: Publications\n")
            f.write("Slug: %s\n" % self.label)
            f.write("Tags: %s\n" % self.get_keywords())
            f.write("Authors: %s\n" % self.get_author_lastnames())
            f.write("Summary: %s\n" % self.get_short_citation())
            f.write("\n%s\n" % self.get_short_citation())
            f.write("\n%s\n" % self.get_links())
            try:
                f.write("\n%s\n" % self.get_string_attr("abstract"))
            except AttributeError:
                _LOGGER.error("%s is missing abstract" % self.label)
            return f.getvalue()
    def parse_field_dict(self, field_dict):
        """ Parse a dictionary of fields associated with an entry """
        for name, value in field_dict.items():
            value = flatten_list(value)
            name = name.lower().strip(",")
            if name == "year":
                year_string = " ".join(value)
                self.year = year_string
            elif name == "day":
                day_string = " ".join(value)
                self.day = day_string
            elif name == "month":
                month_string = " ".join(value)
                self.month = month_string
            elif name == "keywords":
                keywords = set([kw.strip(",") for kw in value])
                self.keywords = keywords - IGNORE_KEYWORDS
            elif name == "pmid":
                self.pmid = " ".join(value)
            elif name == "journal":
                self.journal = " ".join(value)
            elif name == "title":
                self.title = " ".join(value)
                self.title = self.title.replace("{", "").replace("}", "").replace("\"", "")
            elif name == "url":
                self.url = " ".join(value)
            elif name == "author":
                self.authors = []
                tokens = []
                while True:
                    try:
                        token = value.pop(0)
                        token = token.strip(",")
                    except IndexError:
                        self.authors.append(tokens)
                        break
                    if token == "and":
                        self.authors.append(tokens)
                        tokens = []
                    else:
                        tokens.append(token)
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
            elif name == "pdf":
                self.pdf = "".join(value)
            elif name == "abstract":
                self.abstract = " ".join(value)
            elif name in ["organization", "institution"]:
                self.organization = " ".join(value)
            else:
                errstr = "Unknown article field: %s" % name
                raise ValueError(errstr)

class Article(Record):
    """ BibTeX article """
    def __str__(self):
        return "%s" % self.__dict__
    def get_short_citation(self):
        with StringIO() as f:
            f.write("%s. " % self.get_short_authors())
            f.write("%s. " % self.get_string_attr("title"))
            tokens = []
            for attr in ["journal", "volume", "pages", "year"]:
                try:
                    tokens.append(self.get_string_attr(attr))
                except AttributeError:
                    _LOGGER.error("%s is missing %s" % (self.label, attr))
            f.write("%s. " % ", ".join(tokens))
            return f.getvalue()
class InCollection(Record):
    """ BibTeX collection """
    def __str__(self):
        return "%s" % self.__dict__
    def get_short_citation(self):
        with StringIO() as f:
            f.write("%s. " % self.get_short_authors())
            f.write("%s. " % self.get_string_attr("title"))
            f.write("In %s, %s, %s." % (self.get_string_attr("booktitle"), self.pages, self.year))
            return f.getvalue()
class Report(Record):
    """ BibTeX report """
    def __str__(self):
        return "%s" % self.__dict__
    def get_short_citation(self):
        with StringIO() as f:
            f.write("%s. " % self.get_short_authors())
            f.write("%s. " % self.get_string_attr("title"))
            f.write("%s, %s, %s." % (self.get_string_attr("type"), self.get_string_attr("organization"), self.year))
            return f.getvalue()
class InProceedings(Record):
    """ BibTeX proceedings """
    def __str__(self):
        return "%s" % self.__dict__
    def get_short_citation(self):
        with StringIO() as f:
            f.write("%s. " % self.get_short_authors())
            f.write("%s. " % self.get_string_attr("title"))
            f.write("In %s, %s, %s." % (self.get_string_attr("booktitle"), self.pages, self.year))
            return f.getvalue()
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
    label = token_list.pop(0).strip(",")
    _LOGGER.info("Parsing %s..." % label)
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
    records = []
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
        records.append(parse_record(record_string))
    return records

def main():
    """ Main routine """
    with open(BIBTEX_FILE_PATH, "rt") as bibfile:
        records = parse_bibtex(bibfile)
    for record in records:
        _LOGGER.info("Writing %s..." % record.label)
        record_path = "%s/%s.md" % (MARKDOWN_DIR_PATH, record.label)
        with open(record_path, "wt") as recfile:
            recfile.write(record.markdown())

if __name__ == "__main__":
    main()
