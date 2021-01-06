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

################################################################################
# Installing from test Python repository
################################################################################

install-testpy:
	python3 -m pip install -i https://test.pypi.org/simple/ vertere

################################################################################
# Installing from Python repository
################################################################################

install-test-pypi:
	python3 -m pip install -i https://test.pypi.org/simple/ vertere

uninstall:
	python3 -m pip uninstall vertere
