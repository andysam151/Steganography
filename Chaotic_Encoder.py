'''
This program takes an image and encrypts it with a message in the LSB of the red value of the image. It can also decrypt
an encrypted image and will return a string in the output.
'''
from PIL import Image


def encoder(message_to_encode, cover_image, output_file):

    cover_image = Image.open(cover_image)
    red_split = cover_image.split()[0]
    green_split = cover_image.split()[1]
    blue_split = cover_image.split()[2]

    x_size = cover_image.size[0]
    y_size = cover_image.size[1]
    binary_message = ''.join('{:08b}'.format(ord(c)) for c in message_to_encode)
    count = 0
    encoded_image = Image.new('RGB', cover_image.size)
    pixel = encoded_image.load()
    for i in range(x_size):
        for j in range(y_size):
            red_split_pix = bin(red_split.getpixel((i, j)))

            if count < len(binary_message):
                red_split_pix = red_split_pix[:-1] + binary_message[count]
                count = count + 1
            else:
                red_split_pix = red_split_pix[:-1] + '0'
            pixel[i, j] = (int(red_split_pix, 2), green_split.getpixel((i, j)), blue_split.getpixel((i, j)))

    cover_image.close()
    encoded_image.save(output_file)
    encoded_image.close()


def decoder(encoded_file):
    encoded_image = Image.open(encoded_file)
    red_split = encoded_image.split()[0]
    x_size = encoded_image.size[0]
    y_size = encoded_image.size[1]
    n = []
    m = ''
    for i in range(x_size):
        for j in range(y_size):
            n.append(bin(red_split.getpixel((i, j)))[-1])

    for l in range(0, len(n), 8):
        if n[l] == 0 and n[l+1] == 0 and n[l+2] == 0 and n[l+3] == 0 and n[l+4] == 0 and n[l+5] == 0 and n[l+6] == 0 \
                and n[l+7] == 0:
            break
        else:
            m += str(n[l])
            m += str(n[l+1])
            m += str(n[l+2])
            m += str(n[l+3])
            m += str(n[l+4])
            m += str(n[l+5])
            m += str(n[l+6])
            m += str(n[l+7])

    secret = ''.join(chr(int(m[i:i+8], 2)) for i in range(0, len(m), 8))
    encoded_image.close()
    return secret


text = open("C:/Users/andys/Documents/Programming/IDE Workspace/Python/Image Coding/test text/test1.txt", 'r')
template_image = 'C:/Users/andys/Documents/Programming/IDE Workspace/Python/Image Coding/test images/face.jpg'
encrypted_image = 'C:/Users/andys/Documents/Programming/IDE Workspace/Python/Image Coding/output/Encoded_output.png'

encoder(text.read(), template_image, encrypted_image)
print(decoder(encrypted_image))
