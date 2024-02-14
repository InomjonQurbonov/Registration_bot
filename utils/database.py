import sqlite3

class Database:
    def __init__(self,db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        
    def add_new_user(self, tg_id, username, f_name, l_name):
        try:
            self.cursor.execute(
                "INSERT INTO users(tg_username,tg_firstname,tg_lastname,tg_id) VALUES(?,?,?,?);",
                (username, f_name, l_name,tg_id)
            )
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error adding user: {e}")

    def update_user(self, tg_id, full_name, phone):
        try:
            self.cursor.execute(
                "UPDATE users SET full_name=?, tg_phone=?"
                "WHERE tg_id=?;",(full_name, phone, tg_id)
            )
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error updating user: {e}")

    def get_users(self, tg_id):
        try:
            user = self.cursor.execute("SELECT * FROM users WHERE tg_id=?;", (tg_id,))
            return user.fetchone()
        except sqlite3.Error as e:
            print(f"Error getting user: {e}")
            
    def update_user_email(self,tg_id,email):
        try:
            self.cursor.execute(
                "UPDATE users SET email=?"
                "WHERE tg_id=?;", (email,tg_id)
                )
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error updating user: {e}")
            
    def update_user_birt_year(self,tg_id,birth_year):
        try:
            self.cursor.execute(
                "UPDATE users SET birth_year=?"
                "WHERE tg_id=?;", (birth_year,tg_id)
                )
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error updating user: {e}")


    def close_connection(self):
        self.cursor.close()
        self.connection.close()