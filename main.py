import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

patente = []

imagen = cv2.imread('prueba4.jpg')
gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
gris = cv2.blur(gris, (3, 3))
canny = cv2.Canny(gris, 150, 200)
canny = cv2.dilate(canny, None, iterations = 1)

#_, cnts, _ = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE) #OpenCV 3
cnts, _ = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE) #OpenCV 4
#cv2.drawContours(imagen, cnts, -1, (0, 255, 0), 2)

contador = 1

for c in cnts:
    area = cv2.contourArea(c)
    
    x, y, w, h = cv2.boundingRect(c)
    epsilon = 0.09 * cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, epsilon, True)

    if len(approx) == 4 and area > 9000 and contador < 2:
        cv2.drawContours(imagen, [approx], 0, (0, 255, 0), 3)

        aspect_ratio = float(w) / h

        if aspect_ratio > 2.4:
            patente = gris[y : y + h, x : x + w]
            text = pytesseract.image_to_string(patente, config='--psm 11')
            text = text.replace(" ", "")
            text = text.replace("\n", "")
            text = text.replace(":", "")
            text = text.replace("»", "")
            text = text.replace("°", "")
            text = text[0:6]
            text_1 = ''
            text_2 = ''
            if text[2].isdigit():
                text_1 = text[0:2]
                text_2 = text[3:6]
            else:
                text_1 = text[0:4]
                text_2 = text[4:6]
            print('\nPatente: ' + text_1 + '-' + text_2 + '\n')
            #cv2.imshow('Patente', patente)
            #cv2.moveWindow('Patente', 780, 10)
            cv2.rectangle(imagen, (x, y), (x + w, y + h), (0, 255, 0), 3)
            cv2.putText(imagen, text, (x - 20, y - 10), 1, 2.2, (0, 255, 0), 3)

            contador += 1
      
cv2.imshow('Imagen', imagen)
cv2.moveWindow('Imagen', 45, 10)
cv2.waitKey(0)