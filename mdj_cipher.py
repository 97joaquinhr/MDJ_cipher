text_plano = "Lorem ipsum dolor si"
clave = "Lorem ipsu"
code = "utf8"
clave_bin = bytes(clave, code)


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

desplazamiento = extractKBits(clave_bin[-1],3,1) + 1

s = "9"
print(cifrado_cesar(s,desplazamiento))
s = "z"
cesar = cifrado_cesar(text_plano,desplazamiento)
print(cifrado_cesar(cesar,-6))