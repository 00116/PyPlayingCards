import cards_system
import player
import poker_winner

# 5カードドローポーカーの進行を行うクラス
class FiveCardDraw:
    # number_of_playersは1~9, number_of_cardsは52以上, turnsは1以上を想定
    def __init__(self, number_of_players = 8, number_of_cards = 53, turns = 1):
        self.number_of_players = number_of_players
        self.number_of_cards = number_of_cards
        self.turns = turns

        self.table = cards_system.Table(self.number_of_cards, ace14=True)
        self.winner = poker_winner.PokerWinner()
        self.player = []
        for i in range(self.number_of_players):
            self.player.append(player.Player())
            self.player[i].name = 'player' + str(i + 1)

    # ゲーム開始時の処理
    def deal(self):
        self.table.deck_initialize()
        for i in range(self.number_of_players):
            for j in range(5):
                self.player[i].draw(self.table.deck)
    
    # 1ターンにおける処理
    def one_turn(self):
        for i in range(self.number_of_players):    
            # 山札が10枚未満になったときの処理
            if len(self.table.deck) < 10:
                self.table.discard_return_deck()
                
            print(self.player[i].name)
            self.player[i].number_sort(reverse = True)
            print([self.player[i].hand[j].str for j in range(len(self.player[i].hand))])

            # 捨て札選択、ドローの処理
            throwcard, drawcard = self.player[i].five_card_draw_throw(self.table.deck, self.table.discard)
            print('throw in ', end='')
            print([throwcard[j].str for j in range(len(throwcard))])
            print('draw ', end='')
            print([drawcard[j].str for j in range(len(drawcard))])
    
    # ゲーム全体の進行
    def game(self):
        rank = [''] * self.number_of_players
        cardpower = [0] * self.number_of_players

        self.deal()

        for i in range(self.turns):
            self.one_turn()

            # 最終ターンが終了した際の処理
            if i == self.turns - 1:
                for i in range(self.number_of_players):
                    rank[i], cardpower[i] = self.player[i].poker_rank()
                    print(self.player[i].name + ' ' + rank[i])
                    print([self.player[i].hand[j].str for j in range(len(self.player[i].hand))])
                print('winner ' + self.player[self.winner.poker_winner(cardpower)].name)

'''
class TexasHoldem:
    def __init__(self):
        self.number_of_players = 4
        self.number_of_cards = 52
        self.turns = 50
        self.player = []
        for i in range(self.number_of_players):
            self.player.append(cards.Player())
            self.player[i].name = 'player' + str(i + 1)
        self.table = cards.Table(self.number_of_cards)

    def deal(self):
        self.table.shuffle()
        for i in range(2):
            for j in range(self.number_of_players):
                self.player[j].draw(self.table.deck)
        self.table.community.extend(self.table.deck[0:3])
        del self.table.deck[0:3]

    def one_turn(self):
        for i in range(self.number_of_players + 1):
            if len(self.table.deck) < self.number_of_players:
                self.table.deck.extend(self.table.discard)
                self.table.discard = []
                random.shuffle(self.table.deck)
        self.table.community.append(self.table.deck[0])
        del self.table.deck[0]
        for i in range(self.number_of_players + 1):

            print(self.player[i].name)
            self.player[i].sort_cards()
            print([self.player[i].hand[j].str for j in range(len(self.player[i].hand))])
            drawcard = self.player[i].draw(self.table.deck)
            print('draw ', end='')
            print([drawcard[j].str for j in range(len(drawcard))])
    
    def game(self):
        self.deal()
        rank = [0] * self.number_of_players
        rank_str = [0] * self.number_of_players
        cardpower = [0] * self.number_of_players
        for i in range(self.turns):
            self.one_turn()
            if i == self.turns - 1:
                for i in range(self.number_of_players):
                    self.player[i].hand, rank[i], rank_str[i], cardpower[i] = rule.poker_rank(self.player[i].hand)
                winner, judge = rule.poker_winner(rank, cardpower)
                for i in range(self.number_of_players):
                    print(self.player[i].name + ' ' + rank_str[i])
                    print([self.player[i].hand[j].str for j in range(len(self.player[i].hand))])
                if len(judge):
                    print('card power judge')
                    print(judge)
                for i in winner:
                    print('winner ' + self.player[i].name)
'''
