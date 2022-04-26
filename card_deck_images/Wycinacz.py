import cv2
import numpy as np

'''
1. wczytaj zdjecie
1,5. Wymierz ile biale ile zielone
2. dotnij do bialego
3. zielone zamien na przezroczyste hehe
4. zapisz jako png
'''

# W PIXELACH PODANE
start_width = 6
start_height = 9
card_width = 120
card_height = 180
btw_card = 10 # zgadza sie dla wysokosci i szerokosci
cards_number = 12*4


def crop_card():
    '''
    Kurwa j w wysokosci

    i nie i > 2 tylko % 13 daje type(int)
    '''

    j = 0
    j2 = 0
    i2 = 0
    img = cv2.imread("Card_deckv1.jpg")
    for i in range(1,cards_number):

        if i > 1:
            i2 += 1
        if i == 1 or i == 13 or i == 25 or i == 37 :
            j +=1
            i2 = 0

            if i == 13 or i == 25 or i == 37 :
                j2 +=1
        if i >= 13 and i < 25:
            i-=12
        elif i >= 25 and i < 37:
            i-=24
        elif i >= 37:
            i-=36
        cropped_image = img[start_height+btw_card*j2+(card_height*j2):start_height+(card_height*j)+btw_card*j2, start_width+btw_card*i2+(card_width*i2):start_width+(card_width*i)+btw_card*i2] # najpeierw wysokosc potem szerokosc
        cv2.imwrite("test_card{}.jpg".format(i), cropped_image)

def green_to_transparent(img):
    '''
    img - cropped_img (cv2.imread)
    Zmienia zielona otoczke wokol karty na przezroczysta i zapisuje plik w png
    '''
    # Convert to RGB with alpha channel
    output = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    # Color to make transparent
    col = (106, 174, 105)
    # Color tolerance
    tol = (63, 40, 64)
    # Temporary array (subtract color)
    temp = np.subtract(img, col)
    # Tolerance mask
    mask = (np.abs(temp) <= tol)
    mask = (mask[:, :, 0] & mask[:, :, 1] & mask[:, :, 2])

    # Generate alpha channel
    temp[temp < 0] = 0                                            # Remove negative values
    alpha = (temp[:, :, 0] + temp[:, :, 1] + temp[:, :, 2]) / 3   # Generate mean gradient over all channels
    #print(alpha)
    #print(mask)
    alpha[mask] = alpha[mask] / np.max(alpha[mask]) * 255         # Gradual transparency within tolerance mask
    alpha[~mask] = 255                                            # No transparency outside tolerance mask

    # Set alpha channel in output
    output[:, :, 3] = alpha

    # Output images
    #cv2.imwrite('imagescolortrans_alpha.png', alpha)
    #cv2.imwrite('imagescolortrans_output.png', output)
    return output


def crop_card2():
    j = 3
    j2 = 3
    i2 = 0
    img = cv2.imread("Card_deckv1.jpg", cv2.IMREAD_COLOR)
    for i in range(1,14):

        if i > 1:
            i2 += 1
        if i == 1 or i == 13 or i == 25 or i == 37 :
            j +=1
            i2 = 0

            if i == 13 or i == 25 or i == 37 :
                j2 +=1

        cropped_image = img[start_height+btw_card*j2+(card_height*j2):start_height+(card_height*j)+btw_card*j2, start_width+btw_card*i2+(card_width*i2):start_width+(card_width*i)+btw_card*i2] # najpeierw wysokosc potem szerokosc
        # wyciac zielone tlo
        # tolerancje ustawic wycinania i wtyciac i na png zmienic i chuj
        output = green_to_transparent(cropped_image)
        cv2.imwrite("test_card{}.png".format(i), output)



def crop_king():
    '''
    SZKOLA DRUCIARSTWA
    '''
    start_width = 8
    start_height = 7
    img = cv2.imread("Card_deckv2.jpg", cv2.IMREAD_COLOR)
    cropped_image1 = img[start_height:start_height+card_height, start_width:start_width+card_width]
    cropped_image2 = img[start_height+card_height+btw_card:start_height+(card_height*2)+btw_card, start_width:start_width+card_width]
    cropped_image3 = img[start_height+(card_height*2)+(btw_card*2):start_height+(card_height*3)+(btw_card*2), start_width:start_width+card_width]
    cropped_image4 = img[start_height+(card_height*3)+(btw_card*3):start_height+(card_height*4)+(btw_card*3), start_width:start_width+card_width]
    # cv2.imshow("image1", cropped_image1)
    # cv2.imshow("image2", cropped_image2)
    # cv2.imshow("image3", cropped_image3)
    # cv2.imshow("image4", cropped_image4)
    output1 = green_to_transparent(cropped_image1)
    output2 = green_to_transparent(cropped_image2)
    output3 = green_to_transparent(cropped_image3)
    output4 = green_to_transparent(cropped_image4)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    cv2.imwrite("test_card15.png", output1)
    cv2.imwrite("test_card16.png", output2)
    cv2.imwrite("test_card17.png", output3)
    cv2.imwrite("test_card18.png", output4)
    return

if __name__ == '__main__':
    #crop_card2()
    crop_king()
