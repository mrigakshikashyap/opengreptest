import sqlite3

def get_user_data(username):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # VULNERABLE SQL QUERY: User input is directly injected into the query.
    query = "SELECT * FROM users WHERE username = '" + username + "';"

    cursor.execute(query)
    user_data = cursor.fetchall()

    conn.close()

    return user_data

# Example of how the vulnerable function could be called
username_input = input("Enter your username: ")
print(get_user_data(username_input))
