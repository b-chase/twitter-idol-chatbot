import matplotlib.pyplot as plt
from tensorflow import keras
from keras import backend as K
from keras.models import Model
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession

from preprocess import *

config = ConfigProto()
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)

training_model = Model([encoder_inputs, decoder_inputs], decoder_outputs)
# training_model = check_model

training_model.compile(optimizer='rmsprop',
                       loss='CategoricalCrossentropy',
                       metrics=['accuracy'])

print("Default learning rate:", training_model.optimizer.learning_rate.numpy())
K.set_value(training_model.optimizer.learning_rate, 0.0001)
print("Current learning rate:", training_model.optimizer.learning_rate.numpy())

batch_size = 20
epochs = 1000

print("Training the model:\n")
# Train the model:
fit_model = training_model.fit([encoder_input_data,
                               decoder_input_data],
                               decoder_target_data,
                               epochs=epochs,
                               batch_size=batch_size,
                               validation_split=0.25)

training_model.save("training_model.h5")

train_loss = fit_model.history['loss']
val_loss = fit_model.history['val_loss']
xc = range(1, epochs+1)

plt.figure()
plt.plot(xc, train_loss, 'b', label="Training Loss")
plt.plot(xc, val_loss, 'r', label="Validation Loss")
plt.legend()
plt.show()