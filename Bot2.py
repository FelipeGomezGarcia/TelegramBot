from telethon import TelegramClient, events, functions
from telethon.tl.functions.messages import GetDialogsRequest

import os, time, shutil
from colorama import Fore, Back, Style
from telethon.tl.types import Channel, InputPeerEmpty

# Remember to use your own values from my.telegram.org!
api_id = 4538026
api_hash = 'f1c349e295cdacbdb2399a6f082e3d76'
client = TelegramClient('amancioOrteg', api_id, api_hash)

#variables para reenviar mensajes
reenviar = False
usuarioReenvio = ''

assert client.connect()

lista_opciones = {
    "/help",
    "/start ->",
    "/list -> Muestra la lista de productos que tienes dados de alta.",
    "/add -> Añade un producto.",
    "/edit [ID] -> Modificar el producto con el ID indicado.",
    "/remove [ID] -> Eliminar el producto con el ID indicado."
}

@client.on(events.NewMessage)
async def my_event_handler(event):
    chat= await event.get_input_sender()
    users = await client.get_participants(chat)
    user = users[0]
    if reenviar:
        await client.send_message(usuarioReenvio,event)
    if '/help' == event.text:
        await ayuda(event)
    if '/start' == event.text:
        await start(chat,users)
    if '/list' == event.text:
        await listar(chat,user)
    if event.text.__contains__('/add'):
        await añadir(chat)
    if event.text.__contains__('/id'):
        await productoId(event,chat,user)
    if event.text.__contains__('/nombre'):
        await productoNom(event,chat,user)
    if event.text.__contains__('/precio'):
        await productoPvp(event,chat,user)
    if event.text.__contains__('/edit'):
        await editar(event,chat,user)
    if event.text.__contains__('/remove'):
        await remove(event,chat,user)


async def ayuda(event):
    massage = 'Comandos'
    for opcion in lista_opciones:
        massage += '\n' + opcion 
    await event.respond(massage)


async def start(chat,users):
    for user in users:
        await client.send_message(chat, 'Hola ' + user.first_name + ", te acabas de dar de alta en la base de datos.")

    f = open("%s\datos\%s.csv" % (os.getcwd(),"usuariosAlta"),"r+",encoding="utf-8")
    
    if f.read() == '':
        await guardarUsuario(f, user)
    f.seek(0)
    for linea in f:
        columnas = linea.split(", ")
        id_user = columnas[0].replace("'", "")
        if int(id_user) == int(user.id):
            await client.send_message(chat, "Ya estas dado de alta.")
        else:   
            await guardarUsuario(f, user)

    f.close()


async def guardarUsuario(f, user):
    stringUsuario = "'{0}', '{1}', '{2}', '{3}', '{4}'".format(
            user.id,
            user.access_hash,
            user.username,
            user.first_name,
            user.last_name
        )

    f.write(stringUsuario + "\n")


async def listar(chat,user):
    f = open("%s\datos\%s.csv" % (os.getcwd(),user.id),"r",encoding="utf-8")
    for linea in f:
        columnas = linea.split(", ")
        await client.send_message(chat, "ID = " + columnas[0] + "\nProducto = " + columnas[1] + "\nPrecio = " + columnas[2].rstrip('\n') + "€")
    
    f.close()


async def añadir(chat):
    await client.send_message(chat, "ID del producto? (/id [ID])")

async def productoId (event,chat,user):
    text = event.text.split(" ")
    stringProduc = ''
    
    f = open("%s\datos\%s.csv" % (os.getcwd(),user.id),"a+",encoding="utf-8")
    stringProduc = '{0}, '.format(text[1])

    f.write(stringProduc)
    f.close()

    await client.send_message(chat, "Nombre del producto? (/nombre [producto])")

async def productoNom (event,chat,user):
    text = event.text.split(" ", 1)
    stringProduc = ''
    
    f = open("%s\datos\%s.csv" % (os.getcwd(),user.id),"a+",encoding="utf-8")
    stringProduc = '{0}, '.format(text[1])

    f.write(stringProduc)
    f.close()

    await client.send_message(chat, "Precio del producto? (/precio [PvP])")

