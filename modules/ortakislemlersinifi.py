#coding=utf-8
	#################################################################################################
	#												#
	#	Bu dosyada tüm modellerde kullanacağımız ortak işlem, parametre ve fonksiyonları	#
	#	Ortakislemler sınıfında tanımlıyoruz. Diğer model sınıflarına bu sınıfı miras		#
	#	alma yoluyla aktarıyoruz.								#
	#						M. Mutlu YAPICI  -  11.08.2018			#
	#												#
	#################################################################################################

import numpy as np
import time
import scipy
from keras.preprocessing.image import array_to_img, img_to_array, load_img
from modules.dataPreprocess import BinaryResimYukle, PILResimYukle, ResmiYenidenBoyutlandir, ResimSinirlariniBelirle,YeniResimSinirlariniBelirle, CokluImg2Array, CokluCrop, PILResmiYenidenBoyutlandir, ImzaVeritabaniniYukle,ImzaVeritabaniniYukleSIAMES, VeritabaniniDosyayaKaydetHDF5, VeritabaniniDosyadanYukle, VeritabaniniDosyayaKaydet,IzgaraOzniteligi


from keras.applications.imagenet_utils import decode_predictions
from keras.applications.imagenet_utils import preprocess_input


#### Aşağıda Dogrulama Yöntemlerinde elde edilecek doğrulama verilerini nesne halinde göndermek için
class DogrulamaElemanlari:
	def __init__(self, DG, YN, FAR, FRR, TPR, FPR,F1,RECALL,PRECISION,TNR,AER):
		self.DogruSayisi = DG
		self.YanlisSayisi = YN
		self.F1_score=F1
		self.FAR = FAR
		self.FRR = FRR
		self.TPR = TPR
		self.FPR = FPR
		self.RECALL=RECALL
		self.PRECISION=PRECISION
		self.TNR=TNR
		self.AER=AER



