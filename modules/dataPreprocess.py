# coding=utf-8
# !/usr/bin/python
# -*- coding: <utf-8> -*-
"""
###    Muhammed Mutlu YAPICI    ###
###    Doktora Tezinde Kullanılmak Üzer ###
###    05-Ağustos-2017 Tarihinde Geliştirilmiştir. ###


#################    FONKSİYON LİSTESİ    ##########################
#   BinaryResimYukle(kokDizin,dosyaAdi,dizinDerinligi=0,ekranaYaz=False)
	  ---->  Dizinde Bulunan Resimleri Binary Formatında Yükler

#   PILResimYukle(kokDizin,dosyaAdi,dizinDerinligi=0,ekranaYaz=False)
	  ---->  Dizinde Bulunan Resimleri PIL resim Formatında Yükler

#   ResmiYenidenBoyutlandir(resim, yeniEn, yeniBoy)
	  ----> Gelen Numpy Array Dizisindeki Verileri yeniden boyutlandırır Sadece genişlik ve Yüksekliği

#   PILresmiYenidenBoyutlandir(resim, yeniEn, yeniBoy,diziMi=False,orjinallikKorunsunMu=False, arkaRenk=255)
	 ----> PIL Resmi yeniden boyutlandırır PIL resim dizisindeki tüm verileri yeniden boyutlandırır Sadece genişlik ve Yüksekliği

#   ResimSinirlariniBelirle(resim,tolerans=0,arkaReng=255,diziMi=False)
	  ---->  Resimlerin Sınırlarını Bulmak için kullanılır arkaplan rengine göre farklı renkleri seçer

#   YeniResimSinirlariniBelirle(resim,tolerans=0,arkaReng=255,diziMi=False)
	  ---->  Resimlerin Sınırlarını Bulmak için kullanılır arkaplan rengine göre farklı renkleri seçer, üstteki daha yavaş bu hızlı

#   CokluImg2Array(resim,diziMi=false)
	  ---->  PIL Resim Formatında Gelen Resimlerin Tamamını numpy array cinsine çevirir. Normalde  Kerasta img_to_array fonksiyonu var ama bu tektek yapıyor.

#    CokluCrop(resim,sinirlar,diziMi=False)
	 ----> Sınırları Belli Olan Resim Listesinin Tamamını Sınır Değerlerine Göre CROP yapar Aslında PIL Imageda Crop Var ama resimleri tek tek Cropluyor.

#    ImzaVeritabaniniYukle(kokDizin,dosyaAdi,yeniEn, yeniBoy,yuklenecekResimSayisi=0,dizinDerinligi=0,tolerans=0,arkaRenk=255,orjinallikKorunsunMu=False, arkaRenk2=255,ekranaYaz=False)
	----> İmza Veritabanını Yüklemek için Kullanacağım. Bu Fonksiyon ile Yukarıdaki Bir kaç fonksiyonu aynı anda çalıştırmış olacağım

#    VeritabaniniDosyayaKaydet(dosyaAdi,veri,ekranaYaz=False)
	----> İmza Veritabanını Metin Dosyasına Kaydetmek için Kullanacağım. Herzaman Resmi Yüklemek Ve Ön İşlem Yapmak Çok Zaman Alıyor Metin Dosyasına Kaydettiğim Verileri Tekrar Yüklemek Daha Hızlı.

#    VeritabaniniDosyadanYukle(dosyaAdi)
	----> İmza Veritabanını Metin Dosyasından yüklemek için Kullanacağım. Herzaman Resmi Yüklemek Ve Ön İşlem Yapmak Çok Zaman Alıyor. Metin Dosyasına Kaydettiğim Verileri Tekrar Yüklemek Daha Hızlı. İlk Satırlara Tekrar Yüklerken Kullanacağım Shape leri Yükleyeceğim Formatı #HMShape10HM#    şeklinde olacak
"""

###    Bu Fonksiyon Aşağıda Belirtilen Parametrelere Göre Dizinde Bulunan
###    Resimleri Binary Formatında Yüklemek İçin Kullanılacaktır.
"""
 kokDizin  --> okunacak resimlerin bulunduğu ana dizinlerdir. /desktop/Resimler/ gibi
 dosyaAdi  --> okunacak resmin adı, burada *, c*, ari*  gibi kullanılabilir
 dizinDerinligi  -->  Eğer klasör varsa kökDizinden sonra kaç klasör alta doğru bakılacağı
"""


def BinaryResimYukle(kokDizin, dosyaAdi, dizinDerinligi=0, ekranaYaz=False):
    import glob, os
    from keras.preprocessing.image import load_img
    import numpy as np  # dizinin shape ve size olsun diye numpy array kullandım

    for i in range(0, dizinDerinligi):
        kokDizin += "/*"

    sayac = 0
    img = []
    print("Aranacak Dizin ve Dosya Tam Yolu = ", kokDizin + "/" + dosyaAdi)

    for resim in glob.glob(kokDizin + "/" + dosyaAdi):
        dosya, uzanti = os.path.splitext(resim)
        sayac += 1
        if (ekranaYaz == True):
            print(sayac, '. Dosya Adi = ' + dosya)
        b = np.array(load_img(resim), dtype=object)
        img.append(b);
    # if sayac==1:
    # img=np.append(img,np.array(load_img(resim), dtype=object))
    # else:
    #	img=np.vstack((img,np.array(load_img(resim), dtype=object)))



    return img


###    Bu Fonksiyon Aşağıda Belirtilen Parametrelere Göre Dizinde Bulunan
###    Resimleri PIL resim Formatında Yüklemek İçin Kullanılacaktır.
"""
 kokDizin  --> okunacak resimlerin bulunduğu ana dizinlerdir. /desktop/Resimler/ gibi
 dosyaAdi  --> okunacak resmin adı, burada *, c*, ari*  gibi kullanılabilir
 dizinDerinligi  -->  Eğer klasör varsa kökDizinden sonra kaç klasör alta doğru bakılacağı
"""


def PILResimYukle(kokDizin, dosyaAdi, dizinDerinligi=0, ekranaYaz=False):
    import glob, os
    from PIL import Image
    import numpy as np  # dizinin shape ve size olsun diye numpy array kullandım

    for i in range(0, dizinDerinligi):
        kokDizin += "/*"

    sayac = 0
    img = []
    print("Aranacak Dizin ve Dosya Tam Yolu = ", kokDizin + "/" + dosyaAdi)

    for resim in glob.glob(kokDizin + "/" + dosyaAdi):
        dosya, uzanti = os.path.splitext(resim)
        sayac += 1
        if (ekranaYaz == True):
            print(sayac, '. Dosya Adi = ' + dosya)
        b = Image.open(resim)
        img.append(b);

    return img


