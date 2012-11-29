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