class Ortakislemler:
	def __init__(self):
		self.batch_zaman_fark =0
		self.batc_oncekizaman=0


	def veriYukle(self,durum='rastgele',kisi_sayisi=1, resimEn = 500,resimBoy=500,modelSecimi='Normal'):
		"""
		#kisi_sayisi=1
		gercekImzaSayisi=(24*kisi_sayisi)
		sahteImzaSayisi = (30*kisi_sayisi)
		EKGIS=(15*kisi_sayisi) #Eğitimde Kullanılacak Gerçek İmza Sayısı
		EKSIS=(15*kisi_sayisi) #Eğitimde Kullanılacak Sahte İmza Sayısı
		TKGIS=gercekImzaSayisi-EKGIS #Testte Kullanılacak Gerçek İmza Sayısı
		TKSIS=sahteImzaSayisi-EKSIS #Testte Kullanılacak Sahte İmza Sayısı
		"""
		#gercekImzaSayisi = (318 * kisi_sayisi)
		#sahteImzaSayisi = (388 * kisi_sayisi)
		veriGercek=24
		veriSahte=30
		gercekImzaSayisi = (veriGercek * kisi_sayisi)
		sahteImzaSayisi = (veriSahte * kisi_sayisi)
		EKGIS = (15 * kisi_sayisi)  # Eğitimde Kullanılacak Gerçek İmza Sayısı
		EKSIS = (15 * kisi_sayisi)  # Eğitimde Kullanılacak Sahte İmza Sayısı
		TKGIS = gercekImzaSayisi - EKGIS  # Testte Kullanılacak Gerçek İmza Sayısı
		TKSIS = sahteImzaSayisi - EKSIS  # Testte Kullanılacak Sahte İmza Sayısı

		## Resim boyutları yükseklik ve en
		#resimBoy, resimEn = 500, 500







		#Verileri Yükleyelim
		if(modelSecimi=='Normal'): ### 	EĞER NORMAL MODELE GÖRE YAPACAKSAK EEĞİTİM VERİLERİ SAHTE VE GERÇEK KARIŞIK GELSİN

			#GVeri=ImzaVeritabaniniYukle("firmasSINTESISmanuscritas","c-*.jpg", resimEn, resimBoy, gercekImzaSayisi, 1, 10, 255,  True, 255, True)
			##Gerçek verileri Dosyaya Kaydedelim
		#Yüksek veri boyutunda bu dosya tipine kayıt başarısız	VeritabaniniDosyayaKaydet("GVerimmm_"+str(kisi_sayisi), GVeri[0], False)#VeritabaniniDosyayaKaydet(dosyaAdi, veri, ekranaYaz=False):
		#	veriSekli = (gercekImzaSayisi, resimBoy, resimEn, 1)
		#	VeritabaniniDosyayaKaydetHDF5("GVeri_" + str(kisi_sayisi) + ".hdf5", GVeri[0], veriSekli)  ##VeritabaniniDosyayaKaydetHDF5(dosyaAdi, veri, veriSekli):
		#	print("#####################################    GERÇEK VERİLER BİTTİ SAHTELERİ YÜKLEYELİM    ####################################")

			#SVeri=ImzaVeritabaniniYukle("firmasSINTESISmanuscritas","cf*.jpg", resimEn, resimBoy, sahteImzaSayisi, 1, 10, 255,  True, 255, True)
		#	sveriSekli = (sahteImzaSayisi, resimBoy, resimEn, 1)
		#	VeritabaniniDosyayaKaydetHDF5("SVeri_" + str(kisi_sayisi) + ".hdf5", SVeri[0],sveriSekli)  ##VeritabaniniDosyayaKaydetHDF5(dosyaAdi, veri, veriSekli):
		#Yüksek veri boyutunda bu dosya tipine kayıt başarısız	VeritabaniniDosyayaKaydet("SVeri_" + str(kisi_sayisi), SVeri, False)  # VeritabaniniDosyayaKaydet(dosyaAdi, veri, ekranaYaz=False):

		#ImzaVeritabaniniYukle(kokDizin, dosyaAdi, yeniEn, yeniBoy, yuklenecekResimSayisi=0, dizinDerinligi=0,tolerans=0, arkaRenk=255, orjinallikKorunsunMu=False, arkaRenk2=255, ekranaYaz=False):
			##GPDS VERİTABANI
			#GVeri = ImzaVeritabaniniYukle("firmasSINTESISmanuscritas/751", "c-*.jpg", resimEn, resimBoy, gercekImzaSayisi, 0, 10, 255, True, 255,  True)
			#SVeri = ImzaVeritabaniniYukle("firmasSINTESISmanuscritas/751", "cf*.jpg", resimEn, resimBoy, sahteImzaSayisi, 0, 10, 255, True, 255,  True)

			##MCYT VERİTABANI
			#GVeri = ImzaVeritabaniniYukle("MCYT/0098", "*v*.bmp", resimEn, resimBoy, gercekImzaSayisi, 0, 10, 255, True, 255, True)
			#SVeri = ImzaVeritabaniniYukle("MCYT/0098", "*f*.bmp", resimEn, resimBoy,sahteImzaSayisi, 0, 10, 255, True, 255, True)

			##BİZİM YARATTIĞIMIZ HOCALALRIN VERİTABANI
			GVeri = ImzaVeritabaniniYukle("e_bu_fake/renkli/NT", "c-*.jpg", resimEn, resimBoy, gercekImzaSayisi, 0, 10, 255, True, 255, True)
			SVeri = ImzaVeritabaniniYukle("e_bu_fake/renkli/NT", "cf*.jpg", resimEn, resimBoy, sahteImzaSayisi, 0, 10, 255, True, 255, True)


			X_train, Y_train, X_test, Y_test = [[], []], [], [[], []], []
			if(durum=='rastgele'):
				#Eğer Verileri Rastgele Oluşturacaksak
				#nGVeri=np.asarray(GVeri)
				#nSVeri=np.asarray(SVeri)

				print('RASTGELE   ----------------> '+str(kisi_sayisi))
				#GERCEK ve SAHTE Verilerin İndekslerini Oluşturalım
				Gind=list(range(0,(gercekImzaSayisi)))
				Sind = list(range(0,(sahteImzaSayisi)))

				# GERCEK ve SAHTE Verilerin İndekslerini  SUFFLE İle Karıştıralım Böylece RANDOM Gelmiş Olacaklar
				np.random.shuffle(Gind)
				np.random.shuffle(Sind)

				#Gerçek Eğitim Verilerini Aldık Rastgele
				for a in range(EKGIS):
					inn=Gind.pop(0)
					X_train[0].append(GVeri[0][inn])#X_train in 0 ında verileri (resimler) 1 inde gerçek mi sahtemi oldukları var
					X_train[1].append([1, 0])  # Gerçek veriler 1 0
					Y_train.append([1, 0])#Gerçek veriler 1 0

				#Sahtelerden de rastgele Eğitim verielerini alalım
				for a in range(EKSIS):
					inn=Sind.pop(0)
					X_train[0].append(SVeri[0][inn])#X_train in 0 ında verileri (resimler) 1 inde gerçek mi sahtemi oldukları var
					X_train[1].append([0, 1])  # Sahte veriler 0 1
					Y_train.append([0,1])#Sahte veriler 0 1


				#ŞİMDİDE TEST VERİLERİNİ ALALIM TEST VERİLERİ EĞİTİMDEN ARTA KALANLAR OLACAK
				for a in range(TKGIS):
					inn = Gind.pop(0)
					X_test[0].append(GVeri[0][inn])  # X_test in 0 ında verileri (resimler) 1 inde gerçek mi sahtemi oldukları var
					X_test[1].append([1, 0])  # Gerçek veriler 1 0
					Y_test.append([1, 0])  # Gerçek veriler 1 0

				for a in range(TKSIS):
					inn = Sind.pop(0)
					X_test[0].append(SVeri[0][inn])  # X_train in 0 ında verileri (resimler) 1 inde gerçek mi sahtemi oldukları var
					X_test[1].append([0, 1])  # Sahte veriler 0 1
					Y_test.append([0, 1])  # Sahte veriler 0 1
			else:
				##X_train X_test Y_train Y_test Verilerini Yaratalım: Senaryoya göre 24 tane geçek verinin ilk 15 i eğitim de on 9 u testte kullanılacak ve yine Sahte verilerinin Son 15 i eğitimde ilk 15 i de testte kullanılacak.
				GercekX_trn=GVeri[0][0:EKGIS]
				GercekX_trn=np.asarray(GercekX_trn)
				GercekX_trn.shape
				SahteX_trn=SVeri[0][TKSIS:]
				SahteX_trn=np.asarray(SahteX_trn)
				SahteX_trn.shape
				X_train=np.concatenate((GercekX_trn,SahteX_trn),axis=0)
				X_train.shape

				GercekX_test=GVeri[0][EKGIS:]
				GercekX_test=np.asarray(GercekX_test)
				GercekX_test.shape
				SahteX_test=SVeri[0][0:TKSIS]
				SahteX_test=np.asarray(SahteX_test)
				SahteX_test.shape
				X_test=np.concatenate((GercekX_test,SahteX_test),axis=0)
				X_test.shape

				GercekY_trn=GVeri[1][0:EKGIS]
				GercekY_trn=np.asarray(GercekY_trn)
				GercekY_trn.shape
				SahteY_trn=SVeri[1][TKSIS:]
				SahteY_trn=np.asarray(SahteY_trn)
				SahteY_trn.shape
				Y_train=np.concatenate((GercekY_trn,SahteY_trn),axis=0)
				Y_train.shape

				GercekY_test=GVeri[1][EKGIS:]
				GercekY_test=np.asarray(GercekY_test)
				GercekY_test.shape
				SahteY_test=SVeri[1][0:TKSIS]
				SahteY_test=np.asarray(SahteY_test)
				SahteY_test.shape
				Y_test=np.concatenate((GercekY_test,SahteY_test),axis=0)
				Y_test.shape
			return [GVeri, SVeri, X_train, X_test, Y_train, Y_test, resimBoy, resimEn]
		elif(modelSecimi=='SIAMES'): ###	EĞER MODEL SEÇİMİ SIAMES İSE OZMAN EĞİTİM VE TEST VERİLERİNİ SAHTE VE GERÇEK DİYE GRUP HALİNDE GÖNDERELİM
			# ImzaVeritabaniniYukleSIAMES(kokDizin, dosyaAdi, yeniEn, yeniBoy, yuklenecekResimSayisi=0, dizinDerinligi=0,tolerans=0, arkaRenk=255, orjinallikKorunsunMu=False, arkaRenk2=255, ekranaYaz=False):
			TVeri = ImzaVeritabaniniYukleSIAMES("firmasSINTESISmanuscritas", "*.jpg", resimEn, resimBoy, (54 * kisi_sayisi), 1, 10, 255, True, 255, True) ## tüm veriler
			egitim_grubu=[[],[]] ### Eğitim grubunda sahteler ve gerçekler kişi bazlı ayrılacak
			test_grubu=[[],[]] ### Test grubunda sahteler ve gerçekler kişi bazlı ayrılacak

			EKGIS = 15
			EKSIS = 15
			TKGIS = 9
			TKSIS = 15
			#### Her Bireyden Eğitime İmza Alalım
			for k in range(kisi_sayisi):
				####her kişiden eğitime 15 gerçek 15 sahte alalım
				egitim_grubu[0].append([]) #### Eğitim Grubunun Gerçeğine Yeni Kişi Ekledik
				egitim_grubu[1].append([])  #### Eğitim Grubunun Sahtesine Yeni Kişi Ekledik
				test_grubu[0].append([])  #### Test Grubunun Gerçeğine Yeni Kişi Ekledik
				test_grubu[1].append([])  #### Test Grubunun Sahtesine Yeni Kişi Ekledik

				#Rastgele seçelim
				# GERCEK ve SAHTE Verilerin İndekslerini Oluşturalım
				Gind = list(range(0, (24)))
				Sind = list(range(0, (30)))

				# GERCEK ve SAHTE Verilerin İndekslerini  SUFFLE İle Karıştıralım Böylece RANDOM Gelmiş Olacaklar
				np.random.shuffle(Gind)
				np.random.shuffle(Sind)



				for a in range(EKGIS): ###kişiye ait Eğitimde kullanılacak gerçek imzalar
					inn=Gind.pop(0)
					egitim_grubu[0][k].append(TVeri[k][0][inn])

				for a in range(TKGIS): ###kişiye ait Testte kullanılacak Kalan gerçek imzalar
					inn=Gind.pop(0)
					test_grubu[0][k].append(TVeri[k][0][inn])



				for a in range(EKSIS):  ###kişiye ait Eğitimde kullanılacak SAHTE imzalar
					inn = Sind.pop(0)
					egitim_grubu[1][k].append(TVeri[k][1][inn])

				for a in range(TKSIS):  ###kişiye ait Testte kullanılacak Kalan SAHTE imzalar
					inn = Sind.pop(0)
					test_grubu[1][k].append(TVeri[k][1][inn])




			return [TVeri, egitim_grubu, test_grubu, resimBoy, resimEn]
