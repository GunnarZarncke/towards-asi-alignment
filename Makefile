.PHONY: all pdf clean check wordcount bookstats todos generate biber

all: pdf

generate:
	./scripts/generate_manuscript_tex.sh

biber:
	./scripts/biber.sh

pdf:
	./build.sh

clean:
	./clean.sh

check: generate
	python3 scripts/check_structure.py
	python3 scripts/check_citations.py
	python3 scripts/check_bibliography_summaries.py

wordcount:
	python3 scripts/wordcount.py

bookstats:
	python3 scripts/book_stats.py

todos:
	python3 scripts/extract_todos.py
