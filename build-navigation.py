#!/usr/bin/env python3

import argparse
import os
import sys
import ruamel.yaml
from lxml import etree
from shared import *

def enter_section(folder, baseurl, relurl, urlset):
	mdfile = os.path.join(folder, 'index.md')

	try:
		with open(mdfile) as f:
			meta = read_meta(f)
	except FileNotFoundError:
		return None

	urlelem = etree.SubElement(urlset, 'url')
	locelem = etree.SubElement(urlelem, 'loc')
	locelem.text = baseurl + relurl

	section = Section(name=meta['title'], url=relurl)
	for entry in os.listdir(folder):
		subfolder = os.path.join(folder, entry)
		if not os.path.isdir(subfolder):
			continue

		subsection = enter_section(subfolder, baseurl, '%s%s/' % (relurl, entry), urlset)
		if subsection is not None:
			section.children.append(subsection)

	return section

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Builds a Markdown file')
	parser.add_argument('--pages', help='root folder with all Markdown files', type=str, default='pages')
	parser.add_argument('--baseurl', help='base URL', type=str, required=True)
	parser.add_argument('--navfile', help='navigation file', type=str, default='pages/navigation.yml')
	parser.add_argument('--sitemap', help='sitemap file', type=str, default='output/sitemap.xml')
	args = parser.parse_args()

	print('Rescanning sections', file=sys.stderr)

	urlset = etree.Element('urlset', attrib={'xmlns': 'http://www.sitemaps.org/schemas/sitemap/0.9'})
	root_section = enter_section(args.pages, args.baseurl, '/', urlset)

	if root_section is None:
		print('Root section not found', file=sys.stderr)
		sys.exit(1)

	yaml = ruamel.yaml.YAML()
	yaml.register_class(Section)

	try:
		with open(args.navfile) as f:
			old_root = yaml.load(f)

		if old_root == root_section:
			print('No changes', file=sys.stderr)
			sys.exit(0)
	except FileNotFoundError:
		pass

	print('Writing to %s' % args.navfile, file=sys.stderr)
	with open(args.navfile, 'w') as f:
		yaml.dump(root_section, f)

	et = etree.ElementTree(urlset)
	with open(args.sitemap, 'wb') as f:
		et.write(f, encoding='utf-8', xml_declaration=True) 