############ VERİ YÜKLEME BURAYAAAAAAAAAAAA KADAR ################

################ 	RASTGELE VERİ, ÜRETME ########################
#///SİAMES İÇİN GRUPLAR HALİNDE VERİ ÜRETİYOR
	def gen_random_batchSIAMES(self,tumVeri, kisiSayisi, kisiBasiOrnekimza, anchor='Resim'):
		A_verisi, B_verisi, Anchor, cikti = [], [], [], []
		tumKisiIndeksleri = list(range(len(tumVeri[0])))  ### Gelen veri grubunda bulunan kişilerin indexleri

		for i in range(kisiSayisi):  ####her bir kişiden A ve B için veri alacağız Burada A gerçek (Positive) B sahte (Negative)
			kisiInd = np.random.choice((tumKisiIndeksleri))  ## tüm kişiler içerisinden rastgele birini seçelim
			tumImzaInd = list(range(len(tumVeri[0][0])))  ### kişinin tüm gerçek imzalarının indisleri
			for j in range(kisiBasiOrnekimza):  #### tüm imzalar arasından imza sayısı kadar seçeceğiz
				imzaInd = np.random.choice((tumImzaInd))  ## tüm imzaların içerisinden rastgele birini seçelim
				A_verisi += [tumVeri[0][kisiInd][imzaInd]]  ### Gerçek imza tamam şimdi birde sahtesini seçelim
				B_verisi += [tumVeri[1][kisiInd][imzaInd]]  ### birde sahtesini seçelim
				imzaInd = np.random.choice((tumImzaInd))  ## tüm imzaların içerisinden rastgele birini tekrar seçelim çünkü bunu ANCHOR seçmede kullanacağım
				Anchor += [tumVeri[0][kisiInd][imzaInd]]
				cikti += [kisiInd]  ### imza hangi kişiye ait

		return np.stack(A_verisi, 0), np.stack(B_verisi, 0), np.stack(Anchor, 0), np.stack(cikti, 0)


