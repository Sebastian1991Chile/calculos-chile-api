from calculations import calculate_variation, calculate_adjusted_amount
from data_manager import load_data
from menus import mostrar_menu, mostrar_calculadora_ipc, mostrar_calculadora_arriendo, mostrar_calculadora_sueldo, mostrar_calculadora_inflacion
from validations import validate_date
from formats import format_variation, amount_with_currency

def validate_and_get_variation(fecha_inicio, fecha_termino):
    if not validate_date(fecha_inicio, fecha_termino):
        print("Fechas inválidas. Por favor, ingresa fechas correctas.")
        return None
    data = load_data()
    return calculate_variation(fecha_inicio, fecha_termino, data)

def main():
    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción: ")
        if opcion == "1":
            # Lógica para la Calculadora de IPC
            fecha_inicio, fecha_termino = mostrar_calculadora_ipc()
            variation = validate_and_get_variation(fecha_inicio, fecha_termino)
            if variation is None:
                print("No se pudo calcular la variación.")
                continue
            else:
                print(f"Variación: {format_variation(variation)}")

        elif opcion == "2":
            # Lógica para la Calculadora de Arriendo
            fecha_inicio, fecha_termino, monto = mostrar_calculadora_arriendo()
            variation = validate_and_get_variation(fecha_inicio, fecha_termino)
            if variation is None:
                print("No se pudo calcular la variación.")
                continue
            else:
                print(f"Variación: {format_variation(variation)}")
            adjusted_amount = calculate_adjusted_amount(float(monto), variation)
            print(f"Monto original: {amount_with_currency(float(monto))}")
            print(f"Monto ajustado: {amount_with_currency(adjusted_amount)}")

        elif opcion == "3":
            # Lógica para la Calculadora de Sueldo
            fecha_inicio, fecha_termino, monto = mostrar_calculadora_sueldo()
            variation = validate_and_get_variation(fecha_inicio, fecha_termino)
            if variation is None:
                print("No se pudo calcular la variación.")
                continue
            else:
                print(f"Variación: {format_variation(variation)}")
            adjusted_amount = calculate_adjusted_amount(float(monto), variation)
            print(f"Monto original: {amount_with_currency(float(monto))}")
            print(f"Monto ajustado: {amount_with_currency(adjusted_amount)}")

        elif opcion == "4":
            # Lógica para la Calculadora de Inflación
            fecha_inicio, fecha_termino = mostrar_calculadora_inflacion()
            variation = validate_and_get_variation(fecha_inicio, fecha_termino)
            if variation is None:
                print("No se pudo calcular la variación.")
                continue
            else:
                print(f"Variación: {format_variation(variation)}")

        elif opcion == "5":
            break
        else:
            print("Opción inválida. Por favor, selecciona una opción correcta.")

if __name__ == "__main__":
    main()