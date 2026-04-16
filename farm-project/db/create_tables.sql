-- Удалить старую базу если есть
DROP DATABASE IF EXISTS farm_db;

-- Создать новую базу
CREATE DATABASE farm_db;

-- Подключиться к ней
\c farm_db;

-- Создать таблицы
CREATE TABLE animals (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    species VARCHAR(50) NOT NULL,
    breed VARCHAR(50),
    birth_date DATE NOT NULL,
    weight DECIMAL(8,2),
    pen_id INTEGER
);

CREATE TABLE pens (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    area DECIMAL(10,2),
    capacity INTEGER NOT NULL,
    animal_type VARCHAR(50),
    status VARCHAR(20) DEFAULT 'активен'
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    quantity DECIMAL(10,2) NOT NULL,
    unit VARCHAR(20) NOT NULL,
    harvest_date DATE NOT NULL,
    price DECIMAL(10,2)
);

CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    position VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    hire_date DATE NOT NULL,
    salary DECIMAL(10,2),
    email VARCHAR(100)
);

CREATE TABLE finances (
    id SERIAL PRIMARY KEY,
    operation_type VARCHAR(20) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    category VARCHAR(50) NOT NULL,
    description TEXT,
    operation_date DATE NOT NULL,
    payment_method VARCHAR(30)
);

-- Добавить тестовые данные
INSERT INTO animals (name, species, breed, birth_date, weight, pen_id) VALUES
('Буренка', 'корова', 'Голштинская', '2020-05-10', 550.5, 1),
('Зорька', 'корова', 'Джерсейская', '2021-06-15', 480.0, 1),
('Ряба', 'курица', 'Леггорн', '2022-01-20', 2.5, 3),
('Черныш', 'курица', 'Кохинхин', '2022-02-10', 3.2, 3),
('Снежок', 'овца', 'Романовская', '2021-08-05', 65.0, 2);

INSERT INTO pens (name, area, capacity, animal_type, status) VALUES
('Северный загон', 1200.5, 50, 'крупный рогатый скот', 'активен'),
('Южный загон', 950.0, 30, 'овцы', 'активен'),
('Птичник', 450.0, 200, 'птица', 'активен'),
('Карантин', 200.0, 10, 'все виды', 'закрыт'),
('Молодняк', 800.0, 40, 'молодые животные', 'активен');

INSERT INTO products (name, type, quantity, unit, harvest_date, price) VALUES
('Молоко пастеризованное', 'молочная', 250.5, 'литров', '2025-03-15', 85.0),
('Яйца куриные', 'яичная', 1500, 'штук', '2025-03-15', 12.0),
('Сыр твердый', 'молочная', 45.0, 'кг', '2025-03-10', 550.0),
('Шерсть овечья', 'шерстяная', 30.0, 'кг', '2025-03-01', 300.0),
('Мясо куриное', 'мясная', 120.0, 'кг', '2025-03-12', 250.0);

INSERT INTO employees (full_name, position, phone, hire_date, salary, email) VALUES
('Иванов Иван Иванович', 'ветеринар', '+7-999-123-4567', '2018-03-10', 55000, 'ivanov@farm.ru'),
('Петрова Мария Сергеевна', 'зоотехник', '+7-999-234-5678', '2019-06-15', 48000, 'petrova@farm.ru'),
('Сидоров Алексей Владимирович', 'фермер', '+7-999-345-6789', '2017-01-20', 45000, 'sidorov@farm.ru'),
('Кузнецова Елена Петровна', 'бухгалтер', '+7-999-456-7890', '2020-03-01', 52000, 'kuznetsova@farm.ru'),
('Михайлов Дмитрий Андреевич', 'рабочий', '+7-999-567-8901', '2021-02-10', 35000, 'mikhailov@farm.ru');

INSERT INTO finances (operation_type, amount, category, description, operation_date, payment_method) VALUES
('доход', 150000, 'продажа молока', 'Реализация молока оптовым покупателям', '2025-03-14', 'банковский перевод'),
('доход', 75000, 'продажа яиц', 'Продажа в розничные магазины', '2025-03-14', 'наличные'),
('расход', 30000, 'корма', 'Закупка комбикорма и сена', '2025-03-12', 'банковский перевод'),
('расход', 15000, 'ветеринария', 'Вакцинация и лечение животных', '2025-03-10', 'наличные'),
('доход', 50000, 'продажа мяса', 'Реализация мяса птицы', '2025-03-13', 'банковский перевод');