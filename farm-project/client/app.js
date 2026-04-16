const API_URL = 'http://localhost:5000/api';
let currentTab = 'animals';
let editingId = null;
let editingType = null;

// ========== ПЕРЕКЛЮЧЕНИЕ ВКЛАДОК ==========
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        const tabName = this.getAttribute('data-tab');
        switchTab(tabName);
    });
});

function switchTab(tabName) {
    currentTab = tabName;
    
    // Скрыть все вкладки
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Убрать активный класс
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Показать выбранную
    document.getElementById(`${tabName}Tab`).classList.add('active');
    document.querySelector(`.tab-btn[data-tab="${tabName}"]`).classList.add('active');
    
    // Загрузить данные
    loadData(tabName);
}

// ========== ЗАГРУЗКА ДАННЫХ ==========
async function loadData(table) {
    try {
        const response = await fetch(`${API_URL}/${table}`);
        if (!response.ok) throw new Error('Ошибка загрузки');
        const data = await response.json();
        
        const tbody = document.getElementById(`${table}Body`);
        if (!tbody) return;
        
        if (data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="8" class="loading">Нет данных</td></tr>';
            return;
        }
        
        switch(table) {
            case 'animals':
                tbody.innerHTML = data.map(item => `
                    <tr>
                        <td>${item.id}</td>
                        <td>${item.name || '-'}</td>
                        <td>${item.species || '-'}</td>
                        <td>${item.breed || '-'}</td>
                        <td>${item.birth_date || '-'}</td>
                        <td>${item.weight || '-'}</td>
                        <td>${item.pen_id || '-'}</td>
                        <td>
                            <button class="btn btn-edit" onclick="editItem('animals', ${item.id})">✏️</button>
                            <button class="btn btn-delete" onclick="deleteItem('animals', ${item.id})">🗑️</button>
                        </td>
                    </tr>
                `).join('');
                break;
                
            case 'pens':
                tbody.innerHTML = data.map(item => `
                    <tr>
                        <td>${item.id}</td>
                        <td>${item.name || '-'}</td>
                        <td>${item.area || '-'}</td>
                        <td>${item.capacity || '-'}</td>
                        <td>${item.animal_type || '-'}</td>
                        <td>${item.status || '-'}</td>
                        <td>
                            <button class="btn btn-edit" onclick="editItem('pens', ${item.id})">✏️</button>
                            <button class="btn btn-delete" onclick="deleteItem('pens', ${item.id})">🗑️</button>
                        </td>
                    </tr>
                `).join('');
                break;
                
            case 'products':
                tbody.innerHTML = data.map(item => `
                    <tr>
                        <td>${item.id}</td>
                        <td>${item.name || '-'}</td>
                        <td>${item.type || '-'}</td>
                        <td>${item.quantity || '-'}</td>
                        <td>${item.unit || '-'}</td>
                        <td>${item.harvest_date || '-'}</td>
                        <td>${item.price || '-'}</td>
                        <td>
                            <button class="btn btn-edit" onclick="editItem('products', ${item.id})">✏️</button>
                            <button class="btn btn-delete" onclick="deleteItem('products', ${item.id})">🗑️</button>
                        </td>
                    </tr>
                `).join('');
                break;
                
            case 'employees':
                tbody.innerHTML = data.map(item => `
                    <tr>
                        <td>${item.id}</td>
                        <td>${item.full_name || '-'}</td>
                        <td>${item.position || '-'}</td>
                        <td>${item.phone || '-'}</td>
                        <td>${item.hire_date || '-'}</td>
                        <td>${item.salary || '-'}</td>
                        <td>${item.email || '-'}</td>
                        <td>
                            <button class="btn btn-edit" onclick="editItem('employees', ${item.id})">✏️</button>
                            <button class="btn btn-delete" onclick="deleteItem('employees', ${item.id})">🗑️</button>
                        </td>
                    </tr>
                `).join('');
                break;
                
            case 'finances':
                tbody.innerHTML = data.map(item => `
                    <tr>
                        <td>${item.id}</td>
                        <td>${item.operation_type === 'доход' ? '📈 Доход' : '📉 Расход'}</td>
                        <td>${item.amount || 0} ₽</td>
                        <td>${item.category || '-'}</td>
                        <td>${item.description || '-'}</td>
                        <td>${item.operation_date || '-'}</td>
                        <td>${item.payment_method || '-'}</td>
                        <td>
                            <button class="btn btn-edit" onclick="editItem('finances', ${item.id})">✏️</button>
                            <button class="btn btn-delete" onclick="deleteItem('finances', ${item.id})">🗑️</button>
                        </td>
                    </tr>
                `).join('');
                break;
        }
    } catch (error) {
        console.error('Ошибка:', error);
        const tbody = document.getElementById(`${table}Body`);
        if (tbody) {
            tbody.innerHTML = '<tr><td colspan="8" class="loading">Ошибка загрузки. Проверьте сервер</td></tr>';
        }
    }
}

