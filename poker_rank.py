#from operator import attrgetter
#import itertools

# ポーカーの役判定, 役ベースでの手札のソートを行うクラス
class PokerRank:
    # ポーカーの役判定を行う(handが5枚のとき専用)
    def poker_rank(self, hand):
        flush = False
        straight = False

        # rankは上がり役の文字列(表示用)
        # cardpowerは[0]が役の強さ[1]以降は役が同じときの比較用
        rank = ''
        cardpower = []

        numlist = [0 for i in range(15)]
        suitlist = [0 for i in range(5)]

        len_numlist = len(numlist)

        # 4枚以下の時の処理用(未実装)
        len_hand = len(hand)

        for i in range(len_hand):
            numlist[hand[i].number] += 1
            suitlist[hand[i].suit] += 1
        
        # フラッシュの判定
        if max(suitlist) + suitlist[0] == 5:
            flush = True

        straight_numlist = list(numlist)

        # ストレートの判定
        for i in range(2,11):
            if straight_numlist[i] == 1:
                for j in range(4):
                    if straight_numlist[i + j + 1] == 0:
                        if straight_numlist[0] >= 1:
                            straight_numlist[i + j + 1] += 1
                            straight_numlist[0] -= 1
                        else:
                            break
                    if j + 1 == 4:
                        straight_number = i + j + 1
                        straight = True
                break
        
        # ジョーカーを何のカードとして扱うか決定する
        number_of_joker = numlist[0]
        numlist[0] = 0
        if number_of_joker > 0:
            # 前者がスリーカードとフォーカード、後者がワンペアの条件
            if max(numlist) >= 3 or numlist.count(2) == 1:
                numlist[numlist.index(max(numlist))] += number_of_joker
            # ブタとツーペアの時は最も大きい数に重ねる
            else:
                for i in range(len_numlist):
                    if numlist[len_numlist - i - 1] > 0:
                        numlist[len_numlist - i - 1] += number_of_joker
                        break

        # ファイブカードの判定
        if 5 in numlist:
            rank = 'five of a kind'
            cardpower.append(10)
            cardpower.append(numlist.index(5))

        # ストレートフラッシュの判定
        elif flush and straight:
            # ロイヤルストレートフラッシュの判定
            if numlist[14] == 1:
                rank = 'royal flush'
                cardpower.append(9)

            # 普通のストレートフラッシュの判定
            else:
                rank = 'straight flush'
                cardpower.append(8)
                cardpower.append(straight_number)

        # フォーカードの判定
        elif 4 in numlist:
            rank = 'four of a kind'
            cardpower.append(7)
            cardpower.append(numlist.index(4))
            cardpower.append(numlist.index(1))

        # フルハウスの判定
        elif 3 in numlist and 2 in numlist:
            rank = 'full house'
            cardpower.append(6)
            cardpower.append(numlist.index(3))
            cardpower.append(numlist.index(2))

        # フラッシュの判定
        elif flush:
            rank = 'flush'
            cardpower.append(5)
            for i in range(len_numlist):
                # ジョーカー入りのときはジョーカーをAとみなす
                temp = len_numlist - i - 1
                if numlist[temp] > 1:
                    for j in range(numlist[temp] - 1):
                        cardpower.append(14)
                    cardpower.append(temp)
                elif numlist[temp] == 1:
                    cardpower.append(temp)

        # ストレートの判定
        elif straight:
            rank = 'straight'
            cardpower.append(4)
            cardpower.append(straight_number)

        # スリーカードの判定
        elif 3 in numlist:
            rank = 'three of a kind'
            cardpower.append(3)
            cardpower.append(numlist.index(3))
            for i in range(len_numlist):
                temp = len_numlist - i - 1
                if numlist[temp] == 1:
                    cardpower.append(temp)

        # ツーペアの判定
        elif numlist.count(2) == 2:
            rank = 'two pair'
            cardpower.append(2)
            for i in range(len_numlist):
                temp = len_numlist - i - 1
                if numlist[temp] == 2:
                    cardpower.append(temp)
            for i in range(len_numlist):
                temp = len_numlist - i - 1
                if numlist[temp] == 1:
                    cardpower.append(temp)

        # ワンペアの判定
        elif 2 in numlist:
            rank = 'a pair'
            cardpower.append(1)
            cardpower.append(numlist.index(2))
            for i in range(len_numlist):
                temp = len_numlist - i - 1
                if numlist[temp] == 1:
                    cardpower.append(temp)

        # ブタのとき
        else:
            rank = 'high card'
            cardpower.append(0)
            for i in range(len_numlist):
                temp = len_numlist - i - 1
                if numlist[temp] == 1:
                    cardpower.append(temp)

        for i in range(6-len(cardpower)):
            cardpower.append(0)

        return rank, cardpower

    # カードを役ベースでソートする
    def rank_sort(self, hand, cardpower):
        expect_joker_hand = []
        sorted_hand = []
        for card in hand:
            if card.number == 0:
                sorted_hand.append(card)
            else:
                expect_joker_hand.append(card)

        expect_joker_hand.sort(reverse = True, key = lambda h: h.number)

        if cardpower[0] == 0:
            sorted_hand.extend(expect_joker_hand)
        elif cardpower[0] == 1:
            for i in range(4):
                for card in expect_joker_hand:
                    if card.number == cardpower[i + 1]:
                        sorted_hand.append(card)
        elif cardpower[0] == 2 or cardpower[0] == 3:
            for i in range(3):
                for card in expect_joker_hand:
                    if card.number == cardpower[i + 1]:
                        sorted_hand.append(card)
        elif cardpower[0] == 4 or cardpower[0] == 5:
            sorted_hand.extend(expect_joker_hand)
        elif cardpower[0] == 6 or cardpower[0] == 7:
            for i in range(2):
                for card in expect_joker_hand:
                    if card.number == cardpower[i + 1]:
                        sorted_hand.append(card)
        elif cardpower[0] >= 8:
            sorted_hand.extend(expect_joker_hand)

        return sorted_hand
     
    '''        
    def poker_winner(self, cardpower):
        converted_cardpower = [list(x) for x in zip(*cardpower)]
        max_rank = max(converted_cardpower[0])
        if converted_cardpower[0].count(max_rank) == 1:
            winner = converted_cardpower[0].index(max_rank)
            return winner
        else:
            for i in range(len(converted_cardpower[0])):
                if converted_cardpower[0][i] != max_rank:
                    cardpower[i] = [0, 0, 0, 0, 0, 0]
        converted_cardpower = [list(x) for x in zip(*cardpower)]

        for i in range(1, len(converted_cardpower)):
            if converted_cardpower[i].count(max(converted_cardpower[i])) == 1:
                winner = converted_cardpower[i].index(max(converted_cardpower[i]))
                return winner
    '''

        

