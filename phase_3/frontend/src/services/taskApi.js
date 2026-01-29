/**
 * API service for task operations - For FastAPI backend (NOT Better Auth)
 * Better Auth is handled separately via authClient
 */
// Use relative paths in production to leverage Vercel rewrites, absolute URLs in development
const isDevelopment = import.meta.env.DEV;
const API_BASE_URL = isDevelopment
  ? (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8001')
  : ''; // Use relative paths in production to leverage Vercel rewrites

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
      const token = localStorage.getItem('auth-token');
      console.log('getTasks called with token:', token ? 'YES' : 'NO'); // Debug log

      const url = API_BASE_URL ? `${API_BASE_URL}/tasks/` : '/tasks/';
      console.log('Fetching tasks from URL:', url); // Debug log

      const response = await fetch(url, {
        method: 'GET',
        headers: await this.getAuthHeaders()
      });

      console.log('Tasks response status:', response.status); // Debug log

      if (!response.ok) {
        const errorText = await response.text();
        console.error('Tasks API error response:', errorText); // Debug log
        throw new Error(`Failed to fetch tasks: ${response.status} ${response.statusText}. Details: ${errorText}`);
      }

      // Check if response is JSON before parsing
      const contentType = response.headers.get('content-type');
      console.log('Tasks response content-type:', contentType); // Debug log

      if (contentType && contentType.includes('application/json')) {
        const jsonData = await response.json();
        console.log('Tasks response data:', jsonData); // Debug log
        return jsonData;
      } else {
        // If not JSON, try to read as text to see what was returned
        const text = await response.text();
        console.error('Expected JSON but got:', text);
        throw new Error(`Expected JSON response but got: ${text.substring(0, 100)}...`);
      }
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

      const url = API_BASE_URL ? `${API_BASE_URL}/tasks/` : '/tasks/';
      const response = await fetch(url, {
        method: 'POST',
        headers: await this.getAuthHeaders(),
        body: JSON.stringify(mappedTaskData),
      });

      if (!response.ok) {
        throw new Error(`Failed to create task: ${response.status} ${response.statusText}`);
      }

      // Check if response is JSON before parsing
      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('application/json')) {
        return await response.json();
      } else {
        // If not JSON, try to read as text to see what was returned
        const text = await response.text();
        console.error('Expected JSON but got:', text);
        throw new Error(`Expected JSON response but got: ${text.substring(0, 100)}...`);
      }
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

      const url = API_BASE_URL ? `${API_BASE_URL}/tasks/${taskId}` : `/tasks/${taskId}`;
      const response = await fetch(url, {
        method: 'PUT',
        headers: await this.getAuthHeaders(),
        body: JSON.stringify(mappedTaskData),
      });

      if (!response.ok) {
        throw new Error(`Failed to update task: ${response.status} ${response.statusText}`);
      }

      // Check if response is JSON before parsing
      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('application/json')) {
        return await response.json();
      } else {
        // If not JSON, try to read as text to see what was returned
        const text = await response.text();
        console.error('Expected JSON but got:', text);
        throw new Error(`Expected JSON response but got: ${text.substring(0, 100)}...`);
      }
    } catch (error) {
      console.error('Error updating task:', error);
      throw error;
    }
  }

  static async deleteTask(taskId) {
    try {
      const url = API_BASE_URL ? `${API_BASE_URL}/tasks/${taskId}` : `/tasks/${taskId}`;
      const response = await fetch(url, {
        method: 'DELETE',
        headers: await this.getAuthHeaders(),
      });

      if (!response.ok) {
        throw new Error(`Failed to delete task: ${response.status} ${response.statusText}`);
      }

      // Check if response is JSON before parsing
      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('application/json')) {
        return await response.json();
      } else {
        // If not JSON, try to read as text to see what was returned
        const text = await response.text();
        console.error('Expected JSON but got:', text);
        throw new Error(`Expected JSON response but got: ${text.substring(0, 100)}...`);
      }
    } catch (error) {
      console.error('Error deleting task:', error);
      throw error;
    }
  }
}

export default TaskApiService;