###   Bu Fonksiyon Aşağıda Belirtilen Parametrelere Göre  Gelen Numpy Array
###   Dizisindeki verileri yeniden boyutlandırır Sadece genişlik ve Yüksekliği
"""
 resim --> boyutlandırılacak resim dizisi
 yeniEn --> resmin yeni genişliği
 yeniBoy --> resmin yeni yüksekliği
"""


def ResmiYenidenBoyutlandir(resim, yeniEn, yeniBoy):
    import scipy.misc
    img = scipy.misc.imresize(resim, (yeniBoy, yeniEn))
    return img


###   Bu Fonksiyon Aşağıda Belirtilen Parametrelere Göre  Gelen PIL Resmi yeniden boyutlandırır
###   PIL resim dizisindeki tüm verileri yeniden boyutlandırır Sadece genişlik ve Yüksekliği
"""
 resim --> boyutlandırılacak resim dizisi
 yeniEn --> resmin yeni genişliği
 yeniBoy --> resmin yeni yüksekliği
 diziMi  --> Gelen Resim Verisi Dizimi onu Belirliyoruz
 arkaReng  --> Arkplan rengini Belirlemede Kullanılır Varsayılan Beyaz
 orjinallikKorunsunMu  --> Resim yeniden boyutlandırılırken orjinallik korunsun mu. Eğer korunursa en uzun kenara göre boyutlanıp boşlıklar arkaplan rengi ile doldurulur
"""


def PILResmiYenidenBoyutlandir(resim, yeniEn, yeniBoy, diziMi=False, orjinallikKorunsunMu=False, arkaRenk=255):
    from PIL import Image
    if (diziMi == False):
        if (
            orjinallikKorunsunMu == True):  ## Eğer orantı korunacak ise orjinale göre orantı yüzdesi küçük olana göre hesaplamalıyız.
            eo = (float(yeniEn) / float(resim.size[0]))
            bo = (float(yeniBoy) / float(resim.size[1]))
            if (eo > bo):
                yRes = Image.new("L", (yeniEn, yeniBoy), arkaRenk)  ## arka renkle dolu en ve boya göre maske oluşsun
                rr = resim.resize((int(resim.size[0] * bo), int(resim.size[1] * bo)), Image.ANTIALIAS)
                yRes.paste(rr, (int((yRes.size[0] - rr.size[0]) / 2), int((yRes.size[1] - rr.size[1]) / 2)))
                return yRes
            else:
                yRes = Image.new("L", (yeniEn, yeniBoy), arkaRenk)  ## arka renkle dolu en ve boya göre maske oluşsun
                rr = resim.resize((int(resim.size[0] * eo), int(resim.size[1] * eo)), Image.ANTIALIAS)
                yRes.paste(rr, (int((yRes.size[0] - rr.size[0]) / 2), int((yRes.size[1] - rr.size[1]) / 2)))
                return yRes

        else:
            return resim.resize((yeniEn, yeniBoy), Image.ANTIALIAS)
    else:
        if (
            orjinallikKorunsunMu == True):  ## Eğer orantı korunacak ise orjinale göre orantı yüzdesi küçük olana göre hesaplamalıyız.
            img = []
            for i in range(len(resim)):  ## Tüm Resimler İçin
                eo = (float(yeniEn) / float(resim[i].size[0]))
                bo = (float(yeniBoy) / float(resim[i].size[1]))
                if (eo > bo):
                    yRes = Image.new("L", (yeniEn, yeniBoy),
                                     arkaRenk)  ## arka renkle dolu en ve boya göre maske oluşsun
                    rr = resim[i].resize((int(resim[i].size[0] * bo), int(resim[i].size[1] * bo)), Image.ANTIALIAS)
                    yRes.paste(rr, (int((yRes.size[0] - rr.size[0]) / 2), int((yRes.size[1] - rr.size[1]) / 2)))
                    img.append(yRes)
                else:
                    yRes = Image.new("L", (yeniEn, yeniBoy),
                                     arkaRenk)  ## arka renkle dolu en ve boya göre maske oluşsun
                    rr = resim[i].resize((int(resim[i].size[0] * eo), int(resim[i].size[1] * eo)), Image.ANTIALIAS)
                    yRes.paste(rr, (int((yRes.size[0] - rr.size[0]) / 2), int((yRes.size[1] - rr.size[1]) / 2)))
                    img.append(yRes)
            return img

        else:  ## orjinalliğin korunmasına gerek yoksa böyle
            img = []
            for i in range(len(resim)):
                cr = resim[i].resize((yeniEn, yeniBoy), Image.ANTIALIAS)
                img.append(cr)

            return img

    return False


###   Resimlerin Sınırlarını Bulmak için Kullanacağım Bu Fonksiyonu
"""
 resim  --> Array resim formatında gelen resim
 arkaReng  --> Arkplan rengini Belirlemede Kullanılır Varsayılan Beyaz
 diziMi  --> Gelen Resim Verisi Dizimi onu Belirliyoruz.
 tolerans  --> Arka Plana Göre Sinirlari Belirlenecek Renk Toleransını Belirler. Arkaplandan Nekadar Farklı Olacak
"""


def ResimSinirlariniBelirle(resim, tolerans=0, arkaReng=255, diziMi=False):
    if (diziMi == False):
        en = resim.shape[1]
        boy = resim.shape[0]
        enb = [0, 0]
        enk = [500, 500]
        for y in range(boy):
            for x in range(en):
                if (resim[y][x][0] < (arkaReng - tolerans) or resim[y][x][0] > (arkaReng + tolerans)):
                    #	print x, y, resim[y][x][0]
                    if (enb[0] < x):
                        enb[0] = x
                    if (enb[1] < y):
                        enb[1] = y
                    if (enk[0] > x):
                        enk[0] = x
                    if (enk[1] > y):
                        enk[1] = y

        return (enk, enb)
    else:

        enbDizi = []
        enkDizi = []

        for i in range(len(resim)):
            enb = [0, 0]
            enk = [500, 500]
            en = resim[i].shape[1]
            boy = resim[i].shape[0]
            # print i,". Resim En =",en," Boy = ",boy
            print(i + 1), ". Resim İşleniyor En = ", en, " Boy = ", boy
            for y in range(boy):
                for x in range(en):
                    # print "x ---->",x,"y ------> ",y
                    if (resim[i][y][x][0] < (arkaReng - tolerans) or resim[i][y][x][0] > (arkaReng + tolerans)):
                        if (enb[0] < x):
                            enb[0] = x
                        if (enb[1] < y):
                            enb[1] = y
                        if (enk[0] > x):
                            enk[0] = x
                        if (enk[1] > y):
                            enk[1] = y

            enkDizi.append(enk)
            enbDizi.append(enb)

        return (enkDizi, enbDizi)


