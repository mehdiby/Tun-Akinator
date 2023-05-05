import math

import pygame
data = [
    {"name":"Iron man", "human":True, "football_player":False, "movie":True , "fictional":True, "scientist":True, "tunisian":False, "male":True},
    {"name": "Einstein", "human": True, "football_player": False, "movie": False, "fictional": False, "scientist": True,"tunisian": False, "male":True},
    {"name": "Mehdi", "human": True, "football_player": True, "movie": False, "fictional": False, "scientist": True,"tunisian": True, "male":True},
    {"name": "Lionel Messi", "human": True, "football_player": True, "movie": False, "fictional": False, "scientist": False,"tunisian": False, "male":True},
    {"name": "Nemo", "human": False, "football_player": False, "movie": True, "fictional": False, "scientist": False,"tunisian": False, "male":False},
    {"name": "Youssef Msakni", "human": True, "football_player": True, "movie": False, "fictional": False, "scientist": False,"tunisian": True, "male":True},
    {"name": "Jon Snow", "human": True, "football_player": False, "movie": False, "fictional": True, "scientist": False,"tunisian": False, "male":True},
    {"name": "Snow white", "human": True, "football_player": False, "movie": True, "fictional": True, "scientist": False,"tunisian": False, "male":False},
    {"name": "Ada Lovelace", "human": True, "football_player": False, "movie": False, "fictional": False, "scientist": True,"tunisian": False, "male":False},
    {"name": "Donald Trump", "human": True, "football_player": False, "movie": False, "fictional": False, "scientist": False,"tunisian": False, "male":True},
    {"name": "Serena Williams","human": True,"football_player": False,"movie": False,"fictional": False,"scientist": False,"tunisian": False,"male":False},
    {"name": "Ons Jabeur","human": True,"football_player": False,"movie": False,"fictional": False,"scientist": False,"tunisian": True,"male":False},
    {"name": "Sbouii", "human": True, "football_player": False, "movie": False, "fictional": True, "scientist": False,"tunisian": True, "male":True},
    {"name": "mahrouss", "human": False, "football_player": False, "movie": False, "fictional": True, "scientist": False,"tunisian": True, "male":True},
]

class Node:
    def __init__(self, question=None, character=None):
        self.question = question
        self.character = character
        self.children = {}

def entropy(data):
    labels = {}
    for d in data:
        label = d['name']
        if label not in labels:
            labels[label] = 0
        labels[label] += 1
    entropy = 0
    for label in labels:
        p = labels[label] / len(data)
        entropy -= p * math.log2(p)
    return entropy

def information_gain(data, question):
    true_data = []
    false_data = []
    for d in data:
        if d[question['property']] == question['value']:
            true_data.append(d)
        else:
            false_data.append(d)
    if len(true_data) == 0 or len(false_data) == 0:
        return 0
    true_entropy = entropy(true_data)
    false_entropy = entropy(false_data)
    info_gain = entropy(data) - (len(true_data) / len(data)) * true_entropy - (len(false_data) / len(data)) * false_entropy
    return info_gain

def build_decision_tree(data, questions, ask_min_questions=False):
    if len(data) == 0:
        return None
    same_characters = all(d == data[0] for d in data)
    if same_characters:
        return Node(character=data[0]['name'])
    if len(questions) == 0:
        labels = {}
        for d in data:
            label = d['name']
            if label not in labels:
                labels[label] = 0
            labels[label] += 1
        max_label = max(labels, key=lambda k: labels[k])
        return Node(character=max_label)
    if ask_min_questions:
        best_question = max(questions, key=lambda q: information_gain(data, q))
    else:
        best_question = max(questions, key=lambda q: information_gain(data, q), default=None)
    true_data = []
    false_data = []
    for d in data:
        if d[best_question['property']] == best_question['value']:
            true_data.append(d)
        else:
            false_data.append(d)
    node = Node(question=best_question)
    remaining_questions = [q for q in questions if q != best_question]
    if ask_min_questions:
        node.children[True] = build_decision_tree(true_data, remaining_questions, ask_min_questions=True)
        node.children[False] = build_decision_tree(false_data, remaining_questions, ask_min_questions=True)
    else:
        node.children[True] = build_decision_tree(true_data, remaining_questions)
        node.children[False] = build_decision_tree(false_data, remaining_questions)
    return node


def print_tree(node, indent=0):
    if node.question:
        print(' ' * indent, node.question['property'], '=', node.question['value'], ':')
        print_tree(node.children[True], indent + 2)
        print_tree(node.children[False], indent + 2)
    else:
        print(' ' * indent, node.character)

def predict(node, example):
    if node.question:
        if example[node.question['property']] == node.question['value']:
            return predict(node.children[True], example)
        else:
            return predict(node.children[False], example)
    else:
        return node.character



# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
bg=(173,144,200)
fontques=(255,188,61)
# Initialize Pygame
pygame.init()

# Set the width and height of the screen [width, height]
size = (700, 500)
screen = pygame.display.set_mode(size)

# Set the caption for the screen
pygame.display.set_caption("Akinator Game")



# Loop until the user clicks the close button
done = False
show= True
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Define the font to use for the text
font = pygame.font.SysFont('Calibri', 30, True, False)

# Define the question text
question = "Is the character a {}?"

# Define the buttons
yes_button = pygame.Rect(120, 370, 100, 50)
no_button = pygame.Rect(470, 370, 100, 50)

# Define the text for the buttons
yes_text = font.render("Yes", True, WHITE)
no_text = font.render("No", True, WHITE)

# Set the example and the initial node
example = {}
questions = [
    {"property": "human", "value": True},
    {"property": "football_player", "value": True},
    {"property": "movie", "value": True},
    {"property": "fictional", "value": True},
    {"property": "scientist", "value": True},
    {"property": "tunisian", "value": True},
    {"property": "male", "value": True}
]
root = build_decision_tree(data, questions)
node = root

# Load the image and scale it to fit the screen
background_img = pygame.image.load("avatar.png")
background_img = pygame.transform.scale(background_img, size)

# Main loop
while not done:
    # --- Event processing ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the Yes button was clicked
            if yes_button.collidepoint(event.pos):
                example[node.question['property']] = True
                node = node.children[example[node.question['property']]]
            # Check if the No button was clicked
            elif no_button.collidepoint(event.pos):
                example[node.question['property']] = False
                node = node.children[example[node.question['property']]]
        elif event.type == pygame.KEYDOWN:
            # Check if 'r' key is pressed to restart the game
            if event.key == pygame.K_r:
                example = {}
                node =  build_decision_tree(data, questions)
                show = True

    # --- Game logic ---
    if not node.question:
        #print("Prediction:", node.character)
        question_text = font.render('Your character is '+node.character , True, fontques)
        screen.blit(question_text, [200, 100])
        show = False
    else:
        # Draw the question text
        question_text = font.render(question.format(node.question['property']), True, fontques)
        screen.blit(question_text, [200, 100])

        # Draw the Yes button
        pygame.draw.rect(screen, (0, 128, 0), yes_button)
        screen.blit(yes_text, (yes_button.x + 20, yes_button.y + 15))

        # Draw the No button
        pygame.draw.rect(screen, (255, 0, 0), no_button)
        screen.blit(no_text, (no_button.x + 20, no_button.y + 15))

    # --- Update the screen ---
    pygame.display.flip()

    # --- Limit to 60 frames per second ---
    clock.tick(60)

    # --- Drawing ---
    screen.fill(bg)
    # Draw the background image
    screen.blit(background_img, (0, 0))
   

# Close the window and quit.
pygame.quit()
