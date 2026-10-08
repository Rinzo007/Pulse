# Pulse — документация

Pulse — система транспортного планирования и моделирования города и пригорода с приоритетом общественного транспорта.

Документация фиксирует предметную область, математические модели, источники данных, расчётный конвейер, правила валидации и границы применимости результатов. Реализация является отдельным слоем и не должна менять смысл моделей без изменения спецификаций.

## Сквозной цикл

**Землепользование → население и активности → транспортные районы → генерация → распределение спроса → выбор времени → выбор вида транспорта → выбор маршрута → транспортная сеть → ОТ → расписания → эксплуатация → пассажиры → движение → SUMO → задержки/переполнение → качество поездки → обратная связь спроса → KPI → неопределённость → экономическая и социальная оценка → проектное решение → новый сценарий.**

## 1. Назначение и архитектура

- [vision.md](vision.md) — назначение и границы.
- [requirements.md](requirements.md) — функциональные и нефункциональные требования.
- [architecture.md](architecture.md) — архитектура и границы подсистем.
- [domain-model.md](domain-model.md) — предметная модель.
- [implementation-boundaries.md](implementation-boundaries.md) — границы отдельных моделей.
- [roadmap.md](roadmap.md) — последовательность разработки.
- [glossary.md](glossary.md) — терминология.

## 2. Территория, население и спрос

- [land-use-and-activities.md](land-use-and-activities.md)
- [population-and-agents.md](population-and-agents.md)
- [activity-based-demand.md](activity-based-demand.md)
- [demand-model.md](demand-model.md)
- [traffic-assignment.md](traffic-assignment.md)
- [future-demand.md](future-demand.md)
- [synthetic-data.md](synthetic-data.md)

## 3. Транспортная сеть

- [network-model.md](network-model.md)
- [walking-cycling.md](walking-cycling.md)
- [traffic-signals.md](traffic-signals.md)
- [parking-and-pr.md](parking-and-pr.md)
- [freight-and-commercial.md](freight-and-commercial.md)

## 4. Общественный транспорт

- [transport-model.md](transport-model.md)
- [public-transport.md](public-transport.md)
- [gtfs-and-transit-data.md](gtfs-and-transit-data.md)
- [route-planning.md](route-planning.md)
- [route-choice.md](route-choice.md)
- [scheduling.md](scheduling.md)
- [fleet-and-depots.md](fleet-and-depots.md)
- [driver-and-crew.md](driver-and-crew.md)
- [rail-operations.md](rail-operations.md)
- [capacity-model.md](capacity-model.md)
- [bunching-model.md](bunching-model.md)
- [headway-control.md](headway-control.md)
- [transit-priority.md](transit-priority.md)
- [transfer-model.md](transfer-model.md)
- [service-quality.md](service-quality.md)
- [fares-and-ticketing.md](fares-and-ticketing.md)
- [disruptions.md](disruptions.md)

## 5. Пассажир и выбор

- [passenger-model.md](passenger-model.md)
- [mode-choice.md](mode-choice.md)
- [accessibility.md](accessibility.md)
- [accessibility-formulas.md](accessibility-formulas.md)

## 6. Математические модели

- [mathematical-model.md](mathematical-model.md)
- [calculation-pipeline.md](calculation-pipeline.md)
- [units-and-conventions.md](units-and-conventions.md)
- [kpi-formulas.md](kpi-formulas.md)
- [waiting-model.md](waiting-model.md)
- [demand-assignment.md](demand-assignment.md)
- [calibration-methodology.md](calibration-methodology.md)
- [optimization-methodology.md](optimization-methodology.md)
- [scenario-comparison.md](scenario-comparison.md)

## 7. Симуляция

- [simulation-model.md](simulation-model.md)
- [sumo.md](sumo.md)
- [experiment-design.md](experiment-design.md)

## 8. Сценарии и проектирование

- [scenarios.md](scenarios.md)
- [optimization.md](optimization.md)
- [route-planning.md](route-planning.md)
- [health-check.md](health-check.md)

## 9. Калибровка, проверка и неопределённость

- [calibration.md](calibration.md)
- [model-estimation.md](model-estimation.md)
- [validation.md](validation.md)
- [testing.md](testing.md)
- [uncertainty.md](uncertainty.md)
- [assumptions.md](assumptions.md)
- [reproducibility.md](reproducibility.md)
- [data-lineage.md](data-lineage.md)

## 10. Экономика, окружающая среда и общественный эффект

- [economics.md](economics.md)
- [economic-appraisal.md](economic-appraisal.md)
- [emissions-and-energy.md](emissions-and-energy.md)
- [safety.md](safety.md)
- [accessibility.md](accessibility.md)
- [reporting.md](reporting.md)

## 11. Данные

- [data-sources.md](data-sources.md)
- [osm.md](osm.md)
- [gtfs-and-transit-data.md](gtfs-and-transit-data.md)
- [data-lineage.md](data-lineage.md)

## 12. Система и интерфейс

- [api.md](api.md)
- [database.md](database.md)
- [frontend.md](frontend.md)
- [operations.md](operations.md)
- [security-and-governance.md](security-and-governance.md)
- [ai-assistant.md](ai-assistant.md)
- [ai-model-prompt.md](ai-model-prompt.md) — системный промпт ИИ-модели Pulse, включая Rust как основное вычислительное ядро и режим немедленного выполнения задач.

### Исполнительная модель ИИ

ИИ Pulse после получения однозначной задачи должен сразу переходить к её выполнению, если необходимые входы доступны.

- **Rust** — основной язык вычислительного ядра Pulse для производительных расчётов, графов, назначения, маршрутизации, KPI, оптимизации и многократных сценарных запусков.
- **SUMO** — специализированный микроскопический движок дорожного движения; Rust не заменяет его там, где требуется микроскопическая симуляция.
- ИИ должен использовать доступные инструменты и фактически выполнять задачу, а не только описывать способ её выполнения.
- Если необходимых данных недостаточно, ИИ запрашивает только минимально необходимое недостающее условие.
- Выполненное изменение должно сохранять происхождение, версию, параметры и воспроизводимость.
- ИИ не должен утверждать, что задача выполнена, если фактического выполнения не было.

## 13. Основные принципы

1. Реальные, синтетические, производные и калиброванные данные различаются.
2. Эвристика не называется доказанным оптимумом.
3. Без калибровки нельзя заявлять реалистичность численных результатов.
4. Каждый результат привязан к версии входных данных, параметров, сценария и модели.
5. Rust является основным вычислительным ядром Pulse для производительных и воспроизводимых расчётов; SUMO отвечает за микроскопическую динамику и не заменяет спрос, пассажира, эксплуатацию или оценку.
6. Спрос и предложение взаимодействуют итеративно там, где это требуется постановкой.
7. Средние значения не должны скрывать локальные проблемы, переполнение, неравенство доступности или ненадёжность.
8. Сценарии должны проверяться на физическую выполнимость до симуляции.
9. Результат симуляции является результатом заданной модели и входов, а не автоматически фактом о реальном городе.
10. ИИ может объяснять и предлагать изменения, но не превращает модельный вывод в наблюдение или утверждённое проектное решение.
