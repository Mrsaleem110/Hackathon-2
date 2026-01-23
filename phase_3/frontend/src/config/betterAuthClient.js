// Better Auth API client for Express server
const betterAuthBaseURL = import.meta.env.VITE_BETTER_AUTH_URL ||
  (typeof window !== 'undefined' && window.location.origin) ||
  'http://localhost:3000';

// API wrapper for Better Auth endpoints
const betterAuthAPI = {
  async signUpEmail({ email, password, name }) {
    const response = await fetch(`${betterAuthBaseURL}/api/auth/sign-up`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email,
        password,
        name,
      }),
    });

    // Check if response is HTML (starts with <!DOCTYPE or <html>)
    const responseText = await response.text();

    if (responseText.trim().startsWith('<')) {
      // Response is HTML, which means there was an error
      return { error: { message: `HTML response received instead of JSON. Server may not be configured properly. Status: ${response.status}` } };
    }

    // Parse as JSON if it's not HTML
    try {
      const data = responseText ? JSON.parse(responseText) : {};
      if (response.ok) {
        return data;
      } else {
        return { error: data };
      }
    } catch (e) {
      return { error: { message: `Failed to parse JSON response: ${e.message}` } };
    }
  },

  async signInEmail({ email, password }) {
    const response = await fetch(`${betterAuthBaseURL}/api/auth/sign-in/email`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email,
        password,
      }),
    });

    // Check if response is HTML (starts with <!DOCTYPE or <html>)
    const responseText = await response.text();

    if (responseText.trim().startsWith('<')) {
      // Response is HTML, which means there was an error
      return { error: { message: `HTML response received instead of JSON. Server may not be configured properly. Status: ${response.status}` } };
    }

    // Parse as JSON if it's not HTML
    try {
      const data = responseText ? JSON.parse(responseText) : {};
      if (response.ok) {
        return data;
      } else {
        return { error: data };
      }
    } catch (e) {
      return { error: { message: `Failed to parse JSON response: ${e.message}` } };
    }
  },

  async getSession() {
    const response = await fetch(`${betterAuthBaseURL}/api/auth/session`, {
      method: 'GET',
      credentials: 'include', // Important for cookies
    });

    // Check if response is HTML (starts with <!DOCTYPE or <html>)
    const responseText = await response.text();

    if (responseText.trim().startsWith('<')) {
      // Response is HTML, which means there was an error or no session
      return null;
    }

    // Parse as JSON if it's not HTML
    try {
      const data = responseText ? JSON.parse(responseText) : {};
      if (response.ok) {
        return data;
      } else {
        return null;
      }
    } catch (e) {
      return null;
    }
  },

  async signOut() {
    const response = await fetch(`${betterAuthBaseURL}/api/auth/sign-out`, {
      method: 'POST',
      credentials: 'include', // Important for cookies
    });

    return response.ok;
  }
};

export { betterAuthAPI as authClient, betterAuthBaseURL };