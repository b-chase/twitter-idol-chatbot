# Twitter-Idol Chatbot
Codecademy Chatbot Capstone Project

## Premise
The idea of this project is to scrape Twitter for the public conversations of one or more users to try and imitate how they talk with others.

Twitter's API limits pulls to only 200 tweets, and the replied-to tweets are individually pulled, so naturally the code runs up against the API rate limits.

But with roughly 3000 conversations for an active twitter user you can start approximating how they talk to others.

## Implementation
The model used is a transformer model (check link below) and does not come with any validation steps.

https://medium.com/tensorflow/a-transformer-chatbot-tutorial-with-tensorflow-2-0-88bf59e66fe2 

## Known issues
* Without validation during fitting, the model tends to overfit too much and the replies to novel inputs make less sense. 

* Another issue, which is less of a bug and more of an annoyance, is that Tensorflow's libraries are slow to load when the chatbot first runs.
The model weights are saved and loaded without calling the entire fitting process every time you boot up, which is good, but the
 
## Future improvements
~~* Update tweet scraper to batch-retrieve the replied-to tweets and save on API calls~~
* Fix the output to be punctuated and capitalized properly
* Add validation checks to transformer model to prevent overfitting
* allow user to select from list of chatting partner when the boot the program
* change twitter pulls to take more tweets
 
