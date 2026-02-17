import React, { useState, useEffect } from 'react';
import TaskForm from './TaskForm';
import TaskList from './TaskList';
import { useAuth } from '../hooks/useAuth';

const TaskDashboard = () => {
  const [tasks, setTasks] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [editingTask, setEditingTask] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { user } = useAuth();

  // Mock tasks for now - in real implementation, fetch from backend
  useEffect(() => {
    // In real implementation, fetch tasks from backend API
    // const fetchTasks = async () => {
    //   try {
    //     const response = await fetch('/api/tasks', {
    //       headers: {
    //         'Authorization': `Bearer ${user.token}`
    //       }
    //     });
    //     const data = await response.json();
    //     setTasks(data);
    //   } catch (err) {
    //     setError(err.message);
    //   } finally {
    //     setLoading(false);
    //   }
    // };

    // For now, using mock data
    setTasks([
      {
        id: '1',
        title: 'Review quarterly reports',
        description: 'Review and analyze Q4 reports with the team',
        completed: false,
        priority: 'high',
        due_date: '2026-02-20T10:00:00',
        reminder_time: '2026-02-20T09:00:00',
        tags: ['work', 'finance'],
        user_id: 'user1',
        recurrence_pattern: {
          type: 'monthly',
          interval: 1
        }
      },
      {
        id: '2',
        title: 'Morning run',
        description: 'Go for a 5km run',
        completed: true,
        priority: 'medium',
        due_date: '2026-02-17T07:00:00',
        reminder_time: '2026-02-17T06:30:00',
        tags: ['health', 'exercise'],
        user_id: 'user1',
        recurrence_pattern: {
          type: 'daily',
          interval: 1
        }
      },
      {
        id: '3',
        title: 'Team meeting',
        description: 'Weekly team sync meeting',
        completed: false,
        priority: 'medium',
        due_date: '2026-02-19T14:00:00',
        reminder_time: '2026-02-19T13:30:00',
        tags: ['work', 'meeting'],
        user_id: 'user1',
        recurrence_pattern: {
          type: 'weekly',
          interval: 1,
          count: 10
        }
      }
    ]);
    setLoading(false);
  }, [user]);

  const handleSubmitTask = async (taskData) => {
    try {
      // In real implementation, send to backend API
      // const response = await fetch('/api/tasks', {
      //   method: 'POST',
      //   headers: {
      //     'Content-Type': 'application/json',
      //     'Authorization': `Bearer ${user.token}`
      //   },
      //   body: JSON.stringify(taskData)
      // });

      // const newTask = await response.json();

      // For demo purposes, just add to local state
      const newTask = {
        ...taskData,
        id: Date.now().toString(),
        completed: false,
        user_id: 'user1' // In real app, gets from auth
      };

      setTasks(prev => [newTask, ...prev]);
      setShowForm(false);
    } catch (err) {
      setError(err.message);
    }
  };

  const handleTaskComplete = async (taskId, completed) => {
    try {
      // In real implementation, update backend API
      // await fetch(`/api/tasks/${taskId}`, {
      //   method: 'PUT',
      //   headers: {
      //     'Content-Type': 'application/json',
      //     'Authorization': `Bearer ${user.token}`
      //   },
      //   body: JSON.stringify({ completed })
      // });

      // For demo purposes, update local state
      setTasks(prev => prev.map(task =>
        task.id === taskId ? { ...task, completed } : task
      ));
    } catch (err) {
      setError(err.message);
    }
  };

  const handleTaskEdit = (task) => {
    setEditingTask(task);
    setShowForm(true);
  };

  const handleTaskDelete = async (taskId) => {
    if (!window.confirm('Are you sure you want to delete this task?')) {
      return;
    }

    try {
      // In real implementation, delete from backend API
      // await fetch(`/api/tasks/${taskId}`, {
      //   method: 'DELETE',
      //   headers: {
      //     'Authorization': `Bearer ${user.token}`
      //   }
      // });

      // For demo purposes, remove from local state
      setTasks(prev => prev.filter(task => task.id !== taskId));
    } catch (err) {
      setError(err.message);
    }
  };

  const handleCancelForm = () => {
    setShowForm(false);
    setEditingTask(null);
  };

  const handleEditTask = async (taskData) => {
    try {
      // In real implementation, update backend API
      // const response = await fetch(`/api/tasks/${editingTask.id}`, {
      //   method: 'PUT',
      //   headers: {
      //     'Content-Type': 'application/json',
      //     'Authorization': `Bearer ${user.token}`
      //   },
      //   body: JSON.stringify(taskData)
      // });

      // const updatedTask = await response.json();

      // For demo purposes, update local state
      setTasks(prev => prev.map(task =>
        task.id === editingTask.id ? { ...task, ...taskData } : task
      ));

      setShowForm(false);
      setEditingTask(null);
    } catch (err) {
      setError(err.message);
    }
  };

  if (loading) {
    return <div className="loading">Loading tasks...</div>;
  }

  if (error) {
    return <div className="error">Error: {error}</div>;
  }

  return (
    <div className="task-dashboard">
      <div className="dashboard-header">
        <h2>Task Dashboard</h2>
        <button
          onClick={() => setShowForm(true)}
          className="btn-primary"
        >
          + New Task
        </button>
      </div>

      {showForm && (
        <div className="task-form-modal">
          <div className="modal-content">
            <h3>{editingTask ? 'Edit Task' : 'Create New Task'}</h3>
            <TaskForm
              onSubmit={editingTask ? handleEditTask : handleSubmitTask}
              onCancel={handleCancelForm}
              initialData={editingTask}
            />
          </div>
        </div>
      )}

      <div className="dashboard-content">
        <div className="task-stats">
          <div className="stat-card">
            <h3>{tasks.length}</h3>
            <p>Total Tasks</p>
          </div>
          <div className="stat-card">
            <h3>{tasks.filter(t => !t.completed).length}</h3>
            <p>Pending</p>
          </div>
          <div className="stat-card">
            <h3>{tasks.filter(t => t.completed).length}</h3>
            <p>Completed</p>
          </div>
          <div className="stat-card">
            <h3>{tasks.filter(t => t.recurrence_pattern).length}</h3>
            <p>Recurring</p>
          </div>
        </div>

        <TaskList
          tasks={tasks}
          onTaskComplete={handleTaskComplete}
          onTaskEdit={handleTaskEdit}
          onTaskDelete={handleTaskDelete}
        />
      </div>
    </div>
  );
};

export default TaskDashboard;