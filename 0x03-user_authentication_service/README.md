# 0x03. User authentication service

User authentication in Flask, is a crucial aspect of many web applications. It's used to identify who is interacting with your application and to restrict access to certain parts of your application to authorized users.
Flask doesn't come with built-in user authentication functionality, but there are extensions like Flask-Login and Flask-Security that can be used to handle user authentication.
Flask-Login provides user session management, remembering the user's logged-in state across requests. It also provides the @login_required decorator to restrict access to certain views to authenticated users.
Flask-Security is a more feature-complete solution, providing not just session management but also other features like password hashing and reset functionality.
Remember, when implementing user authentication, it's important to store passwords securely. Never store passwords in plain text. Always use a strong hashing algorithm to hash the password before storing it.

## Tasks/Files


|    Tasks       |     Files                     |
|----------------|-------------------------------|
|0. User model|``user.py``|
|1. create user|``db.py``, ``api/v1/app.py``|
|2. Find user|``db.py``|
|3. update user|`db.py`|
|4. Hash password|`auth.py`|
|5. Register user|``auth.py``|
|6. Basic Flask app|``app.py``|
|7. Register user|``app.pyy``|
|8. Credentials validation|``api/v1/auth/session_auth.py``, ``api/v1/views/session_auth.py``|
|9. Generate UUIDs |``auth.py``|
|10. Get session ID | ``auth.py``|
|11. Log in | ``app.py``|
|12.  Find user by session ID | ``auth.py``|
|13.  Destroy session |``auth.py``|
|14.  Log out | ``app.py``|
|15.  User profile | ``app.py``|
|16.  Generate reset password token | ``auth.py``|
|17.  Get reset password token | ``app.py``|
|18.  Update password | ``auth.py``|
|19.  Update password end-point | ``app.py``|
