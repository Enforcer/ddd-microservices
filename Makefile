.PHONY: freeze_deps
freeze_deps:
	pip-compile requirements/app.in -o requirements/app.txt
	pip-compile requirements/dev.in -o requirements/dev.txt

.PHONY: fmt
fmt:
	isort used_stuff_market/
	black used_stuff_market/

.PHONY: lint
lint:
	mypy used_stuff_market/availability/ --ignore-missing-imports
	mypy used_stuff_market/catalog/ --ignore-missing-imports
	mypy used_stuff_market/chat/ --ignore-missing-imports
	mypy used_stuff_market/items/ --ignore-missing-imports
	mypy used_stuff_market/likes/ --ignore-missing-imports
	mypy used_stuff_market/negotiations/ --ignore-missing-imports
