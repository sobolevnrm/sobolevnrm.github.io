input_path = "presentations.bib"

class Presentation:
	def __init__(self, cite_id):
		""" Initialize with the BibTeX cite ID """
		self.cite_id = cite_id
		self.title = None
		self.year = None
		self.how_published = None
		self.authors = []
	def parse_authors(self, author_string):
		""" Extract authors """
		words = author_string.split(" and ")
		for word in words:
			author = word.split(", ")
			author.reverse()
			self.authors.append(author)
	def __str__(self):
		_str = ""
		try:
			_str = _str + "%d\t" % self.year
		except TypeError:
			pass
		formatted_authors = []
		for author in self.authors:
			formatted_authors.append(" ".join(author))
		_str = _str + ", ".join(formatted_authors) + ". "
		_str = _str + self.title + ", "
		try:
			_str = _str + self.how_published
		except TypeError:
			print(self.how_published)
			pass
		return _str
	def check(self):
		""" Check object for completeness """
		if not self.cite_id:
			errstr = "No citation ID"
			raise RuntimeError(errstr)
		if not self.title:
			errstr = "No title"
			raise RuntimeError(errstr)
		if not self.year:
			errstr = "No year"
			raise RuntimeError(errstr)
		if not self.how_published:
			errstr = "No publication description"
			raise RuntimeError(errstr)
		if len(self.authors) == 0:
			errstr = "No authors"
			raise RuntimeError(errstr)
class BibTeXParser:
	def __init__(self, input_file=None):
		""" Initialize with the file to be parsed """
		self.input_file = input_file
		self.presentations = []
		self.current_presentation = None
	def parse_header(self, line):
		""" Parse a new record """
		words = line.split("{")
		cite_id = words[1][:-1]
		if self.current_presentation:
			try:
				self.current_presentation.check()
			except RuntimeError as e:
				print(e)
				print(self.current_presentation.__dict__)
				raise(e)
			self.presentations.append(self.current_presentation)
		self.current_presentation = Presentation(cite_id)
	def parse_attribute(self, line):
		""" Parse an attribute of the record """
		if line[0] == "%":
			return
		words = line.split("=")
		if len(words) == 2:
			key = words[0].strip()
			value = words[1].strip()
			value.replace("\"", "")
			value = value.replace("{", "")
			value = value.replace("}", "")
			while True:
				if value[-1] == ",":
					value = value[:-1]
				else:
					break
			if key == "title":
				self.current_presentation.title = value
			elif key == "year":
				self.current_presentation.year = int(value)
			elif key == "howpublished":
				self.current_presentation.how_published = value
			elif key == "author":
				self.current_presentation.parse_authors(value)
			else:
				errstr = "Unable to parse line: %s" % line
				raise ValueError(errstr)
	def parse(self):
		""" Parse the input file """
		self.lines = []
		for line in self.input_file:
			line = line.strip()
			if len(line) > 0:
				self.lines.append(line)
		for line in self.lines:
			if line[0] == "@":
				self.parse_header(line)
			else:
				self.parse_attribute(line)
		self.presentations.append(self.current_presentation)


with open(input_path, "rt") as input_file:
	bib_parser = BibTeXParser(input_file)
	bib_parser.parse()
	bib_parser.presentations.sort(key=lambda presentation: presentation.year)
	bib_parser.presentations.reverse()
	for p in bib_parser.presentations:
		print("%s." % p)