#n///////////////NORMAL VERİLER İÇİN RASTGELE VERİ ÜRETELİM


	def get_random_batches(self,tumVeriX,tumVeriY,verisayisi,ayri=False):
		uretilenX, uretilenY = [],[]
		print("ACEBA YENI EPOCH GECTIMI")
		while 1:
			tumVeriIndeksleri = list(range(tumVeriX.shape[0]))  ### Gelen veri grubunda bulunan indexleri alalım
			np.random.shuffle(tumVeriIndeksleri)### tüm indisleri karıştırdık
			#print("Veri Şekli = "+str(tumVeriX.shape))
			#print(tumVeriIndeksleri)
			for i in range(verisayisi):  ####veriSayisi kadar veriyi gönderelim
				Ind = tumVeriIndeksleri[i]  ## tüm veriler içerisinden rastgele birini seçelim
				#print("IND =>>>>>>>>>>>>>>><  " + str(Ind))
				uretilenX+=[tumVeriX[Ind]]
				uretilenY += [tumVeriY[Ind]]

			self.batch_zaman_fark = time.time() - self.batc_oncekizaman
			self.batc_oncekizaman = time.time()
			print("ZAMAN FARKI = ",self.batch_zaman_fark," ---> ",uretilenX.__len__())
			if(ayri==True):
				return  (np.stack(uretilenX, 0), np.stack(uretilenY, 0))
			else:
				yield (np.stack(uretilenX, 0), np.stack(uretilenY, 0))
			uretilenX, uretilenY = [], []


