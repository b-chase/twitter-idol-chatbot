from prepare_text_model import *
training_model.load_weights(f"{user}_weights.h5")


class ChatBot:
	negative_responses = ("no", "nope", "nah", "naw", "not a chance", "sorry")
	exit_commands = ("quit", "pause", "exit", "goodbye", "bye", "later", "stop")

	def prompt_user(self, text=None):
		if text is None:
			text = ""
		return input(text + "\n> ")

	def start_chat(self):
		user_response = input("Hi, I'm a chatbot trained to imitate your twitter idol! What do you want to talk about?\n>> ")
		if user_response in self.negative_responses:
			print("Ok, have a great day!")
			return
		self.chat(user_response)
		return

	def chat(self, reply):
		while not self.make_exit(reply):
			reply = input(predict(reply, quiet=True)+"\n>> ")
		return

	def make_exit(self, reply):
		for exit_command in self.exit_commands:
			if exit_command in reply:
				print("Ok, have a great day!")
				return True
		return False


natebot = ChatBot()
natebot.start_chat()