# User database for authentication and permissions
# Format: username: {"password": ..., "role": ..., "permissions": {"filename": "rwx"}}

USERS = {
    "admin": {
        "password": "adminpass",
        "role": "admin",
        "permissions": {"*": "rwx"}  # admin can do everything
    },
    "user1": {
        "password": "user1pass",
        "role": "user",
        "permissions": {"public.txt": "rw"}
    },
    "user2": {
        "password": "user2pass",
        "role": "user",
        "permissions": {"public.txt": "r", "notes.txt": "rw"}
    }
}

def authenticate(username, password):
    user = USERS.get(username)
    if user and user["password"] == password:
        return user
    return None

def check_permission(user, filename, mode):
    # mode: 'r', 'w', or 'x'
    if user["role"] == "admin":
        return True
    perms = user["permissions"]
    if filename in perms:
        return mode in perms[filename]
    if "*" in perms:
        return mode in perms["*"]
    return False
