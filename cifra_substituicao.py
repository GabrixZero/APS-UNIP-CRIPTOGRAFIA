# =============================================================
# APS – Ciência da Computação | UNIP
# Disciplina: Introdução à Programação Estruturada – IPE
# Aluno: Gabriel Gomes | RA: T9250D0
# Técnica: Cifra de Substituição Simples (Keyword Cipher)
# Palavra-chave: UNIP
# =============================================================
#
# COMO USAR:
#   python cifra_substituicao.py
#
# CHAVE GERADA COM "UNIP":
#   Original: A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
#   Cifrada:  U N I P A B C D E F G H J K L M O Q R S T V W X Y Z
#
# =============================================================

import string

# Limite máximo de caracteres exigido pelo regulamento da APS
LIMITE_CARACTERES = 128


class CifradorSubstituicao:
    """
    Implementa a Cifra de Substituição Simples com chave
    gerada a partir de uma palavra-chave (keyword cipher).

    O método de palavra-chave funciona da seguinte forma:
      1. Escreve-se a palavra-chave sem letras repetidas.
      2. Completa-se com as letras restantes do alfabeto em ordem.
      3. O resultado é o alfabeto cifrado (a chave).
    """

    def __init__(self, palavra_chave: str):
        """
        Inicializa o cifrador gerando as tabelas de
        cifragem e decifragem com base na palavra-chave.

        Parâmetro:
            palavra_chave (str): A palavra usada para gerar a chave.
        """
        self.palavra_chave = palavra_chave.upper()
        self.tabela_cifrar, self.tabela_decifrar = (
            self._gerar_chave(palavra_chave)
        )

    def _gerar_chave(self, palavra_chave: str):
        """
        Gera os dicionários de cifragem e decifragem.

        Retorna:
            tuple: (tabela_cifrar, tabela_decifrar)
                   Ambas são dicionários {str: str}.
        """
        palavra_chave = palavra_chave.upper()
        alfabeto = string.ascii_uppercase  # 'ABCDE...Z'

        # Passo 1: Remover letras duplicadas da palavra-chave,
        # preservando a ordem de aparição.
        vistas = set()
        chave_limpa = []
        for letra in palavra_chave:
            if letra in alfabeto and letra not in vistas:
                chave_limpa.append(letra)
                vistas.add(letra)

        # Passo 2: Completar com as letras restantes do alfabeto
        # na ordem alfabética normal.
        for letra in alfabeto:
            if letra not in vistas:
                chave_limpa.append(letra)
                vistas.add(letra)

        # Passo 3: Construir os dicionários de mapeamento.
        # tabela_cifrar:  letra_original  → letra_cifrada
        # tabela_decifrar: letra_cifrada  → letra_original
        tabela_cifrar = {}
        tabela_decifrar = {}
        for i, letra_original in enumerate(alfabeto):
            letra_cifrada = chave_limpa[i]
            tabela_cifrar[letra_original] = letra_cifrada
            tabela_decifrar[letra_cifrada] = letra_original

        return tabela_cifrar, tabela_decifrar

    def _validar_tamanho(self, mensagem: str) -> None:
        """
        Verifica se a mensagem respeita o limite máximo de
        128 caracteres (exigência do regulamento da APS).

        Lança ValueError se o limite for excedido.
        """
        if len(mensagem) > LIMITE_CARACTERES:
            raise ValueError(
                f"\n ERRO: A mensagem possui {len(mensagem)} caracteres.\n"
                f"     O limite máximo permitido é {LIMITE_CARACTERES} "
                f"caracteres.\n"
                f"     Por favor, reduza a mensagem e tente novamente."
            )

    def _processar(self, texto: str, tabela: dict) -> str:
        """
        Percorre o texto caractere por caractere e aplica
        a tabela de substituição.

        Letras (A-Z) são substituídas conforme a tabela.
        Demais caracteres (espaços, números, pontuação)
        são mantidos inalterados.

        Parâmetros:
            texto  (str): Texto a processar.
            tabela (dict): Dicionário de mapeamento a usar.

        Retorna:
            str: Texto processado.
        """
        texto = texto.upper()
        resultado = []
        for char in texto:
            if char in tabela:
                resultado.append(tabela[char])
            else:
                resultado.append(char)  # mantém espaços, números, etc.
        return "".join(resultado)

    def cifrar(self, mensagem: str) -> str:
        """
        Cifra a mensagem usando a tabela de cifragem.

        Parâmetro:
            mensagem (str): Mensagem em texto plano (máx. 128 chars).

        Retorna:
            str: Texto cifrado.

        Lança:
            ValueError: Se a mensagem exceder 128 caracteres.
        """
        self._validar_tamanho(mensagem)
        return self._processar(mensagem, self.tabela_cifrar)

    def decifrar(self, texto_cifrado: str) -> str:
        """
        Decifra o texto cifrado usando a tabela de decifragem.

        Parâmetro:
            texto_cifrado (str): Texto cifrado (máx. 128 chars).

        Retorna:
            str: Mensagem original recuperada.

        Lança:
            ValueError: Se o texto exceder 128 caracteres.
        """
        self._validar_tamanho(texto_cifrado)
        return self._processar(texto_cifrado, self.tabela_decifrar)

    def exibir_tabela(self) -> None:
        """
        Exibe no terminal a tabela completa de substituição,
        mostrando o mapeamento letra a letra gerado pela
        palavra-chave.
        """
        print("\n" + "=" * 58)
        print(f"   TABELA DE SUBSTITUIÇÃO  –  Chave: {self.palavra_chave}")
        print("=" * 58)

        letras = list(string.ascii_uppercase)
        # Exibe em duas colunas (A-M na esquerda, N-Z na direita)
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


# =============================================================
# Interface de linha de comando (menu interativo)
# =============================================================

def separador():
    print("\n" + "-" * 58)


def menu_principal():
    """
    Interface interativa de linha de comando.
    Exibe o menu e processa as escolhas do usuário em loop
    até que ele escolha a opção de sair.
    """
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
            # ── Cifrar ────────────────────────────────────
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
            # ── Decifrar ──────────────────────────────────
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
            # ── Tabela ────────────────────────────────────
            cifrador.exibir_tabela()

        elif opcao == "4":
            # ── Sair ──────────────────────────────────────
            separador()
            print("  Programa encerrado. Até logo!")
            print("-" * 58)
            break

        else:
            print("\n Opção inválida. Por favor, escolha entre 1 e 4.")


# Ponto de entrada do programa
if __name__ == "__main__":
    menu_principal()
