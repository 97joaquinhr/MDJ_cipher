
def main():
    texto_plano = "Hola amigos jej hola"
    # texto_plano = "Lorem ipsum dolor si"
    clave = "t amet orci aliquam."
    # code = "utf8"
    # clave_bin = bytes(clave, code)
    # desplazamiento = extractKBits(clave_bin[-1],3,1) + 1


    # ------ CIFRADO ------
    # Dividir texto plano
    bloques_txt = dividir_bloques(texto_plano, 10)

    print('BLOQUE A CIFRAR:\t', bloques_txt[0])
    # Confusion 1: Cesar
    bloques_txt[0] = cifrado_cesar(bloques_txt[0], get_desplazamiento(clave))
    print('CESAR:\t\t\t',bloques_txt[0])

    # Difusion 1: Mover bits en clave
    clave = mover_bytes(clave)
    print('DIFUSION LLAVE:\t\t', clave)

    # Difusion 2
    bloques_txt[0] = difusion2(bloques_txt[0])
    print('DIFUSION 2:\t\t', bloques_txt[0])

    print('#########################')
    # ------ DESCIFRADO ------
    bloques_txt[0] = desencriptar_difusion2(bloques_txt[0])
    print('DESCIFRADO - DIFUSION 2:\t',bloques_txt[0])

    clave = mover_bytes_i(clave)
    print('DESCIFRADO - DIFUSION LLAVE:\t',clave)

    bloques_txt[0] = cifrado_cesar(bloques_txt[0], -1*get_desplazamiento(clave))
    print('DESCIFRADO - CESAR:\t\t',bloques_txt[0])



def desencriptar_difusion2(te):
    result = ''
    subbloques = dividir_bloques(te, 5)
    for i in range(len(subbloques[0])):
        result += subbloques[0][i] + subbloques[1][i]
    return result

def difusion2(txt):
    subbloques = dividir_bloques(txt, 2)
    result = ''
    
    for i in range(2):
        for b in subbloques:
            result += b[i]

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

def mover_bytes(llave):
    mitad1 = llave[:3]
    mitad2 = llave[3:]
    llave = mitad2 + mitad1
    return llave

def mover_bytes_i(llave):
    return llave[17:] + llave[:17]

def get_desplazamiento(llave):
    code = "utf8"
    clave_bin = bytes(llave, code)
    return extractKBits(clave_bin[-1],3,1) + 1

def dividir_bloques(texto, n):
    return [texto[i:i+n] for i in range(0, len(texto), n)]


"""
desplazamiento = extractKBits(clave_bin[-1],3,1) + 1
print(desplazamiento)
s = "9"
print(cifrado_cesar(s,desplazamiento))
s = "z"
cesar = cifrado_cesar(text_plano,desplazamiento)
print(cifrado_cesar(cesar,-1*desplazamiento))

print(mover_bytes(clave_bin))
"""

if __name__ == "__main__":
    main()



