# R4C - Robots for consumers

## Содержание
- [Описание предметной области](#небольшая-предыстория)
- [Цель продукта](#что-делает-данный-код)
- [Запуск](#запуск-проекта)
- [Реализация](#реализация)
- [Итоги](#как-с-этим-поработала)


## Небольшая предыстория.
Давным-давно, в далёкой-далёкой галактике, была компания производящая различных 
роботов. 

Каждый робот(**Robot**) имел определенную модель выраженную двух-символьной 
последовательностью(например R2). Одновременно с этим, модель имела различные 
версии(например D2). Напоминает популярный телефон различных моделей(11,12,13...) и его версии
(X,XS,Pro...). Вне компании роботов чаще всего называли по серийному номеру, объединяя модель и версию(например R2-D2).

Также у компании были покупатели(**Customer**) которые периодически заказывали того или иного робота. 

Когда роботов не было в наличии - заказы покупателей(**Order**) попадали в список ожидания.

---
## Что делает данный код
Сервис нацелен на удовлетворение потребностей трёх категорий пользователей:
- Технические специалисты компании. Они будут присылать информацию
- Менеджмент компании. Они будут запрашивать информацию
- Клиенты. Им будут отправляться информация


## Запуск проекта
Для запуска проекта выполните последовательно команды:  

```bash
git clone git@github.com:belyashnikovatn/R4C.git 
```

```bash
python -m venv venv   
. venv/Scripts/activate  
python -m pip install --upgrade pip  
pip install -r requirements.txt   
python manage.py migrate   
python manage.py loaddata r4c.json  # для предзаполнения базы
python manage.py runserver   
```

Перейдите по ссылке:  
http://127.0.0.1:8000/api/v1/

# Реализация
## Приложение api

### Эндпоинты
Для urls использовался routers.DefaultRouter(). Доступные эндпоинты:
- http://127.0.0.1:8000/api/v1/robots/  - роботы: CRUD-операции
- http://127.0.0.1:8000/api/v1/robots/download_summary - скачать Excel-файл со сводкой по суммарным показателям производства роботов за последнюю неделю. Период определяется в константе.  
- http://127.0.0.1:8000/api/v1/customers/ - клиенты: CRUD-операции 
- http://127.0.0.1:8000/api/v1/orders/ - заказы: CRUD-операции 

### Уровень данных
- использовались предоставленные модели, изменения не вносились

### Уровень сериализации 
Реализована валидация для каждой модели:  
- Наличие обязательных полей, индивидуальные проверки полей  
- Разные сериализаторы для разных методов (get / post)  


### Уровень представления 
- Использовались ModelViewSet для обеспечения всех CRUD-операций  
- Для экстра-действия (отчёт по роботам) использовался @action и дополнительные функции  
- Для отправки писем использовался django.db.models.signals и EmailMessage. Шаблон письма находится в templates/new_robot.html. Созданные письма можно найти в папке sent_emails

## Используемые сторонние библиотеки
- pandas и xlsxwriter для создания отчёта по созданным за неделю роботам

## Дополнительно
- документация к коду в классах и функциях
- каждая задача в своей ветке и в PR
___

## Как с этим поработала
- [x] Создать для этого проекта репозиторий на GitHub
- [x] Открыть данный проект в редакторе/среде разработки которую вы используете
- [x] Ознакомиться с задачами в файле tasks.md
- [x] Написать понятный и поддерживаемый код для каждой задачи 
- [x] Сделать по 1 отдельному PR с решением для каждой задачи
- [x] Прислать ссылку на своё решение
