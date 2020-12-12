import re
from tensorflow import keras
from keras.layers import Input, LSTM, Dense
from keras.models import Model, load_model
from preprocess import *

encoder_model = load_model("encoder_model.h5")
decoder_model = load_model("decoder_model.h5")

def decode_sequence(test_input):
	encoder_states_value = encoder_model.predict(test_input)
	decoder_states_value = encoder_states_value
	target_seq = np.zeros((1, 1, num_decoder_tokens))
	target_seq[0, 0, target_features_dict['<START>']] = 1.
	decoded_sentence = ''

	stop_condition = False
	while not stop_condition:
		# Run the decoder model to get possible
		# output tokens (with probabilities) & states
		output_tokens, new_decoder_hidden_state, new_decoder_cell_state = decoder_model.predict(
			[target_seq] + decoder_states_value)

		# Choose token with highest probability
		sampled_token_index = np.argmax(output_tokens[0, -1, :])
		sampled_token = reverse_target_features_dict[sampled_token_index]
		decoded_sentence += " " + sampled_token

		# Exit condition: either hit max length
		# or find stop token.
		if (sampled_token == '<END>' or len(decoded_sentence) > max_decoder_seq_length):
			stop_condition = True
			decoded_sentence.replace(" <END>", "")

		# Update the target sequence (of length 1).
		target_seq = np.zeros((1, 1, num_decoder_tokens))
		target_seq[0, 0, sampled_token_index] = 1.

		# Update states
		decoder_states_value = [new_decoder_hidden_state, new_decoder_cell_state]

	return decoded_sentence

class ChatBot:

	negative_responses = ("no", "nope", "nah", "naw", "not a chance", "sorry")

	exit_commands = ("quit", "pause", "exit", "goodbye", "bye", "later", "stop")

	def prompt_user(self, text=None):
		if text is None:
			text = ""
		return input(text + "\n> ")

	def start_chat(self):
		user_response = prompt_user("Hi, I'm a chatbot trained on your twitter idol!")

		if user_response in self.negative_responses:
			print("Ok, have a great day!")
			return

		self.chat(user_response)

	def chat(self, reply):
		while not self.make_exit(reply):
			reply = input(self.generate_response(reply))

	def string_to_matrix(self, user_input):
		tokens = re.findall(r"[\w']+|[^\s\w]", user_input)
		user_input_matrix = np.zeros(
			(1, max_encoder_seq_length, num_encoder_tokens),
			dtype='float32')
		for timestep, token in enumerate(tokens):
			if token in input_features_dict:
				user_input_matrix[0, timestep, input_features_dict[token]] = 1.
		return user_input_matrix

	def generate_response(self, user_input):
		input_matrix = self.string_to_matrix(user_input)
		states_value = encoder_model.predict(input_matrix)
		target_seq = np.zeros((1, 1, num_decoder_tokens))
		target_seq[0, 0, target_features_dict['<START>']] = 1.

		chatbot_response = ''

		stop_condition = False
		while not stop_condition:
			output_tokens, hidden_state, cell_state = decoder_model.predict(
				[target_seq] + states_value)

			sampled_token_index = np.argmax(output_tokens[0, -1, :])
			sampled_token = reverse_target_features_dict[sampled_token_index]



			if (sampled_token == '<END>' or len(chatbot_response) > max_decoder_seq_length):
				stop_condition = True
				chatbot_response += "\n> "
				break

			chatbot_response += " " + sampled_token
			target_seq = np.zeros((1, 1, num_decoder_tokens))
			target_seq[0, 0, sampled_token_index] = 1.

			states_value = [hidden_state, cell_state]

		# remove <START> and <END> tokens
		# from chatbot_response:


		return chatbot_response.replace("<START>", "").replace("<END>", "")

	def make_exit(self, reply):
		for exit_command in self.exit_commands:
			if exit_command in reply:
				print("Ok, have a great day!")
				return True

		return False

chatty_mcchatface = ChatBot()
# call .start_chat():
chatty_mcchatface.start_chat()