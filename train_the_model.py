from prepare_text_model import *
from matplotlib import pyplot as plt
import random

# Can optionally start from original point
if False:
    training_model.load_weights(f"model_weights/{user}_weights.h5")

test_questions = ["What do you like to do in your free time?",
                  "What is your favorite country?",
                  "How are you feeling today?",
                  "Can you tell me a secret?",
                  "Do you think the weather will be nice tomorrow?"]

epochs = 50
samples = len(orig_questions)
cycles = 12
train_loss = []
for i in range(cycles):
    print(f"Fitting next {epochs} epochs, starting from #{i * epochs + 1} (Will be {cycles * epochs} total)")
    fit_model = training_model.fit(dataset, epochs=epochs)
    training_model.save_weights(f"model_weights/{user}_weights.h5")
    print("\n>>Testing model prediction:<<")
    for q in test_questions:
        predict(q)
        print("---")

    train_loss.extend(fit_model.history['loss'])
    # val_loss = fit_model.history['val_loss']
    xc = range(1, (i+1)*epochs+1)

    plt.figure()
    plt.plot(xc, train_loss, 'blue', label="Training Loss")
    # plt.plot(xc, val_loss, 'red', label="Validation Loss")
    plt.legend()
    plt.show()