# n///////////////TENSORFLOWDA NORMAL VERİLER İÇİN RASTGELE VERİ ÜRETELİM
## TENSORFLOWDA Veriler Veri ve Etiket olarak ayrı ayrı ve veriler tek boyutlu dizi halinde gidiyor
	def get_random_batchesTensorFlow(self, tumVeriX, tumVeriY, verisayisi):
		uretilenX, uretilenY = [], []
		while 1:
			tumVeriIndeksleri = list(range(tumVeriX.shape[0]))  ### Gelen veri grubunda bulunan indexleri alalım
			np.random.shuffle(tumVeriIndeksleri)  ### tüm indisleri karıştırdık
			# print("Veri Şekli = "+str(tumVeriX.shape))
			# print(tumVeriIndeksleri)
			for i in range(verisayisi):  ####veriSayisi kadar veriyi gönderelim
				Ind = tumVeriIndeksleri[i]  ## tüm veriler içerisinden rastgele birini seçelim
				# print("IND =>>>>>>>>>>>>>>><  " + str(Ind))


				#### Resmi tensorflow için tek boyutlu diziye çevirelim
				yeniVeri=tumVeriX[Ind].reshape(1,-1)
				uretilenX += [yeniVeri]
				uretilenY += [tumVeriY[Ind]]

			return (np.stack(uretilenX, 0), np.stack(uretilenY, 0))
			uretilenX, uretilenY = [], []

