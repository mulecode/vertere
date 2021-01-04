################################################################################
# Developing
################################################################################

install-localy:
	pip3 install -e .

uninstall:
	pip3 uninstall vertere

test:
	pytest -vv

requirements-install:
	pip3 install -r requirements.txt

requirements-uninstall:
	pip3 uninstall -r requirements.txt

test-readme-renderer:
	pip3 install --user --upgrade readme-renderer && \
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

publish-testpy:
	python3 -m twine upload --repository testpypi dist/*

################################################################################
# Installing from test Python repository
################################################################################

install-vertere-testpy:
	python3 -m pip install -i https://test.pypi.org/simple/ vertere

################################################################################
# Installing from Python repository
################################################################################

install-vertere:
	python3 -m pip install -i https://test.pypi.org/simple/ vertere

uninstall:
	python3 -m pip uninstall vertere
