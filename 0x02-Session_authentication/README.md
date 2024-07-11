# 0x02. Session authentication

Session authentication is a method used in web development to manage user identities across multiple requests. When a user logs in, the server creates a unique session for that user, and then sends a cookie containing the session ID to the user's browser. For subsequent requests, the browser sends the cookie back to the server, which allows the server to identify the user and provide personalized content. This method is widely used because it's relatively secure and doesn't require the server to store the user's credentials. However, it's important to handle sessions carefully to prevent session hijacking or fixation attacks.

<aside>
💡 Session-based authentication can seem to conflict with the principle of RESTful APIS being stateless, as it requires the server to maintatin some state (the session data) between requests.

But it's important to note that the session ID itself is stateless from the server's perspective. The server doesn't need to remember the session ID between requests; it just needs to be able to validate it and look up the corresponding session data when it receives it.

Each request is still self-contained and can be processed independently, which is in line with the principles of REST.
</aside>

## Flask's session and set_cookie

Using Flask's session module is a form of session-based authentication, similar to using cookies. In this method, the server creates a session for the user after successful login and stores session ID in the user's browser as a cookie.

Flask's `session` and `set_cookie` both involve sending cookies to the client's browser, but they are used for different purposes.

Flask's `session` is a feature for storing user-specific data across multiple requests. When you store data in `session`, Flask signs the data with a secret key and sends it to the client's browser as a cookie. On subsequent requests, Flask verifies the signature and if it's valid, lets you access the data.

On the other hand, `set_cookie` is a lower-level function for setting a cookie in the client's browser. You can use it to store any data you want, but it doesn't provide any of the automatic signing or verification features that `session` does.

So, if you're storing sensitive data that needs to be secure and tamper-proof, you should use `session`. If you just need to store some non-sensitive data in the client's browser, `set_cookie` might be sufficient.

## Tasks/Files

|    Tasks       |     Files                     |
|----------------|-------------------------------|
|0. Et moi et moi et moi!|``api/v1/app.py``, ``api/v1/views/users.py``|
|1. Empty session|``api/v1/auth/session_auth.py``, ``api/v1/app.py``|
|2. Create a session|``api/v1/auth/session_auth.py``|
|3. User ID for Session ID|`api/v1/auth/session_auth.py`|
|4. Session cookie|`api/v1/auth/auth.py`|
|5. Before request|``api/v1/app.py``|
|6. Use Session ID for identifying a User|``api/v1/auth/session_auth.py``|
|7. New view for Session Authentication|``api/v1/views/session_auth.py``, ``api/v1/views/__init__.pyy``|
|8. Logout|``api/v1/auth/session_auth.py``, ``api/v1/views/session_auth.py``|
