.PHONY: all pdf clean check lean wordcount bookstats todos generate biber hooks snap-start snap-end

all: pdf

generate:
	./scripts/generate_manuscript_tex.sh

biber:
	./scripts/biber.sh

pdf:
	./build.sh

clean:
	./clean.sh

lean:
	./formal/check.sh

check:
	./scripts/check.sh

wordcount:
	$$(./scripts/resolve_python.sh) scripts/wordcount.py

bookstats:
	$$(./scripts/resolve_python.sh) scripts/book_stats.py

todos:
	$$(./scripts/resolve_python.sh) scripts/extract_todos.py

hooks:
	git config core.hooksPath .githooks

snap-start:
	./scripts/hooks/snapshot.sh agent-start manual $$(id -un) manual

snap-end:
	./scripts/hooks/snapshot.sh agent-end manual $$(id -un) manual
