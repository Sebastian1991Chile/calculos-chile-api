def mostrar_menu():
    print("================================")
    print("CALCULADORA IPC")
    print("================================")
    print("1. Calculadora de IPC")
    print("2. Calculadora de Arriendo")
    print("3. Calculadora de Sueldo")
    print("4. Calculadora de Inflación")
    print("5. Salir")
    print("")

def mostrar_calculadora_ipc():
    print("================================")
    print("CALCULADORA DE IPC")
    print("================================")
    fecha_inicio = input("Ingresar fecha de inicio del cálculo: ")
    fecha_termino = input("Ingresar fecha de término del cálculo: ")
    print("")
    return fecha_inicio, fecha_termino

def mostrar_calculadora_arriendo():
    print("================================")
    print("CALCULADORA DE ARRIENDO")
    print("================================")
    fecha_inicio = input("Ingresar fecha de inicio del cálculo: ")
    fecha_termino = input("Ingresar fecha de término del cálculo: ")
    monto = input("Ingresar monto a calcular: ")
    print("")
    return fecha_inicio, fecha_termino, monto

def mostrar_calculadora_sueldo():
    print("================================")
    print("CALCULADORA DE SUELDO")
    print("================================")
    fecha_inicio = input("Ingresar fecha de inicio del cálculo: ")
    fecha_termino = input("Ingresar fecha de término del cálculo: ")
    monto = input("Ingresar monto a calcular: ")
    print("")
    return fecha_inicio, fecha_termino, monto

def mostrar_calculadora_inflacion():
    print("================================")
    print("CALCULADORA DE INFLACIÓN")
    print("================================")
    fecha_inicio = input("Ingresar fecha de inicio del cálculo: ")
    fecha_termino = input("Ingresar fecha de término del cálculo: ")
    print("")
    return fecha_inicio, fecha_termino