import poker_rank
import random

# 5カードドローポーカーにおける捨て札選択を行うクラス
class FiveCardChoice:
    def throw_card_choice(self, hand):
        prank = poker_rank.PokerRank()
        throw_card = []
        rank_str, cardpower = prank.poker_rank(hand)
        hand = prank.rank_sort(hand, cardpower)
        rank = cardpower[0]

        # ストレート以上確定で何も切らない
        if rank > 3:
            throw_card = []
        # スリーカードのときは他の2枚を切る
        elif rank == 3:
            throw_card = [3, 3]
        
        # ツーペアのときは残り1枚を切る
        elif rank == 2:
            throw_card = [4]
        
        # ワンペアのときは残り3枚を切る
        elif rank == 1:
            throw_card = [2, 2, 2]
        
        # ブタのときはランダムに1~5枚、数字の小さい物から順に捨てる
        else:
            random_number = random.randint(1, 5)
            for i in range(random_number):
                throw_card.append(5 - random_number)
        
        return hand, throw_card

# 手札とプレイヤー名の管理
# 手札のソート, ドロー, 捨て札選択, 手札の役確認の処理を行うクラス
class Player:
    def __init__(self):
        self.hand = []
        self.name = ''

        self.fivedraw = FiveCardChoice()
        self.prank = poker_rank.PokerRank()

    # カードを数字でソートする 標準では小さい順
    def number_sort(self, reverse = False):
        if reverse:
            self.hand.sort(reverse = True, key = lambda h: h.number)
        else:
            self.hand.sort(key = lambda h: h.number)

    # カードをマークでソートする
    def suit_sort(self):
        self.hand.sort(key = lambda h: h.suit)

    # カードをdeckの0から1枚だけドローする
    def draw(self, deck):
        draw_card = deck[0]
        self.hand.append(deck[0])
        del deck[0]
        return draw_card

    # カードを捨てる
    def throw(self, throw_number, discard):
        throw_card = self.hand[throw_number]
        discard.append(self.hand[throw_number])
        del self.hand[throw_number]
        return throw_card

    # 5カードドローポーカーにおける捨て札選択、ドローの一連の処理を行う
    def five_card_draw_throw(self, deck, discard):
        self.hand, throw_num = self.fivedraw.throw_card_choice(self.hand)
        throw_cards = []
        draw_cards = []
        for i in throw_num:
            throw_cards.append(self.throw(i, discard))
            draw_cards.append(self.draw(deck))
        return throw_cards, draw_cards

    # 手札の役を取得する
    def poker_rank(self):
        rank, cardpower = self.prank.poker_rank(self.hand)
        self.hand = self.prank.rank_sort(self.hand, cardpower)
        return rank, cardpower

        #throw_card_number = 4
        #throw_card = self.throw(throw_card_number)
        