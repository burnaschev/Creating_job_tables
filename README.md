Проект для парсинга вакансий с платформы Head Hunter, и заполнения таблиц данными.


ERD диаграмма для базы данных

[ ![2023-07-27_23-42-02.png](..%2F..%2FDownloads%2F2023-07-27_23-42-02.png)](https://drive.google.com/file/d/1IHnTDrOw8YXOhgBjpkGY53-S5ip59jy_/view?usp=drive_link)





База данных состоит из двух таблиц:

Таблица companies:
- company_id 
- company_title

Таблица vacancies:
- vacancy_id
- company_id
- vacancy_title
- salary
- url

Класс для работы с базой данных и вывода информаций с таблиц.
-DBManager.py

Функций для получения информаций о компаниях, создания базы данных, и заполнения таблиц данными.
-utils.py



Необходимые зависимости для проекта:

1. Requests
2. Psycopg2




