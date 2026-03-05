# Vale prose linting

VALE_BIN?=vale
VALE_FLAGS?=--no-exit

.PHONY: docs-vale
docs-vale: $(DOCS_TARGET)
	@echo "Run Vale prose linter"
	@$(VALE_BIN) $(VALE_FLAGS) $(DOCS_SOURCE_FOLDER)

.PHONY: docs-vale-sync
docs-vale-sync:
	@echo "Sync Vale styles"
	@$(VALE_BIN) sync
