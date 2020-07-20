import random

# настройки  колоды
masti = ['пики', 'трефы', 'бубны', 'черви']
posledovatelnost = ['2','3','4','5','6','7','8','9','10','валет','дама','король','туз']
ves = {'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'валет':10,'дама':10,'король':10,'туз':11}

def replay():
    ans = input('\nЕще раз? Да(y) или Нет(n)')
    return ans.lower().startswith('y')

class Card:
    def __init__(self, mast, velichina):
        self.mast = mast
        self.velichina = velichina
        self.ochki = ves[self.velichina]

    def __str__(self):
        return self.mast + ' | ' + self.velichina

class Deck:

    def __init__(self, pointer=0):
        self.deck = []
        self.pointer = pointer
        for i in masti:
            for j in posledovatelnost:
                mycard = Card(i, j)
                self.deck.append(mycard)

    def __str__(self):
        koloda = ''
        for card in self.deck:
            koloda += '\n ' + card.__str__()
        return koloda

    def shuffle(self):
        random.shuffle(self.deck)

    def get_next(self):
        self.pointer += 1
        return self.deck[self.pointer - 1]

    def pervie_dve(self):
        koloda = ''
        counter = 0
        for card in self.deck:
            if counter <= 1:
                koloda += '\n ' + card.__str__()
                counter+=1
            else:
                break
        return koloda

class Gamer:
    def __init__(self, name='', coins=0, score=0, hand=[]):
        self.name = name
        self.coins = coins
        self.hand = hand
        self.score = score

    def plus_bet(self, amount):
        self.coins += amount

    def minus_bet(self, amount):
        self.coins -= amount

    def check_bet(self, amount):
        if (self.coins - amount >= 0):
            return True
        else:
            return False

    def __str__(self):
        return 'Игрок ' + self.name + ' имеет ' + str(self.coins) + ' фишек'

    def take_card(self, card):
        self.hand.append(card)

    def update_score(self):
        score = 0
        for card in self.hand:
            score += card.ochki
        self.score = score

    def est_li_tuz(self):
        hand_values = []
        for card in self.hand:
            hand_values.append(card.velichina)
        if 'туз' in hand_values:
            return True
        else:
            return False



    def tuz_za_1(self):
        self.score-=10

    def show_hand(self):
        for i in self.hand:
            print(i, '=', i.ochki, 'очков')

    def null_hand(self):
        self.hand = []


class Dealer():
    def __init__(self, score=0, hand=[]):
        self.hand = hand
        self.score = score

    def __str__(self):
        return 'Дилер имеет ' + str(self.coins) + ' фишек'

    def take_card(self, card):
        self.hand.append(card)

    def update_score(self):
        score = 0
        for card in self.hand:
            score += card.ochki
        self.score = score

    def est_li_tuz(self):
        pass

    def show_hand(self):
        for i in self.hand:
            print(i, '=', i.ochki, 'очков')

    def null_hand(self):
        self.hand = []


'''
создаем игрока и крупье
'''
print('Добро пожаловать в игру Black Jack ! \n')
user_name = input('Как вас зовут? \n')
user_coins = int(input('Сколько денег в банк? \n'))
user = Gamer(user_name, user_coins)
dealer = Dealer()

play_game = input('Играем? Да(y) или Нет(n) ')
if play_game.lower().startswith('y'):
    game_on = True
else:
    game_on = False
    print('До свидания!')

while True:
    while game_on:
        # создаем колоду карт
        print('||| Тасуем колоду |||')
        koloda = Deck()
        koloda.shuffle()
        '''
        print(koloda.pervie_dve())  
        while input('перетасуем?').lower().startswith('y'):
            koloda.shuffle()
            print(koloda.pervie_dve())
        '''

        #раздача пользователю
        print('2 карты игроку!')
        # обнуляем руку игрока
        user.hand = []
        # сдаем две карты
        for _ in range(2):
            next_card = koloda.get_next()
            user.take_card(next_card)

        #раздача дилеру
        print('2 карты крупье!')
        # обнуляем руку крупье
        dealer.hand = []
        # сдаем две карты дилеру
        for _ in range(2):
            next_card = koloda.get_next()
            dealer.take_card(next_card)

        # принимаем ставку
        print('')
        print('{} '.format(user.name))
        user_bet = int(input('какова ваша ставка? \n'))

        if user.check_bet(user_bet):
            print('\nПринято {} монет в качестве ставки \n'.format(user_bet))
        else:
            print('\nВы не можете поставить {}. У вас есть только {} \n'.format(user_bet, user.coins))

        # показываем карты игрока
        print('У вас {} на руках: \n'.format(user.name))
        for i in user.hand:
            print(i,'=', i.ochki,'очков')
        user.update_score()
        print('это {} очков \n'.format(user.score))

        # показываем карты дилера
        print('У крупье на руках:')
        i = dealer.hand[0]
        print(i,'=', i.ochki,'очков')
        print('еще карта на xxx очков')

        # Начальный вопрос. Спрашиваем игрока после раздачи, нужна ли ему карта и если да, то даем
        one_more_card = input('Еще карту? Да(y) или Нет(n)')
        if one_more_card.lower().startswith('y'):
            next_card = koloda.get_next()
            user.take_card(next_card)
            # печатаем колоду
            print('\nУ вас {} на руках: \n'.format(user.name))
            for i in user.hand:
                print(i,'=', i.ochki,'очков')
            user.update_score()
            print('\nэто {} очков'.format(user.score))
        else:
            print('\n{}, у вас {} очков '.format(user.name, user.score))

        if user.score > 21:
            if user.est_li_tuz():
                user.tuz_za_1()
            else:
                print('Перебор! У вас {} очко. Вы проиграли'.format(user.score))
                user.minus_bet(user_bet)
                print('Ваша ставка {} уходит в банк! У вас осталось {} монет'.format(user_bet, user.coins))
                break
        elif user.score == 21:
            print('Bingo! У вас {} очко. Вы выиграли'.format(user.score))
            user.plus_bet(user_bet)
            print('Ваша ставка {} удваивается! У вас теперь {} монет '.format(user_bet, user.coins))
            break

        '''
        тут пошел основной цикл раунда
        '''
        # ходы игрока
        while user.score < 21:

            reply = input('Еще карту? Yes\y or No\n')
            if reply.lower().startswith('y'):
                # получаем карту
                next_card = koloda.get_next()
                user.take_card(next_card)
                user.update_score()

                # печатаем руку
                print('У вас {} на руках: \n'.format(user.name))
                user.show_hand()
                print('\nэто {} очков'.format(user.score))

                # проверка, что получилось
                if user.score > 21:
                    if user.est_li_tuz():
                        user.tuz_za_1()
                        if user.score > 21:
                            print('вы проиграли. у вас {} очков с учетом туза'.format(user.score))
                            user.minus_bet(user_bet)
                            print('Ваша ставка {} уходит в банк! У вас осталось {} монет'.format(user_bet, user.coins))
                            natural_user_stop = True
                            break
                        else:
                            continue
                    else:
                        print('Перебор! У вас {} очко. Вы проиграли'.format(user.score))
                        user.minus_bet(user_bet)
                        print('Ваша ставка {} уходит в банк! У вас осталось {} монет'.format(user_bet, user.coins))
                        natural_user_stop = True
                        break
                elif user.score == 21:
                    print('Bingo! У вас {} очко. Вы выиграли'.format(user.score))
                    user.plus_bet(user_bet)
                    print('Ваша ставка {} удваивается! У вас теперь {} монет '.format(user_bet, user.coins))
                    natural_user_stop = True
                    break
                elif user.score < 21:
                    natural_user_stop = False
                    break
            else:
                print('\nПередаю ход крупье')
                natural_user_stop = False
                break

        if not natural_user_stop:
        # показываем карты дилера
            dealer.show_hand()
            dealer.update_score()
            print('\nУ крупье {} очков'.format(dealer.score))

        # ходы крупье из двух карт
            if dealer.score >= 17:
                print('у крупье {} очков, а у {} {} очков'.format(dealer.score, user.name, user.score))
                if dealer.score >= user.score:
                    print('выиграло казино! {} проиграл {} монет'.format(user.name, user_bet))
                    user.minus_bet(user_bet)
                    print('\n{} у вас теперь {} монет '.format(user.name, user.coins))
                else:
                    print('Казино проиграло! Выиграл {}'.format(user.name))
                    user.plus_bet(user_bet)
                    print('\n{} у вас теперь {} монет '.format(user.name, user.coins))
                    break

            # крупье добирает карты
            while dealer.score < 17:
                # получаем карту
                next_card = koloda.get_next()
                dealer.take_card(next_card)
                dealer.update_score()

            # печатаем руку
            print('У крупье на руках: \n')
            dealer.show_hand()
            print('\nэто {} очков'.format(dealer.score))

            # проверка, что получилось
            if dealer.score > 21:
                print('Перебор! Казино проиграло! Выиграл {}'.format(user.name))
                user.plus_bet(user_bet)
                print('\n{} у вас теперь {} монет '.format(user.name, user.coins))
                break
            elif dealer.score == 21:
                print('выиграло казино! {} проиграл {} монет'.format(user.name, user_bet))
                user.minus_bet(user_bet)
                print('\n{} у вас теперь {} монет '.format(user.name, user.coins))
                break
            else:
                print('у крупье {} очков, а у {} {} очков'.format(dealer.score, user.name, user.score))
                if dealer.score >= user.score:
                    print('выиграло казино! {} проиграл {} монет'.format(user.name, user_bet))
                    user.minus_bet(user_bet)
                    print('\n{} у вас теперь {} монет '.format(user.name, user.coins))
                else:
                    print('Казино проиграло! Выиграл {}'.format(user.name))
                    user.plus_bet(user_bet)
                    print('\n{} у вас теперь {} монет '.format(user.name, user.coins))
                break

    if not replay():
        break
    else:
        game_on = True