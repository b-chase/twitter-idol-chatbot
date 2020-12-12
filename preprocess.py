import re

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

try:
	max_encoder_seq_length = max([len(line) for line in questions])
	max_decoder_seq_length = max([len(line) for line in answers])
except ValueError:
	pass

