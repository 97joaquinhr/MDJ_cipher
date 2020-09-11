import operator

TAMANO_BLOQUE = 8
CODE = "utf8"
N_FILAS = 2
DIF_LLAVE_BYTES = 3 

def main():
    texto_plano = "Hola amigos jej hol"
    llave = "t amet orci aliquam."

    llave = normalizar_llave(llave,TAMANO_BLOQUE)
    
    # Dividir texto plano
    bloques_txt = dividir_bloques(texto_plano, TAMANO_BLOQUE)
    bloques_bytes = bloques_a_bytes(bloques_txt)
    print(bloques_bytes)
    # ------ CIFRADO ------
    print('BLOQUE A CIFRAR:\t', bloques_bytes[0])
    # Confusion 1: Cesar
    bloques_bytes[0] = cifrado_cesar(bloques_bytes[0], get_desplazamiento(llave))
    print('CESAR:\t\t\t',bloques_bytes[0])
    # Difusion 1: Mover bits en llave
    print('Llave:\t\t\t',llave)
    llave = mover_bytes(llave)
    print('DIFUSION LLAVE:\t\t', llave)

    # Difusion 2
    bloques_bytes[0] = difusion2(bloques_bytes[0])
    print('DIFUSION 2:\t\t', bloques_bytes[0])
    
    #Confusion 2
    bloques_bytes[0] = bytes(map(operator.xor, bloques_bytes[0], llave))
    print('CONFUSION 2 XOR:\t\t', bloques_bytes[0])

    print('#########################')
    # ------ DESCIFRADO ------

    bloques_bytes[0] = bytes(map(operator.xor, bloques_bytes[0], llave))
    print('DESCIFRADO - XOR:\t\t', bloques_bytes[0])

    llave = mover_bytes_i(llave)
    print('DESCIFRADO - DIFUSION LLAVE:\t',llave)

    bloques_bytes[0] = desencriptar_difusion2(bloques_bytes[0])
    print('DESCIFRADO - DIFUSION 2:\t',bloques_bytes[0])

    bloques_bytes[0] = cifrado_cesar(bloques_bytes[0], -1*get_desplazamiento(llave))
    print('DESCIFRADO - CESAR:\t\t',bloques_bytes[0])

   


def desencriptar_difusion2(te):
    result = b''
    subbloques = dividir_bloques(te, int(TAMANO_BLOQUE/N_FILAS))
    for i in range(int(TAMANO_BLOQUE/N_FILAS)):
        print(subbloques[0][i])
        result += bytes([subbloques[0][i]]) + bytes([subbloques[1][i]])
    print(result)
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
"""
def cifrado_cesar(tp, desplazamiento):
    cesar = ''
    for char in tp:
        aux = ord(char) + desplazamiento
        if aux > ord('z'):
            aux = aux - ord('z')
            aux = ord(' ') + aux - 1
        if aux < ord(' '):
            aux = ord(' ') - aux
            aux = ord('z') - aux + 1
        cesar+=chr(aux)
    return cesar
"""

def cifrado_cesar(bloque_bytes, desplazamiento):
    cesar = b''
    for byte in bloque_bytes:
        aux = byte + desplazamiento
        cesar += (bytes([aux]))
    return cesar

def mover_bytes(llave):
    llave = llave[DIF_LLAVE_BYTES:] + llave[:DIF_LLAVE_BYTES]
    return llave

def mover_bytes_i(llave):
    return llave[-1*DIF_LLAVE_BYTES:] + llave[:-1*DIF_LLAVE_BYTES]

def get_desplazamiento(llave):
    return extractKBits(llave[-1],3,1) + 1

def dividir_bloques(texto, n):
    mod_texto = len(texto) % n
    if mod_texto != 0:
        dif = n - mod_texto
        # agregar x como dummy
        texto += 'x'*dif          
    return [texto[i:i+n] for i in range(0, len(texto), n)]

def normalizar_llave(llave, n):
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
"""
desplazamiento = extractKBits(llave_bin[-1],3,1) + 1
print(desplazamiento)
s = "9"
print(cifrado_cesar(s,desplazamiento))
s = "z"
cesar = cifrado_cesar(text_plano,desplazamiento)
print(cifrado_cesar(cesar,-1*desplazamiento))

print(mover_bytes(llave_bin))
"""

if __name__ == "__main__":
    main()



