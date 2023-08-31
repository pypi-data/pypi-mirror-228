################################################################################
#                                 py-fast-trie                                 #
#          Python library for tries with different grades of fastness          #
#                       (C) 2020, 2022-2023 Jeremy Brown                       #
#                Released under Prosperity Public License 3.0.0                #
################################################################################

.POSIX:

.PHONY: ci-test clean release test

clean:
	rm -rf .coverage coverage.xml .eggs/ .hypothesis/ .mypy_cache/ .pytest_cache/ *egg-info/ dist/ build/
	find . -name __pycache__ -exec rm -rf {} +
	find . -name *.pyc -exec rm -rf {} +

test:
	pytest

ci-test:
	pytest --cov-report xml --hypothesis-profile ci

release:
	python -m build .
