install:
	pip3 install -e .

uninstall:
	pip3 uninstall versioning-cli

test:
	pytest -vv

