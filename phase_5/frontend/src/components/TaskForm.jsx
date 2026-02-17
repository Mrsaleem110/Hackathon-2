import React, { useState } from 'react';

const TaskForm = ({ onSubmit, onCancel }) => {
  const [taskData, setTaskData] = useState({
    title: '',
    description: '',
    priority: 'medium',
    due_date: '',
    reminder_time: '',
    tags: '',
    recurrence_pattern: null
  });

  const [showRecurrence, setShowRecurrence] = useState(false);
  const [recurrenceData, setRecurrenceData] = useState({
    type: 'daily',
    interval: 1,
    end_type: 'never', // 'never', 'after', 'on_date'
    end_count: 1,
    end_date: ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setTaskData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleRecurrenceChange = (e) => {
    const { name, value, type, checked } = e.target;
    setRecurrenceData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleTagsChange = (e) => {
    const tags = e.target.value.split(',').map(tag => tag.trim()).filter(tag => tag);
    setTaskData(prev => ({
      ...prev,
      tags: tags
    }));
  };

  const handleCreateTask = (e) => {
    e.preventDefault();

    let taskPayload = {
      ...taskData,
    };

    // Remove recurrence if not enabled
    if (!showRecurrence) {
      taskPayload.recurrence_pattern = null;
    } else {
      // Format recurrence pattern
      const recurrencePattern = {
        type: recurrenceData.type,
        interval: parseInt(recurrenceData.interval),
      };

      if (recurrenceData.end_type === 'after') {
        recurrencePattern.count = parseInt(recurrenceData.end_count);
      } else if (recurrenceData.end_type === 'on_date' && recurrenceData.end_date) {
        recurrencePattern.end_date = recurrenceData.end_date;
      }

      taskPayload.recurrence_pattern = recurrencePattern;
    }

    // Convert tags string to array if not already
    if (typeof taskPayload.tags === 'string') {
      taskPayload.tags = taskPayload.tags.split(',').map(tag => tag.trim()).filter(tag => tag);
    }

    onSubmit(taskPayload);
  };

  return (
    <form onSubmit={handleCreateTask} className="task-form">
      <div className="form-group">
        <label htmlFor="title">Title *</label>
        <input
          type="text"
          id="title"
          name="title"
          value={taskData.title}
          onChange={handleChange}
          required
          placeholder="Task title"
        />
      </div>

      <div className="form-group">
        <label htmlFor="description">Description</label>
        <textarea
          id="description"
          name="description"
          value={taskData.description}
          onChange={handleChange}
          placeholder="Task description"
          rows="3"
        />
      </div>

      <div className="form-row">
        <div className="form-group">
          <label htmlFor="priority">Priority</label>
          <select
            id="priority"
            name="priority"
            value={taskData.priority}
            onChange={handleChange}
          >
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="due_date">Due Date</label>
          <input
            type="datetime-local"
            id="due_date"
            name="due_date"
            value={taskData.due_date}
            onChange={handleChange}
          />
        </div>

        <div className="form-group">
          <label htmlFor="reminder_time">Reminder Time</label>
          <input
            type="datetime-local"
            id="reminder_time"
            name="reminder_time"
            value={taskData.reminder_time}
            onChange={handleChange}
          />
        </div>
      </div>

      <div className="form-group">
        <label htmlFor="tags">Tags (comma-separated)</label>
        <input
          type="text"
          id="tags"
          name="tags"
          value={taskData.tags?.join(', ') || ''}
          onChange={handleTagsChange}
          placeholder="tag1, tag2, tag3"
        />
      </div>

      <div className="form-group">
        <label>
          <input
            type="checkbox"
            checked={showRecurrence}
            onChange={(e) => setShowRecurrence(e.target.checked)}
          />
          Recurring Task
        </label>
      </div>

      {showRecurrence && (
        <div className="recurrence-options">
          <h4>Recurrence Pattern</h4>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="recurrence_type">Recurrence Type</label>
              <select
                id="recurrence_type"
                name="type"
                value={recurrenceData.type}
                onChange={handleRecurrenceChange}
              >
                <option value="daily">Daily</option>
                <option value="weekly">Weekly</option>
                <option value="monthly">Monthly</option>
                <option value="yearly">Yearly</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="recurrence_interval">Every</label>
              <input
                type="number"
                id="recurrence_interval"
                name="interval"
                min="1"
                value={recurrenceData.interval}
                onChange={handleRecurrenceChange}
              />
              <span> {recurrenceData.type}</span>
            </div>
          </div>

          <div className="form-group">
            <label>End</label>
            <div className="end-options">
              <label>
                <input
                  type="radio"
                  name="end_type"
                  value="never"
                  checked={recurrenceData.end_type === 'never'}
                  onChange={handleRecurrenceChange}
                />
                Never
              </label>
              <label>
                <input
                  type="radio"
                  name="end_type"
                  value="after"
                  checked={recurrenceData.end_type === 'after'}
                  onChange={handleRecurrenceChange}
                />
                After
                {recurrenceData.end_type === 'after' && (
                  <input
                    type="number"
                    name="end_count"
                    min="1"
                    value={recurrenceData.end_count}
                    onChange={handleRecurrenceChange}
                    style={{ width: '60px', marginLeft: '5px' }}
                  />
                )}
                occurrences
              </label>
              <label>
                <input
                  type="radio"
                  name="end_type"
                  value="on_date"
                  checked={recurrenceData.end_type === 'on_date'}
                  onChange={handleRecurrenceChange}
                />
                On date
                {recurrenceData.end_type === 'on_date' && (
                  <input
                    type="date"
                    name="end_date"
                    value={recurrenceData.end_date}
                    onChange={handleRecurrenceChange}
                    style={{ marginLeft: '5px' }}
                  />
                )}
              </label>
            </div>
          </div>
        </div>
      )}

      <div className="form-actions">
        <button type="submit" className="btn-primary">Create Task</button>
        <button type="button" onClick={onCancel} className="btn-secondary">Cancel</button>
      </div>
    </form>
  );
};

export default TaskForm;