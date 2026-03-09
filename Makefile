.PHONY: help setup clean clean-all show-docs show-terms build-index rebuild-kb test-search stats run-bot demo-bot test-security task5-test

# Цвета для вывода
RED=\033[0;31m
GREEN=\033[0;32m
YELLOW=\033[1;33m
BLUE=\033[0;34m
NC=\033[0m # No Color

help: ## Показать справку по командам
	@echo "$(BLUE)╔══════════════════════════════════════════════════════════════╗$(NC)"
	@echo "$(BLUE)║$(NC)  $(GREEN)RAG-бот Eternum Nexus - Доступные команды$(NC)                  $(BLUE)║$(NC)"
	@echo "$(BLUE)╚══════════════════════════════════════════════════════════════╝$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-18s$(NC) %s\n", $$1, $$2}'
	@echo ""

setup: ## Установить зависимости и настроить окружение
	@echo "$(GREEN)Установка зависимостей...$(NC)"
	python3 -m venv .venv
	. .venv/bin/activate && pip install -q --upgrade pip
	. .venv/bin/activate && pip install -q -r requirements.txt
	@echo "$(GREEN)✓ Готово! Активируйте окружение: source .venv/bin/activate$(NC)"


build-index: ## Создать векторный индекс из базы знаний
	@echo "$(GREEN)Построение векторного индекса...$(NC)"
	@. .venv/bin/activate && python scripts/build_index.py

rebuild-kb: ## Пересоздать базу знаний из raw/ документов
	@echo "$(GREEN)Пересоздание базы знаний...$(NC)"
	@. .venv/bin/activate && python scripts/replace_terms.py

test-search: ## Запустить интерактивный поиск по индексу
	@echo "$(GREEN)Запуск интерактивного поиска...$(NC)"
	@. .venv/bin/activate && python scripts/test_search.py

run-bot: ## Запустить RAG-бота (требует OPENAI_API_KEY)
	@echo "$(GREEN)Запуск RAG-бота...$(NC)"
	@. .venv/bin/activate && python rag_bot.py

demo-bot: ## Демонстрация RAG-бота с тестовыми запросами
	@echo "$(GREEN)Демонстрация RAG-бота...$(NC)"
	@. .venv/bin/activate && python scripts/demo_bot.py

stats: ## Показать статистику проекта
	@echo "$(BLUE)╔══════════════════════════════════════════════════════════════╗$(NC)"
	@echo "$(BLUE)║$(NC)  $(GREEN)Статистика проекта Eternum Nexus RAG$(NC)                       $(BLUE)║$(NC)"
	@echo "$(BLUE)╚══════════════════════════════════════════════════════════════╝$(NC)"
	@echo ""
	@echo "$(YELLOW)База знаний:$(NC)"
	@echo "  Оригинальных документов: $$(ls -1 data/raw/*.txt 2>/dev/null | wc -l | tr -d ' ')"
	@echo "  Трансформированных: $$(ls -1 knowledge_base/*.txt 2>/dev/null | wc -l | tr -d ' ')"
	@echo "  Терминов заменено: $$(grep -c '":' terms_map.json)"
	@echo ""
	@echo "$(YELLOW)Векторный индекс:$(NC)"
	@if [ -d "chroma_db" ]; then \
		echo "  Статус: $(GREEN)создан$(NC)"; \
		echo "  Размер: $$(du -sh chroma_db 2>/dev/null | cut -f1)"; \
	else \
		echo "  Статус: $(RED)не создан$(NC) (запустите: make build-index)"; \
	fi
	@echo ""
	@echo "$(YELLOW)Модели:$(NC)"
	@if [ -d "models_cache" ]; then \
		echo "  Кэш моделей: $(GREEN)загружен$(NC)"; \
		echo "  Размер: $$(du -sh models_cache 2>/dev/null | cut -f1)"; \
	else \
		echo "  Кэш моделей: $(RED)не загружен$(NC)"; \
	fi
	@echo ""
	@echo "$(YELLOW)Скрипты:$(NC)"
	@echo "  replace_terms.py - замена терминов"
	@echo "  build_index.py - построение индекса"
	@echo "  test_search.py - тестирование поиска"
	@echo ""

clean: ## Очистить кэши и индексы (без удаления .venv)
	@echo "$(YELLOW)Очистка кэшей и индексов...$(NC)"
	rm -rf chroma_db/
	rm -rf models_cache/
	rm -rf __pycache__/
	rm -rf scripts/__pycache__/
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "$(GREEN)✓ Очистка завершена$(NC)"

clean-all: clean ## Полная очистка (включая .venv)
	@echo "$(RED)Удаление виртуального окружения...$(NC)"
	rm -rf .venv/
	@echo "$(GREEN)✓ Полная очистка завершена$(NC)"

# Быстрые команды
quick-start: setup build-index ## Быстрая установка и запуск
	@echo ""
	@echo "$(GREEN)╔══════════════════════════════════════════════════════════════╗$(NC)"
	@echo "$(GREEN)║$(NC)  Проект готов к использованию!                              $(GREEN)║$(NC)"
	@echo "$(GREEN)║$(NC)  Запустите: $(YELLOW)make test-search$(NC)                                $(GREEN)║$(NC)"
	@echo "$(GREEN)╚══════════════════════════════════════════════════════════════╝$(NC)"

test-simple: ## Быстрый тест поиска (без интерактивного режима)
	@echo "$(GREEN)Быстрый тест поиска...$(NC)"
	@. .venv/bin/activate && python -c "from scripts.test_search import *; \
		vs = load_vectorstore(); \
		search(vs, 'What are the main races?', k=3); \
		search(vs, 'Tell me about Stellarium currency', k=3)"

check: ## Проверить состояние проекта
	@echo "$(BLUE)Проверка проекта...$(NC)"
	@echo ""
	@if [ -d ".venv" ]; then \
		echo "$(GREEN)✓$(NC) Виртуальное окружение создано"; \
	else \
		echo "$(RED)✗$(NC) Виртуальное окружение не найдено (запустите: make setup)"; \
	fi
	@if [ -d "knowledge_base" ] && [ "$$(ls -1 knowledge_base/*.txt 2>/dev/null | wc -l)" -gt "0" ]; then \
		echo "$(GREEN)✓$(NC) База знаний создана ($$(ls -1 knowledge_base/*.txt | wc -l | tr -d ' ') документов)"; \
	else \
		echo "$(RED)✗$(NC) База знаний не найдена"; \
	fi
	@if [ -d "chroma_db" ]; then \
		echo "$(GREEN)✓$(NC) Векторный индекс создан"; \
	else \
		echo "$(RED)✗$(NC) Векторный индекс не создан (запустите: make build-index)"; \
	fi
	@if [ -d "models_cache" ]; then \
		echo "$(GREEN)✓$(NC) Модели загружены"; \
	else \
		echo "$(YELLOW)⚠$(NC) Модели будут загружены при первом запуске"; \
	fi
	@echo ""

# Тестирование безопасности (Задание 5)
test-security:  ## Тест защиты от prompt injection
	@echo "$(BLUE)Тестирование защиты RAG-бота...$(NC)"
	@. .venv/bin/activate && python scripts/test_security.py

task5-test:  ## Полное тестирование задания 5 (10 запросов)
	@echo "$(BLUE)Запуск полного тестирования (5 успешных + 5 отказов)...$(NC)"
	@. .venv/bin/activate && python scripts/task5_test.py
	@echo "$(GREEN)Результаты сохранены в: task5_test_results.txt$(NC)"

# По умолчанию показываем help
.DEFAULT_GOAL := help
