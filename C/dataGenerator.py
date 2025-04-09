from faker import Faker
fake = Faker()

def generateTodo():
    return {
        "title": fake.sentence(nb_words=3),
        "doneStatus": False,
        "description": fake.text(max_nb_chars=50)
    }
