import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [todos, setTodos] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // Get backend URL from environment variable
  const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';

  useEffect(() => {
    fetchTodos();
  }, []);

  const fetchTodos = async () => {
    try {
      setIsLoading(true);
      const response = await fetch(`${BACKEND_URL}/todos`);
      const data = await response.json();
      setTodos(data);
    } catch (error) {
      console.error('Error fetching todos:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const addTodo = async (e) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    try {
      const response = await fetch(`${BACKEND_URL}/todos`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          title: inputValue,
          description: '',
          completed: false
        }),
      });

      if (response.ok) {
        const newTodo = await response.json();
        setTodos([...todos, newTodo]);
        setInputValue('');
      }
    } catch (error) {
      console.error('Error adding todo:', error);
    }
  };

  const checkHealth = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/health`);
      const healthData = await response.json();
      alert(`Backend Health: ${healthData.status} - Version: ${healthData.version}`);
    } catch (error) {
      console.error('Error checking health:', error);
      alert('Backend is not reachable');
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>AI Todo Chatbot</h1>

        <button onClick={checkHealth} className="health-btn">
          Check Backend Health
        </button>

        <form onSubmit={addTodo} className="todo-form">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Enter a new todo..."
            className="todo-input"
          />
          <button type="submit" className="add-btn">Add Todo</button>
        </form>

        {isLoading ? (
          <p>Loading todos...</p>
        ) : (
          <ul className="todo-list">
            {todos.map((todo) => (
              <li key={todo.id} className={`todo-item ${todo.completed ? 'completed' : ''}`}>
                <span>{todo.title}</span>
                {todo.description && <small>{todo.description}</small>}
              </li>
            ))}
          </ul>
        )}
      </header>
    </div>
  );
}

export default App;