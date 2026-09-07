.PHONY: all pdf clean check lean wordcount bookstats todos generate biber

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
	python3 scripts/wordcount.py

bookstats:
	python3 scripts/book_stats.py

todos:
	python3 scripts/extract_todos.py
