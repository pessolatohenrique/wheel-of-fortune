import random
import time
import string


# realiza a leitura de arquivo, com a lista de palavras
def read_file():
    list_data = []
    file = open('words.txt', 'r')
    for word in file:
        list_data.append(word.strip().upper())
    file.close()
    return list_data


# realiza o sorteio da palavra
def raffle():
    list_data = read_file()
    index = random.randrange(0, len(list_data))
    choose = list_data[index].partition('*')
    choose_object = {"name": choose[0], "category": choose[2]}

    return choose_object


# mascara uma palavra, de modo a deixá-la "jogável"
def mascarate_word(word):
    mascareted = []
    for letter in word:
        if (letter == " "):
            mascareted.append('*')
        else:
            mascareted.append('_')
    return mascareted


# escolhe o valor a ser aplicado na roleta
def choose_score():
    score_list = [1000, 500, 300, 250, 100, 'lost', 400, 500, 'pass', 800]
    index = random.randrange(0,len(score_list))
    score = score_list[index]

    if (isinstance(score, int)):
        print("Valendo {} pontos".format(score))

    return score


# sorteia aleatoriamente a letra escolhida pelo
# adversário (computador)
def choose_guess_adversary():
    return random.choice(string.ascii_letters.upper())


def choose_guess_user():
    return input("Digite a letra: ").strip().upper()


def verify_pass(score):
    flag = False
    if (score == "pass"):
        print("***Passou a vez!***")
        flag = True

    return flag


def verify_loose_all(score):
    flag = False
    if (score == "lost"):
        print("***Perdeu tudo!***")
        flag = True
    return flag


# realiza a contagem de acertos em uma palavra
def verify_hits(letter, word):
    return word.count(letter.strip().upper())


# calcula o total de pontos acumulados
# de acordo com total de acertos e pontos da roleta
def calculate_hits(total_hits, score):
    total = 0
    if (isinstance(score, int)):
        total = int(total_hits) * int(score)
    return total


# acumula a pontuação
def accumulate_score(previous, score):
    new_score = previous + score
    return new_score


# realiza o merge da palavra "mascarada" com a real
def merge_word(letter_guess, word_mascareted, word):
    index = 0
    for letter in word:
        if (letter_guess == letter):
            word_mascareted[index] = letter
        index = index + 1
    return word_mascareted


def clear_scoreboard(user_round, scoreboard):
    if (user_round):
        scoreboard['user'] = 0
    else:
        scoreboard['computer'] = 0
    return scoreboard


# mostra o palcar geral
def show_scoreboard(scoreboard):
    print("******PLACAR******")
    print("Usuário: {} VS. Computador: {}".format(scoreboard['user'], scoreboard['computer']))
    print("******************")


# calcula quantas letras restam para o jogo finalizar
def verify_remaining(word):
    return word.count("_")


raffled = raffle()
category = raffled['category']
word = raffled['name']
word_mascarated = mascarate_word(word)
finished = False
user_round = True
user_guess = ''
scoreboard = {"user": 0, "computer": 0}
choosed_letters = []
print("A dica é {}".format(category))
print("O formato da palavra é {}".format(word_mascarated))

while (not finished):
    if(verify_remaining(word_mascarated) == 0):
        finished = True
        break

    print('Rodando a roleta...')
    time.sleep(2)
    score = choose_score()

    if (verify_pass(score)):
        user_round = not user_round
        continue

    if (verify_loose_all(score)):
        scoreboard = clear_scoreboard(user_round, scoreboard)
        user_round = not user_round
        continue

    if (user_round):
        user_guess = choose_guess_user()
        if (user_guess in choosed_letters):
            print("***Poxa, essa letra já foi. Passou a vez!***")
            user_round = not user_round
            continue
        choosed_letters.append(user_guess)

        word_mascarated = merge_word(user_guess, word_mascarated, word)
        total_hits = verify_hits(user_guess, word)
        score_hits = calculate_hits(total_hits, score)
        scoreboard['user'] = accumulate_score(scoreboard['user'], score_hits)
        time.sleep(2)
        print("***Situação da palavra: {} ***".format(word_mascarated))
        print("***Você acertou {} letras e ganhou {} pontos***".format(total_hits,score_hits))
        show_scoreboard(scoreboard)
        time.sleep(2)

        if (total_hits == 0): user_round = False
    else:
        guess_adversary = choose_guess_adversary()
        if (guess_adversary in choosed_letters):
            print("***Poxa, essa letra já foi. Passou a vez!***")
            user_round = not user_round
            continue
        choosed_letters.append(user_guess)
        word_mascarated = merge_word(guess_adversary, word_mascarated, word)
        print("O adversário chutou a letra: {}".format(guess_adversary))
        total_hits = verify_hits(guess_adversary, word)
        score_hits = calculate_hits(total_hits, score)
        scoreboard['computer'] = accumulate_score(scoreboard['computer'], score_hits)
        print("***Situação da palavra: {} ***".format(word_mascarated))
        print("***O ADVERSÁRIO acertou {} letras e ganhou {} pontos***".format(total_hits,score_hits))
        show_scoreboard(scoreboard)
        time.sleep(2)

        if (total_hits == 0): user_round = True