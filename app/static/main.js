// API URL for the to-do list
const API_URL = '/todos';

let currentPage = 1;
let perPage = 5; // Number of todos per page
let currentFilter = 'all';

document.addEventListener('DOMContentLoaded', () => {
    fetchTodos();
});

function setFilter(filter) {
    currentFilter = filter;
    currentPage = 1; // Reset to first page on filter change
    fetchTodos();
}

async function fetchTodos() {
    const res = await fetch(`${API_URL}?page=${currentPage}&per_page=${perPage}&status=${currentFilter}`);
    const data = await res.json();
    const list = document.getElementById('todo-list');
    list.innerHTML = '';

    data.todos
    .filter(todo => {
    if (currentFilter === 'done') return todo.done;
    if (currentFilter === 'undone') return !todo.done;
    return true; // 'all' filter
    })
    .sort((a, b) => a.done - b.done || a.task.localeCompare(b.task)) // Sort by done status and then by task name
    .forEach(todo => {
    const li = document.createElement('li');
    li.className = 'list-group-item';
    li.innerHTML = `
        <div class="d-flex justify-content-between align-items-start">
        <div class="form-check">
            <input class="form-check-input me-2" type="checkbox" ${todo.done ? 'checked' : ''} onchange="toggleDone(${todo.id}, this.checked)">
            <label class="form-check-label ${todo.done ? 'text-decoration-line-through text-muted' : ''}">
            <strong>${todo.task}</strong>
            <div class="text-muted small">
                ${todo.due_date ? `🗓️ ${new Date(todo.due_date).toLocaleString()}` : ''}
                ${todo.tags ? `🏷️ ${todo.tags}` : ''}
                ${todo.priority ? `⭐ ${['High', 'Medium', 'Low'][todo.priority - 1]}` : ''}
            </div>
            </label>
        </div>
        <div>
            <button class="btn btn-sm btn-secondary me-1" onclick="updateTodo(${todo.id}, '${todo.task.replace(/'/g, "\\'")}')">
            <i class="bi bi-pencil-square"></i>
            </button>
            <button class="btn btn-sm btn-danger" onclick="deleteTodo(${todo.id})">
            <i class="bi bi-trash"></i>
            </button>
        </div>
        </div>
    `;
    list.appendChild(li);
    });
    renderPagination(data.page, data.pages, data.has_prev, data.has_next);
}

function renderPagination(page, totalPages, hasPrev, hasNext) {
    const pagination = document.getElementById('pagination');
    pagination.innerHTML = '';

    const createPageItem = (label, newPage, disabled = false) => {
    const li = document.createElement('li');
    li.className = `page-item ${disabled ? 'disabled' : ''}`;
    li.innerHTML = `<button class="page-link">${label}</button>`;
    li.querySelector('button').onclick = () => {
        currentPage = newPage;
        fetchTodos();
    };
    return li;
    };

    if (hasPrev) pagination.appendChild(createPageItem('« Previous', page - 1));
    for (let i = 1; i <= totalPages; i++) {
    const li = createPageItem(i, i, false);
    if (i === page) li.classList.add('active');
    pagination.appendChild(li);
    }
    if (hasNext) pagination.appendChild(createPageItem('Next »', page + 1));
}

async function addTodo() {
    const task = document.getElementById('new-task').value.trim();
    const dueDate = document.getElementById('due-date').value;
    const tags = document.getElementById('tags').value.trim();
    const priority = document.getElementById('priority').value;

    if (!task) return;

    await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        task,
        due_date: dueDate || null,
        tags,
        priority
    })
    });

    // Clear form
    document.getElementById('new-task').value = '';
    document.getElementById('due-date').value = '';
    document.getElementById('tags').value = '';
    document.getElementById('priority').value = '2';

    fetchTodos();
}


async function deleteTodo(id) {
    await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
    fetchTodos();
}

async function updateTodo(id, currentTask) {
const newTask = prompt("Update task:", currentTask);
if (newTask === null || newTask.trim() === '') return;

await fetch(`${API_URL}/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ task: newTask })
});

fetchTodos();
}

async function toggleDone(id, isDone) {
    await fetch(`${API_URL}/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ done: isDone })
    });
    fetchTodos();
}

fetchTodos(); // Load todos on page load