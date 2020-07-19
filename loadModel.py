"""  >>>>>>>>>>>>>>>>>>>>>>>>>>>>      SINIFLANDIRMA BÖLÜMÜ     <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<  """
import numpy as np
from keras import layers, models, optimizers
from keras import backend as K
from kapsnet.capsulelayers import CapsuleLayer, PrimaryCap, Length, Mask
from keras.layers import Conv2D, MaxPooling2D, Dense, Input, Dropout, Activation, Flatten, BatchNormalization,ZeroPadding2D,concatenate,Lambda,GlobalAveragePooling2D,AveragePooling2D,merge,Concatenate,GlobalMaxPooling2D

K.set_image_data_format('channels_last')


def CapsNet(input_shape, n_class, num_routing):

	dim_capsule=16
	x = layers.Input(shape=input_shape )
	bn_axis = 3 if K.image_data_format() == 'channels_last' else 1

	# KATMAN 1: Klasik Evrişimli Sinir Ağı Katmanı (Conv2D)
	x1 = layers.Conv2D(filters=32, kernel_size=3, strides=1, padding='valid', activation='relu', name='conv1')(x)
	x2 = BatchNormalization(axis=bn_axis, epsilon=1.001e-5, name='bn_bn')(x1)
	x4 = AveragePooling2D(2, strides=2, name='Av_pool')(x2) #burayıı kaldırınca batch size 100 den 10 düştü
	conv1 = layers.Conv2D(filters=16, kernel_size=5, strides=1, padding='valid', activation='relu', name='conv2')(x4)


	# KATMAN 2: Conv2D katmanı ile ezme (squash) aktivasyonu, [None, num_capsule, dim_capsule]’e yeniden şekil veriliyor.
	primarycaps = PrimaryCap(conv1, dim_capsule=16, n_channels=21, kernel_size=9, strides=2, padding='valid')


	# KATMAN 3: Kapsül Katmanı. Dinamik Yönlendirme algoritması burada çalışıyor.
	digitcaps = CapsuleLayer(num_capsule=n_class, dim_capsule=dim_capsule, num_routing=num_routing,
							 name='digitcaps')(primarycaps)

	# KATMAN 4: Her kapsülün uzunluğunu yeniden düzenleyen yardımcı bir katmandır.
	# Doğru etiketle eşleşmesi için bu işlem yapılır.
	# Eğer Tensorflow kullanıyorsanız bu işleme gerek yok :)

	out_caps = Length(name='capsnet')(digitcaps)

	# Kodçözücü Ağ.
	y = layers.Input(shape=(n_class,))
	masked_by_y = Mask()([digitcaps, y])  # Doğru etiket, kapsül katmanın çıkışını maskelemek için kullanılır (Eğitim için).
	masked = Mask()(digitcaps)  # Filtre (maske), kapsülün maksimal uzunluğu ile kullanılır (Kestirim için).

	# Eğitim ve Kestirimde Kodçözücü Modelin Paylaşımı
	decoder = models.Sequential(name='decoder')
	decoder.add(layers.Dense(32, activation='relu', input_dim=dim_capsule*n_class))
	decoder.add(layers.Dense(16, activation='relu'))
	decoder.add(layers.Dense(np.prod(input_shape), activation='relu'))
	decoder.add(layers.Reshape(target_shape=input_shape, name='out_recon'))

	# Eğitim ve Değerlendirme (Kestirim) için Modeller
	train_model = models.Model([x, y], [out_caps, decoder(masked_by_y)])
	eval_model = models.Model(x, [out_caps, decoder(masked)])
	return train_model, eval_model


def margin_loss(y_true, y_pred):
	"""
	Makaledeki Denklem(4) için hata değeri. y_true[i, :] sadece `1` içermediğinde, bu kayıp hesabı çalışır. (Test yok)
			  : "y_true" parametresi: [None, n_classes]
			  : "y_pred" parametresi: [None, num_capsule]
			  : Fonksiyon çıktısı: Skaler kayıp değeri.

	"""
	L = y_true * K.square(K.maximum(0., 0.9 - y_pred)) + \
		0.5 * (1 - y_true) * K.square(K.maximum(0., y_pred - 0.1))

	return K.mean(K.sum(L, 1))




from keras.callbacks import Callback
from modules.ortakislemlersinifi import Ortakislemler
f=Ortakislemler()