###   Resimlerin Sınırlarını Bulmak için Kullanacağım Bu Fonksiyonu, Üstteki daha yavaş bu hızlı
"""
 resim  --> Array resim formatında gelen resim
 arkaReng  --> Arkplan rengini Belirlemede Kullanılır Varsayılan Beyaz
 diziMi  --> Gelen Resim Verisi Dizimi onu Belirliyoruz.
 tolerans  --> Arka Plana Göre Sinirlari Belirlenecek Renk Toleransını Belirler. Arkaplandan Nekadar Farklı Olacak
"""


def YeniResimSinirlariniBelirle(resim, tolerans=10, arkaReng=255, diziMi=False, renkliMi=False):
    import numpy as np

    if (diziMi == False):
        en = resim.shape[1]
        boy = resim.shape[0]

        enb = [0, 0]
        enk = [500, 500]

        ## önce ilk boyu bulalım
        for i in range(boy):
            if (renkliMi):
                if (np.amin(resim[i], axis=0).any() < (arkaReng - tolerans) or np.amin(resim[i], axis=0).any() > (
                            arkaReng + tolerans)):
                    enk[1] = i
                    break
            else:
                if (np.amin(resim[i], axis=0) < (arkaReng - tolerans) or np.amin(resim[i], axis=0) > (
                    arkaReng + tolerans)):
                    enk[1] = i
                    break

        ## ilk eni bulalım
        for i in range(en):
            if (renkliMi):
                if (np.amin(resim[:, i], axis=0).any() < (arkaReng - tolerans) or np.amin(resim[:, i], axis=0).any() > (
                            arkaReng + tolerans)):
                    enk[0] = i
                    break
            else:
                if (np.amin(resim[:, i], axis=0) < (arkaReng - tolerans) or np.amin(resim[:, i], axis=0) > (
                    arkaReng + tolerans)):
                    enk[0] = i
                    break

        ## Son boyu bulalım
        for i in range(boy):
            if (renkliMi):
                if (np.amin(resim[(boy - i - 1)], axis=0).any() < (arkaReng - tolerans) or np.amin(resim[(boy - i - 1)],
                                                                                                   axis=0).any() > (
                            arkaReng + tolerans)):
                    enb[1] = (boy - i - 1)
                    break
            else:
                if (np.amin(resim[(boy - i - 1)], axis=0) < (arkaReng - tolerans) or np.amin(resim[(boy - i - 1)],
                                                                                             axis=0) > (
                    arkaReng + tolerans)):
                    enb[1] = (boy - i - 1)
                    break

        ## Son eni bulalım
        for i in range(en):
            if (renkliMi):
                if (np.amin(resim[:, (en - i - 1)], axis=0).any() < (arkaReng - tolerans) or np.amin(
                        resim[:, (en - i - 1)], axis=0).any() > (arkaReng + tolerans)):
                    enb[0] = (en - i - 1)
                    break
            else:
                if (np.amin(resim[:, (en - i - 1)], axis=0) < (arkaReng - tolerans) or np.amin(resim[:, (en - i - 1)],
                                                                                               axis=0) > (
                    arkaReng + tolerans)):
                    enb[0] = (en - i - 1)
                    break

        return (enk, enb)
    else:  ##dizi ise
        enbDizi = []
        enkDizi = []
        for j in range(len(resim)):
            enb = [0, 0]
            enk = [500, 500]
            en = resim[j].shape[1]
            boy = resim[j].shape[0]
            # print i,". Resim En =",en," Boy = ",boy
            print(j + 1), ". Resim İşleniyor En = ", en, " Boy = ", boy

            ## önce ilk boyu bulalım
            for i in range(boy):
                if (np.amin(resim[j][i], axis=0) < (arkaReng - tolerans) or np.amin(resim[j][i], axis=0) > (
                    arkaReng + tolerans)):
                    enk[1] = i
                    break

            ## ilk eni bulalım
            for i in range(en):
                if (np.amin(resim[j][:, i], axis=0) < (arkaReng - tolerans) or np.amin(resim[j][:, i], axis=0) > (
                    arkaReng + tolerans)):
                    enk[0] = i
                    break

            ## Son boyu bulalım
            for i in range(boy):
                if (np.amin(resim[j][(boy - i - 1)], axis=0) < (arkaReng - tolerans) or np.amin(resim[j][(boy - i - 1)],
                                                                                                axis=0) > (
                    arkaReng + tolerans)):
                    enb[1] = (boy - i - 1)
                    break

            ## Son eni bulalım
            for i in range(en):
                if (np.amin(resim[j][:, (en - i - 1)], axis=0) < (arkaReng - tolerans) or np.amin(
                        resim[j][:, (en - i - 1)], axis=0) > (arkaReng + tolerans)):
                    enb[0] = (en - i - 1)
                    break

            enkDizi.append(enk)
            enbDizi.append(enb)

        return (enkDizi, enbDizi)


###   Sınırları Belli Olan Resim Listesinin Tamamını Sınır Değerlerine Göre CROP yapar
###   Aslında PIL Imageda Crop Var ama resimleri tek tek Cropluyor.
"""
 resim  --> PIL resim formatında gelen resim
 eksinir  --> Crop için en küçük X ve Y sınır Değerlerin Yüklü Olduğu Dizi
 ebsinir  --> Crop için en büyük X ve Y sınır Değerlerin Yüklü Olduğu Dizi
 diziMi  --> Gelen Resim Verisi Dizimi onu Belirliyoruz.
"""


def CokluCrop(resim, eksinir, ebsinir, diziMi=False):
    if (diziMi == False):
        return resim.crop((eksinir[0], eksinir[1], ebsinir[0], ebsinir[1]))
    else:
        img = []
        for i in range(len(resim)):
            cr = resim[i].crop((eksinir[i][0], eksinir[i][1], ebsinir[i][0], ebsinir[i][1]))
            img.append(cr)

        return img

    return false


