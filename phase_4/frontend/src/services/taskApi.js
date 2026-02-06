/**
 * API service for task operations - For FastAPI backend (NOT Better Auth)
 * Better Auth is handled separately via authClient
 */
// Always use the backend URL in production to ensure API calls reach the correct server
const isDevelopment = import.meta.env.DEV;
const API_BASE_URL = isDevelopment
  ? (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8001')
  : 'https://hackathon-2-p-3-backend.vercel.app'; // Use absolute backend URL in production

class TaskApiService {
  static async getAuthHeaders() {
    const token = localStorage.getItem('auth-token');
    console.log('Task API - Token available:', !!token); // Debug log
    console.log('Task API - Full token in storage:', token); // Debug log

    if (!token) {
      console.error('Task API - Authentication token is missing'); // Debug log
      // Double-check: maybe the token is stored under a different key
      const keys = Object.keys(localStorage);
      for (const key of keys) {
        if (key.toLowerCase().includes('token')) {
          const potentialToken = localStorage.getItem(key);
          if (potentialToken && typeof potentialToken === 'string' && potentialToken.includes('.')) {
            // This might be a JWT token
            const parts = potentialToken.split('.');
            if (parts.length === 3) {
              console.log(`Found potential token in localStorage key: ${key}`); // Debug log
              localStorage.setItem('auth-token', potentialToken); // Store with correct key
              return {
                'Authorization': `Bearer ${potentialToken}`,
                'Content-Type': 'application/json'
              };
            }
          }
        }
      }

      throw new Error('Authentication token is missing');
    }

    console.log('Task API - Using token:', token ? token.substring(0, 10) + '...' : 'NO TOKEN'); // Debug log
    return {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    };
  }

  static async getTasks() {
    try {
      const token = localStorage.getItem('auth-token');
      console.log('getTasks called with token:', token ? 'YES' : 'NO'); // Debug log
      console.log('Full token in getTasks:', token); // Debug log

      const url = API_BASE_URL ? `${API_BASE_URL}/tasks/` : '/tasks/';
      console.log('Fetching tasks from URL:', url); // Debug log

      const headers = await this.getAuthHeaders();
      console.log('Using headers:', headers); // Debug log

      const response = await fetch(url, {
        method: 'GET',
        headers: headers
      });

      console.log('Tasks response status:', response.status); // Debug log
      console.log('Tasks response headers:', response.headers); // Debug log

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
        console.log('Tasks response text:', text); // Debug log
        console.error('Expected JSON but got:', text);
        throw new Error(`Expected JSON response but got: ${text.substring(0, 100)}...`);
      }
    } catch (error) {
      console.error('Error fetching tasks:', error);
      console.error('Error stack:', error.stack); // Debug log
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