# n///////////////GAN VERİLER İÇİN RASTGELE VERİ ÜRETELİM
		## burada aynı tür resme ait orjinal boyut ve küçültülmüş örnekler dönecek
	def get_random_batchesGAN(tumVeriX, verisayisi,kucultme_orani):
		orjinal, kucuk = [], []
		h, w = tumVeriX[0].shape[0],tumVeriX[0].shape[1]
		kucuk_boy, kucuk_en = int(h / kucultme_orani), int(w / kucultme_orani)
		tumVeriIndeksleri = list(range(len(tumVeriX)))  ### Gelen veri grubunda bulunan indexleri alalım
		np.random.shuffle(tumVeriIndeksleri)  ### tüm indisleri karıştırdık

##### Veri Çoğaltmak için başka bir yol deniyorum aynı özelliklerde başka resim gönderelim
		tumVeriIndeksleri_EK = list(range(len(tumVeriX)))  ### Gelen veri grubunda bulunan indexleri alalım
		np.random.shuffle(tumVeriIndeksleri_EK)  ### tüm indisleri karıştırdık


		for i in range(verisayisi):  ####veriSayisi kadar veriyi gönderelim
			Ind1 = tumVeriIndeksleri[i]  ## tüm veriler içerisinden rastgele birini seçelim
			#a=array_to_img(tumVeriX[Ind]).convert('RGB')
			a=array_to_img(tumVeriX[Ind1])
			orjinal += [img_to_array(a)]##resimGREY di üç kanal lazım o nedenle önce RGB donusturddum sonra tekrar arraye
			#kucuk += [np.reshape(scipy.misc.imresize(a, (kucuk_en, kucuk_boy)),(kucuk_en, kucuk_boy,3))]

			Ind = tumVeriIndeksleri_EK[i]
			while True:#aynı veri olmasın diye
				if (Ind1 !=Ind):
					break
				np.random.shuffle(tumVeriIndeksleri_EK)  ### tüm indisleri karıştırdık
				Ind = tumVeriIndeksleri_EK[0]  ## tüm veriler içerisinden rastgele birini seçelim


			#a=array_to_img(tumVeriX[Ind]).convert('RGB')
			a=array_to_img(tumVeriX[Ind])
			kucuk += [img_to_array(a)]##resimGREY di üç kanal lazım o nedenle önce RGB donusturddum sonra tekrar arraye

		orjinal = np.array(orjinal) / 127.5 - 1.
		kucuk = np.array(kucuk) / 127.5 - 1.

		return np.stack(orjinal, 0), np.stack(kucuk, 0)


###########################################################################


	#dizi verisi halinde gelen Gri resimleri Renkli ye çevirme Sadece 1 kanaldan 3 kanal yapacağız
	def Gray2RGB(self,resimler):
		yeniRGB = []
		for i in range(resimler.__len__()):  ####veriSayisi kadar veriyi gönderelim
			a = array_to_img(resimler[i]).convert('RGB')
			yeniRGB += [img_to_array(a)]  ##resimGREY di üç kanal lazım o nedenle önce RGB donusturddum sonra tekrar arraye

		return  yeniRGB

################3	DOĞRULAMA YÇNTEMLERİ ############################################
	# False_reject_rate(FRR) = FN / (TP + FN) = FN / P = 1 - TPR
	# False_accept_rate(FAR) = C / (C + D) = FP / (FP + TN) = FPR
	# True_positive_rate(TPR) = A / (A + B) = TP / (TP + FN) = TP / P
	# False_positive_rate(FPR) = fallout = C / (C + D) = FP / (FP + TN) = FAR = 1 - SPC
