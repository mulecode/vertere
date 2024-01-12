################################################################################
# Developing
################################################################################

install-locally:
	python3 -m pip install -e .

test:
	pytest -vv

requirements-install:
	python3 -m pip install -r requirements.txt

requirements-uninstall:
	python3 -m pip uninstall -r requirements.txt

test-readme-renderer:
	python3 -m pip install --user --upgrade readme-renderer && \
	python3 -m readme_renderer ./README.md -o ./README.html

################################################################################
# Packaging
################################################################################

package:
	python3 -m pip install --user --upgrade setuptools wheel build && \
	python3 -m build && \
	python3 -m pip install --use-pep517 . && \
	python3 -m pip install --user --upgrade twine

################################################################################
# Publishing
################################################################################

publish-testpypi:
	python3 -m twine upload --repository testpypi dist/*

publish-pypi:
	python3 -m twine upload --repository pypi dist/*

################################################################################
# Installing
################################################################################

install-testpypi:
	python3 -m pip install -i https://test.pypi.org/simple/ vertere

install-pypi:
	python3 -m pip install vertere

uninstall:
	python3 -m pip uninstall vertere
