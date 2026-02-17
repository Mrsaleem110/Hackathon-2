import React from 'react';

const TaskList = ({ tasks, onTaskComplete, onTaskEdit, onTaskDelete }) => {
  const getRecurrenceIcon = (recurrencePattern) => {
    if (!recurrencePattern) return null;

    const { type } = recurrencePattern;
    let icon = '🔄';
    let title = '';

    switch (type) {
      case 'daily':
        icon = '📅';
        title = 'Daily';
        break;
      case 'weekly':
        icon = '📆';
        title = 'Weekly';
        break;
      case 'monthly':
        icon = '🗓️';
        title = 'Monthly';
        break;
      case 'yearly':
        icon = '🗓️';
        title = 'Yearly';
        break;
      default:
        icon = '🔄';
        title = 'Recurring';
    }

    return (
      <span className="recurrence-indicator" title={`Recurring: ${title}`}>
        {icon}
      </span>
    );
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high':
        return '#ef4444'; // red
      case 'medium':
        return '#f59e0b'; // amber
      case 'low':
        return '#10b981'; // emerald
      default:
        return '#6b7280'; // gray
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="task-list">
      {tasks.length === 0 ? (
        <div className="empty-state">
          <p>No tasks found. Create your first task!</p>
        </div>
      ) : (
        <ul className="tasks">
          {tasks.map(task => (
            <li key={task.id} className={`task-item ${task.completed ? 'completed' : ''}`}>
              <div className="task-header">
                <div className="task-checkbox">
                  <input
                    type="checkbox"
                    checked={task.completed}
                    onChange={() => onTaskComplete(task.id, !task.completed)}
                    id={`task-${task.id}`}
                  />
                  <label htmlFor={`task-${task.id}`}></label>
                </div>

                <div className="task-content">
                  <h3 className="task-title">{task.title}</h3>
                  {task.description && (
                    <p className="task-description">{task.description}</p>
                  )}

                  <div className="task-meta">
                    {task.priority && (
                      <span
                        className="priority-badge"
                        style={{ backgroundColor: getPriorityColor(task.priority) }}
                      >
                        {task.priority.toUpperCase()}
                      </span>
                    )}

                    {task.due_date && (
                      <span className="due-date">
                        📅 Due: {formatDate(task.due_date)}
                      </span>
                    )}

                    {task.recurrence_pattern && getRecurrenceIcon(task.recurrence_pattern)}

                    {task.tags && task.tags.length > 0 && (
                      <div className="tags">
                        {task.tags.map((tag, index) => (
                          <span key={index} className="tag">{tag}</span>
                        ))}
                      </div>
                    )}
                  </div>
                </div>

                <div className="task-actions">
                  <button
                    onClick={() => onTaskEdit(task)}
                    className="btn-icon"
                    title="Edit task"
                  >
                    ✏️
                  </button>
                  <button
                    onClick={() => onTaskDelete(task.id)}
                    className="btn-icon"
                    title="Delete task"
                  >
                    🗑️
                  </button>
                </div>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default TaskList;