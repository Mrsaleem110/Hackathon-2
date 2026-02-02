// Test script to verify chat API configuration
console.log("Testing Chat API Configuration...");

// Check if the API calls in the frontend are properly configured
const fs = require('fs');

// Test 1: Verify ChatInterface.jsx has the correct URL construction
const chatInterfacePath = './frontend/src/components/ChatInterface.jsx';
if (fs.existsSync(chatInterfacePath)) {
  const chatInterfaceCode = fs.readFileSync(chatInterfacePath, 'utf8');
  if (chatInterfaceCode.includes('https://hackathon-2-p-3-backend.vercel.app')) {
    console.log('✅ ChatInterface.jsx: Uses correct backend URL in production');
  } else {
    console.log('❌ ChatInterface.jsx: Does not use correct backend URL');
  }

  if (chatInterfaceCode.includes('/api/${userId}/chat')) {
    console.log('✅ ChatInterface.jsx: Has correct chat endpoint pattern');
  } else {
    console.log('❌ ChatInterface.jsx: Missing correct chat endpoint pattern');
  }
} else {
  console.log('❌ ChatInterface.jsx: File does not exist');
}

// Test 2: Verify Task API service has correct configuration
const taskApiPath = './frontend/src/services/taskApi.js';
if (fs.existsSync(taskApiPath)) {
  const taskApiCode = fs.readFileSync(taskApiPath, 'utf8');
  if (taskApiCode.includes('https://hackathon-2-p-3-backend.vercel.app')) {
    console.log('✅ taskApi.js: Uses correct backend URL in production');
  } else {
    console.log('❌ taskApi.js: Does not use correct backend URL');
  }
} else {
  console.log('❌ taskApi.js: File does not exist');
}

// Test 3: Verify backend has the modular routes included
const backendPath = './backend/vercel_api.py';
if (fs.existsSync(backendPath)) {
  const backendCode = fs.readFileSync(backendPath, 'utf8');
  if (backendCode.includes('from src.api.chat import router as chat_router') &&
      backendCode.includes('app.include_router(chat_router)')) {
    console.log('✅ vercel_api.py: Includes modular chat router');
  } else {
    console.log('❌ vercel_api.py: Does not include modular chat router');
  }
} else {
  console.log('❌ vercel_api.py: File does not exist');
}

console.log("\nConfiguration verification complete!");
console.log("\nTo test the actual chat functionality:");
console.log("1. Deploy the updated backend code to Vercel");
console.log("2. Deploy the updated frontend code to Vercel");
console.log("3. Visit the frontend application");
console.log("4. Log in to the application");
console.log("5. Navigate to the chat page");
console.log("6. Type a message and submit it");
console.log("7. Verify that the message is processed and a response is received");