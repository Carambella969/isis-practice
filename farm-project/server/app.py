from flask import Flask, jsonify, request, abort, send_from_directory
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

# Путь к базе данных SQLite
DB_PATH = os.path.join(os.path.dirname(__file__), 'farm.db')

def get_db():
    """Создает подключение к SQLite"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Инициализация базы данных при первом запуске"""
    conn = get_db()
    cur = conn.cursor()
    
    # Создание таблиц
    cur.execute('''
        CREATE TABLE IF NOT EXISTS animals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            species TEXT NOT NULL,
            breed TEXT,
            birth_date TEXT NOT NULL,
            weight REAL,
            pen_id INTEGER
        )
    ''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS pens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            area REAL,
            capacity INTEGER NOT NULL,
            animal_type TEXT,
            status TEXT DEFAULT 'активен'
        )
    ''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            quantity REAL NOT NULL,
            unit TEXT NOT NULL,
            harvest_date TEXT NOT NULL,
            price REAL
        )
    ''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            position TEXT NOT NULL,
            phone TEXT,
            hire_date TEXT NOT NULL,
            salary REAL,
            email TEXT
        )
    ''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS finances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            operation_type TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            operation_date TEXT NOT NULL,
            payment_method TEXT
        )
    ''')
    
    # Проверка и добавление тестовых данных
    cur.execute("SELECT COUNT(*) as count FROM pens")
    if cur.fetchone()['count'] == 0:
        # Добавляем загоны
        cur.execute("INSERT INTO pens (name, area, capacity, animal_type, status) VALUES (?, ?, ?, ?, ?)", 
                   ('Северный загон', 1200.5, 50, 'крупный рогатый скот', 'активен'))
        cur.execute("INSERT INTO pens (name, area, capacity, animal_type, status) VALUES (?, ?, ?, ?, ?)", 
                   ('Южный загон', 950.0, 30, 'овцы', 'активен'))
        cur.execute("INSERT INTO pens (name, area, capacity, animal_type, status) VALUES (?, ?, ?, ?, ?)", 
                   ('Птичник', 450.0, 200, 'птица', 'активен'))
        
        # Добавляем животных
        cur.execute("INSERT INTO animals (name, species, breed, birth_date, weight, pen_id) VALUES (?, ?, ?, ?, ?, ?)",
                   ('Буренка', 'корова', 'Голштинская', '2020-05-10', 550.5, 1))
        cur.execute("INSERT INTO animals (name, species, breed, birth_date, weight, pen_id) VALUES (?, ?, ?, ?, ?, ?)",
                   ('Зорька', 'корова', 'Джерсейская', '2021-06-15', 480.0, 1))
        cur.execute("INSERT INTO animals (name, species, breed, birth_date, weight, pen_id) VALUES (?, ?, ?, ?, ?, ?)",
                   ('Ряба', 'курица', 'Леггорн', '2022-01-20', 2.5, 3))
        
        # Добавляем продукцию
        cur.execute("INSERT INTO products (name, type, quantity, unit, harvest_date, price) VALUES (?, ?, ?, ?, ?, ?)",
                   ('Молоко пастеризованное', 'молочная', 250.5, 'литров', '2025-03-15', 85.0))
        cur.execute("INSERT INTO products (name, type, quantity, unit, harvest_date, price) VALUES (?, ?, ?, ?, ?, ?)",
                   ('Яйца куриные', 'яичная', 1500, 'штук', '2025-03-15', 12.0))
        cur.execute("INSERT INTO products (name, type, quantity, unit, harvest_date, price) VALUES (?, ?, ?, ?, ?, ?)",
                   ('Сыр твердый', 'молочная', 45.0, 'кг', '2025-03-10', 550.0))
        
        # Добавляем сотрудников
        cur.execute("INSERT INTO employees (full_name, position, phone, hire_date, salary, email) VALUES (?, ?, ?, ?, ?, ?)",
                   ('Иванов Иван Иванович', 'ветеринар', '+7-999-123-4567', '2018-03-10', 55000, 'ivanov@farm.ru'))
        cur.execute("INSERT INTO employees (full_name, position, phone, hire_date, salary, email) VALUES (?, ?, ?, ?, ?, ?)",
                   ('Петрова Мария Сергеевна', 'зоотехник', '+7-999-234-5678', '2019-06-15', 48000, 'petrova@farm.ru'))
        cur.execute("INSERT INTO employees (full_name, position, phone, hire_date, salary, email) VALUES (?, ?, ?, ?, ?, ?)",
                   ('Сидоров Алексей Владимирович', 'фермер', '+7-999-345-6789', '2017-01-20', 45000, 'sidorov@farm.ru'))
        
        # Добавляем финансы
        cur.execute("INSERT INTO finances (operation_type, amount, category, description, operation_date, payment_method) VALUES (?, ?, ?, ?, ?, ?)",
                   ('доход', 150000, 'продажа молока', 'Реализация молока оптовым покупателям', '2025-03-14', 'банковский перевод'))
        cur.execute("INSERT INTO finances (operation_type, amount, category, description, operation_date, payment_method) VALUES (?, ?, ?, ?, ?, ?)",
                   ('расход', 30000, 'корма', 'Закупка комбикорма и сена', '2025-03-12', 'наличные'))
        cur.execute("INSERT INTO finances (operation_type, amount, category, description, operation_date, payment_method) VALUES (?, ?, ?, ?, ?, ?)",
                   ('доход', 50000, 'продажа мяса', 'Реализация мяса птицы', '2025-03-13', 'банковский перевод'))
    
    conn.commit()
    conn.close()
    print("✅ База данных инициализирована")

