// frontend/config/streamConfig.js
export const streamConfig = {
  // Note: These are example values - you need to replace with your actual Stream Chat API keys
  apiKey: process.env.NEXT_PUBLIC_STREAM_API_KEY || 'YOUR_STREAM_API_KEY',
  userToken: process.env.NEXT_PUBLIC_STREAM_USER_TOKEN || 'YOUR_USER_TOKEN',

  // Example user object - in a real app, this would come from your authentication system
  user: {
    id: 'user-id',
    name: 'User Name',
    image: 'https://getstream.io/random_svg/?name=John+Doe',
  },
};