# False Positive, False Negative, True Positive, True Negative, Dogru, Yanlış
	#testVerisi shape = 120, 300,300, 1 gibi
	# eğer CallBack True ise model.fit içerisinden callback ile çağırılıyordur bunedenle return değeri true olacak değilse object olacak
	def dogtulamaYontemleri(self,model,XtestVerisi,YtestVerisi,CallBack=False,DenseMi=False):
		self.model=model
		self.XtestVerisi=XtestVerisi
		self.YtestVerisi=YtestVerisi

		self.FP = 0.
		self.FN = 0.
		self.TP = 0.
		self.TN = 0.
		self.DG = 0
		self.YN = 0
		self.F1=0
		self.Precision=0
		self.Recall=0
		self.AER=0
		self.FRR =0
		self.FAR =0
		self.TPR =0
		self.FPR =0
		self.TNR =0

		if (DenseMi == False):
			self.p = self.model.predict(self.XtestVerisi, verbose=1)[0]
		else:
			self.p = self.model.predict(self.XtestVerisi, verbose=1)

		for i in range(self.YtestVerisi.shape[0]):
			if (self.YtestVerisi[i][0] == 1):  # eğer imza GERÇEKSE
				if (self.p[i][0] > self.p[i][1]):  # Eğer İmzaya Gerçek Demişsek
					self.TP += 1
					self.DG += 1
				elif (self.p[i][0] < self.p[i][1]):  # Eğer İmzaya Sahte Demişsek
					self.FN += 1
					self.YN += 1
			elif (self.YtestVerisi[i][0] == 0):  # eğer imza SAHTEYSE
				if (self.p[i][0] > self.p[i][1]):  # Eğer İmzaya Gerçek Demişsek
					self.FP += 1
					self.YN += 1
				elif (self.p[i][0] < self.p[i][1]):  # Eğer İmzaya Sahte Demişsek
					self.TN += 1
					self.DG += 1

	# False_reject_rate(FRR) = FN / (TP + FN) = FN / P = 1 - TPR
		if(self.FN.__float__()>0):
			self.FRR = self.FN.__float__() / (self.TP.__float__() + self.FN.__float__())

	# False_accept_rate(FAR) = C / (C + D) = FP / (FP + TN) = FPR
		if (self.FP.__float__() > 0):
			self.FAR = self.FP.__float__() / (self.FP.__float__() + self.TN.__float__())

	# True_positive_rate(TPR) = A / (A + B) = TP / (TP + FN) = TP / P
		if (self.TP.__float__() > 0):
			self.TPR = self.TP.__float__() / (self.TP.__float__() + self.FN.__float__())

	# False_positive_rate(FPR) = fallout = C / (C + D) = FP / (FP + TN) = FAR = 1 - SPC
		if (self.FP.__float__() > 0):
			self.FPR = self.FP.__float__() / (self.FP.__float__() + self.TN.__float__())

	# True Negative Rate (TNR) = Specifity =  TN / (FP + TN) = FAR = 1 - SPC
		if (self.TN.__float__() > 0):
			self.TNR = self.TN.__float__() / (self.FP.__float__() + self.TN.__float__())

	# F1 SCORU
		if (self.TP.__float__() > 0):
			self.F1 =2*self.TP.__float__()  / (2*self.TP.__float__()  + self.FP.__float__()  +self.FN.__float__())

	#recall rcl= TP/(TP+FN)
		if (self.TP.__float__() > 0):
			self.Recall=self.TP.__float__()  / (self.TP.__float__()  +self.FN.__float__())


	#precision Precision=TP/(TP+FP)
		if (self.TP.__float__() > 0):
			self.Precision=self.TP.__float__() / (self.TP.__float__() + self.FP.__float__())

	#Average Error Rate AER = (FAR + FRR) / 2
		self.AER = (self.FAR.__float__()  +self.FRR.__float__())/2

		print("Precision "+str(self.Precision)+" \nRecall "+str(self.Recall)+" \nF1 "+str(self.F1) )
		print("FRR " + str(self.FRR) + " \nFAR " + str(self.FAR) + " \nFPR " + str(self.FPR))
		print( "FP = "+str(self.FP.__float__())+" TP = " +str(self.TP.__float__())+"\nFN = "+str(self.FN.__float__())+" TN = " +str(self.TN.__float__()))

		#print("TP "+str(self.TP)+" \nTN "+str(self.TN)+" \nFP "+str(self.FP)+" \nFN "+str(self.FN) )

		f = DogrulamaElemanlari(self.DG,self.YN, self.FAR,self.FRR,self.TPR,self.FPR,self.F1,self.Recall,self.Precision,self.TNR ,self.AER )
		if(CallBack==True):
			return
		else:
			return f


