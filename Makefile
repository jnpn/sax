LESS=less -RS
DMENU=dmenu -l 10 -i -p "xml: "

# Let's make `try` the main rule.

try:
	python main.py tree `python main.py samples | $(DMENU)` | $(LESS)

all:	clean build
	@echo all

clean:
	find . -type f -iname '*~' -execdir rm {} \;

build:
	python setup.py --version
	python setup.py sdist
	@echo if this is a newer version, and you want to use it
	@echo run 'pip install --upgrade .'

test:
	nosetests -v --with-id
