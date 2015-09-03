all:	clean build
	@echo all

clean:
	rm *~

build:
	python setup.py --version
	python setup.py sdist
	@echo if this is a newer version, and you want to use it
	@echo run 'pip install --upgrade .'