###    PIL Resim Formatında Gelen Resimlerin Tamamını numpy array cinsine çevirir.
###    Normalde  Kerasta img_to_array fonksiyonu var ama bu tektek yapıyor.
"""
 resim  --> PIL resim formatında gelen resim
 diziMi  --> Gelen Resim Verisi Dizimi onu Belirliyoruz.
"""


def CokluImg2Array(resim, diziMi=False):
    from keras.preprocessing.image import img_to_array
    from keras import backend as K
    kanal = K.image_data_format()
    if (diziMi == False):
        r = img_to_array(resim)
        print("Resim Şekli ===================> ", r.shape, "Kanal = ", kanal)

        """if(r.shape.__len__()==3):#eğer gelen dizi boyutunda renk kanalıda varsa onu atalım 1 255 244 gibi
            if(kanal=='channels_last'):
                r = r.reshape(r.shape[0], r.shape[1])
            else:
                r=r.reshape(r.shape[1],r.shape[2])"""

        return r
    else:
        img = []
        for i in range(len(resim)):
            r = img_to_array(resim[i])
            if (r.shape.__len__() == 3):  # eğer gelen dizi boyutunda renk kanalıda varsa onu atalım 1 255 244 gibi
                r = r.reshape(r.shape[1], r.shape[2])
            img.append(r)

        return img

    return false


###   İmza Veritabanını Yüklemek için Kullanacağım. Bu Fonksiyon ile Yukarıdaki Bir kaç fonksiyonu aynı anda çalıştırmış olacağım
###   Önce Resimleri PIL Image Formatında Yükleyeceğiz.
###   PIL Resimleri Diziye Dönüştürüp Sınırları Belirleyeceğiz
###   Sınırlara Göre Resimleri Crop ile Keseceğiz
###   Tüm Resimleri Aynı Boyuta Getirip Veritabanını Oluşturacağız
"""
 kokDizin  --> okunacak resimlerin bulunduğu ana dizinlerdir. /desktop/Resimler/ gibi
 dosyaAdi  --> okunacak resmin adı, burada *, c*, ari*  gibi kullanılabilir
 yeniEn --> resmin yeni genişliği
 yeniBoy --> resmin yeni yüksekliği
 dizinDerinligi  -->  Eğer klasör varsa kökDizinden sonra kaç klasör alta doğru bakılacağı
 tolerans  --> Arka Plana Göre Sinirlari Belirlenecek Renk Toleransını Belirler. Arkaplandan Nekadar Farklı Olacak
 arkaReng  --> Arkplan rengini Belirlemede Kullanılır Varsayılan Beyaz
 yuklenecekResimSayisi  --> Bir Dizindeki Yüklenecek Toplam Resim Sayısı, Eğer Değeri 0 ise Tamamı Yüklenir
 orjinallikKorunsunMu --> 5. adımdaki resmi yeniden boyutlandır aşamasında orjinallği bozmadan boyutlandırmak için
 arkaRenk2 --> 5. adımdaki resmi yeni boyutlandırırken fazlalık olan arkaya gelecek renkler.
"""


def ImzaVeritabaniniYukle(kokDizin, dosyaAdi, yeniEn, yeniBoy, yuklenecekResimSayisi=0, dizinDerinligi=0, tolerans=0,
                          arkaRenk=255, orjinallikKorunsunMu=False, arkaRenk2=255, ekranaYaz=False, RenkliMi=False):
    import glob, os
    from PIL import Image
    import numpy as np
    from keras.preprocessing.image import array_to_img
    from modules.hafenormalize import preprocess_signature
    from scipy.misc import imread
    canvas_size = (yeniBoy + 5, yeniEn + 5)  # Maximum signature size

    for i in range(0, dizinDerinligi):
        kokDizin += "/*"

    sayac = 0
    img = []

    Y_mod = []
    print("Aranacak Dizin ve Dosya Tam Yolu = ", kokDizin + "/" + dosyaAdi)

    ### 1	Önce PIL Resim Yukleme İşlemleri
    for resim in glob.glob(kokDizin + "/" + dosyaAdi):
        dosya, uzanti = os.path.splitext(resim)
        sayac += 1
        if (ekranaYaz == True):
            print(sayac, '. Dosya Adi = ' + dosya)
        print("1 ------------------>")

        if (RenkliMi):
            b = Image.open(resim).convert('RGB')
        elif (Image.open(resim).mode != 'L'):
            b = Image.open(resim).convert('L')
        else:
            b = Image.open(resim)

        ### 2	PIL Resmi Sınırları Belirleyebilmek için Diziye Dönüştürelim
        print("2 ------------------>")
        rdizi = CokluImg2Array(b)
        ### 3 	Dizideki Resmin Sınırlarını Belirleyelim

        print("3 ------------------>")
        ##BU YAVAŞTI (ek,eb)=ResimSinirlariniBelirle(rdizi,tolerans,arkaRenk,False)
        (ek, eb) = YeniResimSinirlariniBelirle(rdizi, tolerans, arkaRenk, False, True)
        ### 4	PIL resmi Sınırlara Göre Resimi Crop Yapalım. Dönen Resim Yine PIL Formatında
        print("4 ------------------>")
        crores = CokluCrop(b, ek, eb, False)
        ### 5  	PIL Resimi Yeniden  Boyutlandıralım
        print("5 ------------------>")
        yeniRes = PILResmiYenidenBoyutlandir(crores, yeniEn, yeniBoy, False, orjinallikKorunsunMu, arkaRenk2)

        ###5.5 PIL Resmi normnalizasyon fonksiyonundan geçirelim burada pıl resmini CSV ye çevirmek gerekiyor
        if (RenkliMi == False):
            print("5.5 ------------------>")
            im_np = np.asarray(yeniRes)
            yeniRes = preprocess_signature(im_np, canvas_size, (yeniBoy, yeniEn), (yeniBoy, yeniEn))

        ### 6  	PIL Resmin Son Halini Diziye Dönüştürelim
        print("6 ------------------>")
        rdizi = CokluImg2Array(yeniRes)
        ### 7	Son Resim Dizisini Listeye Ekleyelim ve resim doğrulmada kullanılacak Y_mod verisini oluşturalım. Resim için [1,0] Gerçek  [0,1] sahte demek
        print("7 ------------------>")
        img.append(rdizi);
        bn = os.path.basename(dosya)
        if ((bn.find('cf-') > -1) or (bn.find('f') > -1) or (bn.find('F') > -1)):
            Y_mod.append([0, 1])
        elif ((bn.find('c-') > -1) or (bn.find('v') > -1) or (bn.find('V') > -1)):
            Y_mod.append([1, 0])

        ### 8	Açık PIL Resmini Kapatalım
        b.close()

        if (sayac >= yuklenecekResimSayisi):
            break;

    #### BELLEĞİ TEMİZLEYELİM
    # del canvas_size, rdizi, ek, eb,crores,yeniRes,im_np


    return (img, Y_mod)