class GeriCagir(Callback):
		def __init__(self, eval_model,GVeri,SVeri):
			super(GeriCagir, self).__init__()
			self.xm = np.asarray(SVeri[0]).astype('float16') / np.asarray(SVeri[0]).max()
			self.ym = np.asarray(SVeri[1])
			self.xm = np.append(self.xm, np.asarray(GVeri[0]).astype('float16') / np.asarray(GVeri[0]).max(), axis=0)
			self.ym = np.append(self.ym, np.asarray(GVeri[1]), axis=0)
			self.eval_model=eval_model
			self.FP=0
			self.FN = 0
			self.FRR = 1
			self.FAR = 1

		def on_epoch_end(self, epoch, logs=None):
			f.dogtulamaYontemleri(self.eval_model, self.xm, self.ym)
			if(((f.FAR + f.FRR)/2) < ((self.FAR + self.FRR)/2) ):
				self.eval_model.save_weights('images/'+imzaAdi2+'_ağirliklarim.h5')
				print("Yeni Ağırlıklar Kaydedildi")
				if(f.FN==0 and f.FP==0):#Eğerki tüm gerçekleri ve tüm sahteleri doğru tespit etmişsek eğitim dursun
					self.model.stop_training = True

				self.FRR = f.FRR
				self.FAR = f.FAR




def train(model, eval_model, data, args):
	"""
   Kapsül Ağının Eğitimi
			  : "model" parametresi: CapsNet (Kapsül Ağ) Modeli
			  :"data" parametresi: Eğitim ve test verisinden bir grup içerir, örneğin; `((x_train, y_train), (x_test, y_test))`
			  :"args" parametresi: Bağımsız değişkenler
			  : Fonksiyon çıktısı: Eğitilmiş model
	"""

	# Verilerin Kullanıma Hazır Hale Getir
	(x_train, y_train), (x_test, y_test) = data


	metrik = 'accuracy'
	loss = 'binary_crossentropy'
	# Model Derlenir
	model.compile(optimizer=args.optimizer,
				  loss=[margin_loss, 'mse'],
				  loss_weights=[1., args.lam_recon],
				  metrics={'capsnet': 'accuracy'})


	# EĞİTİM ÖNCESİ VERİ ARTIRMA (DATA AUGMENTATION) YAPALIM
	### VERİ ARTIRMA BAŞLA
	def train_generator(x, y, batch_size, shift_fraction=0.):
		train_datagen = ImageDataGenerator(width_shift_range=shift_fraction,
										   height_shift_range=shift_fraction)
		generator = train_datagen.flow(x, y, batch_size=batch_size)
		while 1:
			x_batch, y_batch = generator.next()
			yield ([x_batch, y_batch], [y_batch, x_batch])


	# Veri Artırma (Data Augmentation) Yapmadan Modelin Eğitimi:
	model.fit([x_train, y_train], [y_train, x_train], batch_size=args.batch_size, epochs=args.epochs,
			  validation_data=[[x_test, y_test], [y_test, x_test]],callbacks=[GeriCagir(eval_model,GVeri,SVeri)])


	### VERİ ARTIRMA BİTİR

	model.save_weights(args.save_dir + '/trained_model.h5')
	print('Trained model saved to \'%s/trained_model.h5\'' % args.save_dir)

	from kapsnet.utils import plot_log
	plot_log(args.save_dir + '/log.csv', show=True)

	return model


def test(model, data):
	x_test, y_test = data
	y_pred, x_recon = model.predict(x_test, batch_size=100)
	print('-'*50)
	print('Test acc:', np.sum(np.argmax(y_pred, 1) == np.argmax(y_test, 1))/y_test.shape[0])

	import matplotlib.pyplot as plt
	from kapsnet.utils import combine_images
	from PIL import Image

	img = combine_images(np.concatenate([x_test[:50],x_recon[:50]]))
	image = img * 255
	Image.fromarray(image.astype(np.uint8)).save("real_and_recon.png")
	print()
	print('Reconstructed images are saved to ./real_and_recon.png')
	print('-'*50)
	plt.imshow(plt.imread("real_and_recon.png", ))
	plt.show()



import os
from keras.preprocessing.image import ImageDataGenerator



import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--batch_size', default=100, type=int)
parser.add_argument('--epochs', default=100, type=int)
parser.add_argument('--lam_recon', default=0.003, type=float)  # 784 * 0.0005, makalede SE hesaplanmıştır, burada MSE hesaplanıyor
parser.add_argument('--num_routing', default=3, type=int)  # yönlendirme sayısı > 0 olmalı
parser.add_argument('--shift_fraction', default=0.1, type=float)
parser.add_argument('--debug', default=0, type=int)  # debug>0 TensorBoard’ta ağırlıklar tutulur.
parser.add_argument('--save_dir', default='./result')
parser.add_argument('--is_training', default=1, type=int)
parser.add_argument('--weights', default=None)
parser.add_argument('--optimizer', default=optimizers.SGD(lr=0.001))
parser.add_argument('--lr', default=0.001, type=float)

args, unknown = parser.parse_known_args()
print(args)


(x_train, y_train), (x_test, y_test)=(X_train, Y_train), (X_val, Y_val)



model, eval_model = CapsNet(input_shape=input_shape,
								n_class=len(np.unique(np.argmax(y_train, 1))),
								num_routing=args.num_routing)
model.summary()

