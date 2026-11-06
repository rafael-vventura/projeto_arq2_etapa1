class ULA:
    def __init__(self, bits=32):
        # Mascara para limitar os resultados ao tamanho de 32 bits (0xFFFFFFFF)
        self.limite_32bits = (1 << bits) - 1

    def operar(self, f0, f1, inva, inc, entrada_a, entrada_b):
        # Aplica a inversao bit a bit na entrada A caso o sinal INVA esteja ativo
        if inva == 1:
            entrada_a = (~entrada_a) & self.limite_32bits

        # Combina F0 e F1 em um seletor de 0 a 3 (00=0, 01=1, 10=2, 11=3)
        seletor = (f0 << 1) | f1
        vai_um = 0

        if seletor == 0:      # 00: AND logico
            saida = entrada_a & entrada_b
        elif seletor == 1:    # 01: OR logico
            saida = entrada_a | entrada_b
        elif seletor == 2:    # 10: Passa B (ou (~entrada_b) & self.limite_32bits para NOT B)
            saida = entrada_b
        else:                 # 11: Soma aritmetica (A + B + INC)
            soma_bruta = entrada_a + entrada_b + inc
            saida = soma_bruta & self.limite_32bits
            if soma_bruta > self.limite_32bits:
                vai_um = 1

        return saida, vai_um