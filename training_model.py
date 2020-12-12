from tensorflow import keras
import numpy as np
from keras.layers import Input, LSTM, Dense
from keras.models import Model
from preprocess import questions, answers, process_text, input_tokens, target_tokens, num_encoder_tokens, \
	num_decoder_tokens, max_encoder_seq_length, max_decoder_seq_length

if True:  # debugging info
	print('Number of samples:', len(questions))
	print('Number of unique input tokens:', num_encoder_tokens)
	print('Number of unique output tokens:', num_decoder_tokens)
	print('Max sequence length for inputs:', max_encoder_seq_length)
	print('Max sequence length for outputs:', max_decoder_seq_length)

input_features_dict = dict([(token, i) for i, token in enumerate(input_tokens)])
# Build out target_features_dict:
target_features_dict = dict([(token, i) for i, token in enumerate(target_tokens)])

reverse_input_features_dict = dict((i, token) for token, i in input_features_dict.items())
# Build out reverse_target_features_dict:
reverse_target_features_dict = dict((i, token) for token, i in target_features_dict.items())

# Build out encoder input matrix (all zeros so far)
encoder_input_data = np.zeros(
	(len(questions), max_encoder_seq_length, num_encoder_tokens), dtype='float32')
# Build out the decoder input matrix:
decoder_input_data = np.zeros(
	(len(questions), max_decoder_seq_length, num_decoder_tokens), dtype='float32')
# Build out the decoder target matrix:
decoder_target_data = np.zeros(
	(len(answers), max_decoder_seq_length, num_decoder_tokens), dtype='float32')

for line, (question, answer) in enumerate(zip(questions, answers)):
	# fill out matrices with input from the docs
	for word_step, token in enumerate(question):
		print(f"The encoder input at word {word_step} in line {line} is {token}")
		encoder_input_data[line, word_step, input_features_dict[token]] = 1.0

	for word_step, token in enumerate(answer):
		print(f"The decoder input at word {word_step} in line {line} is {token}")
		decoder_input_data[line, word_step, target_features_dict[token]] = 1.0

		if word_step > 0:
			# decoder needs to guess next word from the previous word
			decoder_target_data[line, word_step-1, target_features_dict[token]] = 1.0

lstm_batch_size = 256

encoder_inputs = Input(shape=(None, num_encoder_tokens))
encoder_lstm = LSTM(lstm_batch_size, return_state=True)
encoder_outputs, state_hidden, state_cell = encoder_lstm(encoder_inputs)
encoder_states = [state_hidden, state_cell]

decoder_inputs = Input(shape=(None, num_decoder_tokens))
decoder_lstm = LSTM(lstm_batch_size, return_sequences=True, return_state=True)
decoder_outputs, decoder_state_hidden, decoder_state_cell = decoder_lstm(decoder_inputs, initial_state=encoder_states)

# decoder_dense is a function to output the probabilistic responses expected from the decoder LSTM model outputs
decoder_dense = Dense(num_decoder_tokens, activation="softmax")
decoder_outputs = decoder_dense(decoder_outputs)

training_model = Model([encoder_inputs, decoder_inputs], decoder_outputs)
training_model.summary()

training_model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])

batch_size = 50
epochs = 30

training_model.fit([encoder_input_data, decoder_input_data], decoder_target_data, epochs=epochs, batch_size=batch_size, validation_split=0.2)
training_model.save("training_model.h5")
