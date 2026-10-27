# Common tasks for the Group 13 CS221 mini projects.
# Works from PowerShell, cmd or Git Bash (recipes only use commands valid in all of them).
#
#   make report          build report/report.pdf (needs only MiKTeX)
#   make report-watch    rebuild the PDF on every save (needs Perl, see README)
#   make report-clean    delete LaTeX build files (keeps report.pdf)
#   make notebook        open the notebook in JupyterLab
#   make test A=01_foundations [T=4a-0-basic]   run the official grader (all tests, or one)
#   make package         build dist/ (the notebook + PDF to upload, plus the fallback zip)
#   make env             create the conda environment (first-time setup)

PYTHON ?= python
A ?= 01_foundations
T ?=

# pdflatex is run twice so the table of contents and page references are filled in.
# -aux-directory (MiKTeX) keeps .aux/.log/.toc in report/build/; the PDF lands in report/.
LATEX = pdflatex -interaction=nonstopmode -halt-on-error -file-line-error -jobname=report -aux-directory=build

.PHONY: help report report-watch report-clean notebook test package env

help:
	@echo make report        - build report/report.pdf
	@echo make report-watch  - rebuild the PDF on every save, needs Perl
	@echo make report-clean  - remove LaTeX build files
	@echo make notebook      - open the notebook in JupyterLab
	@echo make test A=02_sentiment T=3a-0-basic - run a grader
	@echo make package       - build the Moodle upload files in dist/
	@echo make env           - create the cs221 conda environment

report:
	cd report && $(LATEX) main.tex && $(LATEX) main.tex

report-watch:
	cd report && latexmk -pvc

report-clean:
	$(PYTHON) -c "import shutil; shutil.rmtree('report/build', ignore_errors=True)"

notebook:
	jupyter lab notebook/CS221_Mini_Projects.ipynb

test:
	cd assignments/$(A) && $(PYTHON) grader.py $(T)

package: report
	$(PYTHON) scripts/package_submission.py --name Group13_CS221_MiniProjects

env:
	conda env create -f environment.yml
	conda run -n cs221 python -m ipykernel install --user --name cs221 --display-name "Python 3.12 (cs221)"
