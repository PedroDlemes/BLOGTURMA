
class AutenticacaoView:

    def SolicitarDadosCadastro(self):
        print("\n===== CADASTRO =====")

        nome = input("Nome: ")
        email = input("Email: ")
        senha = input("Senha: ")

        return nome, email, senha

    def SolicitarCredenciais(self):
        print("\n===== ENTRAR NA CONTA =====")

        email = input("Email: ")
        senha = input("Senha: ")

        return email, senha

    def ExibirMensagem(self, mensagem):
        print(mensagem)
