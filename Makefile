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
	python3 scripts/check_claim_spine.py
	python3 reference/field-agendas/scripts/check-evidence-stance.py
	python3 formal/scripts/check_open_spine_interfaces.py
	python3 formal/scripts/check_specify_construct_instances.py
	cd site && npm run sync:field-v2 -- --check
	python3 scripts/check_quiz_bank.py
	python3 scripts/check_quiz_length_tell.py
	node --test reference/field-agendas/scripts/matrix-cell.test.mjs
	node --test --experimental-strip-types site/src/lib/field-matrix-cell.test.ts site/src/lib/visit-history.test.ts site/src/lib/read-next.test.ts site/src/lib/quiz/quiz.test.ts

wordcount:
	python3 scripts/wordcount.py

bookstats:
	python3 scripts/book_stats.py

todos:
	python3 scripts/extract_todos.py
