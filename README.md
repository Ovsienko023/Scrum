# Scrum

Это бэкенд для приложения по управлению задачами. Карточки задач размещаются на доске и могут перемещаться 
по колонкам меняя свой статус и приоритет выполнения. На задуча можно назначить ответственного, который 
будет эту задачу выполнять. Реализованны методы для составления отчёта по задачам на доске, 
сколько запланированно,сколько в работе, сколько завершено. 

Задачи отцениваются в идеальных еденицах времени:

- __h__ - идеальный рабочий час
- __d__ - идеальный рабочий день. Равен 8 идеальным рабочим часам.
- __w__ - идеальная рабочая неделя. Равна 5 идеальным рабочим дням.
- __m__ - идеальный рабочий месяц. Равен 4 идеальным рабочим неделям.

Проработанна арифметика для отчётности задачам. 

(Пример)

- 7h + 1h = 8h
- 7h + 1h = 1d2h
- 4d + 1d = 1w
- 4m + 5d = 2m1w


## Используемые технологии
- python 3.8
- Архитектурный подход __REST API__
- Фреймворк: __aiohttp__
- Для валидации входных данных: __marshmallow__
- База Данных: __PostgreSQL__
- Для тестирования используется __unittest__
- Документация описана в __swagger__ (openapi3.0)

Для просмотра документации, после запуска api перейти по ссылке: http://localhost:8888/docs

# Для запуска

    TODO
