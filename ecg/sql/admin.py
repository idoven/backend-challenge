CREATE_USERS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL ,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL
);

"""

CREATE_USER_QUERY = """
INSERT INTO users (id, email, password, role)
VALUES (:id, :email, :password, :role)
RETURNING id, email, password, role;
"""

GET_USER_QUERY = """
SELECT id, email, password, role
FROM users
WHERE email = :email;
"""

DELETE_USER_QUERY = """
DELETE FROM users
WHERE email = :email;
"""
