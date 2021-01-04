install:
	pip3 install -e .

package:
	python setup.py sdist bdist_wheel


uninstall:
	pip3 uninstall versioning-cli

test:
	pytest -vv

requirements-install:
	pip3 install -r requirements.txt

requirements-uninstall:
	pip3 uninstall -r requirements.txt
