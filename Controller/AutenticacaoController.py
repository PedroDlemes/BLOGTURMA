
class AutenticacaoController:

    def __init__(self, usuarioService, autenticacaoView, sessaoUsuario):
        self.service = usuarioService
        self.view = autenticacaoView
        self.sessao = sessaoUsuario

    def Cadastrar(self):
        nome, email, senha = self.view.SolicitarDadosCadastro()

        sucesso, mensagem = self.service.Cadastrar(
            nome,
            email,
            senha
        )

        self.view.ExibirMensagem(mensagem)

    def Entrar(self):
        email, senha = self.view.SolicitarCredenciais()

        usuario, mensagem = self.service.Autenticar(email, senha)

        if usuario is not None:
            self.sessao.Iniciar(
                usuario["id"],
                usuario["nome"]
            )

        self.view.ExibirMensagem(mensagem)

    def Sair(self):
        self.sessao.Encerrar()
        self.view.ExibirMensagem("Voce saiu da conta.")