# ========== ОТДАЧА HTML СТРАНИЦ ==========
@app.route('/')
def index():
    return send_from_directory('../client', 'index.html')

@app.route('/app.js')
def js():
    return send_from_directory('../client', 'app.js')

@app.route('/style.css')
def css():
    return send_from_directory('../client', 'style.css')

# ========== API: ЖИВОТНЫЕ ==========
@app.route('/api/animals', methods=['GET'])
def get_animals():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM animals ORDER BY id")
    animals = [dict(row) for row in cur.fetchall()]
    conn.close()
    return jsonify(animals)

@app.route('/api/animals/<int:animal_id>', methods=['GET'])
def get_animal(animal_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM animals WHERE id = ?", (animal_id,))
    animal = cur.fetchone()
    conn.close()
    if not animal:
        abort(404, 'Животное не найдено')
    return jsonify(dict(animal))

@app.route('/api/animals', methods=['POST'])
def create_animal():
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO animals (name, species, breed, birth_date, weight, pen_id)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (data.get('name'), data.get('species'), data.get('breed'),
          data.get('birth_date'), data.get('weight'), data.get('pen_id')))
    conn.commit()
    animal_id = cur.lastrowid
    cur.execute("SELECT * FROM animals WHERE id = ?", (animal_id,))
    new_animal = dict(cur.fetchone())
    conn.close()
    return jsonify(new_animal), 201

@app.route('/api/animals/<int:animal_id>', methods=['PUT'])
def update_animal(animal_id):
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        UPDATE animals 
        SET name=?, species=?, breed=?, birth_date=?, weight=?, pen_id=?
        WHERE id=?
    """, (data.get('name'), data.get('species'), data.get('breed'),
          data.get('birth_date'), data.get('weight'), data.get('pen_id'), animal_id))
    conn.commit()
    cur.execute("SELECT * FROM animals WHERE id = ?", (animal_id,))
    updated = cur.fetchone()
    conn.close()
    if not updated:
        abort(404, 'Животное не найдено')
    return jsonify(dict(updated))

@app.route('/api/animals/<int:animal_id>', methods=['DELETE'])
def delete_animal(animal_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM animals WHERE id = ?", (animal_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Удалено', 'id': animal_id})

# ========== API: ЗАГОНЫ ==========
@app.route('/api/pens', methods=['GET'])
def get_pens():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM pens ORDER BY id")
    pens = [dict(row) for row in cur.fetchall()]
    conn.close()
    return jsonify(pens)

@app.route('/api/pens/<int:pen_id>', methods=['GET'])
def get_pen(pen_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM pens WHERE id = ?", (pen_id,))
    pen = cur.fetchone()
    conn.close()
    if not pen:
        abort(404, 'Загон не найден')
    return jsonify(dict(pen))

@app.route('/api/pens', methods=['POST'])
def create_pen():
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO pens (name, area, capacity, animal_type, status)
        VALUES (?, ?, ?, ?, ?)
    """, (data.get('name'), data.get('area'), data.get('capacity'),
          data.get('animal_type'), data.get('status')))
    conn.commit()
    pen_id = cur.lastrowid
    cur.execute("SELECT * FROM pens WHERE id = ?", (pen_id,))
    new_pen = dict(cur.fetchone())
    conn.close()
    return jsonify(new_pen), 201

@app.route('/api/pens/<int:pen_id>', methods=['PUT'])
def update_pen(pen_id):
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        UPDATE pens 
        SET name=?, area=?, capacity=?, animal_type=?, status=?
        WHERE id=?
    """, (data.get('name'), data.get('area'), data.get('capacity'),
          data.get('animal_type'), data.get('status'), pen_id))
    conn.commit()
    cur.execute("SELECT * FROM pens WHERE id = ?", (pen_id,))
    updated = cur.fetchone()
    conn.close()
    if not updated:
        abort(404, 'Загон не найден')
    return jsonify(dict(updated))

@app.route('/api/pens/<int:pen_id>', methods=['DELETE'])
def delete_pen(pen_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM pens WHERE id = ?", (pen_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Удалено', 'id': pen_id})

# ========== API: ПРОДУКЦИЯ ==========
@app.route('/api/products', methods=['GET'])
def get_products():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products ORDER BY id")
    products = [dict(row) for row in cur.fetchall()]
    conn.close()
    return jsonify(products)

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    product = cur.fetchone()
    conn.close()
    if not product:
        abort(404, 'Продукт не найден')
    return jsonify(dict(product))

@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO products (name, type, quantity, unit, harvest_date, price)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (data.get('name'), data.get('type'), data.get('quantity'),
          data.get('unit'), data.get('harvest_date'), data.get('price')))
    conn.commit()
    product_id = cur.lastrowid
    cur.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    new_product = dict(cur.fetchone())
    conn.close()
    return jsonify(new_product), 201

@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        UPDATE products 
        SET name=?, type=?, quantity=?, unit=?, harvest_date=?, price=?
        WHERE id=?
    """, (data.get('name'), data.get('type'), data.get('quantity'),
          data.get('unit'), data.get('harvest_date'), data.get('price'), product_id))
    conn.commit()
    cur.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    updated = cur.fetchone()
    conn.close()
    if not updated:
        abort(404, 'Продукт не найден')
    return jsonify(dict(updated))

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Удалено', 'id': product_id})

