import numpy as np
from preprocess import *
from keras.layers import Input, LSTM, Dense
from keras.models import Model
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession
config = ConfigProto()
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)

training_model = Model([encoder_inputs, decoder_inputs], decoder_outputs)
training_model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])

batch_size = 10
epochs = 50

print("Training the model:\n")
# Train the model:
training_model.fit([encoder_input_data, decoder_input_data], decoder_target_data, epochs=epochs, batch_size=batch_size, validation_split=0.2)

training_model.save("training_model.h5")