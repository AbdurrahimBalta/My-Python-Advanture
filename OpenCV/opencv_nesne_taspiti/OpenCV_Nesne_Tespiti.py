#%% Kenar algılama

import cv2
import matplotlib.pyplot as plt
import numpy as np

#resmi içe aktar

img = cv2.imread("london.jpg", 0)
plt.figure(), plt.imshow(img, cmap = "gray"), plt.axis("off")

edges = cv2.Canny(image = img, threshold1 = 0, threshold2 = 255)
plt.figure(), plt.imshow(edges, cmap = "gray"), plt.axis("off")

med_val = np.median(img)
print(med_val)

low = int(max(0,(1-0.33)*med_val)) #sık kullanılan alt ve üst eşik belirme yöntemi
high = int(min(255,(1 + 0.33)*med_val))

print(low)
print(high)

edges = cv2.Canny(image = img, threshold1 = low, threshold2 = high)
plt.figure(), plt.imshow(edges, cmap = "gray"), plt.axis("off")

# blur işlemiyle kenarları azalttık tekrardan eşik hesaplıyoruz
blurred_img = cv2.blur(img, ksize = (5,5)) #kernelsize artırılarak kenarlar daha belirginleştirirelibilir
plt.figure(), plt.imshow(blurred_img, cmap = "gray"), plt.axis("off")


med_val = np.median(blurred_img)
print(med_val)


low = int(max(0,(1-0.33)*med_val)) 
high = int(min(255,(1 + 0.33)*med_val))

print(low)
print(high)

edges = cv2.Canny(image = blurred_img, threshold1 = low, threshold2 = high)
plt.figure(), plt.imshow(edges, cmap = "gray"), plt.axis("off")
#%% köşe algılama
import matplotlib.pyplot as plt
import numpy as np
import cv2

img = cv2.imread("sudoku.jpg",0)
img = np.float32(img) #değişken tiğinde farklılıklar olmaması için ondalıklı sayılara çeviriyoruz 
print(img.shape)
plt.figure(),plt.imshow(img, cmap = "gray"), plt.axis("off")

# harris corner detection

dst = cv2.cornerHarris(img, blockSize = 2, ksize = 3, k = 0.04)# blocksize = komşuluk boyutun #ksize = kutucuk boyutu #k = harris free parametr
plt.figure(), plt.imshow(dst, cmap = "gray"), plt.axis("off")

dst = cv2.dilate(dst, None)
img[dst > 0.2 * dst.max()] = 1 # kutucuları genişletmek için bir hesap
plt.figure(), plt.imshow(dst, cmap = "gray"), plt.axis("off")

# shi tomsai detection 

img = cv2.imread("sudoku.jpg",0)
img = np.float32(img) 
corners = cv2.goodFeaturesToTrack(img, 100, 0.001, 10) # 100 = max köşe sayısı,  0.001 = kalite seviyes , 10 iki köşe arasındaki mesafe 
corners = np.int64(corners)

for i in corners:
    x,y = i.ravel()
    cv2.circle(img, (x,y),3,(125,125,125),cv2.FILLED)
#%% Kontur 
    
import cv2 
import matplotlib.pyplot as plt
import numpy as np

img = cv2.imread("contour.jpg",0)
plt.figure(), plt.imshow(img, cmap= "gray"),plt.axis("off")
img, contours, hierarch = cv2.findContours(img, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE) #iç ve dış ayıklamayı , köşelerin felan kodlanmasını sağlıyor

internal_countour = np.zeros(img.shape)   
external_countour  = np.zeros(img.shape)
    
for i in range(len(contours)):
    
    #external
    if hierarch[0][i][3] == -1:
        cv2.drawCountours(external_countour,contours, i, 255, -1)
    else: #internal
        cv2.drawCountours(internal_countour,contours, i, 255, -1)


plt.figure(), plt.imshow(external_countour, cmap= "gray"),plt.axis("off")
plt.figure(), plt.imshow(internal_countour, cmap= "gray"),plt.axis("off")

#%% renk ile nesne tespiti

import cv2
import numpy as np
from collections import deque

# nesne merkezini depolayacak veri tipi
buffer_size = 16
pts = deque(maxlen = buffer_size)

# mavi renk aralığı HSV
blueLower = (84,  98,  0)
blueUpper = (179, 255, 255)

# capture
cap = cv2.VideoCapture(0)
cap.set(3,960)
cap.set(4,480)

while True:
    
    success, imgOriginal = cap.read()
    
    if success: 
        
        # blur
        blurred = cv2.GaussianBlur(imgOriginal, (11,11), 0) 
        
        # hsv
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        cv2.imshow("HSV Image",hsv)
        
        # mavi için maske oluştur
        mask = cv2.inRange(hsv, blueLower, blueUpper)
        cv2.imshow("mask Image",mask)
        # maskenin etrafında kalan gürültüleri sil
        mask = cv2.erode(mask, None, iterations = 2)
        mask = cv2.dilate(mask, None, iterations = 2)
        cv2.imshow("Mask + erozyon ve genisleme",mask)
        
        # farklı sürüm için
        # (_, contours,_) = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # kontur
        (contours,_) = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        center = None

        if len(contours) > 0:
            
            # en buyuk konturu al
            c = max(contours, key = cv2.contourArea)
            
            # dikdörtgene çevir 
            rect = cv2.minAreaRect(c)
            
            ((x,y), (width,height), rotation) = rect
            
            s = "x: {}, y: {}, width: {}, height: {}, rotation: {}".format(np.round(x),np.round(y),np.round(width),np.round(height),np.round(rotation))
            print(s)
            
            # kutucuk
            box = cv2.boxPoints(rect)
            box = np.int64(box)
            
            # moment
            M = cv2.moments(c)
            center = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))
            
            # konturu çizdir: sarı
            cv2.drawContours(imgOriginal, [box], 0, (0,255,255),2)
            
            # merkere bir tane nokta çizelim: pembe
            cv2.circle(imgOriginal, center, 5, (255,0,255),-1)
            
            # bilgileri ekrana yazdır
            cv2.putText(imgOriginal, s, (25,50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255), 2)
            
            
        # deque
        pts.appendleft(center)
        
        for i in range(1, len(pts)):
            
            if pts[i-1] is None or pts[i] is None: continue
        
            cv2.line(imgOriginal, pts[i-1], pts[i],(0,255,0),3) # 
            
        cv2.imshow("Orijinal Tespit",imgOriginal)
        
    if cv2.waitKey(1) & 0xFF == ord("q"): break

#%% Şablon eşleme tepmlate matching
import cv2
import matplotlib.pyplot as plt
import numpy as np


img = cv2.imread("cat.jpg",0)
print(img.shape)
template = cv2.imread("cat_face.jpg",0)
print(template.shape)
h , w = template.shape

methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR', # korelasyon medhodları
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

for meth in methods:
    
    method = eval(meth) #eval stringi fonksiyona çevirir 'TM_CCOEFF_NORMED' ->> TM_CCOEFF_NORMED
    
    res = cv2.matchTemplate(img, template, method)
    
    print(res.shape)
    
    min_val, max_val, min_loc, max_loc =  cv2.minMaxLoc(res)
    
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
        
    bottom_right = (top_left[0] + w, top_left[1] + h)
    
    cv2.rectangle(img, top_left, bottom_right, 255, 2)
    
    plt.figure()
    plt.subplot(121) 
    
    
    
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

































    
    
    











































































