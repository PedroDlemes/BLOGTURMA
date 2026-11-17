
from Comentario import Comentario


class ComentarioService:

    def __init__(self, conexao, sessao):
        self.conexao = conexao
        self.sessao = sessao

    def Adicionar(self, idPublicacao, texto):
        if not self.sessao.EstaAutenticado:
            return False

        if not texto or not texto.strip():
            return False

        cursor = self.conexao.cursor()

        try:
            sql = """
                INSERT INTO comentarios
                (texto, publicacaoId, usuarioId)
                VALUES (%s, %s, %s)
            """

            cursor.execute(sql, (
                texto.strip(),
                idPublicacao,
                self.sessao.UsuarioId
            ))

            self.conexao.commit()
            return True

        except Exception:
            self.conexao.rollback()
            return False

        finally:
            cursor.close()

    def ListarPorPublicacao(self, id):
        cursor = self.conexao.cursor()

        try:
            sql = """
                SELECT c.id, c.texto, u.nome
                FROM comentarios c
                INNER JOIN usuario u ON c.usuarioId = u.id
                WHERE c.publicacaoId = %s
                ORDER BY c.dataCriacao ASC
            """

            cursor.execute(sql, (id,))
            resultados = cursor.fetchall()

            comentarios = []

            for resultado in resultados:
                comentario = Comentario(
                    resultado[0],
                    resultado[1]
                )

                nomeAutor = resultado[2]

                comentarios.append((comentario, nomeAutor))

            return comentarios

        finally:
            cursor.close()
