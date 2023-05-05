![demo gif](file.gif)


# Tun-Akinator
Tunisian Akinator is a Python-based implementation of the classic Akinator game, but with a customizable dataset of characters. The game tries to guess which  character the user is thinking(that includes tunisian fictional characters) of by asking a series of yes/no questions. The questions are chosen based on a decision tree algorithm that uses machine learning techniques to maximize the information gain at each step.

## Getting Started

To play the game, you need to have Python 3 and Pygame installed on your computer. You can install Pygame using pip:

```
pip install pygame
```
Once you have installed Pygame, you can run the game by running the following command in your terminal:
```
python tun_akinator.py
```

## How to Play

When you start the game, you will be asked a series of questions. Answer each question truthfully by clicking on the "Yes" or "No" button. The game will use your answers to narrow down the list of possible characters until it can make a prediction.

If the game makes the correct prediction, click the "r" key to play another round. 


## Data Science

The game uses a decision tree algorithm to generate questions and make predictions. The decision tree is built using a dataset of Tunisian characters and personalities. The questions are chosen based on a metric called information gain, which measures how much a question reduces the uncertainty about the answer.


