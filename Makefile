.PHONY: all pdf clean check wordcount bookstats todos

all: pdf

pdf:
	./build.sh

clean:
	./clean.sh

check:
	python3 scripts/generate_tables.py
	python3 scripts/check_structure.py
	python3 scripts/check_citations.py

wordcount:
	python3 scripts/wordcount.py

bookstats:
	python3 scripts/book_stats.py

todos:
	python3 scripts/extract_todos.py
