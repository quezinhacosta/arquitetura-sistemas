import time
import rpyc
from rpyc.utils.server import ThreadedServer

HOST = "localhost"
PORT = 18861


class CalculadoraService(rpyc.Service):
    """
    Métodos expostos pelo servidor RPC.
    Tudo que começa com exposed_ pode ser chamado remotamente.
    """

    lista_compartilhada = []

    def exposed_somar(self, a, b):
        return a + b

    def exposed_maiusculas(self, texto):
        return str(texto).upper()

    def exposed_adicionar_item(self, item):
        self.__class__.lista_compartilhada.append(item)
        return self.__class__.lista_compartilhada

    def exposed_listar_itens(self):
        return self.__class__.lista_compartilhada

    def exposed_limpar_itens(self):
        self.__class__.lista_compartilhada.clear()
        return self.__class__.lista_compartilhada

    def exposed_demorar(self, segundos):
        """
        Simula processamento lento no servidor para mostrar RPC síncrono.
        """
        segundos = int(segundos)
        time.sleep(segundos)
        return f"Servidor demorou {segundos} segundo(s) para responder"

    def exposed_remover_item(self, texto):
        if item in self.__class__.lista_compartilhada:
            self.__class__.lista_compartilhada.remove(item)
            return f"Item '{item}' removido com sucesso! Lista atual: {self.__class__.lista_compartilhada}"
        return f"Item '{item}' não encontrado na lista. Lista atual: {self.__class__.lista_compartilhada}"

    def exposed_contar_caracteres(self, texto):
        return len(str(texto))


if __name__ == "__main__":
    print(f"Servidor RPC iniciado em {HOST}:{PORT}")
    server = ThreadedServer(CalculadoraService, hostname=HOST, port=PORT)
    server.start()