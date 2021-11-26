import random

# VARIÁVEIS DO PROGRAMA - MEXA APENAS AQUI
inp = input('Nome do arquivo: ') # nome do arquivo de entrada
intended_amplitude = 1           # amplitude de porcentagens desejada. Ex: 2 aceitará, no pior caso, R-32%, S-33%, T-34%
total_phs_employed = 3           # número de fases do quadro
iterations_per_amplitude = 1000  # tentativas em cada amplitude.Ex. depois de 1000 tentativas, a amplitude 1 é aumentada para 2.
##################################


def zero_vector():
    """Produz um vetor nulo de comprimento igual ao número de fases da instalação"""
    return [0 for i in range(total_phs_employed)]


main_list = []


def read_input(inp):
    """Lê o arquivo de entrada e adiciona seus dados a uma variável"""
    with open(inp) as in_file:
        electric_panel = in_file.readlines()
        for circuit in electric_panel:
            circuit = circuit.split()           # separação das linhas em listas
            circuit.append(zero_vector())   # inserção de vetor nulo, que depois será preenchido com a potência 
            main_list.append(circuit)       # de cada fase naquele circuito.
      

def export_to_output(inp):
    """Exporta o balanceamento de cargas para um aquivo .txt"""
    with open(inp.replace('.txt', '')+'_out.txt', 'w') as out_file:
        for circuit in main_list:
            for power in circuit[2]:
                formatted_value = str(f'{power:.1f}').replace(".", ",")
                out_file.write(f'{formatted_value}\t')
            out_file.write('\n')      
        
    
read_input(inp)
amplitude = 100
_round = 0      # número da tentativa atual
while amplitude > intended_amplitude:
    if _round != 0 and _round % iterations_per_amplitude == 0:  # A amplitude mínima é aumentada a cada 'iterations_per_amplitude' tentativas,
        intended_amplitude += 1                                 # para que o programa não trave num loop infinito
        print(f'Aumentando a margem de desigualdade para {intended_amplitude} pontos percentuais')
    ph_powers = zero_vector()   # esse vetor será preenchido com as potências de cada fase na tentativa atual
    for circuit in main_list:     # trecho para preenchimento aleatório das potências
        circuit[2] = zero_vector()       # reset das potências de cada fase do circuito em questão
        circuit_ph_amount = int(circuit[1])    # quantidade de fases a serem preenchidas no circuito da linha em questão
        for number in range(circuit_ph_amount):  # preenchimento aleatório de 'circuit_ph_amount' fases do circuito atual
            while True:
                ph_index = random.randint(0, total_phs_employed-1)  # sorteio de uma fase para ser preenchida
                if not circuit[2][ph_index]:  # se a fase não estiver ocupada, então ela é utilizada
                    circuit[2][ph_index] = int(circuit[0]) / int(circuit[1])  # inserção da potência na fase escolhida
                    ph_powers[ph_index] += int(circuit[0]) / int(circuit[1])  # incremento da potência total da fase em questão
                    break
    total_power = sum(ph_powers)  # potência total do quadro
    for index, value in enumerate(ph_powers):  # cálculo das porcentagens de cada fase
        ph_powers[index] = 100 * value / total_power
    amplitude = max(ph_powers) - min(ph_powers) # cálculo da amplitude das porcentagens (métrica de parada)
    _round += 1      # incremento do número de tentativas


#print('Distribuição de fases')    
#[print(circuit[2]) for circuit in main_list]
print(f'Porcentagem de cada fase: {ph_powers}')
print(f'Amplitude atingida: {amplitude} pontos percentuais')
print(f'Nº de tentativas: {_round}')
input('Pressione qualquer tecla para finalizar ')
export_to_output(inp)












