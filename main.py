##### IMPORTACIONES #####
import cv2
import pytesseract
#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'





##### VARIABLES GLOBALES #####
var_1 = 1
var_2 = 1
var_3 = 25
var_4 = 25
var_5 = 0.0
##### FUNCIONES #####

### DETECTA PLACAS PATENTE DESDE UNA IMAGEN ###
def detecta_patente(ruta_imagen):
    patente = []

    imagen = cv2.imread(ruta_imagen)
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    gris = cv2.blur(gris, (var_1, var_2)) ### CALIBRAR PARA MEJOR DETECCION ###   3, 3
    canny = cv2.Canny(gris, var_3, var_4) ### CALIBRAR PARA MEJOR DETECCION ###   125, 400
    canny = cv2.dilate(canny, None, iterations = 1)

    cnts, _ = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(imagen, cnts, -1, (0, 0, 255), 2)

    for c in cnts:
        area = cv2.contourArea(c)
        
        x, y, w, h = cv2.boundingRect(c)
        epsilon = var_5 * cv2.arcLength(c, True) ### CALIBRAR PARA MEJOR DETECCION ###   0.1
        approx = cv2.approxPolyDP(c, epsilon, True)

        #cv2.drawContours(imagen, [approx], 0, (0, 0, 255), 3)

        if len(approx) == 4 and area > 5000:
            #cv2.drawContours(imagen, [approx], 0, (0, 255, 0), 3)

            aspect_ratio = float(w) / h

            if aspect_ratio > 1.5: ### CALIBRAR PARA FILTRAR PATENTES PERMITIDAS ###   2.4
                patente = gris[y : y + h, x : x + w]

    return patente



### RECONOCE EL TEXTO DE UNA PLACA PATENTE ###
def reconoce_patente(patente):
    texto = pytesseract.image_to_string(patente, config = '--psm 11')

    ### ELIMINA POSIBLE ERROR ###
    texto = texto.replace('HILE', '')
    texto = texto.replace('MILE', '')

    texto_aux = ''
    caracteres_permitidos = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'P', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    ### ELIMINA LOS CARACTERES MAL RECONOCIDOS ###
    for i in texto:
        for j in caracteres_permitidos:
            if i == j:
                texto_aux = texto_aux + i
    
    return texto_aux





##### SISTEMA PRINCIPAL #####

texto_patente = ''

while len(texto_patente) == 0:
    patente = detecta_patente('prueba2.jpg')
    if len(patente) > 0:
        texto_patente = reconoce_patente(patente)
        
        if len(texto_patente) > 5:
            print('\nPatente: ' + texto_patente[0:2] + ' ' + texto_patente[2:4] + ' ' + texto_patente[4:6] + '\n')
            cv2.imshow('Patente', patente)
            cv2.waitKey(0)
        else:
            texto_patente = ''
    else:
        #print('Patente no reconocida!!')
        print()
    
    if var_5 < 0.2:
        var_5 += 0.1
    else:
        var_5 = 0.0
        if var_1 < 10:
            var_1 += 1
        else:
            var_1 = 1
            if var_2 < 10:
                var_2 += 1
            else:
                var_2 = 1
                if var_3 < 500 and var_3 < var_4:
                    var_3 += 25
                else:
                    var_3 = 25
                    if var_4 < 500:
                        var_4 += 25
                    else:
                        print('No se encontró la patente!!')
                        break
    if len(texto_patente) == 0:
        print('VAR 1: ' + str(var_1))
        print('VAR 2: ' + str(var_2))
        print('VAR 3: ' + str(var_3))
        print('VAR 4: ' + str(var_4))
        print('VAR 5: ' + str(var_5))






#cv2.imshow('Patente', patente)
#cv2.waitKey(0)

#cnts, _ = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
#cv2.drawContours(imagen, cnts[64], -1, (0, 255, 0), 2)
"""
for c in cnts:
    area = cv2.contourArea(c)
    
    x, y, w, h = cv2.boundingRect(c)
    epsilon = 0 * cv2.arcLength(c, True)
    #epsilon = 0.1 * cv2.arcLength(c, True) # DETECTA PRUEBA 5
    approx = cv2.approxPolyDP(c, epsilon, True)

    #cv2.drawContours(imagen, [approx], 0, (0, 0, 255), 3)

    if len(approx) == 4 and area > 5000:
        #print(approx)
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
            text = text.replace("e", "")
            text = text.replace(")", "")
            if len(text) > 6:
                text = text[0:6]
            if len(text) == 6:
                text_1 = ''
                text_2 = ''
                if text[2].isdigit():
                    text_1 = text[0:2]
                    text_2 = text[3:6]
                else:
                    text_1 = text[0:4]
                    text_2 = text[4:6]
                print('\nPatente: ' + text_1 + '-' + text_2 + '\n')
            else:
                print('Patente no reconocida: ' + text)
            #cv2.imshow('Patente', patente)
            #cv2.moveWindow('Patente', 780, 10)
            #cv2.rectangle(imagen, (x, y), (x + w, y + h), (0, 255, 0), 3)
            #cv2.putText(imagen, text, (x - 20, y - 10), 1, 2.2, (0, 255, 0), 3)
      
cv2.imshow('Imagen', imagen)
cv2.moveWindow('Imagen', 45, 10)
cv2.waitKey(0)
"""