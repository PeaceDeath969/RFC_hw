@'
# Notification Platform HW4

Домашнее задание №4 по теме "Требования и архитектурное мышление".

## Что внутри

- `docs/requirements.md` — функциональные требования
- `docs/asr.md` — нефункциональные требования и ASR
- `docs/architecture_questions.md` — архитектурные вопросы, последствия ASR, неподходящие решения
- `docs/risks.md` — неопределённости и риски
- `docs/rfc/guaranteed_delivery_rfc.md` — RFC по гарантированной доставке критичных уведомлений
- `docs/diagrams/` — C4 и sequence диаграммы в PlantUML
- `src/notification_platform/` — простой Python-прототип механики доставки и failover
- `tests/` — тесты прототипа

## Запуск

```powershell
poetry install
$env:PYTHONPATH = "src"
poetry run pytest