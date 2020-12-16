from prepare_text_model import *
from matplotlib import pyplot as plt
from tensorflow import keras
import pickle

epochs = 2

fit_model = training_model.fit(dataset, epochs=epochs)

training_model.save_weights("model_weights.h5")


predict("How are you feeling?")

for i in range(5):
	predict(orig_questions[i])

train_loss = fit_model.history['loss']
#val_loss = fit_model.history['val_loss']
xc = range(1, epochs+1)

plt.figure()
plt.plot(xc, train_loss, 'blue', label="Training Loss")
#plt.plot(xc, val_loss, 'red', label="Validation Loss")
plt.legend()
plt.show()

