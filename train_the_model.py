from prepare_text_model import *
from matplotlib import pyplot as plt

epochs = 500

fit_model = training_model.fit(dataset, epochs=epochs)

training_model.save_weights("model_weights.h5")

for i in range(20,30):
	predict(orig_questions[i])
	print("---")
predict("How are you feeling?")


train_loss = fit_model.history['loss']
#val_loss = fit_model.history['val_loss']
xc = range(1, epochs+1)

plt.figure()
plt.plot(xc, train_loss, 'blue', label="Training Loss")
#plt.plot(xc, val_loss, 'red', label="Validation Loss")
plt.legend()
plt.show()

