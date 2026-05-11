import string

LIMITE_CARACTERES = 128


class CifradorSubstituicao:

    def __init__(self, palavra_chave: str):
        self.palavra_chave = palavra_chave.upper()
        self.tabela_cifrar, self.tabela_decifrar = (
            self._gerar_chave(palavra_chave)
        )

    def _gerar_chave(self, palavra_chave: str):
        palavra_chave = palavra_chave.upper()
        alfabeto = string.ascii_uppercase

        vistas = set()
        chave_limpa = []
        for letra in palavra_chave:
            if letra in alfabeto and letra not in vistas:
                chave_limpa.append(letra)
                vistas.add(letra)

        for letra in alfabeto:
            if letra not in vistas:
                chave_limpa.append(letra)
                vistas.add(letra)

        tabela_cifrar = {}
        tabela_decifrar = {}
        for i, letra_original in enumerate(alfabeto):
            letra_cifrada = chave_limpa[i]
            tabela_cifrar[letra_original] = letra_cifrada
            tabela_decifrar[letra_cifrada] = letra_original

        return tabela_cifrar, tabela_decifrar

    def _validar_tamanho(self, mensagem: str) -> None:
        if len(mensagem) > LIMITE_CARACTERES:
            raise ValueError(
                f"\n ERRO: A mensagem possui {len(mensagem)} caracteres.\n"
                f"     O limite máximo permitido é {LIMITE_CARACTERES} "
                f"caracteres.\n"
                f"     Por favor, reduza a mensagem e tente novamente."
            )

    def _processar(self, texto: str, tabela: dict) -> str:
        texto = texto.upper()
        resultado = []
        for char in texto:
            if char in tabela:
                resultado.append(tabela[char])
            else:
                resultado.append(char)
        return "".join(resultado)

    def cifrar(self, mensagem: str) -> str:
        self._validar_tamanho(mensagem)
        return self._processar(mensagem, self.tabela_cifrar)

    def decifrar(self, texto_cifrado: str) -> str:
        self._validar_tamanho(texto_cifrado)
        return self._processar(texto_cifrado, self.tabela_decifrar)

    def exibir_tabela(self) -> None:
        print("\n" + "=" * 58)
        print(f"   TABELA DE SUBSTITUIÇÃO  –  Chave: {self.palavra_chave}")
        print("=" * 58)

        letras = list(string.ascii_uppercase)
        metade = len(letras) // 2
        print(f"  {'Original':<8} {'Cifrada':<10}  {'Original':<8} {'Cifrada'}")
        print("  " + "-" * 52)
        for i in range(metade):
            orig1 = letras[i]
            cifr1 = self.tabela_cifrar[orig1]
            orig2 = letras[i + metade]
            cifr2 = self.tabela_cifrar[orig2]
            print(f"    {orig1:<8}   {cifr1:<12}  {orig2:<8}   {cifr2}")

        print("=" * 58)
        print("  Caracteres não-alfabéticos (espaços, números,")
        print("  pontuação) NÃO são cifrados – mantidos como estão.")
        print("=" * 58)


def separador():
    print("\n" + "-" * 58)


def menu_principal():
    PALAVRA_CHAVE = "UNIP"
    cifrador = CifradorSubstituicao(PALAVRA_CHAVE)

    print("\n" + "=" * 58)
    print("  CIFRA DE SUBSTITUIÇÃO SIMPLES – APS UNIP 2026")
    print("  Aluno : Gabriel Gomes  |  RA: T9250D0")
    print(f"  Chave : gerada a partir de '{PALAVRA_CHAVE}'")
    print(f"  Limite: {LIMITE_CARACTERES} caracteres por mensagem")
    print("=" * 58)

    while True:
        print("\n  MENU PRINCIPAL")
        print("  ┌────────────────────────────────────┐")
        print("  │  [1]  Cifrar mensagem               │")
        print("  │  [2]  Decifrar mensagem              │")
        print("  │  [3]  Exibir tabela de substituição  │")
        print("  │  [4]  Sair                           │")
        print("  └────────────────────────────────────┘")
        print()

        opcao = input("  Escolha uma opção (1-4): ").strip()

        if opcao == "1":
            separador()
            print(f"  CIFRAR MENSAGEM (máx. {LIMITE_CARACTERES} caracteres)")
            mensagem = input("  Digite a mensagem:\n  > ")
            try:
                resultado = cifrador.cifrar(mensagem)
                separador()
                print(f"  Mensagem original : {mensagem.upper()}")
                print(f"  Texto cifrado     : {resultado}")
                print(f"  Total de chars    : {len(mensagem)}")
            except ValueError as erro:
                print(str(erro))

        elif opcao == "2":
            separador()
            print(f"  DECIFRAR MENSAGEM (máx. {LIMITE_CARACTERES} caracteres)")
            texto = input("  Digite o texto cifrado:\n  > ")
            try:
                resultado = cifrador.decifrar(texto)
                separador()
                print(f"  Texto cifrado      : {texto.upper()}")
                print(f"  Mensagem original  : {resultado}")
                print(f"  Total de chars     : {len(texto)}")
            except ValueError as erro:
                print(str(erro))

        elif opcao == "3":
            cifrador.exibir_tabela()

        elif opcao == "4":
            separador()
            print("  Programa encerrado. Até logo!")
            print("-" * 58)
            break

        else:
            print("\n Opção inválida. Por favor, escolha entre 1 e 4.")


if __name__ == "__main__":
    menu_principal()
