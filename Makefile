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

install-package-dependency:
	python3 -m pip install --user --upgrade setuptools wheel

package:
	python3 setup.py sdist bdist_wheel

################################################################################
# Publishing
################################################################################

install-publish-dependency:
	python3 -m pip install --user --upgrade twine

publish-testpy: package
	python3 -m twine upload --repository testpypi dist/*

publish-testpy: package
	python3 -m twine upload --repository pypi dist/*

################################################################################
# Installing
################################################################################

install-testpy:
	python3 -m pip install -i https://test.pypi.org/simple/ vertere

install-py:
	python3 -m pip install vertere

uninstall:
	python3 -m pip uninstall vertere