"""Yukarııdaki fonksi,yonun aynısıydı bunu sadece res,ö adedini saymak için kullanacağız."""


def ImzaVerileriniSay(kokDizin, dosyaAdi, dizinDerinligi=0, ekranaYaz=False):
    import glob, os

    for i in range(0, dizinDerinligi):
        kokDizin += "/*"

    sayac = 0

    print("Aranacak Dizin ve Dosya Tam Yolu = ", kokDizin + "/" + dosyaAdi)

    ### 1	Önce PIL Resim Yukleme İşlemleri
    for resim in glob.glob(kokDizin + "/" + dosyaAdi):
        dosya, uzanti = os.path.splitext(resim)
        sayac += 1
        if (ekranaYaz == True):
            print(sayac, '. Dosya Adi = ' + dosya)


###############3                SİAMAES İÇİN VERİ OKUMA MODELİ             #######################################
############  SİAMES TA HER KULLANICIYA AİT VERİLER SAHTE VE GERÇEK OLARAK İKİ GRUBA AYRILMALI VE KİŞİ BAZINDA AYRILMALI
############ YANİ 1. KULLANICIYA AİT SAHTE ORNEKLER GERÇEKLERİ İLE AYRILIP TEST VE EĞİTİM OLUŞTURULMALI SIRASI DA AYNI OLMALI
############ HER BİR KİŞİYE AİT HEM SAHTE HEM GERÇEK ÇIKIŞ OLACAĞINDAN ÇIKIŞ 3 BOYUTLU OLDU [15,1,0]

###   İmza Veritabanını Yüklemek için Kullanacağım. Bu Fonksiyon ile Yukarıdaki Bir kaç fonksiyonu aynı anda çalıştırmış olacağım
###   Önce Resimleri PIL Image Formatında Yükleyeceğiz.
###   PIL Resimleri Diziye Dönüştürüp Sınırları Belirleyeceğiz
###   Sınırlara Göre Resimleri Crop ile Keseceğiz
###   Tüm Resimleri Aynı Boyuta Getirip Veritabanını Oluşturacağız
"""
 kokDizin  --> okunacak resimlerin bulunduğu ana dizinlerdir. /desktop/Resimler/ gibi
 dosyaAdi  --> okunacak resmin adı, burada *, c*, ari*  gibi kullanılabilir
 yeniEn --> resmin yeni genişliği
 yeniBoy --> resmin yeni yüksekliği
 dizinDerinligi  -->  Eğer klasör varsa kökDizinden sonra kaç klasör alta doğru bakılacağı
 tolerans  --> Arka Plana Göre Sinirlari Belirlenecek Renk Toleransını Belirler. Arkaplandan Nekadar Farklı Olacak
 arkaReng  --> Arkplan rengini Belirlemede Kullanılır Varsayılan Beyaz
 yuklenecekResimSayisi  --> Bir Dizindeki Yüklenecek Toplam Resim Sayısı, Eğer Değeri 0 ise Tamamı Yüklenir
 orjinallikKorunsunMu --> 5. adımdaki resmi yeniden boyutlandır aşamasında orjinallği bozmadan boyutlandırmak için
 arkaRenk2 --> 5. adımdaki resmi yeni boyutlandırırken fazlalık olan arkaya gelecek renkler.
"""


def ImzaVeritabaniniYukleSIAMES(kokDizin, dosyaAdi, yeniEn, yeniBoy, yuklenecekResimSayisi=0, dizinDerinligi=0,
                                tolerans=0, arkaRenk=255, orjinallikKorunsunMu=False, arkaRenk2=255, ekranaYaz=False):
    import glob, os
    from PIL import Image
    import numpy as np
    from keras.preprocessing.image import array_to_img
    from hafeman.preprocess.normalize import preprocess_signature
    from scipy.misc import imread
    canvas_size = (yeniBoy + 5, yeniEn + 5)  # Maximum signature size

    for i in range(0, dizinDerinligi):
        kokDizin += "/*"

    sayac = 0
    img = []  ######[[[],[]]]  Her adamın gerçek ve sahte indisleri var ilk indis adamı gösterecek, içindeki 0 gerçek 1 sahteleri gösterecek böylece herkesin kendi gerçek ve sahtesinbi ayırmış olacağız
    Y_mod = []

    kisi = 'aaa'
    kisi_indisi = -1
    print("Aranacak Dizin ve Dosya Tam Yolu = ", kokDizin + "/" + dosyaAdi)

    ### 1	Önce PIL Resim Yukleme İşlemleri
    for resim in glob.glob(kokDizin + "/" + dosyaAdi):
        dosya, uzanti = os.path.splitext(resim)
        sayac += 1
        if (ekranaYaz == True):
            print(sayac, '. Dosya Adi = ' + dosya)

        if (dosya[(dosya.find('/') + 1):dosya.rfind('/')] != kisi):
            kisi_indisi += 1
            kisi = dosya[(dosya.find('/') + 1):dosya.rfind('/')]
            print("==============  " + kisi + "  YENİ BİR KİŞİ    ================")
            img.append([])  ###yeni bie kişi ekledik
            img[kisi_indisi].append([])  ###bu kişiye Gerçek veri Dzizi Ekledik
            img[kisi_indisi].append([])  ###bu kişiye Gerçek veri Dzizi Ekledik

            """d = "Bilmem"
            if (dosya.find("cf") == -1):
                d = "Gerçek"
            else:
                d = "Sahte"
            print(sayac, '. Dosya Adi = ' + dosya + " --> " + d)"""

        print("1 ------------------>")
        b = Image.open(resim)

        ### 2	PIL Resmi Sınırları Belirleyebilmek için Diziye Dönüştürelim
        print("2 ------------------>")
        rdizi = CokluImg2Array(b)
        ### 3 	Dizideki Resmin Sınırlarını Belirleyelim
        print("3 ------------------>")
        ##BU YAVAŞTI (ek,eb)=ResimSinirlariniBelirle(rdizi,tolerans,arkaRenk,False)
        (ek, eb) = YeniResimSinirlariniBelirle(rdizi, tolerans, arkaRenk, False)
        ### 4	PIL resmi Sınırlara Göre Resimi Crop Yapalım. Dönen Resim Yine PIL Formatında
        print("4 ------------------>")
        crores = CokluCrop(b, ek, eb, False)
        ### 5  	PIL Resimi Yeniden  Boyutlandıralım
        print("5 ------------------>")
        yeniRes = PILResmiYenidenBoyutlandir(crores, yeniEn, yeniBoy, False, orjinallikKorunsunMu, arkaRenk2)

        ###5.5 PIL Resmi normnalizasyon fonksiyonundan geçirelim burada pıl resmini CSV ye çevirmek gerekiyor
        print("5.5 ------------------>")
        im_np = np.asarray(yeniRes)
        yeniRes = preprocess_signature(im_np, canvas_size, (yeniBoy, yeniEn), (yeniBoy, yeniEn))

        ### 6  	PIL Resmin Son Halini Diziye Dönüştürelim
        print("6 ------------------>")
        rdizi = CokluImg2Array(yeniRes)
        ### 7	Son Resim Dizisini Listeye Ekleyelim ve resim doğrulmada kullanılacak Y_mod verisini oluşturalım. Resim için [1,0] Gerçek  [0,1] sahte demek
        print("7 ------------------>")

        ####### Resmi Sahteyse [1]  Gercekse [0] indisine yükleyelim



        if dosya.find('cf-') > -1:  ###sahteyse
            # Y_mod.append([0, 1])
            img[kisi_indisi][1].append(rdizi);
        elif dosya.find('c-') > -1:  ###gerçekse
            # Y_mod.append([1, 0])
            img[kisi_indisi][0].append(rdizi);

        ### 8	Açık PIL Resmini Kapatalım
        b.close()

        if (sayac >= yuklenecekResimSayisi):
            break;

    #### BELLEĞİ TEMİZLEYELİM
    # del canvas_size, rdizi, ek, eb,crores,yeniRes,im_np


    return (img)


