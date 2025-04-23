import numpy as np
from PIL import Image, ImageGrab
import scipy.signal as ss
from scipy.misc import toimage
from time import sleep
from helper import send_email

#Setting
bbox=(0,100,800,800)
scanTime = 20
user = 'xxxxxx@gmail.com'
pwd = 'xxxxxxx'
thres = [-3.5, -3.5, -3., -5., -2.7]

#Initialize
kerf = []
kerm = []
for i in range(5):
    tmp = np.array(Image.open( str(i+1) + '.png' )).astype(np.float32)[:,:,0:3]
    kerf.append(tmp[::-1,::-1,::-1])
    kerm.append(kerf[i]>0)

nm = ['Snorlax', 'Chansey', 'Lapras', 'Porygon', 'Aerodactyl']

#Execution
print 'Scanning...'
for t in range(scanTime):

    im = ImageGrab.grab(bbox=bbox)
    #im.save("foobar.png")
    A = np.array(im).astype(np.float32)[:,:,0:3]
    A2 = A**2

    for i in range(5):
        res = ss.fftconvolve(A2, kerm[i], 'valid') - 2*ss.fftconvolve(A, kerf[i], 'valid')
        nres = np.squeeze(((res - np.mean(res)) / np.std(res)) < thres[i])
        
        if np.any(nres):
            print nm[i] + ' Detected!'
            im2 = toimage(nres)
            im2.save('foobar.png')
            break
            
    sleep(15)
    print str(t)


