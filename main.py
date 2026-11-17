
from Conexao import conexao
from SessaoUsuario import SessaoUsuario

from view.MenuView import MenuView
from view.PublicacaoView import PublicacaoView
from view.AutenticacaoView import AutenticacaoView

from Controller.publicacaoController import PublicacaoController
from Controller.AutenticacaoController import AutenticacaoController

from service.publicacaoservice import PublicacaoService
from service.ComentarioService import ComentarioService
from service.UsuarioService import UsuarioService


def iniciar_sistema():
    banco = conexao.Conector()

    sessaoUsuario = SessaoUsuario()

    menuView = MenuView()
    publicacaoView = PublicacaoView()
    autenticacaoView = AutenticacaoView()

    publicacaoService = PublicacaoService(banco, sessaoUsuario)
    comentarioService = ComentarioService(banco, sessaoUsuario)
    usuarioService = UsuarioService(banco)

    publicacaoController = PublicacaoController(
        publicacaoView,
        publicacaoService,
        comentarioService,
        sessaoUsuario
    )

    autenticacaoController = AutenticacaoController(
        usuarioService,
        autenticacaoView,
        sessaoUsuario
    )

    try:
        while True:
            opcao = menuView.exibir_menu()

            if opcao == "1":
                publicacaoController.Listar()

            elif opcao == "2":
                publicacaoController.Criar()

            elif opcao == "3":
                publicacaoController.Visualizar()

            elif opcao == "4":
                publicacaoController.Editar()

            elif opcao == "5":
                publicacaoController.Excluir()

            elif opcao == "6":
                publicacaoController.Comentar()

            elif opcao == "7":
                autenticacaoController.Cadastrar()

            elif opcao == "8":
                autenticacaoController.Entrar()

            elif opcao == "9":
                autenticacaoController.Sair()

            elif opcao == "0":
                print("Encerrando o blog...")
                break

            else:
                print("Opcao invalida.")

    finally:
        banco.close()


if __name__ == "__main__":
    iniciar_sistema()

