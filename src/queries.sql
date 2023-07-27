--Получаем компаний и количество вакансий в каждой из них.

SELECT companies.title, COUNT(vacancies.vacancy_id) as vacancies_count
FROM companies
JOIN vacancies USING(company_id)
GROUP BY companies.title;

-- Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.

SELECT companies.company_title, vacancies.vacancy_title, vacancies.salary, vacancies.url
FROM companies
JOIN vacancies USING(company_id)
ORDER BY vacancies.salary DESC;

--Получает среднюю зарплату по вакансиям.

SELECT ROUND(AVG(vacancies.salary)) AS average_salary
FROM vacancies;

--Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.

SELECT vacancies.* FROM vacancies
WHERE vacancies.salary > (SELECT ROUND(AVG(vacancies.salary)) FROM vacancies)
ORDER BY vacancies.salary DESC;

--Получает список всех вакансий, в названии которых содержатся переданные в метод слова.

SELECT *
FROM vacancies
WHERE lower(vacancy_title) LIKE '%менеджер%'
OR lower(vacancy_title) LIKE '%менеджер'
OR lower(vacancy_title) LIKE 'менеджер%';