# class PokerWinner:
#     def __init__(self, cardpower_list):
#         converted_cardpower = [list(x) for x in zip(*cardpower_list)]
#         for i in range(len(converted_cardpower)):
#             if converted_cardpower[i].count(max(converted_cardpower[i])) == 1:
#                 winner = converted_cardpower[i].index(max(converted_cardpower[i]))
#                 return winner


"""
class PokerRuleOverSixHand:

    # フラッシュの判定
    def judge_flush(self, hand, suitlist):
        flush_hand = []
        max_suit = max(suitlist)
        if max_suit >= 5:
            for i in range(len(hand)):
                if hand[i].suit == max_suit:
                    flush_hand.append(hand[i])

            # ストレートフラッシュの検出用
            # flush_numlist = [0 for i in range(15)]
            # for i in range(len(flush_numlist)):
            #     if flush_hand[i].number == 1:
            #         flush_numlist[14] += 1
            #     else:
            #         flush_numlist[flush_hand[i].number] += 1

        return flush_hand

    def judge_straight(self, hand, numlist):
        # numlist = numlist = [0 for i in range(15)]
        # for i in range(len_numlist):
        #     if hand[i].number == 1:
        #         numlist[14] += 1
        #     else:
        #         numlist[hand[i].number] += 1
        straight_hand = []
        straight_numlist_idx = []
        #sorted_hand = sorted(hand, key=attrgetter('number'))
        #flag = 0

        # for i in range(len(sorted_hand) - 1):
        #     if sorted_hand[i+1].number - sorted_hand[i].number <= 1:
        #         flag += 1
        #     if flag == 4:
        #         for j in range(flag + 1):
        #             straight_hand.append(i + 1 - j)
        #     if sorted_hand[i+1].number - sorted_hand[i].number > 1:
        #         flag = 0
        for i in range(11):
            if numlist[i] > 0:
                for j in range(4):
                    if numlist[i + j + 1] == 0:
                        break
                    elif j + 1 == 4:
                        #straight = True
                        #straight_number = 14 - i
                        straight_numlist_idx.append([i+k for k in range(5)])

        straight_numlist = list(numlist)
        for i in range(len_numlist):
            if not i in list(itertools.chain.from_iterable(straight_numlist_idx)):
                straight_numlist[i] = 0
        straight_hand_list = []
        for i in range(len(straight_numlist_idx)):
            for j in range(len(straight_numlist_idx[i])):
                for k in range(len(hand)):
                    if hand[k].number == straight_numlist_idx[i][j]:
                        straight_hand.append(hand[k])
            straight_hand_list.append(straight_hand)

            #for j in range(5):

                #if max(numlist[straight_numlist_idx[i][j]]) > 1:


        #for i in range(len(hand)):
        #    if hand[i].number in straight_numlist:
        #        straight_hand.append(hand[i])
        return straight_hand

    # def judge_straight_flush(self, flush_hand, straight_hand):
    #     for straight_card in straight_hand:
    #         if flush_card in straight_hand

    # handの要素数は5～7枚を想定
    # 10枚以上で2組フラッシュ、ストレートが発生した場合、
    # 8枚以上で2組フォーカードが発生した場合に正常動作しないことが考えられる
    def poker_rank(self, hand):
        flush = False
        straight = False

        hand_rank = ''
        hand_cardpower = []
        suitlist = [0 for i in range(5)]
        numlist = [0 for i in range(15)]

        hand_result = []
        flush_hand = list(hand.sort(key=attrgetter('suit')))
        straight_hand = list(hand.sort(key=attrgetter('number')))

        for i in range(len_numlist):
            if hand[i].number == 1:
                numlist[14] += 1
            else:
                numlist[hand[i].number] += 1
            suitlist[hand[i].suit] += 1

        flush_hand = self.judge_flush(hand)
        straight_hand = self.judge_straight(hand, numlist)
        if len(flush_hand) >= 5 and len(straight_hand) >= 5:
            straight_flush_hand = self.judge_flush(straight_hand)
        else:
            straight_flush_hand = []

        if numlist[0] > 0:
            numlist[numlist.index(max(numlist))] += numlist[0]
            numlist[0] = 0

        # ファイブカードの判定
        if max(numlist) >= 5:
            hand_rank = 'five of a kind'
            hand_result = [hand[i] for i in range(len(hand)) if hand[i].number == numlist.index(max(numlist))]

        # ストレートフラッシュの判定
        elif len(straight_flush_hand) >= 5:
            straight_number = max(straight_flush_hand, key=attrgetter('number')).number

            # ロイヤルストレートフラッシュか判定
            if straight_number == 14:
                hand_rank = 'royal flush'
                hand_cardpower = [9, 14, 13, 12, 11, 10]
                hand_result = straight_flush_hand

            # 普通のストレートフラッシュの場合
            else:
                hand_rank = 'straight flush'
                hand_cardpower.append(8)
                for i in range(5):
                    hand_cardpower.append(straight_number - i)
                hand_result = straight_flush_hand

        # フォーカードの判定
        elif max(numlist) + numlist[0] >= 4:
            hand_rank = 'four of a kind'
            hand_result = [hand[i] for i in range(len(hand)) if hand[i].number == numlist.index(max(numlist))]
            hand_cardpower = [numlist.index(max(numlist)) for i in range(4)]
            for i in range(len(hand)):
                if not hand[len(hand) - 1 - i] in hand_result:
                    hand_result.append(hand[len(hand) - 1 - i])
                    hand_cardpower.append(hand[len(hand) - 1 - i].number)

        # フルハウスの判定
        elif 3 in numlist and 2 in numlist:
            hand_rank = 'full house'

        elif flush:
            hand_rank = 'flush'
            flush_hand.sort

        elif straight:
            hand_rank = 'straight'

        elif 3 in numlist:
            hand_rank = 'three of a kind'

        elif numlist.count(2) >= 2:
            hand_rank = 'two pair'

        elif 2 in numlist:
            hand_rank = 'a pair'

        else:
            hand_rank = 'high card'

        return hand_rank, hand_result


    def poker_rank(hand):

        # 0=ブタ、1=ワンペア、2=ツーペア、3=スリーカード、4=ストレート、5=フラッシュ
        # 6=フルハウス、7=フォーカード、8=ストレートフラッシュ、9=ロイヤルストレートフラッシュ
        rank = 0
        card_power = []
        rank_str = ''
        fixed_hand = []
        # 手札が6枚以上のときも判定できるようにしていた

        flush = False
        straight = False
        straight_flush = False
        straight_number = 0
        straight_flush_number = 0

        suitlist = [0 for i in range(5)]
        numberlist = [0 for i in range(14)]

        for card in hand:
            suitlist[card.suit] += 1
            numberlist[card.number] += 1
        if max(suitlist) >= 5:
            flush = True
            flush_numlist = list(numberlist)
            for card in hand:
                if card.suit != suitlist.index(max(suitlist)):
                    flush_numlist[card.number] = 0
        for i in range(14):
            if numberlist[i] > 0:
                judge_straight_flush = True
                for j in range(4):
                    if i + j + 1 > 13:
                        break
                    if numberlist[i + j + 1] == 0:
                        break
                    elif j == 3:
                        straight = True
                        straight_number = i + j + 1
                    if flush:
                        if flush_numlist[i + j + 1] == 0:
                            judge_straight_flush = False
                            for k in range(j + 1):
                                flush_numlist[k + i] = 0
                        elif j == 3 and judge_straight_flush:
                            straight_flush = True
                            straight_flush_number = i + j + 1

        # indexメソッドで強い順にインデックスを取得するためリストを反転
        numberlist.reverse()

        if straight_flush:
            if straight_flush_number == 13:
                rank = 9
                rank_str = 'royal flush'
                for i in range(5):
                    card_power.append(i)
            else:
                rank = 8
                rank_str = 'straight flush'
                for i in range(5):
                    card_power.append(13 - straight_number + i)

        elif max(numberlist) >= 4:
            rank = 7
            rank_str = 'four of a kind'
            for i in range(4):
                card_power.append(numberlist.index(max(numberlist)))
            temp = list(numberlist)
            temp[temp.index(max(temp))] = 0
            card_power.append(temp.index(max(temp)))
            flush = False

        elif 3 in numberlist and 2 in numberlist:
            rank = 6
            rank_str = 'a full house'
            for i in range(3):
                card_power.append(numberlist.index(3))
            for i in range(2):
                card_power.append(numberlist.index(2))
            flush = False

        elif flush:
            rank = 5
            rank_str = 'flush'
            flush_numlist.reverse()      
            #for i in range(5):
            #    card_power.append(flush_numlist.index(1))
            for i in range(len(flush_numlist)):
                if flush_numlist[i] == 1:
                    card_power.append(i)
                if len(card_power) == 5:
                    break

        elif straight:
            rank = 4
            rank_str = 'straight'
            for i in range(5):
                card_power.append(13 - straight_number + i)

        elif 3 in numberlist:
            rank = 3
            rank_str = 'three of a kind'
            card_power.append(numberlist.index(3))
            card_power.append(numberlist.index(3))
            card_power.append(numberlist.index(3))
            for i in range(len(numberlist)):
                if numberlist[i] == 1:
                    card_power.append(i)
                if len(card_power) == 5:
                    break

        elif numberlist.count(2) == 2:
            rank = 2
            rank_str = 'two pair'
            for i in range(len(numberlist)):
                if numberlist[i] == 2:
                    card_power.append(i)
                    card_power.append(i)
                if len(card_power) == 4:
                    break            
            card_power.append(numberlist.index(1))

        elif 2 in numberlist:
            rank = 1
            rank_str = 'a pair'
            card_power.append(numberlist.index(2))
            card_power.append(numberlist.index(2))
            for i in range(len(numberlist)):
                if numberlist[i] == 1:
                    card_power.append(i)
                if len(card_power) == 5:
                    break
        else:
            rank = 0
            rank_str = 'high card'
            for i in range(len(numberlist)):
                if numberlist[i] == 1:
                    card_power.append(i)
                if len(card_power) == 5:
                    break

        for i in range(len(card_power)):
            card_power[i] = 13 - card_power[i]
            for j in range(len(hand)):
                if hand[j].number == card_power[i] and not hand[j] in fixed_hand:
                    fixed_hand.append(hand[j])
                    break
        return fixed_hand, rank, rank_str, card_power

    def poker_winner(rank, cardpower):
        winner = []
        card_power_judge = []

        if rank.count(max(rank)) == 1:
            winner.append(rank.index(max(rank)))
            return winner, card_power_judge
        else:
            player_rank_idx = []
            cardpower_tie = []
            for j in range(len(rank)):
                if rank[j] == max(rank):
                    player_rank_idx.append(j)
                    cardpower_tie.append(cardpower[j])

            # 2次元配列の行と列を入れ替える
            #print(cardpower_tie)
            converted_cardpower = [list(x) for x in zip(*cardpower_tie)]
            print(converted_cardpower)

            #print(converted_cardpower)
            for i in range(len(cardpower_tie[0])):
                card_power_judge.append(converted_cardpower[i])
                if converted_cardpower[i].count(max(converted_cardpower[i])) == 1:
                    #print(player_rank_idx[converted_cardpower[i].index(max(converted_cardpower[i]))])
                    winner.append(player_rank_idx[converted_cardpower[i].index(max(converted_cardpower[i]))])
                    return winner, card_power_judge
                elif i == len(cardpower_tie[0]) - 1:
                    winner = [player_rank_idx[converted_cardpower[j].index(max(converted_cardpower[j]))] for j in range(len(cardpower_tie[0]))]
                    return winner, card_power_judge
"""