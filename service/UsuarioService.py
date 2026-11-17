
from service.SenhaService import SenhaService


class UsuarioService:

    def __init__(self, conexao):
        self.conexao = conexao
        self.senhaService = SenhaService()

    def Cadastrar(self, nome, email, senha):
        nome = nome.strip()
        email = email.strip().lower()

        if not nome or not email or not senha:
            return False, "Preencha todos os campos."

        if "@" not in email or "." not in email:
            return False, "E-mail inválido."

        if len(senha) < 8:
            return False, "A senha deve ter pelo menos 8 caracteres."

        cursor = self.conexao.cursor()

        try:
            
            cursor.execute(
                "SELECT id FROM usuario WHERE LOWER(email) = %s",
                (email,)
            )

            if cursor.fetchone():
                return False, "Este e-mail já está cadastrado."

            # Gera o hash da senha
            hashSenha = self.senhaService.GerarHash(senha)

            
            cursor.execute(
                """
                INSERT INTO usuario (nome, email, senhahash)
                VALUES (%s, %s, %s)
                """,
                (nome, email, hashSenha)
            )

            self.conexao.commit()

            return True, "Conta cadastrada com sucesso!"

        except Exception as erro:
            self.conexao.rollback()
            return False, f"Erro ao cadastrar: {erro}"

        finally:
            cursor.close()

    def Autenticar(self, email, senha):
        email = email.strip().lower()

        if not email or not senha:
            return None, "Informe o e-mail e a senha."

        cursor = self.conexao.cursor()

        try:
           
            cursor.execute(
                """
                SELECT id, nome, senhahash
                FROM usuario
                WHERE LOWER(email) = %s
                """,
                (email,)
            )

            usuario = cursor.fetchone()

            if not usuario:
                return None, "E-mail ou senha incorretos."

            idUsuario, nomeUsuario, hashSenha = usuario

           
            if not self.senhaService.Verificar(senha, hashSenha):
                return None, "E-mail ou senha incorretos."

            return {
                "id": idUsuario,
                "nome": nomeUsuario
            }, "Login realizado com sucesso!"

        except Exception:
            return None, "Não foi possível realizar o login."

        finally:
            cursor.close()
