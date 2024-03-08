# -*- coding: utf-8 -*-
import base64
import hashlib
from Crypto.Cipher import AES
from urllib.parse import quote, unquote

pwd_aes_key = b'6d3121b650e42855'
pwd_aes_key2 = b'AAAANINIk8rMEVbG'


def get_sign(interface, data, timestamp):
    interface_list = ["/api/v2/weather", "/api/v2/h5model/list", "/api/school",
                      "/api/v2/school/detail", "/api/getRoute", "/api/feedback",
                      "/api/version", "/api/feedback/list", "/api/v2/phoneset"]
    if interface in interface_list:
        sign_key = '6d3121b650e42855976d0f70dd2048e4'
    else:
        sign_key = '262b6c001ea05beceb9d560be1dbf14f'
    key_value_str = ''.join(
        [str(key) + str(value) for key, value in sorted(data.items())])
    final_str = f'{sign_key}{interface}{key_value_str}{timestamp} {sign_key}'
    # print(final_str)
    return md5_encrypt(final_str)


def get_enc_pwd(pwd):
    return aes_encrypt(pwd, pwd_aes_key).strip()


def get_dec_pwd(data):
    return aes_decrypt(data, pwd_aes_key).strip()


def md5_encrypt(data):
    md = hashlib.md5()
    md.update(data.encode())
    return md.hexdigest()


def aes_encrypt(data, key):
    BS = AES.block_size
    padded_data = data + (BS - len(data) % BS) * chr(BS - len(data) % BS)
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_data = cipher.encrypt(padded_data.encode())
    encoded_data = base64.b64encode(encrypted_data).decode()
    return encoded_data


def aes_decrypt(encoded_data, key):
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_data = base64.b64decode(encoded_data.encode())
    decrypted_data = cipher.decrypt(encrypted_data)
    padding_length = decrypted_data[-1]
    decrypted_data = decrypted_data[:-padding_length].decode()
    return decrypted_data


if __name__ == '__main__':
    enc_string = "ARXBF33cp7XELyB%2FEXalRr6ras6EZJ5gWAG5ek97EIdGiPAxvV2%2F3tROde0BokfiHmvPSbrkKhAqsMO6hpOYK1qD7T9mKTUfOVGVd8%2FuwrnxvpXSUIAnyjtYGibBWazmS1Xp%2FhbmESsbYk8FcLcJ7FTjCVMlqtwWuokzDxe6WSDVIDNbjRPyIQLiioXv%2B35z1ql4518mzRjx9T%2BhjSxcB4q%2FYd9w7qbWvJ%2Ff6OC30R8B3hL%2B1b%2BeFl6FEWsXHCxILqZQuBRc47WxbAijbtscT0LnYI7xJPXNhXa16ixN9ryiCXzdABr0B9n2uYtN4j%2Bfw9%2F%2F%2Bnv7aL2lafjg3mfYLXS3G46pAB6qhmVa3uSCj%2B4zuVWHrcnazrpbZbPDJKEfQwQnzWUkKNzZSIwAgBpVtOXWofWD6cwdZGuDnKLfk07UG2eFs8kEXMrUD2c7HwWVlC%2FflEbbYi%2FsQX3%2BtuRiDPv3rtyRZRvco81ZxB%2Bkjy06GlroqM%2FiaTbtC39k2wLvXBOAtWXkmx0G%2FEdmPeZJhAPMIClQP5aWK5xMnAd5DFkzDC7XA4e9srgZM2F9xlyXFZ0lR54bzQVLVw9wrfQcBSbcnGIX%2F%2BglwoQWzFCZonKa53RyOb58KNIiretPCbBJ6ZTp%2FCBnxZwetllTc%2BU%2FFGqv99icRVkuIW6d7VWhO2lQHk1rN8DsbGn7UHJFPJmkIaX3mrnHByzmx3FX%2FCp6EbmtQ0wpRvwzsTap9g1JGGzHTe9JHidZpQDkvF0zUqlD6MZ0T1zsbO8zmtnyfrUQOqjPf%2BeA%2FhrCieEh%2FMn4qbOMPB899sqMYZNCxuD3W7887AejTTTDv2cRNZPwNGzRx7nfSTLx8SRm5kDYE1ZGlzTxB2kDq2PqPDlVElkoG4ISCo%2FKayB6yt8o7Mzbx8LwkTpb7BWhUpQCIXvGsoiZCtTukqQDHarlXbS%2FItK0gb6Eov9liWmjgQbkPMOLh4dwflGcBQ6TP8pza8uSb1WiMof82bTyoNAXWOfHnZV0rWhzw8wVbX5wXJI6Mhzj8nZULNOc0Q%2FPNDsCrgB0lllaiuVnBnH%2FjPdUwD06OpqmdZ4X89B9IugMfLQ4UgvwRUsAljDb5kGMePtKhzSXNhkElfhI8%2Ft4Dmw2qv3L%2Fr5SkM6%2BtfQQXRrKgulzMrbZy%2F3Yo1qKp%2FdJP48QjQcjT2Oby%2FdrXvA29wDFA1R2Wc%2BUBhh95XGSH7NZjv6vODezuugxv%2BSi96OCoLJ2huPFATpJWejtZ2uEEuySlTkqGr%2FLph5ChDxoXgDN5MsUnssRFVwdLi76fYcIWAKB%2FtXLbdkKCw1ngJ4apTpVbHbwzNE5L1cRW2OoAXIeWO6MXUWuhs1XBmuaEd%2Fow%2F5EZjOXTSbl9yKpmlqnBzgqRYozkxRH4dd9LEqyEgjoa2fO%2BLx5V9rh%2Fhjtk5Pid%2FznEkX672oEFjRtUn6CRTUnRjXtjBcWdkutEmCA%2Bok21uRK6BD8%2BhDe%2B3C%2BieeMR8M%2BDqzi8mS8zAyjxvX%2FoAw%2B9zJI%2FhSbdKcxau0%2FkbI3nce24R217CN7KXqXWIZlJ09UAK2I7iPyoHDPvojf%2FMGxK3Sgre0TXGbf7ub6GJCbbkWhAqqvC7dlYY02mE2%2BE%2BsiuDrbtLjtQdKnc%2BbBWEFC79MZlId0g64xrHlmYm5zGRUfB46CDbhAcJcBaBBlxl87mVs34ABHeTr9eJLpDii%2FDipdDOVg5F77No5A7JGKYuTI2y7dd%2B216jQ5gLex%2FdS2C0zQIWulI76OyoWuPHHhdYPDkyfRIDsSM5LU9pJFSBYgvfxMQTO08Giiq4qdi1jK%2BZmwfyu%2FOT3v4NZcpNOGaWXJBRcjVvFKYJkR2cklxSklcYYEjrjoZ%2BSbgaliZmVarlXUhnJRxyqIUWKTH9CAdotPqdnv4Yk0vWdMb9s%2BqpUAVcHQCfx1Bts%2Fn%2Fn%2BnscpLozwfLlz7Ae8SLk0d6N%2FxdzhXYD6K7JPd5YDIiiVDaxnkmFDK6LoAaoCYnD8N2%2BNcR9CkgAlBzYLceav4IW5WbtlwJzrGVT1tRT1rRDZOMBckKxwxySIS1sufKXw3aZg19UaJkYVnOpcufdd%2BhNKXpw0ac7zQRt15H2Dj%2FwZ7jE5vwsNs4rzoKJezNYrC75mqSkrDgw42bM%3D"
    print(aes_decrypt(unquote(enc_string), b"AAAANG4EOnTybYEj"))
