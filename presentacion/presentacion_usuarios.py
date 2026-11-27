from prettytable import PrettyTable
import maskpass
import bcrypt

import re

from auxiliares.auxiliar import nombre_app, version_app
from datos.modelos.usuario import Usuario
from negocio.negocio_usuarios import cargar_usuarios, crear_usuario, modificar_usuario, buscar_usuario_rut
from negocio.negocio_paises import buscar_pais
from presentacion.menu import menu_principal
from auxiliares.validaciones import validar_rut, validar_correo, validar_contrasenia_segura, validar_genero


def mostrar_usuarios():
    tabla_usuarios = PrettyTable()
    tabla_usuarios = cargar_usuarios(tabla_usuarios)
    print(tabla_usuarios)


def datos_usuario():
    rut = nombre = apellido = correo = nombre_pais = fecha_nacimiento = genero = contrasenia = ''
    print('\nIngrese Datos Usuario')

    while rut == '':
        rut = input('RUT (12.345.678-5): ')
        if not validar_rut(rut):
            print('Rut NO VÁLIDO, ingrese nuevamente...')
            rut = ''

    while nombre == '':
        nombre = input('Nombre: ')

    while apellido == '':
        apellido = input('Apellido: ')

    correo = solicitar_correo()

    nombre_pais = input('Nombre País: ')
    tabla_paises = PrettyTable()
    tabla_paises = buscar_pais(tabla_paises, nombre_pais)
    print(tabla_paises)
    id_pais = input('Id País: ')

    fecha_nacimiento = input('Fecha Nacimiento (dd/MM/aaaa): ')

    while genero == '':
        print('Opciones de Género')
        print('[1] Masculino')
        print('[2] Femenino')
        print('[3] Otro')
        genero = input('Opción Género [1-3]: ')
        if not validar_genero(genero):
            print('Género NO corresponde, ingrese nuevamente...')
            genero = ''

    while contrasenia == '':
        print('Ingrese una contraseña segura:')
        print('Al menos una minúscula\nAl menos una mayúscula\nAl menos un dígito\nAl menos un caracter especial')
        print('Al menos 8 caracteres de largo')
        contrasenia = maskpass.askpass(prompt="Contraseña: ", mask="*")
        if not validar_contrasenia_segura(contrasenia):
            print('Su contraseña NO es segura, ingrese nuevamente...')
            contrasenia = ''
        else:
            hashed = bcrypt.hashpw(
                contrasenia.encode('utf-8'), bcrypt.gensalt())

    crear_usuario(rut, nombre.title(), apellido.title(), correo,
                  id_pais, fecha_nacimiento, genero, hashed)


def actualizar_datos_usuario():
    rut = nombre = apellido = correo = nombre_pais = fecha_nacimiento = genero = ''
    print('\nIngrese Nuevos Datos de Usuario')
    print('Introduzca nuevos datos para actualizar\no Enter para conservar.')

    while rut == '':
        rut = input('RUT (12.345.678-5) (o Enter para conservar): ')
        if not validar_rut(rut):
            print('Rut NO VÁLIDO, ingrese nuevamente...')
            rut = ''
        else:
            usuario, mensaje = buscar_usuario_rut(rut)
            print(mensaje)

            if usuario:
                nombre = input('Nombre (o Enter para conservar): ')
                apellido = input('Apellido (o Enter para conservar): ')
                correo = input('Correo (o Enter para conservar): ')
                if not validar_correo(correo):
                    print('Correo electrónico NO corresponde, no será modificado...')
                    correo = ''

                nombre_pais = input('Nombre País: ')
                tabla_paises = PrettyTable()
                tabla_paises = buscar_pais(tabla_paises, nombre_pais)
                print(tabla_paises)
                id_pais = input('Id País (o Enter para conservar): ')

                fecha_nacimiento = input(
                    'Fecha Nacimiento (dd/MM/aaaa) (o Enter para conservar): ')

                print('Opciones de Género')
                print('[1] Masculino')
                print('[2] Femenino')
                print('[3] Otro')
                genero = input('Opción Género [1-3]: ')
                if not validar_genero(genero):
                    print('Género NO corresponde, no será modificado...')
                    genero = ''

                modificar_usuario(rut, nombre.title(), apellido.title(
                ), correo, id_pais, fecha_nacimiento, genero, usuario)


def deshabilitar_usuario():
    rut = ''
    print('\nIngrese Nuevos Datos de Usuario')

    rut = solicitar_rut('RUT (12.345.678-5): ')
    usuario, mensaje = buscar_usuario_rut(rut)
    print(mensaje)

    if usuario:
        print('Usuario encontrado.')
        print(f'¿Está seguro de deshabilitar al usuario {usuario.apellido}, {usuario.nombre}?')
        opcion = input('Indique SI o NO (s/n): ')
        if opcion.lower() == 's':
            usuario.habilitado = False
            modificar_usuario('', '', '', '', '', '', '', usuario)


def login_usuario():
    while True:
        print(f'\n{nombre_app} {version_app}')
        print('='*len(nombre_app) + "=" + '='*len(version_app))
        print('\nIngrese los datos de\nInicio de Sesión')

        correo = solicitar_correo()
        usuario, mensaje = buscar_usuario_rut(correo)
        print(mensaje)

        if usuario and usuario.habilitado == True:
            comparar_contrasenia(usuario)

        elif usuario and usuario.habilitado == False:
            print(
                'Usuario Deshabilitado.\nDirígase a atención de usuarios para revisar su situación.')
            break
        else:
            print('Usuario no registrado.\n¿Desea registrarse?')
            solicitar_registro()


def inicio_sistema():
    print("¡Contraseña Correcta!")
    menu_principal()


def solicitar_correo():
    correo = mensaje = ''
    while correo == '':
        correo = input('Correo: ')
        if validar_correo(correo):
            mensaje = 'Correo electrónico correcto'
        else:
            mensaje = 'Correo electrónico NO corresponde, ingrese nuevamente...'
            correo = ''
    return correo, mensaje


def solicitar_registro():
    opcion_registro = input('Ingrese Si/No [s-n]: ')

    match opcion_registro.lower():
        case 's':
            datos_usuario()
        case 'n':
            return


def comparar_contrasenia(usuario):
    intentos = 0
    contrasenia = ''

    while intentos <= 2 and contrasenia == '':
        contrasenia = maskpass.askpass(prompt="Contraseña: ", mask="*")
        contrasenia_guardada = usuario.password
        if bcrypt.checkpw(contrasenia.encode('utf-8'), contrasenia_guardada.encode('utf-8')):
            inicio_sistema()
        else:
            print("Contraseña incorrecta,\n ingrese nuevamente...")
            contrasenia = ''
            intentos += 1

            if intentos == 2 and contrasenia == '':
                print('Ha superado la cantidad de intentos\nDehabilitando al usuario...')
                usuario.habilitado = False
                modificar_usuario('', '', '', '', '', '', '', usuario)


def solicitar_rut(msg_input):
    rut = mensaje = ''
    while rut == '':
        rut = input(msg_input)
        if validar_rut(rut):
            mensaje = 'RUT VÁLIDO'
        else:
            mensaje = 'RUT NO VÁLIDO, ingrese nuevamente...'
            rut = ''
    return rut, mensaje
