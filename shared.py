
import re
import ruamel.yaml

class Section:
	def __init__(self, name, url):
		self.name = name
		self.url = url
		self.children = []

	def __repr__(self):
		return str(self.__dict__)

	def __eq__(self, other):
		return (
				self.name == other.name and
				self.url == other.url and
				self.children == other.children
		)

def read_meta(fh):
	for line in fh:
		if re.match('---\s*$', line):
			break

	meta_block = ''
	end_found = False
	for line in fh:
		if re.match('---\s*$', line):
			return ruamel.yaml.safe_load(meta_block)

		meta_block += line

	raise NoMetaException()

class NoMetaException(Exception):
	pass
