SPELLTEX=$(shell egrep '^\\\input' tiny-tasks.tex | sed 's/^.*input[^{]*{//' | sed 's/}.*$$/.tex/')

all:
	pdflatex tiny-tasks && bibtex tiny-tasks && pdflatex tiny-tasks && pdflatex tiny-tasks

paper: all
	open tiny-tasks.pdf

clean:
	rm -f *.aux
	rm -f *.bbl
	rm -f *.log
	rm -f *.blg
	rm tiny-tasks.pdf

spellcheck:
	for i in $(SPELLTEX); do \
	  echo $$i; \
	  aspell -c --home-dir=. $$i; \
	done