# ========== API: СОТРУДНИКИ ==========
@app.route('/api/employees', methods=['GET'])
def get_employees():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM employees ORDER BY id")
    employees = [dict(row) for row in cur.fetchall()]
    conn.close()
    return jsonify(employees)

@app.route('/api/employees/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM employees WHERE id = ?", (employee_id,))
    employee = cur.fetchone()
    conn.close()
    if not employee:
        abort(404, 'Сотрудник не найден')
    return jsonify(dict(employee))

@app.route('/api/employees', methods=['POST'])
def create_employee():
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO employees (full_name, position, phone, hire_date, salary, email)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (data.get('full_name'), data.get('position'), data.get('phone'),
          data.get('hire_date'), data.get('salary'), data.get('email')))
    conn.commit()
    employee_id = cur.lastrowid
    cur.execute("SELECT * FROM employees WHERE id = ?", (employee_id,))
    new_employee = dict(cur.fetchone())
    conn.close()
    return jsonify(new_employee), 201

@app.route('/api/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        UPDATE employees 
        SET full_name=?, position=?, phone=?, hire_date=?, salary=?, email=?
        WHERE id=?
    """, (data.get('full_name'), data.get('position'), data.get('phone'),
          data.get('hire_date'), data.get('salary'), data.get('email'), employee_id))
    conn.commit()
    cur.execute("SELECT * FROM employees WHERE id = ?", (employee_id,))
    updated = cur.fetchone()
    conn.close()
    if not updated:
        abort(404, 'Сотрудник не найден')
    return jsonify(dict(updated))

@app.route('/api/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM employees WHERE id = ?", (employee_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Удалено', 'id': employee_id})

# ========== API: ФИНАНСЫ ==========
@app.route('/api/finances', methods=['GET'])
def get_finances():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM finances ORDER BY operation_date DESC")
    finances = [dict(row) for row in cur.fetchall()]
    conn.close()
    return jsonify(finances)

@app.route('/api/finances/<int:finance_id>', methods=['GET'])
def get_finance(finance_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM finances WHERE id = ?", (finance_id,))
    finance = cur.fetchone()
    conn.close()
    if not finance:
        abort(404, 'Операция не найдена')
    return jsonify(dict(finance))

@app.route('/api/finances', methods=['POST'])
def create_finance():
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO finances (operation_type, amount, category, description, operation_date, payment_method)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (data.get('operation_type'), data.get('amount'), data.get('category'),
          data.get('description'), data.get('operation_date'), data.get('payment_method')))
    conn.commit()
    finance_id = cur.lastrowid
    cur.execute("SELECT * FROM finances WHERE id = ?", (finance_id,))
    new_finance = dict(cur.fetchone())
    conn.close()
    return jsonify(new_finance), 201

@app.route('/api/finances/<int:finance_id>', methods=['PUT'])
def update_finance(finance_id):
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        UPDATE finances 
        SET operation_type=?, amount=?, category=?, description=?, operation_date=?, payment_method=?
        WHERE id=?
    """, (data.get('operation_type'), data.get('amount'), data.get('category'),
          data.get('description'), data.get('operation_date'), data.get('payment_method'), finance_id))
    conn.commit()
    cur.execute("SELECT * FROM finances WHERE id = ?", (finance_id,))
    updated = cur.fetchone()
    conn.close()
    if not updated:
        abort(404, 'Операция не найдена')
    return jsonify(dict(updated))

@app.route('/api/finances/<int:finance_id>', methods=['DELETE'])
def delete_finance(finance_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM finances WHERE id = ?", (finance_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Удалено', 'id': finance_id})

# ========== ОБРАБОТКА ОШИБОК ==========
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': str(error.description)}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': str(error.description)}), 400

# ========== ЗАПУСК ==========
if __name__ == '__main__':
    # Удаляем старую БД для пересоздания (опционально)
    # if os.path.exists(DB_PATH):
    #     os.remove(DB_PATH)
    
    init_db()
    print("=" * 50)
    print("🚀 Фермерское хозяйство - сервер запущен!")
    print("📱 Откройте в браузере: http://localhost:5000")
    print("💾 Используется SQLite (не требует PostgreSQL)")
    print("=" * 50)
    app.run(debug=True, port=5000)