current_dir = $(shell pwd)
MKDOCS_PORT=8104


build:
	mkdocs build --clean

serve:
	mkdocs serve --dev-addr localhost:$(MKDOCS_PORT)

publish:
	mkdocs gh-deploy --config-file ./mkdocs.yml --remote-branch gh-pages

clean:
	rm -rf ./site


FORCE:
