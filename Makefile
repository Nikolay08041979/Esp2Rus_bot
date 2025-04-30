.PHONY: run-dev run-prod

run-dev:
	@echo "🛠 Запуск бота в DEV-режиме"
	@ENV_MODE=dev python main.py

run-prod:
	@echo "🚀 Запуск бота в PROD-режиме"
	@ENV_MODE=prod python main.py
