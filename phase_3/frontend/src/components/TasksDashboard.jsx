import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import TaskApiService from '../services/taskApi';

const TasksDashboard = () => {
  const { user, loading: authLoading, isAuthenticated } = useAuth();
  const [tasks, setTasks] = useState([]);
  const [newTask, setNewTask] = useState({ title: '', description: '', priority: 'medium' });
  const [filter, setFilter] = useState('all');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const filteredTasks = tasks.filter(task => {
    if (filter === 'completed') return task.completed;
    if (filter === 'pending') return !task.completed;
    if (filter === 'high') return task.priority === 'high' && !task.completed;
    if (filter === 'medium') return task.priority === 'medium' && !task.completed;
    if (filter === 'low') return task.priority === 'low' && !task.completed;
    return true;
  });

  const loadTasks = async () => {
    try {
      setLoading(true);
      const tasksData = await TaskApiService.getTasks();

      // Normalize tasks data to ensure consistent field names
      const normalizedTasks = tasksData.map(task => ({
        ...task,
        dueDate: task.due_date || task.dueDate || task.dueDate,
        id: task.id
      }));

      setTasks(normalizedTasks);
      setError(null);
    } catch (err) {
      setError('Failed to load tasks. Please try again.');
      console.error('Error loading tasks:', err);
    } finally {
      setLoading(false);
    }
  };

  const toggleTask = async (taskId) => {
    const task = tasks.find(t => t.id === taskId);
    if (task) {
      try {
        const updatedTask = await TaskApiService.updateTask(taskId, {
          ...task,
          completed: !task.completed,
          dueDate: task.dueDate  // Ensure dueDate is passed correctly
        });

        // Normalize the response to ensure consistent field names
        const normalizedTask = {
          ...updatedTask,
          dueDate: updatedTask.due_date || updatedTask.dueDate,
          id: updatedTask.id
        };

        setTasks(tasks.map(t =>
          t.id === taskId ? normalizedTask : t
        ));
      } catch (err) {
        setError('Failed to update task. Please try again.');
        console.error('Error updating task:', err);
      }
    }
  };

  const addTask = async (e) => {
    e.preventDefault();
    if (newTask.title.trim()) {
      try {
        const taskData = {
          title: newTask.title,
          description: newTask.description,
          priority: newTask.priority,
          completed: false,
          due_date: new Date().toISOString().split('T')[0]  // Use the correct field name expected by backend
        };

        const newTaskResult = await TaskApiService.createTask(taskData);

        // Ensure the returned task has all expected fields
        const normalizedTask = {
          ...newTaskResult,
          dueDate: newTaskResult.due_date || newTaskResult.dueDate,
          id: newTaskResult.id
        };

        setTasks([...tasks, normalizedTask]);
        setNewTask({ title: '', description: '', priority: 'medium' });
      } catch (err) {
        setError('Failed to create task. Please try again.');
        console.error('Error creating task:', err);
      }
    }
  };

  const deleteTask = async (taskId) => {
    try {
      await TaskApiService.deleteTask(taskId);
      setTasks(tasks.filter(task => task.id !== taskId));
    } catch (err) {
      setError('Failed to delete task. Please try again.');
      console.error('Error deleting task:', err);
    }
  };

  useEffect(() => {
    if (isAuthenticated && user) {
      loadTasks();
    } else if (!authLoading) {
      setError('User not authenticated. Please log in.');
      setLoading(false);
    }
  }, [isAuthenticated, user, authLoading]);

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high': return '#ef4444';
      case 'medium': return '#f59e0b';
      case 'low': return '#10b981';
      default: return '#6b7280';
    }
  };

  return (
    <div className="tasks-dashboard">
      <div className="tasks-header">
        <h2>Task Management</h2>
        <div className="tasks-stats">
          <span>Total: {tasks.length}</span>
          <span>Completed: {tasks.filter(t => t.completed).length}</span>
          <span>Pending: {tasks.filter(t => !t.completed).length}</span>
        </div>
      </div>

      {error && (
        <div className="error-message" style={{ padding: '10px', backgroundColor: '#fee', border: '1px solid #fcc', borderRadius: '4px', margin: '10px', color: '#c33' }}>
          {error}
        </div>
      )}

      {loading && (
        <div className="loading" style={{ textAlign: 'center', padding: '20px' }}>
          Loading tasks...
        </div>
      )}

      {!loading && (
        <>
          {/* Task Form */}
          <div className="task-form-section">
            <form onSubmit={addTask} className="task-form">
              <div className="form-group">
                <input
                  type="text"
                  placeholder="Task title..."
                  value={newTask.title}
                  onChange={(e) => setNewTask({ ...newTask, title: e.target.value })}
                  required
                />
              </div>
              <div className="form-group">
                <textarea
                  placeholder="Task description..."
                  value={newTask.description}
                  onChange={(e) => setNewTask({ ...newTask, description: e.target.value })}
                />
              </div>
              <div className="form-group">
                <select
                  value={newTask.priority}
                  onChange={(e) => setNewTask({ ...newTask, priority: e.target.value })}
                >
                  <option value="low">Low Priority</option>
                  <option value="medium">Medium Priority</option>
                  <option value="high">High Priority</option>
                </select>
              </div>
              <button type="submit" className="add-task-btn">
                Add Task
              </button>
            </form>
          </div>

          {/* Filters */}
          <div className="tasks-filters">
            <button
              className={`filter-btn ${filter === 'all' ? 'active' : ''}`}
              onClick={() => setFilter('all')}
            >
              All
            </button>
            <button
              className={`filter-btn ${filter === 'completed' ? 'active' : ''}`}
              onClick={() => setFilter('completed')}
            >
              Completed
            </button>
            <button
              className={`filter-btn ${filter === 'pending' ? 'active' : ''}`}
              onClick={() => setFilter('pending')}
            >
              Pending
            </button>
            <button
              className={`filter-btn ${filter === 'high' ? 'active' : ''}`}
              onClick={() => setFilter('high')}
            >
              High Priority
            </button>
            <button
              className={`filter-btn ${filter === 'medium' ? 'active' : ''}`}
              onClick={() => setFilter('medium')}
            >
              Medium Priority
            </button>
            <button
              className={`filter-btn ${filter === 'low' ? 'active' : ''}`}
              onClick={() => setFilter('low')}
            >
              Low Priority
            </button>
          </div>

          {/* Tasks List */}
          <div className="tasks-list">
            {filteredTasks.length === 0 ? (
              <div className="no-tasks">
                <p>No tasks found. Add a new task to get started!</p>
              </div>
            ) : (
              filteredTasks.map(task => (
                <div key={task.id} className={`task-item ${task.completed ? 'completed' : ''}`}>
                  <div className="task-checkbox">
                    <input
                      type="checkbox"
                      checked={task.completed}
                      onChange={() => toggleTask(task.id)}
                      id={`task-${task.id}`}
                    />
                    <label htmlFor={`task-${task.id}`}></label>
                  </div>

                  <div className="task-content">
                    <h4>{task.title}</h4>
                    <p>{task.description}</p>
                    <div className="task-meta">
                      <span
                        className="priority-badge"
                        style={{ backgroundColor: getPriorityColor(task.priority) }}
                      >
                        {task.priority}
                      </span>
                      <span className="due-date">Due: {task.dueDate}</span>
                    </div>
                  </div>

                  <div className="task-actions">
                    <button
                      onClick={() => deleteTask(task.id)}
                      className="delete-btn"
                      aria-label="Delete task"
                    >
                      🗑️
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>
        </>
      )}
    </div>
  );
};

export default TasksDashboard;