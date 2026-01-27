import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import OpenAIChatKitUI from './OpenAIChatKitUI';
import TaskApiService from '../services/taskApi';

const Dashboard = () => {
  const { user, loading: authLoading, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const [stats, setStats] = useState({
    totalTasks: 0,
    completedTasks: 0,
    pendingTasks: 0,
    activeConversations: 0
  });
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        setLoading(true);
        // Get all tasks to calculate stats
        const tasksData = await TaskApiService.getTasks();
        setTasks(tasksData);

        // Calculate task statistics
        const totalTasks = tasksData.length;
        const completedTasks = tasksData.filter(task => task.completed).length;
        const pendingTasks = tasksData.length - completedTasks;

        // For now, set activeConversations to a reasonable default
        // In a real app, this would come from a conversations API
        setStats({
          totalTasks,
          completedTasks,
          pendingTasks,
          activeConversations: 1  // Default to 1 for the current chat
        });

        setError(null);
      } catch (err) {
        console.error('Error fetching dashboard stats:', err);
        setError('Failed to load dashboard data. Please try again.');

        // Set default values on error
        setStats({
          totalTasks: 0,
          completedTasks: 0,
          pendingTasks: 0,
          activeConversations: 0
        });
        setTasks([]);
      } finally {
        setLoading(false);
      }
    };

    if (isAuthenticated && user) {
      fetchStats();
    } else if (!authLoading) {
      setError('User not authenticated. Please log in.');
      setLoading(false);
    }
  }, [user, isAuthenticated, authLoading]);

  if (loading && stats.totalTasks === 0) {
    return (
      <div className="dashboard">
        <div className="loading-spinner" style={{ textAlign: 'center', padding: '40px' }}>
          Loading dashboard...
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <div className="dashboard-grid">
        {/* Stats Cards */}
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-icon">📋</div>
            <div className="stat-info">
              <h3>{stats.totalTasks}</h3>
              <p>Total Tasks</p>
            </div>
          </div>

          <div className="stat-card completed">
            <div className="stat-icon">✅</div>
            <div className="stat-info">
              <h3>{stats.completedTasks}</h3>
              <p>Completed</p>
            </div>
          </div>

          <div className="stat-card pending">
            <div className="stat-icon">⏳</div>
            <div className="stat-info">
              <h3>{stats.pendingTasks}</h3>
              <p>Pending</p>
            </div>
          </div>

          <div className="stat-card active">
            <div className="stat-icon">💬</div>
            <div className="stat-info">
              <h3>{stats.activeConversations}</h3>
              <p>Conversations</p>
            </div>
          </div>
        </div>

        {/* Main Content Area */}
        <div className="dashboard-content-area">
          <div className="welcome-section">
            <h2>Welcome back, {user?.name || user?.email || 'User'}!</h2>
            <p>How can I help you today?</p>
          </div>

          {/* Chat Interface */}
          <div className="chat-section">
            <div className="section-header">
              <h3>AI Assistant</h3>
              <span className="status-indicator online">● Online</span>
            </div>
            <div className="chat-container">
              <OpenAIChatKitUI userId={user?.id} />
            </div>
          </div>

          {/* Recent Activity */}
          <div className="activity-section">
            <div className="section-header">
              <h3>Recent Activity</h3>
            </div>
            <div className="activity-list">
              {error && (
                <div className="error-message" style={{ padding: '10px', backgroundColor: '#fee', border: '1px solid #fcc', borderRadius: '4px', margin: '10px', color: '#c33' }}>
                  {error}
                </div>
              )}
              {stats.totalTasks > 0 ? (
                <>
                  {stats.completedTasks > 0 && (
                    <div className="activity-item">
                      <div className="activity-icon">✅</div>
                      <div className="activity-content">
                        <p>Completed {stats.completedTasks} task{stats.completedTasks !== 1 ? 's' : ''}</p>
                        <span className="activity-time">Just now</span>
                      </div>
                    </div>
                  )}
                  {stats.pendingTasks > 0 && (
                    <div className="activity-item">
                      <div className="activity-icon">📝</div>
                      <div className="activity-content">
                        <p>You have {stats.pendingTasks} pending task{stats.pendingTasks !== 1 ? 's' : ''}</p>
                        <span className="activity-time">Just now</span>
                      </div>
                    </div>
                  )}
                </>
              ) : (
                <div className="activity-item">
                  <div className="activity-icon">👋</div>
                  <div className="activity-content">
                    <p>Welcome! No tasks yet. Start by creating your first task.</p>
                    <span className="activity-time">Just now</span>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Right Sidebar */}
        <div className="dashboard-sidebar">
          <div className="quick-actions">
            <h4>Quick Actions</h4>
            <button className="action-btn" onClick={() => navigate('/tasks')}>
              <span>➕</span> New Task
            </button>
            <button className="action-btn" onClick={() => navigate('/chat')}>
              <span>💬</span> New Chat
            </button>
            <button className="action-btn" onClick={() => navigate('/analytics')}>
              <span>📊</span> View Analytics
            </button>
          </div>

          <div className="upcoming-tasks">
            <h4>Recent Tasks</h4>
            {stats.totalTasks > 0 ? (
              <>
                {tasks.slice(0, 2).map((task, index) => (
                  <div key={index} className="task-item">
                    <div className={`task-status ${task.completed ? 'completed' : 'pending'}`}></div>
                    <div className="task-info">
                      <p>{task.title}</p>
                      <span>{task.completed ? 'Completed' : 'Pending'}</span>
                    </div>
                  </div>
                ))}
              </>
            ) : (
              <div className="no-tasks">
                <p>No tasks found. Create your first task to get started!</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;