"""BURAYI RESİMLERİN TÜRÜNÜ BELİRLEMEK İÇN YAPMIŞTIM
say=-1
for j in train_groups[1]:
	say += 1
	bo = False
	for i in GVeri[0]:
		n = i / 255.
		bo=np.allclose(j,n)
		if(bo==True):
			print(say," Verisi Gerçek")
			break

	if(bo==False):
		print(say , " Verisi Sahte")

"""

###   İmza Veritabanını HDF5 Dosyasına Kaydetmek için Kullanacağım. Herzaman Resmi Yüklemek Ve Ön İşlem Yapmak Çok Zaman Alıyor
###   Metin Dosyasına Kaydettiğim Verileri Tekrar Yüklemek Daha Hızlı.
"""
 dosyaAdi  --> Metin Dosyasının Adı
 veri --> resmin yüklü olduğu matris dizisi halindeki liste verisi
 ekranaYaz --> İşlem Yapılırken Ekrana Yazılıp Yazılmayacağı
 veriSekli  --> kaydedilecek HDF5 veri sekli (255,122,1) lik 10 resim için (10, 255,122,1) gibi
"""


def VeritabaniniDosyayaKaydetHDF5(dosyaAdi, veri, veriSekli):
    import h5py
    import numpy as np

    hdf5_file = h5py.File(dosyaAdi, mode='w')
    hdf5_file.create_dataset("train_img", veriSekli, np.float16)
    for i in range(veri.__len__()):
        hdf5_file["train_img"][i] = (veri[i])  ##verideki herresmi kaydedelim

    hdf5_file.close()
    print("Kayıt Başarılı")


###   İmza Veritabanını Metin Dosyasına Kaydetmek için Kullanacağım. Herzaman Resmi Yüklemek Ve Ön İşlem Yapmak Çok Zaman Alıyor
###   Metin Dosyasına Kaydettiğim Verileri Tekrar Yüklemek Daha Hızlı.
"""
 dosyaAdi  --> Metin Dosyasının Adı
 veri --> resmin yüklü olduğu matris dizisi halindeki liste verisi
 ekranaYaz --> İşlem Yapılırken Ekrana Yazılıp Yazılmayacağı
"""


def VeritabaniniDosyayaKaydet(dosyaAdi, veri, ekranaYaz=False):
    import numpy as np
    import scipy.io
    sifre = 'HM'
    """

#   Veri Şeklini alıp diziye yükleyelim
    sekil=str(veri[0].shape)
    sekildizi=sekil.split(',') ##burada (2,4,5)  => ["(2","4","5)"] şeklinde olacak parantezleri silelim
    sekildizi[0]=sekildizi[0][1:]
    sekildizi[len(sekildizi)-1]=sekildizi[len(sekildizi)-1][0:(len(sekildizi[len(sekildizi)-1])-1)]
    sekildizi=map(str.strip, sekildizi) #Varsa boşlukları temizleyelim

    baslik=""
    for vr in sekildizi:
        baslik+="#HMShape"+vr+"HM#\n"

    sayac=0
    with file(dosyaAdi, 'wb') as dsy:
        dsy.write('# coding=utf-8\n#!/usr/bin/python\n# -*- coding: <utf-8> -*-\n# BU Dosya İmza Veritabanını Text Dosyasına Kaydetmek İçin Mutlu YAPICI Tarafından Oluşturuldu Array shape: {0}\n'.format(veri[0].shape))
        dsy.writelines(baslik)
        for v in veri:
            sayac+=1
            if(ekranaYaz==True):
                print(sayac,'. Dosya Kaydediliyor ---->\n ')
            np.savetxt(dsy, v, fmt='%3.8f')
            dsy.write('# Yeni Resim Başlıyor\n')

    dsy.close()	"""

    # Daha iyi bir yöntem buldum şifreleyerek saklıyor şfre HM
    scipy.io.savemat(dosyaAdi, mdict={sifre: veri}, oned_as='row')
    return "Kayıt Başarılı"


###   İmza Veritabanını Metin Dosyasına Kaydetmek için Kullanacağım. Herzaman Resmi Yüklemek Ve Ön İşlem Yapmak Çok Zaman Alıyor
###   Metin Dosyasına Kaydettiğim Verileri Tekrar Yüklemek Daha Hızlı.
###   İlk Satırlara Tekrar Yüklerken Kullanacağım Shape leri Yükleyeceğim Formatı #HMShape 10HM#    şeklinde olacak
"""
 dosyaAdi  --> Metin Dosyasının Adı
"""


