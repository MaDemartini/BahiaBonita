def validar_dv(rut: str, dv: str) -> bool:
    rut = rut.strip()
    dv = dv.lower().strip()

    suma = 0
    multiplicador = 2

    for numero in reversed(rut):
        suma += int(numero) * multiplicador
        multiplicador += 1
        if multiplicador > 7:
            multiplicador = 2  
    
    resultado = 11 - (suma % 11)
    if resultado == 11:
        dv_esperado = '0'
    elif resultado == 10:
        dv_esperado = 'k'
    else:
        dv_esperado = str(resultado)

    return dv_esperado == dv.lower()
