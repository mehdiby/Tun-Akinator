import math
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


if __name__ == '__main__':
    print("Welcome to the tun Akinator game!")
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
    while node.question:
        answer = input(f"Is the character a {node.question['property']} (y/n): ")
        example[node.question['property']] = True if answer.lower() == 'y' else False
        node = node.children[example[node.question['property']]]
    print("Prediction:", node.character)