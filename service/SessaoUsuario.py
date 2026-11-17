class SessaoUsuario:

    def __init__(self):
        self.UsuarioId = None
        self.NomeUsuario = None

    @property
    def EstaAutenticado(self):
        return self.UsuarioId is not None

    def Iniciar(self, usuarioId, nomeUsuario):
        self.UsuarioId = usuarioId
        self.NomeUsuario = nomeUsuario

    def Encerrar(self):
        self.UsuarioId = None
        self.NomeUsuario = None
