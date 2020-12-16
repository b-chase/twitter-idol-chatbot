from prepare_text_model import *
from matplotlib import pyplot as plt
import random

# Can optionally start from original point
if False:
	training_model.load_weights("model_weights.h5")

epochs = 10
samples = len(orig_questions)
cycles = 20
for i in range(cycles):
	print(f"Fitting next 10 epochs, starting from #{i*epochs+1} (Will be {cycles*epochs} total)")
	fit_model = training_model.fit(dataset, epochs=epochs)
	training_model.save_weights("model_weights.h5")
	print("\nTesting model prediction:")
	for i in range(3):
		predict(random.choice(orig_questions))
		print("---")
	predict("What do you like to do in your free time?")
	print("---")


train_loss = fit_model.history['loss']
#val_loss = fit_model.history['val_loss']
xc = range(1, epochs+1)

plt.figure()
plt.plot(xc, train_loss, 'blue', label="Training Loss")
#plt.plot(xc, val_loss, 'red', label="Validation Loss")
plt.legend()
plt.show()

