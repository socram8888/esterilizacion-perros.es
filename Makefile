
# Folder structure
STRUCTURE=$(shell find pages/ template/ -type d -printf "output/%P/\n")

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

# Generate structure, copy resources, then generate HTMLs
all: $(STRUCTURE) $(RAWTEMPLATE) $(RAWSOURCES) $(MDHTML)

pages/navigation.yml output/sitemap.xml: $(MDFILES)
	python3 build-navigation.py --baseurl https://www.esterilizacion-perros.es

output//:
	mkdir -p $@

output/%/:
	mkdir -p $@

output/%.html: pages/%.md pages/navigation.yml $(TEMPLATEHTML)
	python3 build-html.py --input $< --output $@

output/%.jpg: pages/%.jpg
	convert $< -sampling-factor 4:2:0 -strip -quality 85 -interlace JPEG $@

output/%.jpg: template/%.jpg
	convert $< -sampling-factor 4:2:0 -strip -quality 85 -interlace JPEG $@

output/%.png: pages/%.png
	convert $< -strip $@

output/%.png: template/%.png
	convert $< -strip $@

output/%.css: pages/%.css
	python3 -m csscompressor $< -o $@

output/%.css: template/%.css
	python3 -m csscompressor $< -o $@

output/%: pages/%
	cp $< $@

output/%: template/%
	cp $< $@

clean:
	rm -f pages/navigation.yml
	rm -rf output

server:
	cd output && python3 -m http.server 8000
