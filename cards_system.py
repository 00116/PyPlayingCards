import random

# カードの数字, マーク, 表示用の文字列を管理するクラス
# allnumber=0~51が1~13のカード4種類ずつ, 52~はjokerを表す
# 標準で数字は1~13, マークは1~4(順にspade, heart, diamond, clubを想定)
# jokerは数字マークともに0
# ace14, two15をTrueにするとAと2の数字がそれぞれ14, 15扱いとなる
class Card:
    def __init__(self, allnumber, ace14 = False, two15 = False):
        if allnumber >= 52:
            self.number = 0
            self.suit = 0
            self.str = 'joker'
        else:
            self.number = allnumber % 13 + 1
            self.suit =  allnumber // 13 + 1
            if self.suit == 1:
                self.str =  'spade ' + str(self.number)
            elif self.suit == 2:
                self.str = 'heart ' + str(self.number)
            elif self.suit == 3:
                self.str = 'daimond ' + str(self.number)
            elif self.suit == 4:
                self.str = 'club ' + str(self.number)

            if ace14 and self.number == 1:
                self.number = 14
            elif two15 and self.number == 2:
                self.number = 15

# 全カードリスト, 山札, 捨て札の管理
# 山札のシャッフル, 山札の初期化, 捨て札を山札に戻す処理を行うクラス
class Table:
    def __init__(self, number_of_cards, ace14 = False, two15 = False):
        self.card = [Card(i, ace14, two15) for i in range(number_of_cards)]
        self.deck = []
        self.community = []
        self.discard = []

    # 山札のシャッフル
    def shuffle(self):
        self.deck = list(self.deck)
        random.shuffle(self.deck)

    # 山札の初期化
    def deck_initialize(self):
        self.deck = list(self.card)
        random.shuffle(self.deck)

    # 捨て札を山札に戻してシャッフルする
    def discard_return_deck(self):
        self.deck.extend(self.discard)
        self.discard = []
        self.shuffle()
'''
class Player:
    def __init__(self):
        self.hand = []
        self.name = ''

        self.fivedraw = poker_select.FivecardSelect()

    def number_sort(self, reverse = False):
        if reverse:
            self.hand.sort(reverse = True, key = lambda h: h.number)
        else:
            self.hand.sort(key = lambda h: h.number)

    def suit_sort(self):
        self.hand.sort(key = lambda h: h.suit)

    def draw(self, deck):
        draw_card = deck[0]
        self.hand.append(deck[0])
        del deck[0]
        return draw_card

    def throw(self, throw_number, discard):
        throw_card = self.hand[throw_number]
        discard.append(self.hand[throw_number])
        del self.hand[throw_number]
        return throw_card

    def five_card_draw_throw(self, deck, discard):
        throw_num = self.fivedraw.throw_card_choice(self.hand)
        throw_cards = []
        draw_cards = []
        for i in throw_num:
            throw_cards.append(self.throw(i, discard))
            draw_cards.append(self.draw(deck))
        return throw_cards, draw_cards

    #def five_card_draw_throw_algorithm(self, discard):
    #    # 捨てるカードの選択を行う
    #    # 今は5番目のカードを選択
    #    throw_card = []
    #    fixed_hand, rank, rank_str, card_power = poker_system.poker_rank(self.hand)
    #    self.hand = fixed_hand
    #    # ストレート以上確定で何も切らない
    #    if rank > 3:
    #        return []
    #    # スリーカードのときは他の2枚を切る
    #    elif rank == 3:
    #        for i in range(2):
    #            throw_card.append(self.throw(3, discard))
    #        return throw_card
    #    # ツーペアのときは残り1枚を切る
    #    elif rank == 2:
    #        throw_card.append(self.throw(4, discard))
    #        return throw_card
    #    # ワンペアのときは残り3枚を切る
    #    elif rank == 1:
    #        for i in range(3):
    #            throw_card.append(self.throw(2, discard))
    #        return throw_card
    #    # ブタのときはランダムに1~5枚、数字の小さい物から順に捨てる
    #    else:
    #        random_number = random.randint(1, 5)
    #        for i in range(random_number):
    #            throw_card.append(self.throw(5 - random_number, discard))
    #        return throw_card
            
        #throw_card_number = 4
        #throw_card = self.throw(throw_card_number)
        #return throw_card
'''