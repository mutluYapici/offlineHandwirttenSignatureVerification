import numpy as np
import cv2

#from dataAugmentationMakale import CV_sayisi
from prokod.imzaFonksiyonlarim import BinaryResimYukle, PILResimYukle, ResmiYenidenBoyutlandir, ResimSinirlariniBelirle,YeniResimSinirlariniBelirle, CokluImg2Array, CokluCrop, PILResmiYenidenBoyutlandir, ImzaVeritabaniniYukle,ImzaVeritabaniniYukleSIAMES, VeritabaniniDosyayaKaydetHDF5, VeritabaniniDosyadanYukle, VeritabaniniDosyayaKaydet,IzgaraOzniteligi
from keras.preprocessing.image import array_to_img, img_to_array, load_img
import keras

"""       ÖNCELİKLE TÜM MALLWARE BYTE DOSYLARINI OKUYUP RENKLİ VE GRİ OLMAK ÜZERE DOSYALARA KAYDEDELİM      """
##gELEN X DİZİSİNDEKİ HERBİR HEX DEĞERİNİ PİKSEL İÇİN DECİMAL DEĞERİNE ÇEVİRİYORUZ
def hextodec(x):
  v=[]
  for t in x:
	try:
	   int(t, 16)
	   v.append(int(t,16))
	except:
	  False
  return np.asarray(v)


## BYTE DOSYALARINI OKUYALIM VE SIRASIYLA DECİMAL MATRİSLERE ÇEVİRELİM
## okunacakElemanSayisi değeri -1 iken tüm dosyayı sonuna kadar okuyarak diziye yükler okunacakElemanSayisi değeri gelirse
# okunacakElemanSayisi değeri kadar dizi elemani okur dosyanın tamamını okumaz
def byteDosyasiniOku(dosyaAdi,okunacakElemanSayisi=-1):
	a=0
	im=[]
	with open(dosyaAdi, "rb") as f:
		line = f.readline()
		while line:
			if a>=okunacakElemanSayisi and okunacakElemanSayisi >= 0:
				break
			line=np.asarray(line.split())
			h=hextodec(line[1:]) #ilk eleman satır sayısı onu almayalım
			if (len(h) > 0):
				im.append(h)
				a+=len(h)
			line = f.readline()
	return np.asarray(im).flatten("F")




## CSV dokyasını okuyarak dizi gönderiyor, eğer ayraç belliyse ayraca göre okuyor değilse object şeklinde başlıklara göre saklıyor
def CSVOku(dosya,ayrac=False):
	import csv
	dizi=[]
	with open(dosya, newline='') as csvfile:
		if(ayrac!=False):
			read = csv.reader(csvfile, delimiter=ayrac, quotechar='|')

		else:
			read = csv.DictReader(csvfile)

		for row in read:
			dizi.append(row)
	return dizi


###Dizide gelen şekli resim olarak CV2 ile kaydedecek
#kayitAdi değilse kayit içinde gelen isme göre kaydedecek False ise return edecek
def diziyiResmOlarakKaydet(dizi,kayitAdi):
	try:
		a=dizi.shape[0]
		a = dizi.shape[1]
		a = dizi.shape[2]
		cv2.imwrite(kayitAdi, dizi)
	except:
		print("Dizinin Resme Çevilebilmesi İçin NUMPY Tipinde ve Sonuncusu Renk Kanalı Olan 3 Boyut Olmalıdır. (224,224,3) ")


### GELEN TEK BOYUTLU DİZİYİ ÇEVRİLEBİLECEK EN YAKIN KARE MATRİS BOYUTLARINA GÖRE AYARLAYALIM
# Eğer mod GRI ise Dizi boyutunun en yakın tam karesine göre boyut ayarlayıp 1 kanal verelim
# mod RENKLİ ya da RGB ise Dizi boyutunun 3 te birinin en yakın tam karesine göre boyut ayarlayıp 3 kanal verelim
def diziResimBoyutuAyarlama(dizi, mod="GRI"):
	if(mod.upper() =="GRI"):
		# gri renk için diziyi tam kare yapmalıyız tam kare içi eksik kalan alanlara 0 dolduralım
		c = int(np.ceil(np.sqrt(b.shape[0])))
		k = int(np.square(c))  # en yakın tam kare sayısı
		r = np.append(b, np.zeros(k - b.shape[0]))  ## 0 ile dolduralım sonunu
		r = r.reshape(c, c, 1)  # gri renk için 1 kanal
	elif (mod.upper() == "RENKLİ" or mod.upper() == "RGB"):
		## Renkli resim için önce 3 e tam bölünenini bulup daha sonra en yakın karesini bulalım
		c = int(np.ceil(np.sqrt(b.shape[0] / 3)))
		k = int(np.square(c)) * 3  # en yakın tam kare sayısının üç katını alalım
		r = np.append(b, np.zeros(k - b.shape[0]))  ## 0 ile dolduralım sonunu
		r = r.reshape(c, c, 3)  # gri renk için 1 kanal
	else:
		r=False
	return r







### Convert ALL BYTE Files to GREY and RGB images

dosyaAdlari=CSVOku("malware_veri/trainLabels.csv")

sifirliklar=[]
print("Toplam Dosya Sayısı ="+str(dosyaAdlari.__len__()))
i=1
for ad in dosyaAdlari:
	kayitAdi="HMY_"+ad['Id']+"_"+ad['Class']+".png"
	kaynak="/media/mutlu/7EEAA1A1EAA15665/malware-classification/test/"+ad['Id']+".bytes"
	print(str(i)+". Okunacak Dosya ----> "+kaynak)
	a=byteDosyasiniOku(kaynak)

	if(a.shape[0]==0):
		sifirliklar.append(kayitAdi)
		continue

	print("Dosyada  "+str(a.__len__())+" Satır Veri Var")
	b=np.hstack(a)
	im=diziResimBoyutuAyarlama(b, mod="GRI")
	yol="malware_veri/grey/test/"
	print("Gri Şekil = "+str(im.shape))
	diziyiResmOlarakKaydet(im,yol+kayitAdi)

	yol="malware_veri/rgb/test/"
	im=diziResimBoyutuAyarlama(b, mod="RGB")
	print("Renkli Şekil = "+str(im.shape))
	diziyiResmOlarakKaydet(im,yol+kayitAdi)
	i+=1