def VeritabaniniDosyadanYukle(dosyaAdi):
    """import numpy as np

###	Önce Dosyanın En Başında Olan ve #HMShape20HM# Şeklinde Şifrelediğim Şekil Verisini Alalım
    sekilDz=[]
    print("Dosyadan Yüklenen Dizi Verisinin Şekli")
###	Eğer Şekil Verisi Varsa İlk 20 Satırda Vardır ondan sonra tüm satırları boşuna okumasın
    sayac=0
    with open(dosyaAdi, "r") as ins:
        for line in ins:
            sayac+=1
            if(sayac>20):
                break #daha fazla bakmasına gerek yok
            if line.find('#HMShape')>-1 and line.find('HM#')>-1:
                print(line[8:(line.find('HM#'))])
                sekilDz.append(int(line[8:(line.find('HM#'))]))


    print(sekilDz)
    ins.close()


### 	Şimdi Dosyadan Verileri Yükleyelim
    veriler = np.loadtxt(dosyaAdi)


###	Verileri Şekillendirelim
    if(len(sekilDz)==2):
        veriler=veriler.reshape(sekilDz[0],sekilDz[1])
    elif(len(sekilDz)==3):
        veriler=veriler.reshape(sekilDz[0],sekilDz[1],sekilDz[2])
    elif(len(sekilDz)==4):
        veriler=veriler.reshape(sekilDz[0],sekilDz[1],sekilDz[2],sekilDz[3])
    elif(len(sekilDz)==5):
        veriler=veriler.reshape(sekilDz[0],sekilDz[1],sekilDz[2],sekilDz[3],sekilDz[4])
    elif(len(sekilDz)==6):
        veriler=veriler.reshape(sekilDz[0],sekilDz[1],sekilDz[2],sekilDz[3],sekilDz[4],sekilDz[5])
    elif(len(sekilDz)==7):
        veriler=veriler.reshape(sekilDz[0],sekilDz[1],sekilDz[2],sekilDz[3],sekilDz[4],sekilDz[5],sekilDz[6])
        """
    import scipy.io
    veriler = scipy.io.loadmat(dosyaAdi)
    return veriler


###   Bu fonksiyon ile gönderdiğim resim içerisindeki yatay ve dikey olarak her pikseldeki renk adedini buldurdum
###   iki adet piksel histogramı çıktı 0. indisteki resmin yatay piksellerindeki renk sayıları
###   1. indisteki ise resmin dikey piksellerindeki renk sayısını vermektedir
"""
 resim  --> Piksel renk sayısı hesaplanacak dizi şeklindeki resim
 arkaReng  --> Arkplan rengini Belirlemede Kullanılır Varsayılan Beyaz
"""


def pikselYogunlukHistogramiCikarimi(resim, arkaReng=255):
    import numpy as np
    en = resim.shape[1]
    boy = resim.shape[0]
    yogunlukHist = []
    hx = np.zeros((en))
    hy = np.zeros((boy))
    yogunlukHist.append(hx)
    yogunlukHist.append(hy)

    Zy = np.zeros((boy))

    for e in range(en):
        top = 0
        for b in range(boy):
            if (resim[b, e] != arkaReng):
                top += 1
                yogunlukHist[1][b] += 1
        yogunlukHist[0][e] = top

    return yogunlukHist


"""""""""""""""""""""""""""""""""
							MNIST VERİ SETİ YÜKLEME

"""""""""""""""""""""""""""""""""


def MNISTYukle():
    """Loads the Fashion-MNIST dataset.
    # Returns
        Tuple of Numpy arrays: `(x_train, y_train), (x_test, y_test)`.
    """

    import gzip
    import os
    import numpy as np
    from keras.utils.data_utils import get_file
    dirname = os.path.join('datasets', 'fashion-mnist')
    base = 'http://fashion-mnist.s3-website.eu-central-1.amazonaws.com/'
    files = ['train-labels-idx1-ubyte.gz', 'train-images-idx3-ubyte.gz',
             't10k-labels-idx1-ubyte.gz', 't10k-images-idx3-ubyte.gz']

    paths = []
    for fname in files:
        paths.append(get_file(fname,
                              origin=base + fname,
                              cache_subdir=dirname))

    with gzip.open(paths[0], 'rb') as lbpath:
        y_train = np.frombuffer(lbpath.read(), np.uint8, offset=8)

    with gzip.open(paths[1], 'rb') as imgpath:
        x_train = np.frombuffer(imgpath.read(), np.uint8,
                                offset=16).reshape(len(y_train), 28, 28)

    with gzip.open(paths[2], 'rb') as lbpath:
        y_test = np.frombuffer(lbpath.read(), np.uint8, offset=8)

    with gzip.open(paths[3], 'rb') as imgpath:
        x_test = np.frombuffer(imgpath.read(), np.uint8,
                               offset=16).reshape(len(y_test), 28, 28)

    return (x_train, y_train), (x_test, y_test)


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
	------------------------------>>>>>>>            ÖZ NITELİK ÇIKARIM YÖNTEMLERİ           <<<<<<<-----------------------------------------
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

### IZGARA ÖZNİTELİK ÇIKARMI
### Bu Fonksiyon Kendisine resim dizisi biçimde gelen resim/resimlerin üzerine belirtilen Xkare Ykare adedince ızgara eklemektedir
"""
 resim  --> array resim formatında gelen resim yada resim listesi
 XKare  --> Resimlerin enine eklenecek kare sayısı
 YKare  --> Resimlerin boyuna eklenecek kare sayısı
 diziMi  --> Gelen Resim Verisi Dizimi onu Belirliyoruz.
 cizgiRengi  --> Eklenecek çizgilerin rengi 0 -255 arası

"""


