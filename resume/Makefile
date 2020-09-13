resume.pdf: resume.aux
	pdflatex resume.tex
	mv resume.pdf ..

resume.aux:
	pdflatex resume.tex

clean:
	rm *.aux *.log *.out
