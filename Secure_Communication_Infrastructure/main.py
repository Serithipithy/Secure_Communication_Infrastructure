from Crypto.Cipher import AES

if __name__ == '__main__':
    text=b'decripteaza te r'

    text = text + b'\0' * (16 - len(text))
    aes=AES.new(b'\xe8l\xda,d\xec\xcf\t*WN\xff\r\xcd\x82\xfa',AES.MODE_ECB)
    encriptat=aes.encrypt(text)
    decriptat=aes.decrypt(encriptat)

    print(encriptat)
    print(decriptat)