import time
import rpyc

HOST = "localhost"
PORT = 18861


def menu():
    print("\n=== CLIENTE RPC ===")
    print("1 - Somar dois números")
    print("2 - Converter texto para maiúsculas")
    print("3 - Adicionar item na lista remota")
    print("4 - Listar itens da lista remota")
    print("5 - Limpar lista remota")
    print("6 - Chamada lenta (RPC síncrono)")
    print("0 - Sair")


def main():
    try:
        conn = rpyc.connect(HOST, PORT)
        print(f"Conectado ao servidor {HOST}:{PORT}")
    except Exception as e:
        print("Não foi possível conectar ao servidor.")
        print(f"Erro: {e}")
        return

    while True:
        menu()
        opcao = input("Escolha uma opção: ").strip()

        try:
            if opcao == "1":
                a = int(input("Digite o primeiro número: "))
                b = int(input("Digite o segundo número: "))
                resultado = conn.root.somar(a, b)
                print(f"Resultado remoto: {resultado}")

            elif opcao == "2":
                texto = input("Digite um texto: ")
                resultado = conn.root.maiusculas(texto)
                print(f"Resultado remoto: {resultado}")

            elif opcao == "3":
                item = input("Digite o item a adicionar: ")
                resultado = conn.root.adicionar_item(item)
                print(f"Lista remota atual: {resultado}")

            elif opcao == "4":
                resultado = conn.root.listar_itens()
                print(f"Lista remota atual: {resultado}")

            elif opcao == "5":
                resultado = conn.root.limpar_itens()
                print(f"Lista remota após limpeza: {resultado}")

            elif opcao == "6":
                segundos = int(input("Quantos segundos o servidor deve demorar? "))
                inicio = time.time()
                resultado = conn.root.demorar(segundos)
                fim = time.time()

                print(resultado)
                print(f"Tempo total de espera no cliente: {fim - inicio:.2f} s")

            elif opcao == "0":
                print("Encerrando cliente.")
                conn.close()
                break

            else:
                print("Opção inválida.")

        except EOFError:
            print("\nConexão encerrada.")
            break
        except Exception as e:
            print(f"Erro durante a chamada remota: {e}")


if __name__ == "__main__":
    main()