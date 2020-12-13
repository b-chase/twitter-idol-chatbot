import re
import numpy as np
from keras.layers import Input, LSTM, Dense
from keras.models import Model


with open("saved_tweets2.txt", 'r') as tweets_file:
	corpus = tweets_file.read().lower().split("+++||+++")


def process_text(text):
	tokenized = re.findall(r"[\w\d]+|[^\s\w]", text.lower().strip())
	return tokenized


questions = []
answers = []
input_tokens = []
target_tokens = []

for i, line in enumerate(corpus):
	tokens = line.strip().lower().split()
	tokens = [t.strip() for t in tokens if "@" not in t and "https://t.co" not in t]
	cleaned_line = "<START> " + " ".join(tokens) + " <END>"  # still want to tokenize punctuation!
	cleaned_tokens = cleaned_line.split()
	if i % 2 == 0:
		questions.append(cleaned_tokens)
		input_tokens.extend(cleaned_tokens)
	else:
		answers.append(cleaned_tokens)
		target_tokens.extend(cleaned_tokens)

input_tokens = sorted(list(set(input_tokens)))
target_tokens = sorted(list(set(target_tokens)))
num_encoder_tokens = len(input_tokens)
num_decoder_tokens = len(target_tokens)


max_encoder_seq_length = max([len(line) for line in questions])
max_decoder_seq_length = max([len(line) for line in answers])

input_features_dict = dict(
	[(token, i) for i, token in enumerate(input_tokens)])
target_features_dict = dict(
	[(token, i) for i, token in enumerate(target_tokens)])

reverse_input_features_dict = dict(
	(i, token) for token, i in input_features_dict.items())
reverse_target_features_dict = dict(
	(i, token) for token, i in target_features_dict.items())

encoder_input_data = np.zeros(
	(len(questions), max_encoder_seq_length, num_encoder_tokens),
	dtype='float32')
decoder_input_data = np.zeros(
	(len(questions), max_decoder_seq_length, num_decoder_tokens),
	dtype='float32')
decoder_target_data = np.zeros(
	(len(questions), max_decoder_seq_length, num_decoder_tokens),
	dtype='float32')

for line, (input_doc, target_doc) in enumerate(zip(questions, answers)):

	for timestep, token in enumerate(input_doc):
		print("Encoder input timestep & token:", timestep, token)
		# Assign 1. for the current line, timestep, & word
		# in encoder_input_data:
		encoder_input_data[line, timestep, input_features_dict[token]] = 1.

	for timestep, token in enumerate(target_doc):
		# decoder_target_data is ahead of decoder_input_data by one timestep
		print("Decoder input timestep & token:", timestep, token)
		# Assign 1. for the current line, timestep, & word
		# in decoder_input_data:
		decoder_input_data[line, timestep, target_features_dict[token]] = 1.

		if timestep > 0:
			# decoder_target_data is ahead by 1 timestep
			# and doesn't include the start token.
			#print("Decoder target timestep:", timestep)
			# Assign 1. for the current line, timestep, & word
			# in decoder_target_data:
			decoder_target_data[line, timestep - 1, target_features_dict[token]] = 1.


latent_dim = 256

encoder_inputs = Input(shape=(None, num_encoder_tokens))
encoder_lstm = LSTM(latent_dim, return_state=True)
encoder_outputs, state_hidden, state_cell = encoder_lstm(encoder_inputs)
encoder_states = [state_hidden, state_cell]

decoder_inputs = Input(shape=(None, num_decoder_tokens))
decoder_lstm = LSTM(latent_dim, return_sequences=True, return_state=True)
decoder_outputs, decoder_state_hidden, decoder_state_cell = decoder_lstm(decoder_inputs, initial_state=encoder_states)
decoder_dense = Dense(num_decoder_tokens, activation="softmax")
decoder_outputs = decoder_dense(decoder_outputs)


