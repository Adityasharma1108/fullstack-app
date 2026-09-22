const form = document.getElementById("todo-form");
const input = document.getElementById("task-input");
const list = document.getElementById("todo-list");

async function loadTodos() {
  const res = await fetch("/api/todos");
  const todos = await res.json();
  list.innerHTML = "";
  todos.forEach(renderTodo);
}

function renderTodo(todo) {
  const li = document.createElement("li");
  li.className = todo.done ? "done" : "";

  const checkbox = document.createElement("input");
  checkbox.type = "checkbox";
  checkbox.checked = todo.done;
  checkbox.addEventListener("change", () => toggleTodo(todo.id, checkbox.checked));

  const span = document.createElement("span");
  span.textContent = todo.task;

  const delBtn = document.createElement("button");
  delBtn.textContent = "Delete";
  delBtn.className = "delete-btn";
  delBtn.addEventListener("click", () => deleteTodo(todo.id));

  li.appendChild(checkbox);
  li.appendChild(span);
  li.appendChild(delBtn);
  list.appendChild(li);
}

async function addTodo(task) {
  await fetch("/api/todos", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ task }),
  });
  loadTodos();
}

async function toggleTodo(id, done) {
  await fetch(`/api/todos/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ done }),
  });
  loadTodos();
}

async function deleteTodo(id) {
  await fetch(`/api/todos/${id}`, { method: "DELETE" });
  loadTodos();
}

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const task = input.value.trim();
  if (!task) return;
  addTodo(task);
  input.value = "";
});

loadTodos();