async def productoPvp (event,chat,user):
    text = event.text.split(" ", 1)
    stringProduc = ''
    
    f = open("%s\datos\%s.csv" % (os.getcwd(),user.id),"a+",encoding="utf-8")
    stringProduc = '{0}\n'.format(text[1])

    f.write(stringProduc)
    f.close()

    await client.send_message(chat, "Producto correctamente guardado")


async def editar(event,chat,user):
    text = event.text.split(" ")
    
    f = open("%s\datos\%s.csv" % (os.getcwd(),user.id),"r+",encoding="utf-8")

    for linea in f:
        columnas = linea.split(", ")
        if columnas[0] == text[1]:
            await client.send_message(chat, "Este es el producto con esa ID")
            await client.send_message(chat, "ID = " + columnas[0] + "\nProducto = " + columnas[1] + "\nPrecio = " + columnas[2].rstrip('\n') + "€")
            borrarLinea = linea
        else:
            await client.send_message(chat, "No existe un producto con esa ID")
    await borrar(user,f,borrarLinea)
    await añadir(event)
    f.close()


async def remove(event,chat,user):
    text = event.text.split(" ")

    f = open("%s\datos\%s.csv" % (os.getcwd(),user.id),"r",encoding="utf-8")

    for linea in f:
        columnas = linea.split(", ")
        if columnas[0] == text[1]:
            await client.send_message(chat, "Este es el producto borrado con esa ID")
            await client.send_message(chat, "ID = " + columnas[0] + "\nProducto = " + columnas[1] + "\nPrecio = " + columnas[2].rstrip('\n') + "€")
            borrarLinia = linea
    f.seek(0)
    await borrar(user,f,borrarLinia)
    f.close()

async def borrar(user,f,borrarLinia):
    fw = open("%s\productos\%s_c.csv" % (os.getcwd(),user.id),"w",encoding="utf-8")
    if fw == '':
        print("Esta vacio")
    for linea in f:
        if linea != borrarLinia:
            fw.write(linea)
    fw.close()
    shutil.copy("%s\productos\%s_c.csv" % (os.getcwd(),user.id), "%s\datos\%s.csv" % (os.getcwd(),user.id))


@client.on(events.NewMessage)
async def administrador(event):
    global usuarioReenvio
    global reenviar
    chat= await event.get_input_sender()

    if event.text.__contains__('/join'):
        await join(event)
    if event.text.__contains__('/left'):
        await left(event)
    if event.text.__contains__('/name'):
        await rename(event)
    if event.text.__contains__('/send msg -u'):
        await msgUsuario(event)
    if event.text.__contains__('/send msg -c'):
        await msgCanal(event,chat)
    if event.text.__contains__('/redirect +'):
        usuarioReenvio = await redirect(event)
        reenviar = True
    if event.text.__contains__('/redirect -'):
        reenviar = False


async def join(event):
    mensaje = event.text.split(' ',1)
    grupo = mensaje[1]
    await client(functions.channels.JoinChannelRequest(channel=grupo))


async def left(event):
    mensaje = event.text.split(' ',1)
    grupo = mensaje[1]
    await client(functions.channels.LeaveChannelRequest(channel=grupo))


async def rename(event):
    mensaje = event.text.split(' ',1)
    nombreNuevo = mensaje[1]
    await client(functions.account.UpdateProfileRequest(about=nombreNuevo))


async def msgCanal(event,chat):
    result = await client.get_dialogs()
    mensaje = ''
    canal = event.text.split(' ',4)
    if canal[3] == '':
        for chats in result:
            mensaje = mensaje + chats.title + " " + str(chats.id) + "\n"
        await client.send_message(chat, mensaje)
    else:
        await client.send_message(canal[3], canal[4])
    

async def msgUsuario(event):
    usuario = event.text.split(' ',4)
    await client.send_message(usuario[3],usuario[4])


async def redirect(event):
    text = event.text.split(" ")
    return text[2]

client.start()
client.run_until_disconnected()