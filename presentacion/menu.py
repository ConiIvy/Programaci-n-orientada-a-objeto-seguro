import sys
from datos import nombre_app,version_app,main_menu

def menu_principal():
    print(f'\n{nombre_app} {version_app}')
    print('='*len(nombre_app) + "=" + '='*len(version_app))

    while True:
        for clave,valor in main_menu.items():
            print(f'[{clave}] - {valor}')

        opcion_usuario = input('Ingrese una opción [1-4]: ')

        match opcion_usuario:
            case '1':
                pass
            case '2':
                pass
            case '3':
                pass
            case '4':
                print('Cerrar Sesión')
                break
            case _:
                print('Opción Ingresada NO corresponde...\nIngrese nuevamente.')