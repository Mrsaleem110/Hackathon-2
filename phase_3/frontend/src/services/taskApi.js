/**
 * API service for task operations
 */
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8001';

class TaskApiService {
  static async getAuthHeaders() {
    const token = localStorage.getItem('auth-token');
    if (!token) {
      throw new Error('Authentication token is missing');
    }
    return {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    };
  }

  static async getTasks() {
    try {
      const response = await fetch(`${API_BASE_URL}/tasks/`, {
        method: 'GET',
        headers: await this.getAuthHeaders()
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch tasks: ${response.status} ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching tasks:', error);
      throw error;
    }
  }

  static async createTask(taskData) {
    try {
      // Create task data with proper field mapping
      const mappedTaskData = {
        title: taskData.title || '',
        description: taskData.description || '',
        completed: taskData.completed || false,
        priority: taskData.priority || 'medium',
        due_date: taskData.dueDate || null,  // Map dueDate to due_date
        user_id: taskData.user_id  // This should be handled by the backend from auth
      };

      // Don't send user_id from frontend as it should be set from auth
      delete mappedTaskData.user_id;

      const response = await fetch(`${API_BASE_URL}/tasks/`, {
        method: 'POST',
        headers: await this.getAuthHeaders(),
        body: JSON.stringify(mappedTaskData)
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Failed to create task: ${response.status} ${response.statusText}. Details: ${errorText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error creating task:', error);
      throw error;
    }
  }

  static async updateTask(taskId, taskData) {
    try {
      // Create task data with proper field mapping
      const mappedTaskData = {
        title: taskData.title,
        description: taskData.description,
        completed: taskData.completed,
        priority: taskData.priority,
        due_date: taskData.dueDate  // Map dueDate to due_date
      };

      // Only include fields that are defined
      const filteredTaskData = {};
      Object.keys(mappedTaskData).forEach(key => {
        if (mappedTaskData[key] !== undefined) {
          filteredTaskData[key] = mappedTaskData[key];
        }
      });

      const response = await fetch(`${API_BASE_URL}/tasks/${taskId}`, {
        method: 'PUT',
        headers: await this.getAuthHeaders(),
        body: JSON.stringify(filteredTaskData)
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Failed to update task: ${response.status} ${response.statusText}. Details: ${errorText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error updating task:', error);
      throw error;
    }
  }

  static async deleteTask(taskId) {
    try {
      const response = await fetch(`${API_BASE_URL}/tasks/${taskId}`, {
        method: 'DELETE',
        headers: await this.getAuthHeaders()
      });

      if (!response.ok) {
        throw new Error(`Failed to delete task: ${response.status} ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error deleting task:', error);
      throw error;
    }
  }
}

export default TaskApiService;