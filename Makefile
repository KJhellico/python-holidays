help:
	@echo "Usage: make <target>"
	@echo "    check         run pre-commit and tests"
	@echo "    doc           run documentation build process"
	@echo "    help          show summary of available commands"
	@echo "    l10n          update .pot and .po files"
	@echo "    package       build package distribution"
	@echo "    pre-commit    run pre-commit against all files"
	@echo "    setup         setup development environment"
	@echo "    test          run tests (in parallel)"

check:
	make l10n
	make pre-commit
	make doc
	make test

clean:
	@for ext in mo pot pyc; do \
		find . -type f -name "*.$$ext" -delete; \
	done
	@rm -rf .mypy_cache .pytest_cache dist .tox

doc:
	mkdocs build

generate-mo:
	uv run --no-default-groups --group build scripts/l10n/generate_mo_files.py

l10n:
	find . -type f -name "*.pot" -delete
	uv run scripts/l10n/generate_po_files.py >/dev/null 2>&1
	make generate-mo

package:
	make generate-mo
	uv build

pre-commit:
	pre-commit run --all-files

release-notes:
	@scripts/generate_release_notes.py

sbom:
	uv tool run --from cyclonedx-bom cyclonedx-py requirements requirements/runtime.txt

setup:
	curl -LsSf https://astral.sh/uv/install.sh | sh
	uv venv
	uv sync --all-groups
	uv tool install pre-commit --with pre-commit-uv
	pre-commit install --hook-type pre-commit
	pre-commit install --hook-type pre-push
	make l10n
	make package

snapshot:
	make generate-mo
	uv run scripts/generate_snapshots.py

test:
	make generate-mo
	pytest --cov=. --cov-config=pyproject.toml --cov-report term-missing --cov-report xml --durations 10 --durations-min=0.75 --dist loadscope --no-cov-on-fail --numprocesses auto