def IzgaraOzniteligi(resim, XKare=10, YKare=10, diziMi=False, cizgiRengi=0):
    import numpy as np
    import math as mt
    izgaraliResimDizisi = []

    if (diziMi == False):
        en = resim.shape[1]
        boy = resim.shape[0]
        izgaraliresim = np.copy(resim)
        X = int(mt.ceil(en / XKare))
        Y = int(mt.ceil(boy / YKare))
        X_koor = en / 2
        Y_koor = boy / 2

        ## ızgaralı yeni resmin ortasından itibaren sağ tarafa tüm dikey çizgileri çizelim
        while (X_koor < en):
            for p in range((boy)):
                izgaraliresim[p, X_koor] = cizgiRengi
            X_koor += X

        X_koor = (en / 2) - X
        ## ızgaralı yeni resmin ortasının bir boy eksiğinden itibaren sol tarafa tüm dikey çizgileri çizelim
        while (X_koor > 0):
            for p in range((boy)):
                izgaraliresim[p, X_koor] = cizgiRengi;
            X_koor -= X

        ## ızgaralı yeni resmin ortasından itibaren asağı tarafa tüm yatay çizgileri çizelim
        while (Y_koor < boy):
            for p in range((en)):
                izgaraliresim[Y_koor, p] = cizgiRengi
            Y_koor += Y

        Y_koor = (boy / 2) - Y
        ## ızgaralı yeni resmin ortasının bir boy eksiğinden itibaren yukarı tarafa tüm yatay çizgileri çizelim
        while (Y_koor > 0):
            for p in range((en)):
                izgaraliresim[Y_koor, p] = cizgiRengi;
            Y_koor -= Y

        izgaraliResimDizisi.append(izgaraliresim)



    else:  ##dizi ise
        for j in range(len(resim)):
            en = resim[j].shape[1]
            boy = resim[j].shape[0]
            izgaraliresim = np.copy(resim[j])
            X = int(mt.ceil(en / XKare))
            Y = int(mt.ceil(boy / YKare))
            X_koor = en / 2
            Y_koor = boy / 2

            ## ızgaralı yeni resmin ortasından itibaren sağ tarafa tüm dikey çizgileri çizelim
            while (X_koor < en):
                for p in range((boy)):
                    izgaraliresim[p, X_koor] = cizgiRengi
                X_koor += X

            X_koor = (en / 2) - X
            ## ızgaralı yeni resmin ortasının bir boy eksiğinden itibaren sol tarafa tüm dikey çizgileri çizelim
            while (X_koor > 0):
                for p in range((boy)):
                    izgaraliresim[p, X_koor] = cizgiRengi;
                X_koor -= X

            ## ızgaralı yeni resmin ortasından itibaren asağı tarafa tüm yatay çizgileri çizelim
            while (Y_koor < boy):
                for p in range((en)):
                    izgaraliresim[Y_koor, p] = cizgiRengi
                Y_koor += Y

            Y_koor = (boy / 2) - Y
            ## ızgaralı yeni resmin ortasının bir boy eksiğinden itibaren yukarı tarafa tüm yatay çizgileri çizelim
            while (Y_koor > 0):
                for p in range((en)):
                    izgaraliresim[Y_koor, p] = cizgiRengi;
                Y_koor -= Y

            izgaraliResimDizisi.append(izgaraliresim)

    return izgaraliResimDizisi


def IzgaraIciPikselSay(resim, arka, izgaraEn=10, izgaraBoy=10, diziMi=False, cizgiRengi=0):
    import numpy as np
    import math as mt
    izgaraMaskesi = np.ones((izgaraBoy, izgaraEn),
                            dtype=np.int16)  # maskemiz ızgara boyutunda 1 lerden oluşacak ki piksellerle matris çarpımı yaptığımızda siyah piksel sayısını bulalım
    izgaraliResimDizisi = []

    if (diziMi == False):
        en = resim.shape[1]
        boy = resim.shape[0]
        izgaraliresim = np.copy(resim)
        XKare = int(mt.ceil(en / izgaraEn))
        YKare = int(mt.ceil(boy / izgaraBoy))
        X = int(mt.ceil(en / XKare))
        Y = int(mt.ceil(boy / YKare))
        X_koor = en / 2
        Y_koor = boy / 2
        pikselSayiMatrisi = np.zeros((YKare, XKare), dtype=np.int16)

        X_koor = 0
        Y_koor = 0

        while (Y_koor < (boy - 10)):
            while (X_koor < (en - 10)):
                top = 0
                for e in range(izgaraEn):
                    for b in range((izgaraBoy)):
                        if (resim[(Y_koor + b), (X_koor + e)] < arka):
                            top += 1
                print('x_koor = ', X_koor, ' Y_koor = ', Y_koor, ' Dizinin Y = ', (Y_koor / izgaraBoy), ' X = ',
                      (X_koor / izgaraEn), ' Top = ', top)
                pikselSayiMatrisi[(Y_koor / izgaraBoy), (X_koor / izgaraEn)] = top
                X_koor += izgaraEn
            Y_koor += izgaraBoy
            X_koor = 0

        ## ızgaralı yeni resmin ortasından itibaren sağ tarafa tüm dikey çizgileri çizelim
        """while(X_koor<(en-10) and Y_koor<(boy-10)):
            top=0
            for e in range(izgaraEn):
                for b in range((izgaraBoy)):
                    if(resim[(Y_koor+b),(X_koor+e)]<arka):
                        top+=1
            pikselSayiMatrisi[(Y_koor/izgaraBoy),(X_koor/izgaraEn)]=top
            X_koor +=izgaraEn
            Y_koor +=izgaraBoy


        X_koor=en/2
        Y_koor=boy/2
        while(X_koor>=0 and Y_koor<(boy-10)):
            top=0
            for e in range(izgaraEn):
                for b in range((izgaraBoy)):
                    if(resim[(Y_koor+b),(X_koor+e)]<arka):
                        top+=1
            pikselSayiMatrisi[(Y_koor/izgaraBoy),(X_koor/izgaraEn)]=top
            X_koor -=izgaraEn
            Y_koor +=izgaraBoy


        X_koor=en/2
        Y_koor=boy/2
        while(X_koor>=0 and Y_koor>=0):
            top=0
            for e in range(izgaraEn):
                for b in range((izgaraBoy)):
                    if(resim[(Y_koor+b),(X_koor+e)]<arka):
                        top+=1
            pikselSayiMatrisi[(Y_koor/izgaraBoy),(X_koor/izgaraEn)]=top
            X_koor -=izgaraEn
            Y_koor -=izgaraBoy


        X_koor=en/2
        Y_koor=boy/2
        while(X_koor<(en-10) and Y_koor>=0):
            top=0
            for e in range(izgaraEn):
                for b in range((izgaraBoy)):
                    if(resim[(Y_koor+b),(X_koor+e)]<arka):
                        top+=1
            pikselSayiMatrisi[(Y_koor/izgaraBoy),(X_koor/izgaraEn)]=top
            X_koor +=izgaraEn
            Y_koor -=izgaraBoy"""

        return pikselSayiMatrisi











