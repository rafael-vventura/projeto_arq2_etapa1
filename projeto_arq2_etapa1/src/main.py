from pathlib import Path
from ula import ULA

class SimuladorEtapa1:
    def __init__(self):
        self.pc = 0
        self.ir = 0
        # Estado inicial fixo definido para a Etapa 1
        self.reg_a = 0xFFFFFFFF
        self.reg_b = 0x00000001
        self.saida_s = 0
        self.co = 0
        self.ula = ULA()

        # Define os caminhos de entrada e saida
        pasta_raiz = Path(__file__).parent.parent
        self.caminho_entrada = pasta_raiz / 'data' / 'arquivo.txt'
        self.caminho_log = pasta_raiz / 'logs' / 'log.txt'
        self.caminho_log.parent.mkdir(parents=True, exist_ok=True)

    def separar_sinais(self):
        # Isola cada um dos 6 bits da instrucao (F0, F1, ENA, ENB, INVA, INC)
        f0   = (self.ir >> 5) & 1
        f1   = (self.ir >> 4) & 1
        ena  = (self.ir >> 3) & 1
        enb  = (self.ir >> 2) & 1
        inva = (self.ir >> 1) & 1
        inc  = (self.ir >> 0) & 1
        return f0, f1, ena, enb, inva, inc

    def executar_ciclo(self, arquivo_log):
        f0, f1, ena, enb, inva, inc = self.separar_sinais()

        # Define os valores efetivos que entram na ULA conforme ENA e ENB
        a_efetivo = self.reg_a if ena == 1 else 0
        b_efetivo = self.reg_b if enb == 1 else 0

        self.pc += 1
        self.saida_s, self.co = self.ula.operar(f0, f1, inva, inc, a_efetivo, b_efetivo)

        # Registra o estado do ciclo atual no log
        arquivo_log.write("=" * 60 + "\n")
        arquivo_log.write(f"Cycle {self.pc}\n\n")
        arquivo_log.write(f"PC = {self.pc}\n")
        arquivo_log.write(f"IR = {self.ir:06b}\n")
        arquivo_log.write(f"b = {b_efetivo:032b}\n")
        arquivo_log.write(f"a = {a_efetivo:032b}\n")
        arquivo_log.write(f"s = {self.saida_s:032b}\n")
        arquivo_log.write(f"co = {self.co}\n")

    def rodar(self):
        # Abre o arquivo de log uma unica vez durante toda a simulacao
        with open(self.caminho_log, 'w') as log:
            log.write(f"b = {self.reg_b:032b}\n")
            log.write(f"a = {self.reg_a:032b}\n\n")
            log.write("Start of Program\n")

            with open(self.caminho_entrada, 'r') as entrada:
                for linha in entrada:
                    linha = linha.strip()
                    if linha:
                        self.ir = int(linha, 2)
                        self.executar_ciclo(log)

            # Grava o encerramento do programa (EOP)
            log.write("=" * 60 + "\n")
            log.write(f"Cycle {self.pc + 1}\n\n")
            log.write(f"PC = {self.pc + 1}\n")
            log.write("> Line is empty, EOP.\n")

if __name__ == "__main__":
    simulador = SimuladorEtapa1()
    simulador.rodar()