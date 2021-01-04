################################################################################
# Developing
################################################################################

install:
	pip3 install -e .

uninstall:
	pip3 uninstall vertere

test:
	pytest -vv

requirements-install:
	pip3 install -r requirements.txt

requirements-uninstall:
	pip3 uninstall -r requirements.txt

################################################################################
# Packaging
################################################################################

package-required-install:
	python3 -m pip install --user --upgrade setuptools wheel

package:
	python3 setup.py sdist bdist_wheel

################################################################################
# Publishing
################################################################################

publish-required-install:
	python3 -m pip install --user --upgrade twine

publish-testpy:
	python3 -m twine upload --repository testpypi dist/*

# --no-deps example-pkg-YOUR-USERNAME-HERE
install-testpy:
	python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps versioning-mulecode
