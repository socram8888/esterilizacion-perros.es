#!/usr/bin/env python3

import argparse
import jinja2
import markdown
import os
import sys
import ruamel.yaml
from shared import *

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Builds a Markdown file')
	parser.add_argument('--input', help='file to build', type=argparse.FileType('r'), default=sys.stdin)
	parser.add_argument('--output', help='output file', type=argparse.FileType('w'), default=sys.stdout)
	parser.add_argument('--template', help='template folder', type=str, default='template')
	parser.add_argument('--navigation', help='navigation file', type=str, default='pages/navigation.yml')
	args = parser.parse_args()

	loader = jinja2.PrefixLoader(
			{
					'template': jinja2.FileSystemLoader(args.template)
			},
			delimiter='@'
	)
	env = jinja2.Environment(
		loader=loader,
		autoescape=jinja2.select_autoescape()
	)

	yaml = ruamel.yaml.YAML()
	yaml.register_class(Section)

	with open(args.navigation) as f:
		root_section = yaml.load(f)

	page_meta = read_meta(args.input)

	page_source = args.input.read()
	page_source = env.from_string(page_source).render(meta=page_meta, home=root_section)

	page_content = markdown.markdown(page_source, extensions=('markdown.extensions.toc', 'markdown.extensions.footnotes'))

	template = env.get_template('template@template.html')
	page_html = template.render(content=jinja2.Markup(page_content), meta=page_meta, home=root_section)
	args.output.write(page_html)
