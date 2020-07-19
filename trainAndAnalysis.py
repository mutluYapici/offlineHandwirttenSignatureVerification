""""""
"""Run to train the model (Modeli Eğitimek için Çalıştırın)"""
train(model=model,eval_model=eval_model, data=((x_train, y_train), (x_test, y_test)), args=args)



"""Run to LOAD TRAINED WEIGHTS (Eğitilmiş Ağırlıkları Yüklemek İçin Çalıştırın)"""
eval_model.load_weights('data/'+imzaAdi+'/M0115_weight.h5')

"""Run to See Analysis Results of The Model (Eğitilmiş Modele Ait Analiz Sonuçlarını Göremek İçin Çalıştırın)"""

#Skilled Forgers and Genuines (Sadece Sahte Temel verilerle ölçelim)
xm=np.asarray(SVeri[0]).astype('float16') / np.asarray(SVeri[0]).max()
ym=np.asarray(SVeri[1])
xm=np.append(xm ,  np.asarray(GVeri[0]).astype('float16') / np.asarray(GVeri[0]).max(),axis=0)
ym=np.append(ym ,  np.asarray(GVeri[1]),axis=0)

conmat2=f.dogtulamaYontemleri(eval_model,xm, ym)




