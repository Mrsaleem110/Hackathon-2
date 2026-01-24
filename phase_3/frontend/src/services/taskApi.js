/**
 * API service for task operations - For FastAPI backend (NOT Better Auth)
 * Better Auth is handled separately via authClient
 */
// Use relative URL for production deployments, fallback to env var for development
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ||
                     (window.location.hostname.includes('localhost') || window.location.hostname.includes('127.0.0.1')
                       ? 'http://localhost:8001'
                       : window.location.origin);

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
        due_date: taskData.dueDate || null,
      };

      const response = await fetch(`${API_BASE_URL}/tasks/`, {
        method: 'POST',
        headers: await this.getAuthHeaders(),
        body: JSON.stringify(mappedTaskData),
      });

      if (!response.ok) {
        throw new Error(`Failed to create task: ${response.status} ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error creating task:', error);
      throw error;
    }
  }

  static async updateTask(taskId, taskData) {
    try {
      const mappedTaskData = {
        title: taskData.title,
        description: taskData.description,
        completed: taskData.completed,
        priority: taskData.priority,
        due_date: taskData.dueDate,
      };

      const response = await fetch(`${API_BASE_URL}/tasks/${taskId}`, {
        method: 'PUT',
        headers: await this.getAuthHeaders(),
        body: JSON.stringify(mappedTaskData),
      });

      if (!response.ok) {
        throw new Error(`Failed to update task: ${response.status} ${response.statusText}`);
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
        headers: await this.getAuthHeaders(),
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