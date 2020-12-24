# Twitter-Idol Chatbot
Codecademy Chatbot Capstone Project

## Premise
The idea of this project is to scrape Twitter for the public conversations of one or more users to try and imitate how they talk with others.

Twitter's API limits pulls to only 200 tweets, and the replied-to tweets are individually pulled, so naturally the code runs up against the API rate limits.

But with roughly 3000 conversations for an active twitter user you can start approximating how they talk to others.

## Implementation
The model used is a transformer model (check link below).

https://medium.com/tensorflow/a-transformer-chatbot-tutorial-with-tensorflow-2-0-88bf59e66fe2 

I chose to go with an open-domain chatbot because it seems less tedious than manually setting up canned responses. Though the amount of tweaking to create this chatbot may have been more than it would take to go through conversation trees.

## Concerns
* The model doesn't have a validation step, so it will be prone to overfitting.

* The version of tensorflow and Nvidia CUDA/CUDnn can break the training module, and it is very slow to train on a CPU.

* It may be immoral to "copy" the speech of a specific real person, but this bot seems to be better at amplifying tropes among a single person's speech habits. A better version of this bot may present more ethical problems.

## Known issues
* Without validation during fitting, the model tends to overfit too much and the replies to novel inputs make less sense. 

* Twitter only lets you capture 3200 tweets at a time, and many of those will not be 

* Outputs are not punctuated or capitalized properly
 
## Dependencies:
* Tensorflow (+ tf.datasets, tf.keras)
* Python-Twitter
* Regex
* urllib
* time
* matplotlib
