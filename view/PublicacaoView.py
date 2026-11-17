class PublicacaoView:

    def ExibirPublicacoes(self, publicacoes):
        print("\n===== PUBLICACOES DO BLOG =====")

        if not publicacoes:
            print("Nenhuma publicacao cadastrada.")
            return

        for publicacao in publicacoes:
            print("-------------------------")
            print("ID:", publicacao[0])
            print("Título:", publicacao[1])
            print("Texto:", publicacao[2])
            print("Data:", publicacao[3])

    def SolicitarDadosPublicacao(self):
        print("\n===== CRIAR PUBLICACAO =====")
        titulo = input("Titulo: ")
        texto = input("Texto: ")

        return titulo, texto

    def SolicitarId(self):
        while True:
            try:
                return int(input("Digite o ID da publicacao: "))
            except ValueError:
                print("Digite um numero valido.")

    def SolicitarTextoComentario(self):
        print("\n===== ADICIONAR COMENTARIO =====")
        return input("Digite seu comentario: ")

    def ConfirmarExclusao(self):
        resposta = input(
            "Tem certeza que deseja excluir esta publicacao? (s/n): "
        ).strip().lower()

        return resposta == "s"

    def ExibirDetalhes(self, publicacao, autor, comentarios):
        print("\n===== DETALHES DA PUBLICACAO =====")
        print("ID:", publicacao.id)
        print("Título:", publicacao.titulo)
        print("Autor:", autor)
        print("Data:", publicacao.datacriacao)
        print("\nTexto:")
        print(publicacao.texto)

        print("\n===== COMENTARIOS =====")

        if not comentarios:
            print("Nenhum comentario ainda.")
        else:
            for comentario, nomeAutor in comentarios:
                print("-------------------------")
                print("Autor:", nomeAutor)
                print("Comentario:", comentario.texto)

    def ExibirMensagem(self, mensagem):
        print(mensagem)