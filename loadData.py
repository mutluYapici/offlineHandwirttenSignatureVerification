
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


import numpy as np
import matplotlib.pyplot as plt
from keras import backend as K


imzaAdi="Mimza_0115"
gercek_imza_sayisi=214
resimEn,resimBoy=224,224
class_num=2
K.image_data_format()
kanal=1
input_shape = (resimEn ,resimBoy, kanal)



"""############################      MCYT WRİTER DEPENDENT       #############################"""


#################################################   VERİ YÜKLEME SON AŞAMA  SADECE ÇOĞALTTIĞIM KLASÖRLERDEN YÜKLEYELİM YUKARISI ÖNEMLİ DEĞİL    ##############################################
from modules.dataPreprocess import ImzaVeritabaniniYukle

Gegitim = ImzaVeritabaniniYukle("data/"+imzaAdi+"/reconstructed_Genuine_10", "c-*.jpg", resimEn,resimBoy,214, 0, 10, 255, True, 255,  True)
Gtest= ImzaVeritabaniniYukle("data/"+imzaAdi+"/reconstructed_Genuine_5", "c-*.jpg", resimEn,resimBoy,229, 0, 10, 255, True, 255,  True)
Stest= ImzaVeritabaniniYukle("data/"+imzaAdi+"/reconstructed_Forgeries", "cf-*.jpg", resimEn,resimBoy,200, 0, 10, 255, True, 255,  True)


GVeri = ImzaVeritabaniniYukle("data/0115", "*v*.bmp", resimEn, resimBoy, 15, 0, 10, 255, True, 255, True)
SVeri = ImzaVeritabaniniYukle("data/0115", "*f*.bmp", resimEn, resimBoy,15, 0, 10, 255, True, 255, True)

X_train = np.asarray(Gegitim[0]).astype('float16') / np.asarray(Gegitim[0]).max()
Y_train = np.asarray(Gegitim[1])

X_val = np.asarray(Gtest[0]).astype('float16') / np.asarray(Gtest[0]).max()
Y_val = np.asarray(Gtest[1])


"""   EĞİTİMDE SAHTE İMZALARI KULLANMAYINCA SAHTELERİ BULAMIYOR BU NEDENLE YİNE SAHTELERİ KULLANMAYACAĞIM
ANCAK FARKLI İMZALARIN GERÇEKLERİNİ BU İMZANIN SAHTESİYMİŞ GİBİ EĞİTİME KATACAĞIM DİĞER BİR YÖNTEM DE TRANSFER LEARNİNG OLABİLİR İMAGENET ÜZERİNE EĞİTEBİLİRİM"""

#SUANDA 553 İMZZASINI EĞİTİYORUM BUNDAN FARKLI 15 İMZANIN GERÇEKLERİNİ ALALIM EĞİTİMDE SAHTE DİYE KULLANMAK İÇİN

SahteymisGibiegitim = ImzaVeritabaniniYukle("data/1*", "cf-*.jpg", resimEn, resimBoy, 10, 0, 10, 255, True, 255,  True)

##Eğitime katalım
SGY_egitim=[]
for i in range(SahteymisGibiegitim[1].__len__()):
	SGY_egitim.append([0,1])

X_train=np.append(X_train ,  np.asarray(SahteymisGibiegitim[0]).astype('float16') / np.asarray(SahteymisGibiegitim[0]).max(),axis=0)
Y_train=np.append(Y_train ,  np.asarray(SGY_egitim),axis=0)
imzaAdi2=imzaAdi+"_"+str(gercek_imza_sayisi)+"_"
