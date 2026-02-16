To apply the fix and restart your services using Docker, please follow these steps:

1.  **Stop and remove existing Docker containers (if running):**
    Open a terminal in the root directory of your project (`C:\Users\Chohan Laptop's\Documents\GitHub\Hackathon-2\phase_4`) and run:
    ```bash
    docker-compose down
    ```
    This command will stop and remove all containers, networks, and volumes associated with your `docker-compose.yml` file.

2.  **Rebuild the `auth_service` and `frontend` images and restart all services:**
    After stopping the containers, rebuild the `auth_service` image (to incorporate the `Dockerfile` change) and restart all services:
    ```bash
    docker-compose up --build
    ```
    The `--build` flag will ensure that Docker rebuilds the images, specifically the `auth_service` image where we made the `Dockerfile` change and the `frontend` image where we made the `package.json` change (which is implied to be needed because the package.json was changed. It's better to rebuild both of them).

    If you want to run them in detached mode (in the background), you can add `-d`:
    ```bash
    docker-compose up --build -d
    ```

After the containers are up and running, navigate to `http://localhost:3000` in your browser and check if the sign-in and sign-up functionalities are working as expected.
