import pyodbc
from config import Config

config = Config()
class APPDB():
    def __init__(self, entities=[]):
        self.conn = pyodbc.connect(
                f'DRIVER={config.dbdriver};'
                f'SERVER={config.host};'
                f'DATABASE={config.dbname};'
                'Trusted_Connection=yes;'
                'Encrypt=yes;'
                'TrustServerCertificate=yes;'
            )
        self.cursor = self.conn.cursor()
        for entity in entities:
            self.create_table_if_not_exists(entity.lower())
        
    def create_table_if_not_exists(self, table_name):
        try:
            self.cursor.execute(f"SELECT 1 FROM {table_name}")
            
        except pyodbc.ProgrammingError as e:
            if "Invalid object name" in str(e):
                if table_name == 'trails':
                    self.cursor.execute("""
                        CREATE TABLE trails (
                            trail_id INT PRIMARY KEY IDENTITY(1,1),
                            name VARCHAR(100) UNIQUE NOT NULL,
                            description TEXT,
                            created_date DATE,
                            owner_id INT NOT NULL
                        )
                    """)
                elif table_name == 'users':
                    self.cursor.execute("""
                        CREATE TABLE users (
                            user_id INT PRIMARY KEY IDENTITY(1,1),
                            username VARCHAR(50) UNIQUE NOT NULL,
                            email VARCHAR(100) UNIQUE NOT NULL,
                            role VARCHAR(20)
                        )
                    """)
                elif table_name == 'locations':
                    self.cursor.execute("""
                        CREATE TABLE locations (
                            location_id INT PRIMARY KEY IDENTITY(1,1),
                            trail_id INT NOT NULL,
                            latitude DECIMAL(9,6) NOT NULL,
                            longitude DECIMAL(9,6) NOT NULL,
                            sequence INT NOT NULL,
                            FOREIGN KEY (trail_id) REFERENCES trails(trail_id)
                        )
                    """)
                elif table_name == 'trail_access_logs':
                    self.cursor.execute("""
                        CREATE TABLE trail_access_logs (
                            log_id INT PRIMARY KEY IDENTITY(1,1),
                            trail_id INT NOT NULL,
                            user_id INT NOT NULL,
                            access_date DATETIME NOT NULL,
                            view_type VARCHAR(20),
                            FOREIGN KEY (trail_id) REFERENCES trails(trail_id),
                            FOREIGN KEY (user_id) REFERENCES users(user_id)
                        )
                    """)
                self.conn.commit()
                print(f"Table '{table_name}' created successfully.")
            else:
                raise
            
    def create_trail(self, name, description, owner_id): 
        try:
            self.cursor.execute("""
                INSERT INTO trails (name, description, owner_id, created_date)
                VALUES (?, ?, ?, GETDATE())
            """, (name, description, owner_id))
            self.conn.commit()
            trail_id = self.cursor.execute("SELECT SCOPE_IDENTITY()").fetchone()[0]
            return {'message': 'Trail created successfully', 'trail_id': trail_id}
        except Exception as e:
            return {'error': str(e)}


    def get_trails(self):
        try:
            self.cursor.execute("SELECT * FROM trails")
            rows = self.cursor.fetchall()
            trails = [dict(zip([column[0] for column in self.cursor.description], row)) for row in rows]
            return trails
        except Exception as e:
            return {'error': str(e)}

    def get_trail(self, trail_id):
        try:
            self.cursor.execute("SELECT * FROM trails WHERE trail_id = ?", (trail_id,))
            row = self.cursor.fetchone()
            if row:
                return dict(zip([column[0] for column in self.cursor.description], row))
            return {'error': 'Trail not found'}
        except Exception as e:
            return {'error': str(e)}

    def update_trail(self, trail_id, name, description):
        try:
            self.cursor.execute("""
                UPDATE trails
                SET name = ?, description = ?
                WHERE trail_id = ?
            """, (name, description, trail_id))
            self.conn.commit()
            return {'message': 'Trail updated successfully'}
        except Exception as e:
            return {'error': str(e)}

    def delete_trail(self, trail_id):
        try:
            self.cursor.execute("DELETE FROM trails WHERE trail_id = ?", (trail_id,))
            self.conn.commit()
            return {'message': 'Trail deleted successfully'}
        except Exception as e:
            return {'error': str(e)}

    def close_connection(self):
        self.cursor.close()
        self.conn.close()       