// ========== ПОКАЗАТЬ ФОРМУ ==========
function showAddForm(type) {
    editingId = null;
    editingType = type;
    document.getElementById('modalTitle').innerHTML = `➕ Добавить ${getTypeName(type)}`;
    document.getElementById('formFields').innerHTML = getFormFields(type);
    document.getElementById('modal').style.display = 'block';
}

// ========== РЕДАКТИРОВАНИЕ ==========
async function editItem(type, id) {
    try {
        const response = await fetch(`${API_URL}/${type}/${id}`);
        if (!response.ok) throw new Error('Не найдено');
        const item = await response.json();
        
        editingId = id;
        editingType = type;
        document.getElementById('modalTitle').innerHTML = `✏️ Редактировать ${getTypeName(type)}`;
        document.getElementById('formFields').innerHTML = getFormFields(type, item);
        document.getElementById('modal').style.display = 'block';
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Не удалось загрузить данные для редактирования');
    }
}

// ========== УДАЛЕНИЕ ==========
async function deleteItem(type, id) {
    if (!confirm('Вы уверены, что хотите удалить эту запись?')) return;
    
    try {
        const response = await fetch(`${API_URL}/${type}/${id}`, { method: 'DELETE' });
        if (response.ok) {
            loadData(currentTab);
        } else {
            alert('Ошибка при удалении');
        }
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Ошибка при удалении');
    }
}

// ========== СОХРАНЕНИЕ ==========
document.getElementById('dynamicForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });
    
    const url = editingId ? `${API_URL}/${editingType}/${editingId}` : `${API_URL}/${editingType}`;
    const method = editingId ? 'PUT' : 'POST';
    
    try {
        const response = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            closeModal();
            loadData(currentTab);
        } else {
            const error = await response.json();
            alert('Ошибка: ' + (error.error || 'Неизвестная ошибка'));
        }
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Ошибка при сохранении');
    }
});

// ========== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ==========
function getTypeName(type) {
    const names = {
        animals: 'животное',
        pens: 'загон',
        products: 'продукцию',
        employees: 'сотрудника',
        finances: 'операцию'
    };
    return names[type] || type;
}

function closeModal() {
    document.getElementById('modal').style.display = 'none';
    editingId = null;
    editingType = null;
}

// Закрытие по клику вне окна
window.onclick = function(event) {
    const modal = document.getElementById('modal');
    if (event.target === modal) {
        closeModal();
    }
}

