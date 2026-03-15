# Makefile for simulator-worksheet
# Requires: pdflatex, pandoc, python3

MAIN        = simulator-worksheet
LATEX       = pdflatex
LATEX_FLAGS = -interaction=nonstopmode -halt-on-error
PYTHON      = python3
GEN_SCRIPT  = generate_table.py

SRCS = simulator-worksheet.tex \
       simulator_selection_worksheet.tex \
       simulator-notes.tex

HTML_DIR = html

.PHONY: all quick html clean cleanall watch help

## Default target: full build (two passes to resolve internal references)
all: $(MAIN).pdf

$(MAIN).pdf: $(SRCS)
	$(LATEX) $(LATEX_FLAGS) $(MAIN)
	$(LATEX) $(LATEX_FLAGS) $(MAIN)

## Single-pass build (faster, references may be unresolved)
quick: $(SRCS)
	$(LATEX) $(LATEX_FLAGS) $(MAIN)

## Build HTML version (requires pandoc + python3)
html: $(HTML_DIR)/$(MAIN).html

$(HTML_DIR)/$(MAIN).html: $(SRCS) simulator-worksheet.css $(GEN_SCRIPT)
	mkdir -p $(HTML_DIR)
	$(PYTHON) $(GEN_SCRIPT) -o $(HTML_DIR)/$(MAIN).html

## Remove auxiliary files, keep PDF and HTML
clean:
	rm -f $(MAIN).aux $(MAIN).log $(MAIN).out $(MAIN).toc \
	      $(MAIN).fls $(MAIN).fdb_latexmk $(MAIN).synctex.gz

## Remove all generated files including PDF and HTML
cleanall: clean
	rm -f $(MAIN).pdf
	rm -rf $(HTML_DIR)

## Watch for changes and rebuild (requires fswatch or inotifywait)
watch:
	@if command -v fswatch >/dev/null 2>&1; then \
		fswatch -o $(SRCS) | xargs -n1 -I{} make quick; \
	elif command -v inotifywait >/dev/null 2>&1; then \
		while inotifywait -e modify $(SRCS); do make quick; done; \
	else \
		echo "Install fswatch (macOS: brew install fswatch) or inotify-tools (Linux)."; \
		exit 1; \
	fi

help:
	@echo "Targets:"
	@echo "  all      - Full build: two pdflatex passes to resolve references (default)"
	@echo "  quick    - Single pdflatex pass (fast)"
	@echo "  html     - Build HTML version with pandoc (requires pandoc)"
	@echo "  clean    - Remove auxiliary files, keep PDF and HTML"
	@echo "  cleanall - Remove all generated files including PDF and HTML"
	@echo "  watch    - Rebuild on file changes (requires fswatch or inotifywait)"
	@echo "  help     - Show this help message"
