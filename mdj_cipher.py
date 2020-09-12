import operator
from codecs import encode


TAMANO_BLOQUE = 8
CODE = "utf8"
N_FILAS = 2
DIF_LLAVE_BYTES = 3
R = 3

def main():
    
    print('###########\nCIFRADO MDJ\n###########\n\n')
    print('MENU:\n1) Cifrar \n2) Descifrar\n')
    decision = input('Ingrese una opcion: ')

    

    if decision == '1':
        texto_plano = input('Ingrese el texto a cifrar: ')
        llave = input('Ingrese la llave: ')
        print(texto_plano)
        cifrado = cifrar(texto_plano, llave)
        print('\n\nTEXTO CIFRADO:\t',cifrado)
        return 0

    if decision == '2':
        texto_cifrado = input('Ingrese el texto a descifrar: ')
        llave = input('Ingrese la llave: ')
        texto_cifrado = bytes(texto_cifrado, CODE)
        texto_cifrado = remover_backslash(texto_cifrado)
        res = decifrar(texto_cifrado, llave)
        print('\n\nTEXTO DESCIFRADO:\t',res)



def remover_backslash(texto_cifrado):
    return texto_cifrado.decode('unicode-escape').encode('ISO-8859-1')

def cifrar(texto_plano, llave):
    llave = normalizar_llave(llave,TAMANO_BLOQUE)
    texto_plano = agregar_espacio(texto_plano)  
    # Dividir texto plano
    bloques_txt = dividir_bloques(texto_plano, TAMANO_BLOQUE)
    bloques_bytes = bloques_a_bytes(bloques_txt)
    print(bloques_bytes)
    for _ in range(R):
        for i in range(len(bloques_bytes)):
    # ------ CIFRADO ------
        
            # print('BLOQUE A CIFRAR:\t', bloques_bytes[i])
            # Confusion 1: Cesar
            bloques_bytes[i] = cifrado_cesar(bloques_bytes[i], get_desplazamiento(llave))
            # print('CESAR:\t\t\t',bloques_bytes[i])
            # Difusion 1: Mover bits en llave
            # print('Llave:\t\t\t',llave)
            llave = mover_bytes(llave)
            # print('DIFUSION LLAVE:\t\t', llave)

            # Difusion 2
            bloques_bytes[i] = difusion2(bloques_bytes[i])
            # print('DIFUSION 2:\t\t', bloques_bytes[i])
            
            #Confusion 2
            bloques_bytes[i] = bytes(map(operator.xor, bloques_bytes[i], llave))
            # print('CONFUSION XOR:\t\t', bloques_bytes[i])
    return(b''.join(bloques_bytes))

def decifrar(cifrado, llave):
    llave = normalizar_llave(llave,TAMANO_BLOQUE)
    # Dividir texto plano
    bloques_bytes = dividir_bloques(cifrado, TAMANO_BLOQUE)
    print(bloques_bytes)
    for _ in range(R*len(bloques_bytes)):
        llave = mover_bytes(llave)
    for _ in range(R):
        for i in reversed(range(len(bloques_bytes))):
        
            # print('Llave:\t\t\t',llave)
            bloques_bytes[i] = bytes(map(operator.xor, bloques_bytes[i], llave))
            # print('DESCIFRADO - XOR:\t\t', bloques_bytes[i])

            llave = mover_bytes_i(llave)
            # print('DESCIFRADO - DIFUSION LLAVE:\t',llave)

            bloques_bytes[i] = desencriptar_difusion2(bloques_bytes[i])
            # print('DESCIFRADO - DIFUSION 2:\t',bloques_bytes[i])

            bloques_bytes[i] = cifrado_cesar(bloques_bytes[i], -1*get_desplazamiento(llave))
            # print('DESCIFRADO - CESAR:\t\t',bloques_bytes[i])
    for i in range(len(bloques_bytes)):
        bloques_bytes[i] = bloques_bytes[i].decode(CODE)
    return(''.join(bloques_bytes))

def agregar_espacio(texto):
    mod_texto = len(texto) % TAMANO_BLOQUE
    if mod_texto != 0:
        dif = TAMANO_BLOQUE - mod_texto
        # agregar x como dummy
        texto += ' '*dif  
    return texto


def desencriptar_difusion2(te):
    result = b''
    subbloques = dividir_bloques(te, int(TAMANO_BLOQUE/N_FILAS))
    for i in range(int(TAMANO_BLOQUE/N_FILAS)):
        result += bytes([subbloques[0][i]]) + bytes([subbloques[1][i]])
    return result

def difusion2(txt):
    subbloques = dividir_bloques(txt, N_FILAS)
    result = b''
    for i in range(N_FILAS):
        for b in subbloques:
            result += bytes([b[i]])

    return result
    
    

def extractKBits(num,k,p): 
  
     # convert number into binary first 
     binary = bin(num) 
  
     # remove first two characters 
     binary = binary[2:] 
  
     end = len(binary) - p 
     start = end - k + 1
  
     # extract k  bit sub-string 
     kBitSubStr = binary[start : end+1] 
  
     # convert extracted sub-string into decimal again 
     return int(kBitSubStr,2)

def cifrado_cesar(bloque_bytes, desplazamiento):
    cesar = b''
    for byte in bloque_bytes:
        aux = (byte + desplazamiento) % 256
        cesar+=bytes([aux])
    return cesar

def mover_bytes(llave):
    llave = llave[DIF_LLAVE_BYTES:] + llave[:DIF_LLAVE_BYTES]
    return llave

def mover_bytes_i(llave):
    return llave[-1*DIF_LLAVE_BYTES:] + llave[:-1*DIF_LLAVE_BYTES]

def get_desplazamiento(llave):
    return extractKBits(llave[-1],3,1) + 1

def dividir_bloques(texto, n):        
    return [texto[i:i+n] for i in range(0, len(texto), n)]

def normalizar_llave(llave, n):
    llave = agregar_espacio(llave)
    bloques = dividir_bloques(llave,n)
    for i in range(len(bloques)):
        bloques[i] = bytes(bloques[i], CODE)
        if i > 0:
            bloques[i] = bytes(map(operator.xor, bloques[i], bloques[i-1]))
    return bloques[-1]

def bloques_a_bytes(bloques_txt):
    bloques_bytes = []
    for b in bloques_txt:
        bloques_bytes.append(bytes(b, CODE))
    return bloques_bytes

if __name__ == "__main__":
    main()



