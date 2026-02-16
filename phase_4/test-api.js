// Test script to verify frontend-backend communication
console.log('Testing API communication...');

// Test registration
async function testRegistration() {
  try {
    console.log('Testing registration...');
    const response = await fetch('http://localhost:8000/auth/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: 'test3@example.com',
        password: 'testpass123',
        name: 'Test User 3'
      })
    });

    const data = await response.json();
    console.log('Registration response:', data);

    if (response.ok) {
      console.log('✅ Registration successful!');

      // Test getting user profile with the token
      console.log('Testing user profile retrieval...');
      const userResponse = await fetch('http://localhost:8000/auth/me', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${data.access_token}`
        }
      });

      const userData = await userResponse.json();
      console.log('User profile response:', userData);

      if (userResponse.ok) {
        console.log('✅ User profile retrieved successfully!');
      } else {
        console.log('❌ User profile retrieval failed:', userData);
      }
    } else {
      console.log('❌ Registration failed:', data);
    }
  } catch (error) {
    console.log('❌ Error during test:', error);
  }
}

// Run the test
testRegistration();