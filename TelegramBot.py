from telethon import TelegramClient, events, functions

import os, time, shutil
from colorama import Fore, Back, Style
from telethon.tl.types import Channel

# Remember to use your own values from my.telegram.org!
api_id = 4538026
api_hash = 'f1c349e295cdacbdb2399a6f082e3d76'
client = TelegramClient('amancioOrteg', api_id, api_hash)

assert client.connect()

lista_opciones = {
    "/help",
    "/start ->",
    "/list -> Muestra la lista de productos que tienes dados de alta.",
    "/add -> Añade un producto.",
    "/edit [ID] -> Modificar el producto con el ID indicado.",
    "/remove [ID] -> Eliminar el producto con el ID indicado."
}

@client.on(events.NewMessage(pattern='/help'))
async def my_event_handler(event):
    massage = 'Comandos'
    for opcion in lista_opciones:
        massage += '\n' + opcion 
    await event.respond(massage)

@client.on(events.NewMessage(pattern='/start'))
async def handler(event):
    chat= await event.get_input_sender()
    users = await client.get_participants(chat)
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

@client.on(events.NewMessage(pattern='/add *'))
async def añadir(event):
    chat= await event.get_input_sender()
    users = await client.get_participants(chat)
    user = users[0]

    await client.send_message(chat, "ID del producto? (/id [ID])")

@client.on(events.NewMessage(pattern='/list'))
async def lista(event):
    chat= await event.get_input_sender()
    users = await client.get_participants(chat)
    user = users[0]

    f = open("%s\datos\%s.csv" % (os.getcwd(),user.id),"r",encoding="utf-8")

    for linea in f:
        columnas = linea.split(", ")
        await client.send_message(chat, "ID = " + columnas[0] + "\nProducto = " + columnas[1] + "\nPrecio = " + columnas[2] + "€")
    
    f.close()

@client.on(events.NewMessage(pattern='/edit *'))
async def edit(event):
    chat= await event.get_input_sender()
    users = await client.get_participants(chat)
    user = users[0]
    text = event.text.split(" ")
    
    f = open("%s\datos\%s.csv" % (os.getcwd(),user.id),"r+",encoding="utf-8")

    for linea in f:
        columnas = linea.split(", ")
        if columnas[0] == text[1]:
            await client.send_message(chat, "Este es el producto con esa ID")
            await client.send_message(chat, "ID = " + columnas[0] + "\nProducto = " + columnas[1] + "\nPrecio = " + columnas[2] + "€")
            borrarLinea = linea
        else:
            await client.send_message(chat, "No existe un producto con esa ID")
    await borrar(user,f,borrarLinea)
    await añadir(event)
    f.close()

@client.on(events.NewMessage(pattern='/remove *'))
async def eliminar(event):
    chat= await event.get_input_sender()
    users = await client.get_participants(chat)
    user = users[0]
    text = event.text.split(" ")

    f = open("%s\datos\%s.csv" % (os.getcwd(),user.id),"r",encoding="utf-8")

    for linea in f:
        columnas = linea.split(", ")
        if columnas[0] == text[1]:
            await client.send_message(chat, "Este es el producto borrado con esa ID")
            await client.send_message(chat, "ID = " + columnas[0] + "\nProducto = " + columnas[1] + "\nPrecio = " + columnas[2] + "€")
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



@client.on(events.NewMessage(pattern='/id *'))
async def productoId (event):
    chat= await event.get_input_sender()
    users = await client.get_participants(chat)
    user = users[0]
    text = event.text.split(" ")
    stringProduc = ''
    
    f = open("%s\datos\%s.csv" % (os.getcwd(),user.id),"a+",encoding="utf-8")
    stringProduc = '{0}, '.format(text[1])

    f.write(stringProduc)
    f.close()

    await client.send_message(chat, "Nombre del producto? (/nombre [producto])")

@client.on(events.NewMessage(pattern='/nombre *'))
async def productoNom (event):
    chat= await event.get_input_sender()
    users = await client.get_participants(chat)
    user = users[0]
    text = event.text.split(" ", 1)
    stringProduc = ''
    
    f = open("%s\datos\%s.csv" % (os.getcwd(),user.id),"a+",encoding="utf-8")
    stringProduc = '{0}, '.format(text[1])

    f.write(stringProduc)
    f.close()

    await client.send_message(chat, "Precio del producto? (/precio [PvP])")

@client.on(events.NewMessage(pattern='/precio *'))
async def productoPvp (event):
    chat= await event.get_input_sender()
    users = await client.get_participants(chat)
    user = users[0]
    text = event.text.split(" ", 1)
    stringProduc = ''
    
    f = open("%s\datos\%s.csv" % (os.getcwd(),user.id),"a+",encoding="utf-8")
    stringProduc = '{0}\n '.format(text[1])

    f.write(stringProduc)
    f.close()

    await client.send_message(chat, "Producto correctamente guardado")

@client.on(events.NewMessage(pattern='/join *'))
async def join(event):
    chat= await event.get_input_sender()
    users = await client.get_participants(chat)
    user = users[0]
    mensaje = event.text.split(' ',1)
    grupo = mensaje[1]
    await client(functions.channels.JoinChannelRequest(channel=grupo))
    
@client.on(events.NewMessage(pattern='/left *'))
async def left(event):
    chat= await event.get_input_sender()
    users = await client.get_participants(chat)
    user = users[0]
    mensaje = event.text.split(' ',1)
    grupo = mensaje[1]
    await client(functions.channels.LeaveChannelRequest(channel=grupo))

@client.on(events.NewMessage(pattern='/send msg -u *'))
async def enviarMsg(event):
    chat= await event.get_input_sender()
    users = await client.get_participants(chat)
    user = users[0]

    usuario = event.text.split(' ',4)
    print(usuario)
    entidad = client.get_entity(usuario)
    await client.send_message(usuario[3],usuario[4])

@client.on(events.NewMessage(pattern='/name *'))
async def rename(event):
    chat= await event.get_input_sender()
    users = await client.get_participants(chat)
    user = users[0]
    mensaje = event.text.split(' ',1)
    nombreNuevo = mensaje[1]
    await client(functions.account.UpdateProfileRequest(about=nombreNuevo))

async def guardarUsuario(f, user):
    stringUsuario = "'{0}', '{1}', '{2}', '{3}', '{4}'".format(
            user.id,
            user.access_hash,
            user.username,
            user.first_name,
            user.last_name
        )

    f.write(stringUsuario + "\n")


client.start()
client.run_until_disconnected()