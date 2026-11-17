
from service.publicacaoservice import PublicacaoService
from service.ComentarioService import ComentarioService


class PublicacaoController:

    def __init__(self, publicacaoView, publicacaoService,
                 comentarioService, sessaoUsuario):

        self.view = publicacaoView
        self.service = publicacaoService
        self.comentarioService = comentarioService
        self.sessao = sessaoUsuario

    def Listar(self):
        publicacoes = self.service.ListarRecentes()
        self.view.ExibirPublicacoes(publicacoes)
        return publicacoes

    def Criar(self):
        if not self.VerificarSessao():
            return

        titulo, texto = self.view.SolicitarDadosPublicacao()

        try:
            sucesso = self.service.Criar(titulo, texto)

            if sucesso:
                self.view.ExibirMensagem("Publicacao criada com sucesso!")
            else:
                self.view.ExibirMensagem("Nao foi possivel criar a publicacao.")

        except ValueError as erro:
            self.view.ExibirMensagem(str(erro))

    def Visualizar(self):
        idPublicacao = self.view.SolicitarId()

        publicacao = self.service.ObterPorId(idPublicacao)

        if publicacao is None:
            self.view.ExibirMensagem("Publicacao nao encontrada.")
            return

        autor = self.service.ObterNomeAutor(idPublicacao)

        comentarios = self.comentarioService.ListarPorPublicacao(
            idPublicacao
        )

        self.view.ExibirDetalhes(
            publicacao,
            autor,
            comentarios
        )

    def Editar(self):
        if not self.VerificarSessao():
            return

        idPublicacao = self.view.SolicitarId()

        publicacao = self.service.ObterPorId(idPublicacao)

        if publicacao is None:
            self.view.ExibirMensagem("Publicacao nao encontrada.")
            return

        titulo, texto = self.view.SolicitarDadosPublicacao()

        try:
            sucesso = self.service.Editar(
                idPublicacao,
                titulo,
                texto
            )

            if sucesso:
                self.view.ExibirMensagem("Publicacao editada com sucesso!")
            else:
                self.view.ExibirMensagem(
                    "Nao foi possivel editar a publicacao."
                )

        except ValueError as erro:
            self.view.ExibirMensagem(str(erro))

    def Excluir(self):
        if not self.VerificarSessao():
            return

        idPublicacao = self.view.SolicitarId()

        if not self.view.ConfirmarExclusao():
            self.view.ExibirMensagem("Exclusao cancelada.")
            return

        sucesso = self.service.Excluir(idPublicacao)

        if sucesso:
            self.view.ExibirMensagem("Publicacao excluida com sucesso!")
        else:
            self.view.ExibirMensagem(
                "Nao foi possivel excluir a publicacao."
            )

    def Comentar(self):
        if not self.VerificarSessao():
            return

        idPublicacao = self.view.SolicitarId()

        publicacao = self.service.ObterPorId(idPublicacao)

        if publicacao is None:
            self.view.ExibirMensagem("Publicacao nao encontrada.")
            return

        texto = self.view.SolicitarTextoComentario()

        sucesso = self.comentarioService.Adicionar(
            idPublicacao,
            texto
        )

        if sucesso:
            self.view.ExibirMensagem("Comentario adicionado com sucesso!")
        else:
            self.view.ExibirMensagem("Nao foi possivel adicionar o comentario.")

    def VerificarSessao(self):
        if not self.sessao.EstaAutenticado:
            self.view.ExibirMensagem(
                "Voce precisa entrar na conta para realizar esta acao."
            )
            return False

        return True
