-- seed_data.sql для фермерского хозяйства

INSERT INTO pens (name, capacity) VALUES
('Северный загон', 50),
('Южный загон', 30),
('Птичник', 200);

INSERT INTO animals (name, species, birth_date, pen_id) VALUES
('Буренка', 'корова', '2020-05-10', 1),
('Зорька', 'корова', '2021-06-15', 1),
('Ряба', 'курица', '2022-01-20', 3),
('Черныш', 'курица', '2022-02-10', 3);

INSERT INTO products (type, quantity, date, animal_id) VALUES
('молоко', 25.5, '2025-03-10', 1),
('молоко', 22.0, '2025-03-11', 1),
('яйца', 120, '2025-03-10', 3),
('яйца', 115, '2025-03-11', 3);

INSERT INTO checkups (animal_id, vet_name, diagnosis, checkup_date) VALUES
(1, 'Иванов А.А.', 'здорова', '2025-02-01'),
(3, 'Петров Б.В.', 'авитаминоз', '2025-02-10');

INSERT INTO finances (type, amount, category, date) VALUES
('доход', 15000, 'продажа молока', '2025-03-10'),
('расход', 5000, 'корма', '2025-03-09');