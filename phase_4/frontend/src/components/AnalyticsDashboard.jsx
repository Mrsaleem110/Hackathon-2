import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import TaskApiService from '../services/taskApi';

const AnalyticsDashboard = () => {
  const { user, loading: authLoading, isAuthenticated } = useAuth();
  const [analyticsData, setAnalyticsData] = useState({
    totalTasks: 0,
    completedTasks: 0,
    pendingTasks: 0,
    productivityData: [],
    priorityData: [],
    completionRate: 0
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAnalyticsData = async () => {
      try {
        setLoading(true);
        // Get all tasks to calculate analytics
        const tasks = await TaskApiService.getTasks();

        // Calculate analytics
        const totalTasks = tasks.length;
        const completedTasks = tasks.filter(task => task.completed).length;
        const pendingTasks = tasks.length - completedTasks;
        const completionRate = totalTasks > 0 ? Math.round((completedTasks / totalTasks) * 100) : 0;

        // Calculate priority distribution
        const priorityCounts = tasks.reduce((acc, task) => {
          acc[task.priority] = (acc[task.priority] || 0) + 1;
          return acc;
        }, {});

        const priorityData = [
          { name: 'High Priority', value: priorityCounts.high || 0, color: '#ef4444' },
          { name: 'Medium Priority', value: priorityCounts.medium || 0, color: '#f59e0b' },
          { name: 'Low Priority', value: priorityCounts.low || 0, color: '#10b981' },
        ];

        // Mock productivity data based on actual task completion
        const daysOfWeek = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
        const productivityData = daysOfWeek.map(day => ({
          day,
          tasks: Math.floor(Math.random() * 15) + 1, // Random data for now
          completed: Math.floor(Math.random() * 10) + 1 // Random data for now
        }));

        setAnalyticsData({
          totalTasks,
          completedTasks,
          pendingTasks,
          productivityData,
          priorityData,
          completionRate
        });

        setError(null);
      } catch (err) {
        console.error('Error fetching analytics:', err);
        setError('Failed to load analytics data. Please try again.');

        // Fallback to mock data
        setAnalyticsData({
          totalTasks: 0,
          completedTasks: 0,
          pendingTasks: 0,
          productivityData: [
            { day: 'Mon', tasks: 8, completed: 6 },
            { day: 'Tue', tasks: 12, completed: 10 },
            { day: 'Wed', tasks: 6, completed: 4 },
            { day: 'Thu', tasks: 10, completed: 8 },
            { day: 'Fri', tasks: 14, completed: 12 },
            { day: 'Sat', tasks: 4, completed: 2 },
            { day: 'Sun', tasks: 6, completed: 5 },
          ],
          priorityData: [
            { name: 'High Priority', value: 15, color: '#ef4444' },
            { name: 'Medium Priority', value: 45, color: '#f59e0b' },
            { name: 'Low Priority', value: 40, color: '#10b981' },
          ],
          completionRate: 0
        });
      } finally {
        setLoading(false);
      }
    };

    if (isAuthenticated && user) {
      fetchAnalyticsData();
    } else if (!authLoading) {
      setError('User not authenticated. Please log in.');
      setLoading(false);
    }
  }, [user, isAuthenticated, authLoading]);

  const { totalTasks, completedTasks, pendingTasks, productivityData, priorityData, completionRate } = analyticsData;

  if (loading) {
    return (
      <div className="analytics-dashboard">
        <div className="loading-spinner" style={{ textAlign: 'center', padding: '40px' }}>
          Loading analytics...
        </div>
      </div>
    );
  }

  return (
    <div className="analytics-dashboard">
      <div className="analytics-header">
        <h2>Analytics & Insights</h2>
        <div className="date-range-selector">
          <select>
            <option>Last 7 Days</option>
            <option>Last 30 Days</option>
            <option>Last 90 Days</option>
            <option>This Year</option>
          </select>
        </div>
      </div>

      {/* Overview Cards */}
      <div className="analytics-overview">
        <div className="overview-card">
          <h3>Total Tasks</h3>
          <p className="metric">{totalTasks}</p>
          <p className="trend">↑ 12% from last week</p>
        </div>
        <div className="overview-card">
          <h3>Completion Rate</h3>
          <p className="metric">{completionRate}%</p>
          <p className="trend">↑ 5% from last week</p>
        </div>
        <div className="overview-card">
          <h3>Active Projects</h3>
          <p className="metric">{pendingTasks}</p>
          <p className="trend">→ Same as last week</p>
        </div>
        <div className="overview-card">
          <h3>Avg. Response Time</h3>
          <p className="metric">2.3m</p>
          <p className="trend">↓ 0.5m from last week</p>
        </div>
      </div>

      {error && (
        <div className="error-message" style={{ padding: '10px', backgroundColor: '#fee', border: '1px solid #fcc', borderRadius: '4px', margin: '10px', color: '#c33' }}>
          {error}
        </div>
      )}

      {/* Charts Grid */}
      <div className="charts-grid">
        {/* Productivity Chart */}
        <div className="chart-container">
          <h4>Weekly Productivity</h4>
          <div className="productivity-chart">
            {productivityData.map((day, index) => (
              <div key={index} className="chart-bar-group">
                <div className="bar-container">
                  <div
                    className="bar completed-bar"
                    style={{ height: `${(day.completed / Math.max(...productivityData.map(d => d.tasks))) * 100}%` }}
                    title={`Completed: ${day.completed}`}
                  ></div>
                  <div
                    className="bar total-bar"
                    style={{ height: `${(day.tasks / Math.max(...productivityData.map(d => d.tasks))) * 100}%` }}
                    title={`Total: ${day.tasks}`}
                  ></div>
                </div>
                <span className="bar-label">{day.day}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Priority Distribution */}
        <div className="chart-container">
          <h4>Task Priority Distribution</h4>
          <div className="pie-chart">
            {priorityData.map((item, index) => (
              <div
                key={index}
                className="pie-segment"
                style={{
                  '--color': item.color,
                  '--size': `${item.value}%`,
                }}
              >
                <span>{item.name}</span>
              </div>
            ))}
          </div>
          <div className="legend">
            {priorityData.map((item, index) => (
              <div key={index} className="legend-item">
                <span
                  className="legend-color"
                  style={{ backgroundColor: item.color }}
                ></span>
                <span>{item.name}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Recent Activity */}
        <div className="chart-container">
          <h4>Recent Activity</h4>
          <div className="activity-timeline">
            <div className="timeline-item">
              <div className="timeline-marker completed"></div>
              <div className="timeline-content">
                <h5>Completed project review</h5>
                <p>Reviewed all deliverables and provided feedback</p>
                <span className="timestamp">2 hours ago</span>
              </div>
            </div>
            <div className="timeline-item">
              <div className="timeline-marker new"></div>
              <div className="timeline-content">
                <h5>Created new task</h5>
                <p>Added "Prepare presentation" to your task list</p>
                <span className="timestamp">4 hours ago</span>
              </div>
            </div>
            <div className="timeline-item">
              <div className="timeline-marker message"></div>
              <div className="timeline-content">
                <h5>New message received</h5>
                <p>Team member sent an update on project timeline</p>
                <span className="timestamp">1 day ago</span>
              </div>
            </div>
          </div>
        </div>

        {/* Performance Metrics */}
        <div className="chart-container">
          <h4>Performance Metrics</h4>
          <div className="metrics-grid">
            <div className="metric-item">
              <div className="metric-header">
                <span>On-time Completion</span>
                <span className="metric-value">92%</span>
              </div>
              <div className="metric-progress">
                <div className="progress-bar" style={{ width: '92%' }}></div>
              </div>
            </div>
            <div className="metric-item">
              <div className="metric-header">
                <span>Task Efficiency</span>
                <span className="metric-value">87%</span>
              </div>
              <div className="metric-progress">
                <div className="progress-bar" style={{ width: '87%' }}></div>
              </div>
            </div>
            <div className="metric-item">
              <div className="metric-header">
                <span>Goal Achievement</span>
                <span className="metric-value">76%</span>
              </div>
              <div className="metric-progress">
                <div className="progress-bar" style={{ width: '76%' }}></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnalyticsDashboard;