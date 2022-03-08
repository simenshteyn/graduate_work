# Проектная работа: сервис биллинга

**Описание проекта:** система биллинга для онлайн-кинотеатра обеспечивает 
процесс формирования подписки, выставления счетов на оплату и снятие с
расчетных картов подписчиков денежных средств в соответствии с выбранным тарифом.

**Технологии:** 
1. В качестве внешнего платежного шлюза используется российский сервис
[CloudPayments](https://cloudpayments.ru/), это позволяет избержать
хранения данных платежных карт непосредственно на сервисе биллинга.
Вместо этого для проведения платежей используются криптограммы и токены, 
генерируемые скриптами CloudPayments на фронт-енде. С целью тестирования и
качественной интеграции создан локальный эмулятор API данного шлюза.
2. В качестве фрейморка для сервиса биллинга использован [Django Rest Framework](https://www.django-rest-framework.org/),
что дает возможность организации прямого доступа через веб-панель для конечных
пользователей с минимальными накладными расходами по созданию веб-интерфейса.
Идемпотентность и горизонтальная масштабируемость сервиса достигается путем
использования воркеров [Celery](https://docs.celeryproject.org/en/stable/) с
[RabbitMQ](https://www.rabbitmq.com/) в качестве брокера и [Redis](https://redis.io/) на
бэкенде. Для хранения применен PostgreSQL. Запуск всех компонентов сервиса
контейнеризован в Docker, http интерфейсы обернуты в Nginx.
3. Для мониторинга очередей воркеров взят [Flower](https://flower.readthedocs.io/en/latest/).
Для логгирования используется [Sentry](https://docs.sentry.io/)
4. Взаимодействие с другими компонентами системы (сервисы аутентификации,
нотификации и фронтендом) осуществляется по протоколу [gRPC](https://grpc.io/).
Также в Django присутствует REST API для отдельных функций.
5. В качестве планировщика регулярных заданий использован Celery Beat.

**Схема компонентов**:
![Alt text](docs/schema.png?raw=true "Schema")

**Диаграмма базы**:
![Alt text](docs/db_uml_diagram.png?raw=true "DB uml")

**Описание процесса оплаты**:
1. В системе биллинга предусмотрено три типа платажей:
- Первичный платеж без дополнительной авторизации по криптограмме;
- Первичный платеж с подтверждением 3D Secure;
- Повторный платеж по платежному токену.


В первом и втором случае на фронтенде скриптом формируется необходимые вводные данные
для проведения платежа, они передаются по протоколу gRPC в сервис биллинга. 

**Диаграмма первичного платежа по криптограмме**:
![Alt text](docs/create_subscription_sequence_diagram.png?raw=true "Create subscription")


В третьем случае платеж проводится с помощью ранее сохраненного платежного токена,
являющегося результатом предыдущего успешного первичного или повторного платежа.


**Диаграмма повторного платежа по платежному токену**:
![Alt text](docs/scheduler_sequence_diagram.png?raw=true "Scheduler")

2. Получив сигнал на осуществление первичного платежа в отношении пользователя
сервис биллинга:
- при отсутствии аккаунта плательщика регистрирует новый;
- формирует Счет на оплату очередного периода согласно тарифа;
- отправляет UUID Счета на оплату в Воркер;

3. Получив UUID Счета на полату Воркер:
- собирает необходимые данные для проведения платежа из хранилища и отправляет сигнал на списание в API платежного шлюза;
- сохраняет результат платежа (успешный или нет) в Транзакцию, включая токен для последующих платежей;
- возвращает UUID транзакции в сервис для управления доступом пользователя и нотификацией;

4. Планировщик выполняет следующие регулярные задачи:
- ежедневное выставление счетов аккаунтам, поделажащим оплате в соответствии с тарифом;
- попытки списания по выставленным, но неоплаченным счетам (повторные транзакции);

**Запуск сервисов**:
1. Запустите сервис эмулятор CloudPayments API:

`cd cloud_gate`

`cp env.sample .env`

`docker-compose up --build -d`

Документация: [http://localhost:81/api/docs](http://localhost:81/api/docs)

2. Запустите сервис биллинга:

`cd ../manager_service`

`cp template.env .env`

`docker-compose up --build -d`

Мониторинг Flower: [http://localhost:5555](http://localhost:5555) (username: user, password: test).

Документация: [http://localhost/swagger/](http://localhost/swagger/)

Панель администратора: [http://localhost/admin](http://localhost/admin) (username: user, password: password)
