import mysql.connector

class conexao:

    @staticmethod
    def Conector():
        return mysql.connector.connect(
            host="localhost",
            port=3310,
            user="root",
            password="",
            database="blog_turma"
        )