###########################################################################


	### Gelen resmin Gerçek mi Sahtemi olduğunu gönderiyor, Test Edebilmek için Gerçek imza verilerinin olduğu resim dizisi GVeri yi göndermemiz gerekiyor
	def resimTuru(self,resim, GVeriler):
		indeks = -1
		bo = False
		for i in GVeriler[0]:
			n = i / 255.
			indeks+=1
			bo = np.allclose(resim, n)
			if (bo == True):
				print(indeks, " Verisi Gerçek")
				break

		if (bo == False):
			print(indeks, " Verisi Sahte")
		return [indeks,bo]


	def tahmin(x,model):
		x = np.expand_dims(x, axis=0)   #Verinin şeklini 210,300,1 den 1, 210,300,1 a çevirmek için
		return model.predict(x)



	### EĞİTİĞİMİZ MODELİ DAHA SONRA KULLANMAK İÇİN DOSYAYA KAYDEDELİM ###
	def EgitimVerileriniKaydet(yol,model):
		model.save(yol)
		print("Modele Ait Eğitim Verileri "+yol+" Dosyasına Kaydedildi")





	##########		VERİLERİ MATPLOTLIB KUTUPHANESİ İLE GÖRSELLEŞTİRME	#############
	"""Modeli, Test verilerini, ekrana bastırılacak resim sayısını en boy oranlarını gönderdiğimizde 2 sınıfa göre gerçek mi sahtemi olduğunu ve doğru mu yanlışmı tahmin ettiğimizi buluyor"""
import math as math
def GorselTahmin(modelim,X_testler,Y_testler,TSay = 2,en=30,boy=30,DenseMi=False):
	global axi
	label = ['Gerçek', 'Sahte']
	####PREDICTIONDA İKİ FARKLI SONUÇ VAR MODLİN DENSENET OLMASINA GÖRE
	if (DenseMi == False):
		p = modelim.predict(X_testler, verbose=1)[0]
	else:
		p = modelim.predict(X_testler, verbose=1)


	satir, sutun=1,2
	if(TSay>1):
		sutun=(int)(math.ceil(math.sqrt(TSay)))
		satir =(int)(math.sqrt(TSay))

	fgr, ax = plt.subplots(satir,sutun, figsize=(en, boy))



	left = 0
	bottom = 0

	#Gelen Verielrden Rastgele Alalım
	m = np.arange(X_testler.shape[0])
	np.random.shuffle(m)

	for i, axi in enumerate(ax.flat):
		if(i<TSay):
			img=X_testler[m[i]].astype(np.float32) #veriyi plot ile yazmak için tipini float32 yapmalı
			img=img[:,:,0] #veriyi plot ile yazmak için boyutu [224 224 1] den [224 244] yapmalı
			axi.imshow(np.squeeze(img), cmap='binary')
			# ek=unicode(str(label[(int)(Y_testler[m[i]][1])]), 'utf-8')##python 2.x
			#ek = str(label[(int)(Y_testler[m[i]][1])]).encode('utf-8')  ##python 3.x
			ek=str(label[(int)(Y_testler[m[i]][1])])
			print('---------------------------------------- '+ek)
			axi.set_title(ek+' -> '+ str(m[i]),fontsize=12,color="blue", fontweight='bold')
			metin=""
			for n in range(2):
				metin+=(' |'+ (u'\u2589' * int(p[m[i], n] * 10)) + ' ' + label[n] + ' {:.5f}%'.format(p[m[i], n] * 100)+'\n'  )

			print('---------------------------------------- ' + metin)


			renk = "red"
			if(((p[m[i], 0] > p[m[i], 1]) and ((Y_testler[m[i]][0])==1)) or ((p[m[i], 0] < p[m[i], 1]) and ((Y_testler[m[i]][0])==0))):
				renk="green"##Eğer bilirsek bar rengi yeşiş bilemezsek kırmızı olsun


			axi.text(left, bottom,metin,fontsize=9,color=renk,
					horizontalalignment='left',
					verticalalignment='bottom',
					transform=axi.transAxes)
			#axi.set_xlabel(metin)
			#axi.set_ylabel('vvvvvvvv')
			axi.set(xticks=[], yticks=[])
	plt.show()
