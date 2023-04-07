import math

# Preliminary Treatment
def DesignBarScreens(
    s,
    b,
    Q,
    h_min,
    h_max,
    alfa,
    beta,
    h_free=0.20,
    g=9.81,
    opening_area_bs_min=1.7,
    v_bs_max=10,
    logs=False
):
    '''
    Dimensionar gradeamento conforme a NBR 12213/92
    
    Material de consulta para entender o processo:
    https://youtu.be/Mwie0uUNAxM

    s = Largura da barra - cm
    b = Espaçamento livre - cm
    Q = Vazão de entrada - L/s
    hmin = Altura mínima do nível d'água - m
    hmax = Altura máxima do nível d'água - m
    alfa = Inclinação do gradeamento - graus
    beta = coeficiente que compõe o k referente ao tipo de barra
    h = altura de borda livre - m
    g = aceleração da gravidade - m/s²
    opening_area_bs_min = área mínima de abertura de telas de barra - cm².min/L
    v_bs_max = velocidade máxima no gradeamento - cm/s
    '''

    import math
    report = {        
        'Q':Q,
        's':s,
        'b':b,
        'h_min':h_min,
        'h_max':h_max,
        'alfa':alfa,
        'beta':beta
    }

    # Processamento
    
    # Conversão de unidades para o SI
    s = s*1e-2
    b = b*1e-2
    Q = Q*1e-3
    alfa = math.radians(alfa)

    # Requisitos mínimos
    # Área ùtil máxina - m
    Au = opening_area_bs_min*(Q*60000)*1e-4
    # Largura Útil - m
    Bu = Au/h_min
    # Velocidade no gradeamento - cm/s
    v_bs = (Q/Au)*100

    # Gradeamento
    # Número de barras de espessura b
    n = (Bu/b) + 1
    n_real = math.ceil(n)
    # Largura total do canal - m
    B = (n_real*s) + (n_real-1)*b
    # Altura total do canal - m
    H = h_max + h_free
    # Comprimento da grade - m
    L = H/math.sin(alfa)

    # Verificação da perda de carga
    # Velocidade com 50% de oclusão no gradeamento
    v = Q/(B*h_min*0.5)
    # Perda de carga
    k = beta*((s/b)**1.33)*math.sin(alfa)
    h_loss = (k*(v**2))/2*g

    if logs:
        print('RESULTADOS'.center(50,'#'))

        print('REQUISITOS MÍNIMOS'.center(50,'-'))
        print(f'Área útil (mínimo de {opening_area_bs_min} cm².min/L): {round(Au,3)} m²')
        print(f'Largura Útil: {round(Bu,3)} m')
        print(f'Velocidade no gradeamento (máxima de {v_bs_max} cm/s): {round(v_bs,3)} cm/s')
        
        print('GRADEAMENTO'.center(50,'-'))
        print(f'Número de barras de {s*100} cm: {n}')
        print(f'Espaçamento livre entre barras: {b*100} cm')
        print(f'Altura do Canal: {round(H,3)} m')
        print(f'Comprimento da Grade: {round(L,3)} m')
        print(f'Largura do Canal e Grade: {round(B,3)} m')
        
        print('VERIFICAR PERDA DE CARGA'.center(50,'-'))
        print(f'Velocidade com 50% de obstrução à montante: {round(v,3)} m/s')
        print(f'Constante k: {round(k,3)}')
        print(f'Perda de carga: {round(h_loss,3)} m')
        
        print(''.center(50,'#'))
    
    report.update({
        'n':n,
        'n_real':n_real,
        'H':H,
        'B':B,
        'L':L,
        'opening_area_bs_min':opening_area_bs_min,
        'v_bs_max':v_bs_max,
        'v_bs':v_bs,
        'Au':Au,
        'Bu':Bu,
        'v':v,
        'k':k,
        'h_loss':h_loss,
        'g':g,
        'h_free':h_free
    })
    
    return report

def DesignSandSedimentationTank():
    # Constantes - SI
    g = 9.81
    v0 = 0.3
    vs = 0.021

    # Verificar Caixa de Areia
    # Entradas com unidades usuais
    # Vazão de entrada - L/s
    Q = 20
    # Comprimento do Canal - m
    L = 6
    # Largura do Canal - m
    b = 1
    # Altura de Sedimentção - m
    hs = 0.3

    # Processamento
    # Conversão de unidades para o SI
    Q = Q*1e-3

    # Verificar Comprimento Mínimo
    if L >= (v0/vs)*hs:
        CML = True
        FS = L/((v0/vs)*hs)
    else:
        CML = False
        FS = L/((v0/vs)*hs)

    # Verificar Largura Mínima
    if b >= 0.5:
        CMW = True
    else:
        CMW = False
    LWf = L/b

    # Saída
    print('RESULTADOS'.center(50,'#'))
    print('VERIFICAÇÃO DO COMPRIMENTO MÍNIMO'.center(50,'-'))
    print(f'Comprimento do Canal: {L} m')
    print(f'Altura de Sedimentção: {hs} m')
    print(f'FS = {round(FS,2)}')
    print('VERIFICAÇÃO DA LARGURA MÍNIMA'.center(50,'-'))
    print(f'Largura do Canal: {b} m')
    print(f'Fator Comprimento/Largura: {round(LWf,2)}')
    print(''.center(50,'#'))