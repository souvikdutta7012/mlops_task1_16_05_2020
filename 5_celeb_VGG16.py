from keras.applications import VGG16
img_rows = 224
img_cols = 224
model = VGG16(weights = 'imagenet',include_top = False, input_shape = (img_rows, img_cols, 3))
for (i,layer) in enumerate(model.layers):
    print(str(i) + " "+ layer.__class__.__name__, layer.trainable)
from keras.applications import VGG16
img_rows = 224
img_cols = 224
model = VGG16(weights = 'imagenet', include_top = False, input_shape = (img_rows, img_cols, 3))
for layer in model.layers:
    layer.trainable = False
for (i,layer) in enumerate(model.layers):
    print(str(i) + " "+ layer.__class__.__name__, layer.trainable)
def addTopModel(bottom_model, num_classes, D=256):
    top_model = bottom_model.output
    top_model = Flatten(name = "flatten")(top_model)
    top_model = Dense(D, activation = "relu")(top_model)
    top_model = Dropout(0.3)(top_model)
    top_model = Dense(num_classes, activation = "softmax")(top_model)
    return top_model
model.input
model.layers
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D, ZeroPadding2D
from keras.layers.normalization import BatchNormalization
from keras.models import Model
num_classes = 5
FC_Head = addTopModel(model, num_classes)
modelnew = Model(inputs=model.input, outputs=FC_Head)
print(modelnew.summary())
from keras.preprocessing.image import ImageDataGenerator
train_data_dir = '5_celeb/5_celeb/train/'
validation_data_dir = '5_celeb/5_celeb/val/'
train_datagen = ImageDataGenerator(rescale=1./255,rotation_range=20,width_shift_range=0.2,height_shift_range=0.2,horizontal_flip=True,fill_mode='nearest')
validation_datagen = ImageDataGenerator(rescale=1./255)
train_batchsize = 16
val_batchsize = 10
train_generator = train_datagen.flow_from_directory(train_data_dir,target_size=(img_rows, img_cols),batch_size=train_batchsize,class_mode='categorical')
validation_generator = validation_datagen.flow_from_directory(validation_data_dir,target_size=(img_rows, img_cols),batch_size=val_batchsize,class_mode='categorical',shuffle=False)
from keras.optimizers import RMSprop
from keras.callbacks import ModelCheckpoint, EarlyStopping
checkpoint = ModelCheckpoint("image_celeb.h5",monitor="val_loss",mode="min",save_best_only = True,verbose=1)
earlystop = EarlyStopping(monitor = 'val_loss', min_delta = 0, patience = 3,verbose = 1,restore_best_weights = True)
callbacks = [earlystop, checkpoint]
modelnew.compile(loss = 'categorical_crossentropy',optimizer = RMSprop(lr = 0.001),metrics = ['accuracy'])
nb_train_samples = 1190
nb_validation_samples = 170
epochs = 3
batch_size = 16
history = modelnew.fit_generator(train_generator,steps_per_epoch = nb_train_samples // batch_size,epochs = epochs,callbacks = callbacks,validation_data = validation_generator,validation_steps = nb_validation_samples // batch_size)
modelnew.save("image_celeb.h5")
from keras.applications import VGG16
img_rows = 64
img_cols = 64
vgg16 = VGG16(weights = 'imagenet', include_top = False, input_shape = (img_rows, img_cols, 3))
for layer in vgg16.layers:
    layer.trainable = False
for (i,layer) in enumerate(vgg16.layers):
    print(str(i) + " "+ layer.__class__.__name__, layer.trainable)
from keras.applications import VGG16
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D, ZeroPadding2D
from keras.layers.normalization import BatchNormalization
from keras.models import Model
from keras.optimizers import RMSprop
from keras.preprocessing.image import ImageDataGenerator
train_data_dir = '5_celeb/5_celeb/train/'
validation_data_dir = '5_celeb/5_celeb/val/'
train_datagen = ImageDataGenerator(rescale=1./255,rotation_range=20,width_shift_range=0.2,height_shift_range=0.2,horizontal_flip=True,fill_mode='nearest')
validation_datagen = ImageDataGenerator(rescale=1./255)
train_batchsize = 32
val_batchsize = 16
train_generator = train_datagen.flow_from_directory(train_data_dir,target_size=(img_rows, img_cols),batch_size=train_batchsize,class_mode='categorical')
validation_generator = validation_datagen.flow_from_directory(validation_data_dir,target_size=(img_rows, img_cols),batch_size=val_batchsize,class_mode='categorical',shuffle=False)
vgg16 = VGG16(weights = 'imagenet', include_top = False, input_shape = (img_rows, img_cols, 3))
for layer in vgg16.layers:
    layer.trainable = False
num_classes = 5
FC_Head = addTopModel(vgg16, num_classes)
model = Model(inputs=vgg16.input, outputs=FC_Head)
print(model.summary())
from keras.optimizers import RMSprop
from keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
checkpoint = ModelCheckpoint("image_celeb.h5",monitor="val_loss",mode="min",save_best_only = True,verbose=1)
earlystop = EarlyStopping(monitor = 'val_loss', min_delta = 0, patience = 5,verbose = 1,restore_best_weights = True)
reduce_lr = ReduceLROnPlateau(monitor = 'val_loss',factor = 0.2,patience = 3,verbose = 1,min_delta = 0.00001)
callbacks = [earlystop, checkpoint, reduce_lr]
model.compile(loss = 'categorical_crossentropy',optimizer = RMSprop(lr = 0.0001),metrics = ['accuracy'])
nb_train_samples = 1190
nb_validation_samples = 170
epochs = 25
batch_size = 32
history = model.fit_generator(
    train_generator,
    steps_per_epoch = nb_train_samples // batch_size,
    epochs = epochs,
    callbacks = callbacks,
    validation_data = validation_generator,
    validation_steps = nb_validation_samples // batch_size)
model.save("image_celeb.h5")
from keras.models import load_model
classifier = load_model('image_celeb.h5')
import os
import cv2
import numpy as np
from os import listdir
from os.path import isfile, join
monkey_breeds_dict = {"[0]": "ben_afflek","[1]": "elton_john","[2]": "jerry_seinfeld","[3]": "madonna","[4]": "mindy_kaling"}
monkey_breeds_dict_n = {"n0": "ben_afflek", "n1": "elton_john","n2": "jerry_seinfeld","n3": "madonna","n4": "mindy_kaling"}
def draw_test(name, pred, im):
    monkey = monkey_breeds_dict[str(pred)]
    BLACK = [0,0,0]
    expanded_image = cv2.copyMakeBorder(im, 80, 0, 0, 100 ,cv2.BORDER_CONSTANT,value=BLACK)
    cv2.putText(expanded_image, monkey, (20, 60) , cv2.FONT_HERSHEY_SIMPLEX,1, (0,0,255), 2)
    cv2.imshow(name, expanded_image)
def getRandomImage(path):
    """function loads a random images from a random folder in our test path """
    folders = list(filter(lambda x: os.path.isdir(os.path.join(path, x)), os.listdir(path)))
    random_directory = np.random.randint(0,len(folders))
    path_class = folders[random_directory]
    print("Class - " + monkey_breeds_dict_n[str(path_class)])
    file_path = path + path_class
    file_names = [f for f in listdir(file_path) if isfile(join(file_path, f))]
    random_file_index = np.random.randint(0,len(file_names))
    image_name = file_names[random_file_index]
    return cv2.imread(file_path+"/"+image_name)
for i in range(0,10):
    input_im = getRandomImage("5_celeb/5_celeb/val/")
    input_original = input_im.copy()
    input_original = cv2.resize(input_original, None, fx=0.5, fy=0.5, interpolation = cv2.INTER_LINEAR)
    input_im = cv2.resize(input_im, (64, 64), interpolation = cv2.INTER_LINEAR)
    input_im = input_im / 255.
    input_im = input_im.reshape(1,64,64,3)
    res = np.argmax(classifier.predict(input_im, 1, verbose = 0), axis=1)
    draw_test("Prediction", res, input_original) 
    cv2.waitKey(0)
cv2.destroyAllWindows()