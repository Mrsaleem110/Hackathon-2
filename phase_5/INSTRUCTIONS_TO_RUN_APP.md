To restart all services and verify the fix, please follow these steps:

1.  **Stop any running processes:** If you have any backend, frontend, or auth services currently running, please stop them. You might need to use `Ctrl+C` in their respective terminal windows.

2.  **Start the authentication and backend services:**
    Open a terminal in the root directory of your project (`C:\Users\Chohan Laptop's\Documents\GitHub\Hackathon-2\phase_4`) and run:
    ```bash
    npm run dev-all
    ```
    This command will concurrently start the `auth_service` and the `backend` service.

3.  **Start the frontend service:**
    Open *another* terminal window, navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```
    Then run:
    ```bash
    npm run dev
    ```
    This will start the frontend development server.

After following these steps, navigate to `http://localhost:3000` (or whatever address `vite` indicates) in your browser and check if the sign-in and sign-up functionalities are working correctly.
