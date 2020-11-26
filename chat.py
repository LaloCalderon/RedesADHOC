from socket import socket, AF_PACKET, SOCK_RAW, htons
from struct import *
import threading
import time
import os, sys
import zlib

ethertype = '\x08\x02'
protocol = 0x0802
src_addr = "\x90\x48\x9a\x2c\x2a\x44"
dst_addr = "\xff\xff\xff\xff\xff\xff"
#usuarios = {"\x10\x0b\xa9\xd4\xf8\xc0": "Ulises", "\x80\x91\x33\xf4\x58\x99": "Miguel"}
#recibidos = {"Ulises": [], "Miguel": []}
seqrecv = []
seq = 0

def enviarMensaje(env):
	global seq
	ide = 1
	while True:
		seq+=1
		mensaje = raw_input("\nLalo: ")  
		empaq1 = dst_addr + src_addr + ethertype + pack('!QH', seq, ide) + mensaje #El mensajese adjunta al ultimo
		crc = zlib.crc32(empaq1) #CRC
		
		empaq2 = empaq1 + pack('!l', crc)
		
		env.sendall(empaq2)


def recibirMensaje(env):
	my_ide = 4
	print("\n ######## CHAT ACTIVO ########")
	while True:
		recibir = env.recv(1024) #Recibir paquetes de 1024 bytes
		#src = usuarios [recibir[6:12]]
		meno = recibir[0:-4] #meno -> msj recibido 
		c_crc = zlib.crc32(meno) #CRC meno
		r_crc = unpack('!l', recibir[-4:]) #
		r_crc1 = r_crc[0]
		
		secuencial = unpack('!Q', recibir [14:22])
		secuencial1 = secuencial[0]
		idde = unpack ('!H', recibir [22:24])
		idde1 = idde[0]

		if c_crc == r_crc1:
			if idde1 == my_ide:
				if seqrecv.count(secuencial1) == 0:
					seqrecv.append(secuencial1)
					print("\nMsj recibido: {}".format(recibir[24:-4]))
				else:
					pass
			else:
				pass
		else:
			print("Error detectado")

if __name__=='__main__':
    env = socket(AF_PACKET, SOCK_RAW, htons(protocol))
    env.bind(('wlp3s0', 0))
    rx = threading.Thread(target = recibirMensaje, args=(env, ))
    tx = threading.Thread(target = enviarMensaje, args=(env, ))
    rx.start()
    tx.start()
    rx.join()
    tx.join()