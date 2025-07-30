import sqlite3

# VULNERABLE SETUP - Insecure DB initialization
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# No input sanitization, unsafe schema creation
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, email TEXT);")
cursor.execute("CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY, log TEXT);")
conn.commit()

def create_user(username, password, email):
    # VULNERABILITY 1: Full SQL injection possible
    query = f"INSERT INTO users (username, password, email) VALUES ('{username}', '{password}', '{email}');"
    cursor.execute(query)
    conn.commit()

def get_user_data(username):
    # VULNERABILITY 2: Unsanitized input
    query = "SELECT * FROM users WHERE username = '" + username + "';"
    cursor.execute(query)
    return cursor.fetchall()

def delete_user(user_id):
    # VULNERABILITY 3: Type confusion + SQL injection via ID
    query = f"DELETE FROM users WHERE id = {user_id};"
    cursor.execute(query)
    conn.commit()

def search_users(term):
    # VULNERABILITY 4: LIKE with unsanitized input
    query = "SELECT * FROM users WHERE username LIKE '%" + term + "%';"
    cursor.execute(query)
    return cursor.fetchall()

def log_action(action):
    # VULNERABILITY 5: Log injection
    query = f"INSERT INTO logs (log) VALUES ('{action}');"
    cursor.execute(query)
    conn.commit()

def get_email_by_username(username):
    # VULNERABILITY 6: Info disclosure via unsanitized SELECT
    query = f"SELECT email FROM users WHERE username = '{username}';"
    cursor.execute(query)
    return cursor.fetchone()

def authenticate(username, password):
    # VULNERABILITY 7: Auth bypass via injection
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}';"
    cursor.execute(query)
    return cursor.fetchone()

def change_email(user_id, new_email):
    # VULNERABILITY 8: Insecure UPDATE
    query = f"UPDATE users SET email = '{new_email}' WHERE id = {user_id};"
    cursor.execute(query)
    conn.commit()

def get_all_logs():
    # VULNERABILITY 9: Exposes sensitive data
    query = "SELECT * FROM logs;"
    cursor.execute(query)
    return cursor.fetchall()

def run_admin_query(raw_query):
    # VULNERABILITY 10: Arbitrary SQL execution
    cursor.execute(raw_query)
    return cursor.fetchall()

def get_all_users(order_by):
    # VULNERABILITY 11: ORDER BY injection
    query = f"SELECT * FROM users ORDER BY {order_by};"
    cursor.execute(query)
    return cursor.fetchall()

def insecure_search(query_fragment):
    # VULNERABILITY 12: Poorly concatenated WHERE clause
    query = f"SELECT * FROM users WHERE {query_fragment};"
    cursor.execute(query)
    return cursor.fetchall()

def batch_insert(user_list):
    # VULNERABILITY 13: No input validation in loop
    for user in user_list:
        query = f"INSERT INTO users (username, password, email) VALUES ('{user[0]}', '{user[1]}', '{user[2]}');"
        cursor.execute(query)
    conn.commit()

def drop_table(table_name):
    # VULNERABILITY 14: Dangerous DDL with unvalidated input
    query = f"DROP TABLE {table_name};"
    cursor.execute(query)
    conn.commit()

def update_password_by_username(username, new_password):
    # VULNERABILITY 15: SQL injection in UPDATE
    query = f"UPDATE users SET password = '{new_password}' WHERE username = '{username}';"
    cursor.execute(query)
    conn.commit()

# === DEMO CALLS ===
username_input = input("Enter your username: ")
print(get_user_data(username_input))

search_term = input("Search username term: ")
print(search_users(search_term))

auth_user = input("Username for login: ")
auth_pass = input("Password for login: ")
print(authenticate(auth_user, auth_pass))

raw_sql = input("Enter raw SQL to run (admin only!): ")
print(run_admin_query(raw_sql))

order_by = input("Enter column to order users by: ")
print(get_all_users(order_by))
