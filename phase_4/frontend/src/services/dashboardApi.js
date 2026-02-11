/**
 * API service for dashboard operations
 */

// Use relative paths in production to leverage Vercel rewrites, absolute URLs in development
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

class DashboardApiService {
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

  static async getDashboardStats() {
    try {
      const url = API_BASE_URL ? `${API_BASE_URL}/dashboard/stats` : '/dashboard/stats';

      const response = await fetch(url, {
        method: 'GET',
        headers: await this.getAuthHeaders()
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Failed to fetch dashboard stats: ${response.status} ${response.statusText}. Details: ${errorText}`);
      }

      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('application/json')) {
        const jsonData = await response.json();
        return jsonData;
      } else {
        const text = await response.text();
        throw new Error(`Expected JSON response but got: ${text.substring(0, 100)}...`);
      }
    } catch (error) {
      console.error('Error fetching dashboard stats:', error);
      throw error;
    }
  }

  static async getDashboardOverview() {
    try {
      const url = API_BASE_URL ? `${API_BASE_URL}/dashboard/overview` : '/dashboard/overview';

      const response = await fetch(url, {
        method: 'GET',
        headers: await this.getAuthHeaders()
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Failed to fetch dashboard overview: ${response.status} ${response.statusText}. Details: ${errorText}`);
      }

      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('application/json')) {
        const jsonData = await response.json();
        return jsonData;
      } else {
        const text = await response.text();
        throw new Error(`Expected JSON response but got: ${text.substring(0, 100)}...`);
      }
    } catch (error) {
      console.error('Error fetching dashboard overview:', error);
      throw error;
    }
  }
}

export default DashboardApiService;