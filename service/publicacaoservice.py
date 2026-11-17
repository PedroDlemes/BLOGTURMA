
from Publicacao import Publicacao


class PublicacaoService:

    def __init__(self, conexao, sessao):
        self.conexao = conexao
        self.sessao = sessao

    def ListarRecentes(self):
        cursor = self.conexao.cursor()

        try:
            sql = """
                SELECT id_publicacao, titulo, texto, data_publicacao
                FROM publicacoes
                ORDER BY data_publicacao DESC
            """

            cursor.execute(sql)
            return cursor.fetchall()

        finally:
            cursor.close()

    def Criar(self, titulo, texto):
        usuarioId = self.ObterUsuarioAutenticado()

        if usuarioId is None:
            return False

        self.ValidarDados(titulo, texto)

        cursor = self.conexao.cursor()

        try:
            sql = """
                INSERT INTO publicacoes
                (titulo, texto, usuarioId)
                VALUES (%s, %s, %s)
            """

            cursor.execute(sql, (
                titulo.strip(),
                texto.strip(),
                usuarioId
            ))

            self.conexao.commit()
            return True

        except Exception:
            self.conexao.rollback()
            return False

        finally:
            cursor.close()

    def ObterPorId(self, id):
        cursor = self.conexao.cursor()

        try:
            sql = """
                SELECT id_publicacao, titulo, texto, data_publicacao
                FROM publicacoes
                WHERE id_publicacao = %s
            """

            cursor.execute(sql, (id,))
            resultado = cursor.fetchone()

            if resultado is None:
                return None

            return Publicacao(
                resultado[0],
                resultado[1],
                resultado[2],
                resultado[3]
            )

        finally:
            cursor.close()

    def ObterNomeAutor(self, id):
        cursor = self.conexao.cursor()

        try:
            sql = """
                SELECT u.nome
                FROM usuario u
                INNER JOIN publicacoes p ON p.usuarioId = u.id
                WHERE p.id_publicacao = %s
            """

            cursor.execute(sql, (id,))
            resultado = cursor.fetchone()

            if resultado:
                return resultado[0]

            return None

        finally:
            cursor.close()

    def Editar(self, id, titulo, texto):
        usuarioId = self.ObterUsuarioAutenticado()

        if usuarioId is None:
            return False

        self.ValidarDados(titulo, texto)

        cursor = self.conexao.cursor()

        try:
            self.conexao.start_transaction()

            self.VerificarAutoria(
                id,
                usuarioId,
                self.conexao,
                cursor
            )

            sql = """
                UPDATE publicacoes
                SET titulo = %s, texto = %s
                WHERE id_publicacao = %s
            """

            cursor.execute(sql, (
                titulo.strip(),
                texto.strip(),
                id
            ))

            self.conexao.commit()
            return True

        except Exception:
            self.conexao.rollback()
            return False

        finally:
            cursor.close()

    def Excluir(self, id):
        usuarioId = self.ObterUsuarioAutenticado()

        if usuarioId is None:
            return False

        cursor = self.conexao.cursor()

        try:
            self.conexao.start_transaction()

            self.VerificarAutoria(
                id,
                usuarioId,
                self.conexao,
                cursor
            )

            sql = """
                DELETE FROM publicacoes
                WHERE id_publicacao = %s
            """

            cursor.execute(sql, (id,))

            self.conexao.commit()
            return True

        except Exception:
            self.conexao.rollback()
            return False

        finally:
            cursor.close()

    def ValidarDados(self, titulo, texto):
        if not titulo or not titulo.strip():
            raise ValueError("O titulo e obrigatorio.")

        if not texto or not texto.strip():
            raise ValueError("O texto e obrigatorio.")

    def ObterUsuarioAutenticado(self):
        if not self.sessao.EstaAutenticado:
            return None

        return self.sessao.UsuarioId

    def VerificarAutoria(self, idPublicacao, idUsuario,
                         conexao, transacao):

        sql = """
            SELECT usuarioId
            FROM publicacoes
            WHERE id_publicacao = %s
            FOR UPDATE
        """

        transacao.execute(sql, (idPublicacao,))
        resultado = transacao.fetchone()

        if resultado is None or resultado[0] != idUsuario:
            raise PermissionError(
                "Voce nao e o autor desta publicacao."
            )