// ========== ГЕНЕРАЦИЯ ПОЛЕЙ ФОРМ ==========
function getFormFields(type, data = {}) {
    switch(type) {
        case 'animals':
            return `
                <div class="form-group"><label>Кличка:</label><input type="text" name="name" value="${data.name || ''}" required></div>
                <div class="form-group"><label>Вид:</label><input type="text" name="species" value="${data.species || ''}" required></div>
                <div class="form-group"><label>Порода:</label><input type="text" name="breed" value="${data.breed || ''}"></div>
                <div class="form-group"><label>Дата рождения:</label><input type="date" name="birth_date" value="${data.birth_date || ''}" required></div>
                <div class="form-group"><label>Вес (кг):</label><input type="number" step="0.1" name="weight" value="${data.weight || ''}"></div>
                <div class="form-group"><label>ID Загона:</label><input type="number" name="pen_id" value="${data.pen_id || ''}"></div>
            `;
        case 'pens':
            return `
                <div class="form-group"><label>Название:</label><input type="text" name="name" value="${data.name || ''}" required></div>
                <div class="form-group"><label>Площадь (м²):</label><input type="number" step="0.1" name="area" value="${data.area || ''}"></div>
                <div class="form-group"><label>Вместимость:</label><input type="number" name="capacity" value="${data.capacity || ''}" required></div>
                <div class="form-group"><label>Тип животных:</label><input type="text" name="animal_type" value="${data.animal_type || ''}"></div>
                <div class="form-group"><label>Статус:</label>
                    <select name="status">
                        <option value="активен" ${data.status === 'активен' ? 'selected' : ''}>Активен</option>
                        <option value="закрыт" ${data.status === 'закрыт' ? 'selected' : ''}>Закрыт</option>
                    </select>
                </div>
            `;
        case 'products':
            return `
                <div class="form-group"><label>Название:</label><input type="text" name="name" value="${data.name || ''}" required></div>
                <div class="form-group"><label>Тип:</label>
                    <select name="type">
                        <option value="молочная" ${data.type === 'молочная' ? 'selected' : ''}>Молочная</option>
                        <option value="мясная" ${data.type === 'мясная' ? 'selected' : ''}>Мясная</option>
                        <option value="яичная" ${data.type === 'яичная' ? 'selected' : ''}>Яичная</option>
                    </select>
                </div>
                <div class="form-group"><label>Количество:</label><input type="number" step="0.1" name="quantity" value="${data.quantity || ''}" required></div>
                <div class="form-group"><label>Единица измерения:</label><input type="text" name="unit" value="${data.unit || ''}" required></div>
                <div class="form-group"><label>Дата сбора:</label><input type="date" name="harvest_date" value="${data.harvest_date || ''}" required></div>
                <div class="form-group"><label>Цена (₽):</label><input type="number" step="0.01" name="price" value="${data.price || ''}"></div>
            `;
        case 'employees':
            return `
                <div class="form-group"><label>ФИО:</label><input type="text" name="full_name" value="${data.full_name || ''}" required></div>
                <div class="form-group"><label>Должность:</label><input type="text" name="position" value="${data.position || ''}" required></div>
                <div class="form-group"><label>Телефон:</label><input type="text" name="phone" value="${data.phone || ''}"></div>
                <div class="form-group"><label>Дата приема:</label><input type="date" name="hire_date" value="${data.hire_date || ''}" required></div>
                <div class="form-group"><label>Зарплата (₽):</label><input type="number" name="salary" value="${data.salary || ''}"></div>
                <div class="form-group"><label>Email:</label><input type="email" name="email" value="${data.email || ''}"></div>
            `;
        case 'finances':
            return `
                <div class="form-group"><label>Тип операции:</label>
                    <select name="operation_type">
                        <option value="доход" ${data.operation_type === 'доход' ? 'selected' : ''}>Доход</option>
                        <option value="расход" ${data.operation_type === 'расход' ? 'selected' : ''}>Расход</option>
                    </select>
                </div>
                <div class="form-group"><label>Сумма (₽):</label><input type="number" step="0.01" name="amount" value="${data.amount || ''}" required></div>
                <div class="form-group"><label>Категория:</label><input type="text" name="category" value="${data.category || ''}" required></div>
                <div class="form-group"><label>Описание:</label><textarea name="description">${data.description || ''}</textarea></div>
                <div class="form-group"><label>Дата операции:</label><input type="date" name="operation_date" value="${data.operation_date || ''}" required></div>
                <div class="form-group"><label>Метод оплаты:</label>
                    <select name="payment_method">
                        <option value="наличные" ${data.payment_method === 'наличные' ? 'selected' : ''}>Наличные</option>
                        <option value="банковский перевод" ${data.payment_method === 'банковский перевод' ? 'selected' : ''}>Банковский перевод</option>
                    </select>
                </div>
            `;
        default:
            return '<div class="form-group">Форма не найдена</div>';
    }
}

// ========== ЗАГРУЗКА ПРИ СТАРТЕ ==========
loadData('animals');