# 勝者を決定するクラス
class PokerWinner:
    def poker_winner(self, cardpower):
        # 2次元配列の行列の変換
        converted_cardpower = [list(x) for x in zip(*cardpower)]

        max_rank = max(converted_cardpower[0])

        # 役だけで勝敗が確定するときの処理
        if converted_cardpower[0].count(max_rank) == 1:
            winner = converted_cardpower[0].index(max_rank)
            return winner

        # 役で決まらなかった場合は最強役以外のプレイヤーのcardpowerを全て0にする
        else:
            for i in range(len(converted_cardpower[0])):
                if converted_cardpower[0][i] != max_rank:
                    cardpower[i] = [0, 0, 0, 0, 0, 0]

        converted_cardpower = [list(x) for x in zip(*cardpower)]

        # cardpowerを比較し勝敗を決定する
        # 完全に同じ場合はプレイヤー番号が若い方が勝者となる
        for i in range(1, len(converted_cardpower)):
            if converted_cardpower[i].count(max(converted_cardpower[i])) == 1:
                winner = converted_cardpower[i].index(max(converted_cardpower[i]))
                return winner
        