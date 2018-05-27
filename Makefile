
# All raw Markdown source files
MDFILES=$(shell find pages/ -type f -name "*.md")

# HTML files that should be generated
MDHTML=$(patsubst pages/%.md, output/%.html, $(MDFILES))

# All template files
TEMPLATEHTML=$(shell find template/ -type f -name "*.html")

# Raw resources that should be copied as-is
RAWSOURCES=$(shell find pages/ -type f ! -name "*.md" ! -name "navigation.yml" -printf "output/%P\n")
RAWTEMPLATE=$(shell find template/ -type f ! -name "*.html" -printf "output/%P\n")

# Disable built-in rules
.SUFFIXES:

.PHONY: all clean

# Copy resources, then generate HTMLs
all: $(RAWTEMPLATE) $(RAWSOURCES) $(MDHTML)

pages/navigation.yml output/sitemap.xml: $(MDFILES)
	python3 build-navigation.py --baseurl https://www.esterilizacion-perros.es

output/%.html: pages/%.md pages/navigation.yml $(TEMPLATEHTML)
	mkdir -p $(dir $@)
	python3 build-html.py --input $< --output $@

output/%: pages/%
	mkdir -p $(dir $@)
	cp $< $@

output/%: template/%
	mkdir -p $(dir $@)
	cp $< $@

clean:
	rm -f pages/navigation.yml
	rm -rf output

server:
	cd output && python3 -m http.server 8000
