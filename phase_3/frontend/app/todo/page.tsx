'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

interface TodoItem {
  id: number;
  title: string;
  description: string;
  completed: boolean;
  priority: 'low' | 'medium' | 'high';
  category: string | null;
  due_date: string | null;
  recurring: string | null;
  owner_id: number;
  created_at: string;
  updated_at: string;
}

interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
}

// Extend the window interface to include Notification API
declare global {
  interface Window {
    Notification: typeof Notification;
  }
}

// Helper function to highlight search terms in text
const highlightText = (text: string, searchTerm: string) => {
  if (!searchTerm.trim()) return <span>{text}</span>;

  const regex = new RegExp(`(${searchTerm})`, 'gi');
  const parts = text.split(regex);

  return (
    <>
      {parts.map((part, index) =>
        regex.test(part) ? (
          <mark key={index} className="bg-yellow-200 text-gray-900 dark:bg-yellow-500 dark:text-gray-900">
            {part}
          </mark>
        ) : (
          <span key={index}>{part}</span>
        )
      )}
    </>
  );
};

export default function TodoPage() {
  const [todos, setTodos] = useState<TodoItem[]>([]);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [priority, setPriority] = useState<'low' | 'medium' | 'high'>('medium');
  const [category, setCategory] = useState('');
  const [dueDate, setDueDate] = useState<string>('');
  const [recurring, setRecurring] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editTitle, setEditTitle] = useState('');
  const [editDescription, setEditDescription] = useState('');
  const [editPriority, setEditPriority] = useState<'low' | 'medium' | 'high'>('medium');
  const [editCategory, setEditCategory] = useState('');
  const [editDueDate, setEditDueDate] = useState<string>('');
  const [editRecurring, setEditRecurring] = useState<string>('');
  const [searchTerm, setSearchTerm] = useState('');
  const [filterCompleted, setFilterCompleted] = useState<string>('all');
  const [filterPriority, setFilterPriority] = useState<string>('all');
  const [filterCategory, setFilterCategory] = useState<string>('all');
  const [sortBy, setSortBy] = useState<string>('created_at');
  const [sortOrder, setSortOrder] = useState<string>('desc');
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const router = useRouter();

  const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

  // Check for existing token and user on mount
  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      router.push('/');
      return;
    }

    fetchCurrentUser(token);
  }, [router]);

  // Handle recurring tasks and reminders
  useEffect(() => {
    const checkReminders = () => {
      todos.forEach(todo => {
        if (todo.due_date && !todo.completed) {
          const dueDate = new Date(todo.due_date);
          const now = new Date();
          const timeDiff = dueDate.getTime() - now.getTime();
          const minutesDiff = Math.floor(timeDiff / (1000 * 60));

          if (minutesDiff >= 0 && minutesDiff <= 5) {
            const notificationKey = `reminder_${todo.id}_${dueDate.getTime()}`;
            if (!localStorage.getItem(notificationKey)) {
              if (typeof window !== 'undefined' && 'Notification' in window) {
                if (Notification.permission === 'granted') {
                  new Notification(`Todo Reminder: ${todo.title}`, {
                    body: `Task "${todo.title}" is due now!`,
                    icon: '/favicon.ico',
                  });
                  localStorage.setItem(notificationKey, 'shown');
                } else if (Notification.permission !== 'denied') {
                  Notification.requestPermission().then(permission => {
                    if (permission === 'granted') {
                      new Notification(`Todo Reminder: ${todo.title}`, {
                        body: `Task "${todo.title}" is due now!`,
                        icon: '/favicon.ico',
                      });
                      localStorage.setItem(notificationKey, 'shown');
                    }
                  });
                }
              } else {
                alert(`Reminder: Task "${todo.title}" is due now!`);
              }
            }
          }
        }
      });
    };

    const processRecurringTasks = () => {
      todos.forEach(todo => {
        if (todo.recurring && todo.completed && todo.due_date) {
          const lastCompleted = new Date(todo.updated_at);
          const now = new Date();
          let shouldCreateNew = false;
          let nextDueDate: Date | null = null;

          switch (todo.recurring) {
            case 'daily':
              const nextDaily = new Date(lastCompleted);
              nextDaily.setDate(nextDaily.getDate() + 1);
              if (now >= nextDaily) {
                shouldCreateNew = true;
                nextDueDate = new Date(now);
                nextDueDate.setDate(nextDueDate.getDate() + 1);
              }
              break;
            case 'weekly':
              const nextWeekly = new Date(lastCompleted);
              nextWeekly.setDate(nextWeekly.getDate() + 7);
              if (now >= nextWeekly) {
                shouldCreateNew = true;
                nextDueDate = new Date(now);
                nextDueDate.setDate(nextDueDate.getDate() + 7);
              }
              break;
            case 'monthly':
              const nextMonthly = new Date(lastCompleted);
              nextMonthly.setMonth(nextMonthly.getMonth() + 1);
              if (now >= nextMonthly) {
                shouldCreateNew = true;
                nextDueDate = new Date(now);
                nextDueDate.setMonth(nextDueDate.getMonth() + 1);
              }
              break;
            case 'yearly':
              const nextYearly = new Date(lastCompleted);
              nextYearly.setFullYear(nextYearly.getFullYear() + 1);
              if (now >= nextYearly) {
                shouldCreateNew = true;
                nextDueDate = new Date(now);
                nextYearly.setFullYear(nextYearly.getFullYear() + 1);
              }
              break;
          }

          if (shouldCreateNew) {
            const newTask = {
              title: todo.title,
              description: todo.description,
              priority: todo.priority,
              category: todo.category,
              due_date: nextDueDate ? nextDueDate.toISOString() : null,
              recurring: todo.recurring,
              completed: false,
            };

            const token = localStorage.getItem('access_token');
            if (token) {
              fetch(`${API_BASE_URL}/items/`, {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                  'Authorization': `Bearer ${token}`,
                },
                body: JSON.stringify(newTask),
              }).then(response => {
                if (response.ok) {
                  fetchTodos(token);
                }
              });
            }
          }
        }
      });
    };

    const interval = setInterval(() => {
      checkReminders();
      processRecurringTasks();
    }, 60000);

    checkReminders();
    processRecurringTasks();

    return () => clearInterval(interval);
  }, [todos, API_BASE_URL]);

  // Fetch current user
  const fetchCurrentUser = async (token: string) => {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/me`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      if (response.ok) {
        const user = await response.json();
        setCurrentUser(user);

        // Store user ID in localStorage for chat functionality
        localStorage.setItem('user_id', user.id.toString());

        fetchTodos(token);
      } else {
        localStorage.removeItem('access_token');
        router.push('/');
      }
    } catch (err) {
      console.error('Error fetching user:', err);
      localStorage.removeItem('access_token');
      router.push('/');
    }
  };

  // Fetch todos
  const fetchTodos = async (token: string) => {
    try {
      setLoading(true);
      const params = new URLSearchParams();
      params.append('skip', '0');
      params.append('limit', '100');

      if (searchTerm) params.append('search', searchTerm);
      if (filterCompleted !== 'all') {
        params.append('completed', filterCompleted === 'completed' ? 'true' : 'false');
      }
      if (filterPriority !== 'all') params.append('priority', filterPriority);
      if (filterCategory !== 'all') params.append('category', filterCategory);
      params.append('sort_by', sortBy);
      params.append('sort_order', sortOrder);

      const response = await fetch(`${API_BASE_URL}/items/?${params.toString()}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      if (response.ok) {
        const data = await response.json();
        setTodos(data);
      } else {
        setError('Failed to fetch todos');
      }
    } catch (err) {
      setError('Error fetching todos');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // Logout
  const handleLogout = () => {
    localStorage.removeItem('access_token');
    setCurrentUser(null);
    setTodos([]);
    router.push('/');
  };

  // Create new todo
  const handleCreateTodo = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!title.trim()) {
      setError('Title is required');
      return;
    }

    const token = localStorage.getItem('access_token');
    if (!token) {
      setError('Not authenticated');
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/items/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          title,
          description,
          priority,
          category: category || null,
          due_date: dueDate || null,
          recurring: recurring || null,
        }),
      });

      if (response.ok) {
        const newTodo = await response.json();
        setTodos([newTodo, ...todos]);
        setTitle('');
        setDescription('');
        setPriority('medium');
        setCategory('');
        setDueDate('');
        setRecurring('');
        setError(null);

        // Send creation notification to chat
        await sendTodoUpdateToChat(`I've added a new todo: "${title}". Description: "${description || 'No description'}".`);
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to create todo');
      }
    } catch (err) {
      setError('Error creating todo');
      console.error(err);
    }
  };

  // Send a message to the chat to indicate the todo update
  const sendTodoUpdateToChat = async (message: string) => {
    try {
      // Get user ID from localStorage (same as used in chat)
      const storedUserId = localStorage.getItem('user_id');
      if (!storedUserId) {
        console.error('User ID not found in localStorage');
        return;
      }

      const chatMessage = {
        message: message
      };

      // Use the correct API endpoint for chat - should be /api/{user_id}/chat
      const baseUrl = API_BASE_URL.replace('/api/v1', '');
      const chatApiUrl = `${baseUrl}/api/${storedUserId}/chat`;
      const response = await fetch(chatApiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(chatMessage),
      });

      if (!response.ok) {
        console.error('Failed to send update to chat:', await response.text());
      }
    } catch (err) {
      console.error('Error sending update to chat:', err);
    }
  };

  // Update todo
  const handleUpdateTodo = async (id: number) => {
    if (!editTitle.trim()) {
      setError('Title is required');
      return;
    }

    const token = localStorage.getItem('access_token');
    if (!token) {
      setError('Not authenticated');
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/items/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          title: editTitle,
          description: editDescription,
          priority: editPriority,
          category: editCategory || null,
          due_date: editDueDate || null,
          recurring: editRecurring || null,
        }),
      });

      if (response.ok) {
        const updatedTodo = await response.json();
        setTodos(todos.map(todo =>
          todo.id === id ? updatedTodo : todo
        ));
        setEditingId(null);
        setError(null);

        // Send update notification to chat
        await sendTodoUpdateToChat(`I've updated the todo: "${editTitle}". Description: "${editDescription || 'No description'}".`);
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to update todo');
      }
    } catch (err) {
      setError('Error updating todo');
      console.error(err);
    }
  };

  // Delete todo
  const handleDeleteTodo = async (id: number) => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      setError('Not authenticated');
      return;
    }

    // Find the todo being deleted to get its title
    const deletedTodo = todos.find(todo => todo.id === id);

    try {
      const response = await fetch(`${API_BASE_URL}/items/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        setTodos(todos.filter(todo => todo.id !== id));
        setError(null);

        // Send delete notification to chat
        if (deletedTodo) {
          await sendTodoUpdateToChat(`I've deleted the todo: "${deletedTodo.title}".`);
        }
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to delete todo');
      }
    } catch (err) {
      setError('Error deleting todo');
      console.error(err);
    }
  };

  // Start editing
  const startEditing = (todo: TodoItem) => {
    setEditingId(todo.id);
    setEditTitle(todo.title);
    setEditDescription(todo.description);
  };

  // Toggle todo completion status
  const toggleTodoCompletion = async (id: number) => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      setError('Not authenticated');
      return;
    }

    // Find the todo being toggled to get its title
    const todoToToggle = todos.find(todo => todo.id === id);

    try {
      const response = await fetch(`${API_BASE_URL}/items/${id}/toggle-completed`, {
        method: 'PATCH',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const updatedTodo = await response.json();
        setTodos(todos.map(todo =>
          todo.id === id ? updatedTodo : todo
        ));
        setError(null);

        // Send completion status update to chat
        if (todoToToggle) {
          const status = updatedTodo.completed ? 'completed' : 'marked as pending';
          await sendTodoUpdateToChat(`I've ${status} the todo: "${todoToToggle.title}".`);
        }
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to update todo status');
      }
    } catch (err) {
      setError('Error updating todo status');
      console.error(err);
    }
  };

  // Cancel editing
  const cancelEditing = () => {
    setEditingId(null);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
          <p className="mt-4 text-lg text-gray-600 dark:text-gray-300">Loading your todos...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        {/* User Info and Logout */}
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8 space-y-4 sm:space-y-0">
          <div>
            <h1 className="text-3xl sm:text-4xl font-bold text-gray-900 dark:text-white flex items-center">
              <svg className="h-8 w-8 mr-3 text-blue-600 dark:text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
              Todo App
            </h1>
            {currentUser && (
              <p className="text-gray-600 dark:text-gray-300 mt-2 text-sm sm:text-base">
                Welcome back, <span className="font-semibold">{currentUser.first_name || currentUser.username}</span>!
              </p>
            )}
          </div>
          <button
            onClick={handleLogout}
            className="flex items-center px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 transition duration-200"
          >
            <svg className="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
            Logout
          </button>
        </div>

        {error && (
          <div className="mb-6 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg">
            {error}
          </div>
        )}

        {/* Add Todo Form */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6 mb-8">
          <h2 className="text-xl sm:text-2xl font-semibold text-gray-800 dark:text-white mb-4 flex items-center">
            <svg className="h-6 w-6 mr-2 text-blue-600 dark:text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            {editingId ? 'Edit Todo' : 'Add New Todo'}
          </h2>
          <form onSubmit={editingId ? (e) => { e.preventDefault(); handleUpdateTodo(editingId); } : handleCreateTodo}>
            <div className="mb-4">
              <label htmlFor="title" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Title *
              </label>
              <input
                type="text"
                id="title"
                value={editingId ? editTitle : title}
                onChange={(e) =>
                  editingId
                    ? setEditTitle(e.target.value)
                    : setTitle(e.target.value)
                }
                className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white transition duration-200"
                placeholder="Enter todo title"
                autoFocus={!editingId}
              />
            </div>
            <div className="mb-6">
              <label htmlFor="description" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Description
              </label>
              <textarea
                id="description"
                value={editingId ? editDescription : description}
                onChange={(e) =>
                  editingId
                    ? setEditDescription(e.target.value)
                    : setDescription(e.target.value)
                }
                rows={3}
                className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white transition duration-200"
                placeholder="Enter todo description (optional)"
              ></textarea>
            </div>

            {/* Priority, Category, Due Date, and Recurring fields */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
              <div>
                <label htmlFor="priority" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Priority
                </label>
                <select
                  id="priority"
                  value={editingId ? editPriority : priority}
                  onChange={(e) =>
                    editingId
                      ? setEditPriority(e.target.value as 'low' | 'medium' | 'high')
                      : setPriority(e.target.value as 'low' | 'medium' | 'high')
                  }
                  className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white transition duration-200"
                >
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                </select>
              </div>

              <div>
                <label htmlFor="category" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Category
                </label>
                <input
                  type="text"
                  id="category"
                  value={editingId ? editCategory : category}
                  onChange={(e) =>
                    editingId
                      ? setEditCategory(e.target.value)
                      : setCategory(e.target.value)
                  }
                  className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white transition duration-200"
                  placeholder="Enter category (e.g., work, personal)"
                />
              </div>

              <div>
                <label htmlFor="dueDate" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Due Date
                </label>
                <input
                  type="datetime-local"
                  id="dueDate"
                  value={editingId ? editDueDate : dueDate}
                  onChange={(e) =>
                    editingId
                      ? setEditDueDate(e.target.value)
                      : setDueDate(e.target.value)
                  }
                  className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white transition duration-200"
                />
              </div>

              <div>
                <label htmlFor="recurring" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Recurring
                </label>
                <select
                  id="recurring"
                  value={editingId ? editRecurring : recurring}
                  onChange={(e) =>
                    editingId
                      ? setEditRecurring(e.target.value)
                      : setRecurring(e.target.value)
                  }
                  className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white transition duration-200"
                >
                  <option value="">None</option>
                  <option value="daily">Daily</option>
                  <option value="weekly">Weekly</option>
                  <option value="monthly">Monthly</option>
                  <option value="yearly">Yearly</option>
                </select>
              </div>
            </div>

            <div className="flex flex-col sm:flex-row sm:space-x-3 space-y-3 sm:space-y-0">
              {editingId ? (
                <>
                  <button
                    type="button"
                    onClick={() => handleUpdateTodo(editingId)}
                    className="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition duration-200 flex items-center justify-center"
                  >
                    <svg className="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    Update Todo
                  </button>
                  <button
                    type="button"
                    onClick={cancelEditing}
                    className="px-6 py-3 bg-gray-500 text-white rounded-lg hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 transition duration-200 flex items-center justify-center"
                  >
                    <svg className="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                    Cancel
                  </button>
                </>
              ) : (
                <button
                  type="submit"
                  className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition duration-200 flex items-center justify-center"
                >
                  <svg className="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                  </svg>
                  Add Todo
                </button>
              )}
            </div>
          </form>
        </div>

        {/* Search, Filter, and Sort Controls */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6 mb-6">
          <h3 className="text-lg font-semibold text-gray-800 dark:text-white mb-4">Filter & Sort</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div>
              <label htmlFor="search" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Search
              </label>
              <input
                type="text"
                id="search"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                placeholder="Search by title or description"
              />
            </div>

            <div>
              <label htmlFor="filterCompleted" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Status
              </label>
              <select
                id="filterCompleted"
                value={filterCompleted}
                onChange={(e) => setFilterCompleted(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
              >
                <option value="all">All</option>
                <option value="pending">Pending</option>
                <option value="completed">Completed</option>
              </select>
            </div>

            <div>
              <label htmlFor="filterPriority" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Priority
              </label>
              <select
                id="filterPriority"
                value={filterPriority}
                onChange={(e) => setFilterPriority(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
              >
                <option value="all">All</option>
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
            </div>

            <div>
              <label htmlFor="sortBy" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Sort By
              </label>
              <div className="flex space-x-2">
                <select
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value)}
                  className="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                >
                  <option value="created_at">Created Date</option>
                  <option value="updated_at">Updated Date</option>
                  <option value="due_date">Due Date</option>
                  <option value="priority">Priority</option>
                  <option value="title">Title</option>
                </select>
                <button
                  onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')}
                  className="px-3 py-2 bg-gray-200 dark:bg-gray-700 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition duration-200"
                  title="Toggle sort order"
                >
                  {sortOrder === 'asc' ? '↑' : '↓'}
                </button>
              </div>
            </div>
          </div>

          <div className="mt-4">
            <button
              onClick={() => {
                setSearchTerm('');
                setFilterCompleted('all');
                setFilterPriority('all');
                setSortBy('created_at');
                setSortOrder('desc');
              }}
              className="px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 transition duration-200"
            >
              Clear Filters
            </button>
          </div>
        </div>

        {/* Todo List */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6">
          <div className="flex items-center mb-4">
            <h2 className="text-xl sm:text-2xl font-semibold text-gray-800 dark:text-white flex items-center">
              <svg className="h-6 w-6 mr-2 text-blue-600 dark:text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
              Your Todos
              <span className="ml-2 bg-blue-100 text-blue-800 text-xs font-medium px-2.5 py-0.5 rounded-full dark:bg-blue-900 dark:text-blue-300">
                {todos.length}
              </span>
            </h2>
          </div>

          {todos.length === 0 ? (
            <div className="text-center py-12">
              <svg className="mx-auto h-16 w-16 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
              <h3 className="mt-4 text-lg font-medium text-gray-900 dark:text-white">No todos yet</h3>
              <p className="mt-2 text-gray-500 dark:text-gray-400">
                Get started by creating a new todo.
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              {todos.map((todo) => (
                <div
                  key={todo.id}
                  className={`border rounded-xl p-5 hover:shadow-lg transition-all duration-200 bg-white dark:bg-gray-800 ${
                    todo.completed
                      ? 'border-green-200 dark:border-green-700 bg-green-50 dark:bg-green-900/20'
                      : 'border-gray-200 dark:border-gray-700'
                  }`}
                >
                  {editingId === todo.id ? (
                    <div className="space-y-4">
                      <input
                        type="text"
                        value={editTitle}
                        onChange={(e) => setEditTitle(e.target.value)}
                        className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white font-semibold"
                        autoFocus
                      />
                      <textarea
                        value={editDescription}
                        onChange={(e) => setEditDescription(e.target.value)}
                        rows={2}
                        className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                      ></textarea>

                      {/* Editing fields for priority, category, due date, and recurring */}
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                            Priority
                          </label>
                          <select
                            value={editPriority}
                            onChange={(e) => setEditPriority(e.target.value as 'low' | 'medium' | 'high')}
                            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                          >
                            <option value="low">Low</option>
                            <option value="medium">Medium</option>
                            <option value="high">High</option>
                          </select>
                        </div>

                        <div>
                          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                            Category
                          </label>
                          <input
                            type="text"
                            value={editCategory}
                            onChange={(e) => setEditCategory(e.target.value)}
                            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                            placeholder="Category"
                          />
                        </div>

                        <div>
                          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                            Due Date
                          </label>
                          <input
                            type="datetime-local"
                            value={editDueDate}
                            onChange={(e) => setEditDueDate(e.target.value)}
                            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                          />
                        </div>

                        <div>
                          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                            Recurring
                          </label>
                          <select
                            value={editRecurring}
                            onChange={(e) => setEditRecurring(e.target.value)}
                            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                          >
                            <option value="">None</option>
                            <option value="daily">Daily</option>
                            <option value="weekly">Weekly</option>
                            <option value="monthly">Monthly</option>
                            <option value="yearly">Yearly</option>
                          </select>
                        </div>
                      </div>

                      <div className="flex flex-col sm:flex-row sm:space-x-2 space-y-2 sm:space-y-0">
                        <button
                          onClick={() => handleUpdateTodo(todo.id)}
                          className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 flex items-center justify-center"
                        >
                          <svg className="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                          </svg>
                          Save
                        </button>
                        <button
                          onClick={cancelEditing}
                          className="px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 flex items-center justify-center"
                        >
                          <svg className="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                          </svg>
                          Cancel
                        </button>
                      </div>
                    </div>
                  ) : (
                    <div>
                      <div className="flex items-start">
                        {/* Completion toggle checkbox */}
                        <button
                          onClick={() => toggleTodoCompletion(todo.id)}
                          className={`mr-3 mt-1 flex-shrink-0 w-5 h-5 rounded border-2 flex items-center justify-center ${
                            todo.completed
                              ? 'bg-green-500 border-green-500 text-white'
                              : 'border-gray-300 dark:border-gray-600'
                          }`}
                        >
                          {todo.completed && (
                            <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                            </svg>
                          )}
                        </button>

                        <div className="flex-1">
                          <div className="flex items-center">
                            <h3 className={`text-lg font-semibold ${
                              todo.completed
                                ? 'text-green-600 dark:text-green-400 line-through'
                                : 'text-gray-900 dark:text-white'
                            }`}>
                              {highlightText(todo.title, searchTerm)}
                            </h3>
                            {todo.completed && (
                              <span className="ml-2 px-2 py-1 text-xs bg-green-100 text-green-800 rounded-full dark:bg-green-900/30 dark:text-green-300">
                                Completed
                              </span>
                            )}
                          </div>

                          <p className={`mt-2 ${todo.completed ? 'text-gray-500 dark:text-gray-500 line-through' : 'text-gray-600 dark:text-gray-300'}`}>
                            {highlightText(todo.description, searchTerm)}
                          </p>

                          {/* Priority, Category, Due Date, and Recurring info */}
                          <div className="mt-3 flex flex-wrap gap-2">
                            <span className={`px-2 py-1 text-xs rounded-full ${
                              todo.priority === 'high'
                                ? 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300'
                                : todo.priority === 'medium'
                                  ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300'
                                  : 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300'
                            }`}>
                              {todo.priority?.toUpperCase()}
                            </span>

                            {todo.category && (
                              <span className="px-2 py-1 text-xs bg-purple-100 text-purple-800 rounded-full dark:bg-purple-900/30 dark:text-purple-300">
                                {todo.category}
                              </span>
                            )}

                            {todo.due_date && (
                              <span className="px-2 py-1 text-xs bg-orange-100 text-orange-800 rounded-full dark:bg-orange-900/30 dark:text-orange-300">
                                Due: {new Date(todo.due_date).toLocaleDateString()}
                              </span>
                            )}

                            {todo.recurring && (
                              <span className="px-2 py-1 text-xs bg-teal-100 text-teal-800 rounded-full dark:bg-teal-900/30 dark:text-teal-300">
                                {todo.recurring.charAt(0).toUpperCase() + todo.recurring.slice(1)}
                              </span>
                            )}
                          </div>
                        </div>
                      </div>

                      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
                        <div className="flex flex-wrap gap-2 text-xs text-gray-500 dark:text-gray-400">
                          <span className="flex items-center">
                            <svg className="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            Created: {new Date(todo.created_at).toLocaleString()}
                          </span>
                          {todo.due_date && (
                            <span className="flex items-center">
                              <svg className="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                              </svg>
                              Due: {new Date(todo.due_date).toLocaleString()}
                            </span>
                          )}
                        </div>

                        <div className="flex space-x-2 mt-2 sm:mt-0">
                          <button
                            onClick={() => startEditing(todo)}
                            className="px-3 py-1.5 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700 flex items-center"
                          >
                            <svg className="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                            </svg>
                            Edit
                          </button>
                          <button
                            onClick={() => handleDeleteTodo(todo.id)}
                            className="px-3 py-1.5 bg-red-600 text-white text-sm rounded-lg hover:bg-red-700 flex items-center"
                          >
                            <svg className="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                            </svg>
                            Delete
                          </button>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}