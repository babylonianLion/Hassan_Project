# Simple Login Application

This is a basic web application built with Python Flask that allows users to register, login, view their dashboard, change their password, and logout. The application uses SQLite as the database to store user information and login sessions.

## Prerequisites

Before running the application, make sure you have the following installed:

- Python 3.x
- Flask

## Getting Started

1. Clone the repository to your local machine:

```bash
git clone https://github.com/babylonianLion/Hassan_Project.git
cd Hassan_Project
```

2. Install the required dependencies:

```bash
pip install flask
```

3. Run the application:

```bash
python login_backend.py
```

4. Open your web browser and visit `http://127.0.0.1:5000/` to access the login page.

## Functionality

### Login

- Users can log in with their registered username and password.
- If the login is successful, the user is redirected to their dashboard.
- If the login fails due to incorrect credentials, an error message is displayed.

### Registration

- Users can register with a unique username, password, email, and full name.

### Dashboard

- Once logged in, users can view their dashboard, which displays their username, email, and last login time.

### Change Password

- Logged-in users can change their password by providing their current password and a new password.

### Logout

- Users can log out to end their session.

## Database

The application uses SQLite as the database. The `login_database.db` file will be created in the same directory when you run the application.

## Important Note

- In this project, passwords are stored as plain text for simplicity. In a real-world application, it's essential to implement proper password hashing for security.
- For production use, consider deploying the application on a secure web server and set up SSL certificates to ensure secure communication.

## License

This project is licensed under the [MIT License](LICENSE).

## Credits

This project is created by [Hussain Al Zerjawi](https://github.com/babylonianLion).

---

Feel free to customize the README.md file to include any additional information, such as deployment instructions, project structure, or any other relevant details about your project.
