from raumschach.board import INITIAL_5_5_BOARD_SETUP, ChessBoard
from raumschach.figures import Colour, Pawn, Queen
from raumschach.game import ChessGame
from raumschach.player import ConsolePlayer, DummyPlayer, RandomPlayer
import datetime

# script = ['N:Ab1-Aa3', 'n:Eb5-Ea3', 'N:Aa3-Ab1', 'n:Ea3-Eb5', 'N:Ab1-Aa3', 'n:Eb5-Ea3', 'N:Aa3-Ab1', 'n:Ea3-Eb5', 'N:Ab1-Aa3'] # Testing threefold repetition rule
# script = ['P:Ad2-Ad3', 'p:Ee4-Ee3', 'B:Ba1-Ca2', 'q:Dc5-Cc5', 'B:Ca2-Cb1', 'u:Db5-Cc4', 'N:Ab1-Bb3', 'p:Ed4-Ed3', 'B:Bd1-Cd2', 'p:Ed3-Dd3', 'P:Ad3-Bd3', 'p:Ea4-Ea3', 'B:Cb1-Db2', 'p:Dd4-Cd4', 'N:Bb3-Cb1', 'p:Dd3-Cd3', 'B:Db2-Dd4', 'u:De5-Ed4', 'P:Ac2-Ac3', 'n:Ed5-Db5', 'P:Ab2-Ab3', 'q:Cc5-Ca5', 'B:Dd4-Dc5', 'p:Da4-Da3', 'P:Ab3-Ab4', 'r:Ee5-Ae5', 'R:Aa1-Ca1', 'p:Cd4-Bd4', 'R:Ca1-Ca3', 'n:Eb5-Cb4', 'U:Bb1-Ee4', 'p:Eb4-Eb3', 'P:Ab4-Ab5', 'p:De4-De3', 'P:Ac3-Bc3', 'q:Ca5-Aa5', 'P:Ae2-Ae3', 'p:Bd4xBc3', 'N:Cb1-Cc3', 'n:Cb4xBb2', 'P:Be2-Ce2', 'p:Ec4-Ec3', 'B:Cd2-Bd1', 'q:Aa5-Aa3+w', 'U:Ee4-Cc2+w', 'n:Db5-Cd5+w', 'P:Aa2xBb2+w', 'p:Ea3-Ea2+w', 'Q:Bc1-Bb1+w', 'p:Ea2-Da2+w', 'P:Bb2-Bb3+w', 'p:Dc4-Dc3+w', 'R:Ca3xAa3', 'p:De3-De2', 'B:Bd1-Be2', 'p:Db4-Db3', 'B:Dc5-Ec4', 'p:Da3-Ca3', 'B:Ec4-Dc5', 'u:Ed4-De5', 'R:Ae1-Ae2', 'r:Ea5-Ea3', 'P:Ae3-Ae4', 'b:Dd5-Cd4', 'R:Ae2-Ab2', 'p:Dc3-Dc2', 'B:Dc5-Dd4', 'p:Cd3xCe2', 'P:Bd3-Cd3', 'p:Dc2-Dc1', 'P:Ab5-Bb5', 'u:De5-Ed4', 'Q:Bb1-Db1', 'p:Da2-Da1', 'B:Dd4-De5', 'p:Ec3-Dc3', 'P:Bb5-Cb5', 'p:Dc1-Cc1', 'Q:Db1-Dc1', 'k:Ec5-Dd5', 'P:Bd2-Bd3', 'n:Cd5-Db5', 'R:Aa3-Ba3', 'b:Da5-Ea4', 'B:De5-Be3', 'p:Ce2-Ce1', 'U:Cc2-Db1', 'r:Ea3-Ea1', 'P:Bc2-Cc2', 'u:Ed4-Dc5', 'N:Cc3-Ac2', 'u:Cc4-Dd3', 'U:Db1-Ec2', 'u:Dc5xBa3', 'P:Bb3-Cb3', 'n:Db5-Da3', 'B:Be3-Bc1', 'p:Da1-Ca1', 'R:Ab2-Cb2', 'k:Dd5-Ed5', 'U:Ec2xDb3', 'p:De2-Ce2', 'P:Cb5-Db5', 'r:Ea1-Ea3', 'U:Db3-Cc4', 'n:Da3-Ea1', 'P:Ba2-Ca2', 'p:Dc3-Cc3', 'N:Ac2-Cd2', 'p:Ca3xCb2', 'U:Be1-Ad2', 'n:Ea1xCa2', 'B:Be2-Ee5', 'b:Cd4xBd3', 'K:Ac1-Bb1+w', 'b:Bd3-Dd5+w', 'K:Bb1-Aa1+w', 'k:Ed5-Dd4++', 'N:Cd2-Ed1+w', 'k:Dd4-Ed3+w', 'U:Ad2xBc3+w', 'n:Ca2-Cb4', 'K:Aa1-Ab1', 'k:Ed3-Ed4+b', 'B:Ee5-Be2', 'u:Dd3-Ee4', 'P:Ae4-Be4', 'r:Ea3-Ca3', 'B:Bc1-Ac2', 'n:Cb4xCd3', 'N:Ad1-Ae3', 'p:Ca1-Ba1+w', 'K:Ab1-Ac1', 'u:Ee4-Dd3', 'B:Be2-Ce3', 'p:Cb2-Bb2', 'P:Cb3-Cb4', 'u:Ba3-Ab2', 'U:Bc3-Ad2', 'p:Eb3-Eb2', 'P:Be4-Ce4', 'p:Ce1-Be1', 'K:Ac1-Bb1+w', 'r:Ae5-De5+w', 'P:Ce4-Ce5+w', 'k:Ed4-Dc3++', 'Q:Dc1-Db1+w', 'k:Dc3xCc4++', 'N:Ae3-Bc3+w', 'p:Be1-Ae1+w', 'Q:Db1xEb2+w', 'p:Bb2xAc2+w', 'P:Ce5xDd5+w', 'p:Ac2-Ac1+w', 'P:Cb4-Db4+w', 'k:Cc4-Bd5++', 'N:Bc3-Db3+w', 'r:Ca3-Ca5+w', 'Q:Eb2-Ed2+w', 'p:Ee3xEd2+w', 'P:Db4xEa4+w', 'p:Cc3-Bc3+w', 'B:Ce3-De2+w', 'r:Ca5-Ba5+w', 'P:Ea4-Ea5+w', 'p:Ed2-Dd2+w', 'P:Cc2-Dc2+w', 'p:Bc3-Ac3+w', 'P:Dc2-Ec2+w', 'p:Dd2-Cd2+w', 'P:Db5-Eb5+w', 'k:Bd5-Be5+w', 'N:Db3-Cb1+w', 'b:Ae1-Be2+w', 'P:Dd5-Ed5+w', 'n:Cd3-Bd1+w', 'N:Ed1-Eb2+w', 'p:Ac3xAd2+w', 'N:Cb1-Db3+w', 'u:Dd3-Ee4+w', 'K:Bb1-Ac2', 'n:Ac1-Aa2', 'B:De2-Ee1', 'u:Ee4-Dd5', 'K:Ac2-Bc2+w', 'p:Ad2-Ad1+w', 'U:Ed5-Ba2+w', 'u:Dd5-Ce4+w', 'N:Db3-Da5+w', 'p:Cd2-Bd2+w', 'N:Da5-Ec5+w', 'u:Ab2-Bc3+w', 'K:Bc2-Ad3+w', 'p:Ce2-Ce1+w', 'N:Ec5-Cd5+w', 'b:Ad1-Ae2+w', 'N:Cd5-Ee5+w', 'b:Ae2-Be1+w', 'N:Eb2-Ea4+w', 'u:Ce4-Dd3+w', 'N:Ea4-Ec5+w', 'b:Be2-De4+w', 'P:Ec2-Ec3+w', 'b:Be1-Ae2+w', 'B:Ee1-De2+w', 'p:Ce1-Be1+w', 'N:Ec5-Da5+w', 'k:Be5-Ad5+w', 'Q:Ea5-Db4+w', 'n:Bd1-Dd2+w', 'U:Ba2-Dc4+w', 'b:De4-Ce5+w', 'N:Da5-Ba4+w', 'r:De5-Dd5+w', 'K:Ad3-Ae3+w', 'p:Bd2-Ad2+w', 'N:Ba4xAa2+w', 'p:Ad2-Ad1+w', 'R:Eb5-Eb1+w', 'b:Ce5-De4', 'N:Aa2-Ba4', 'u:Dd3-Cc4', 'P:Ec3-Ec4', 'p:Be1-Ae1', 'K:Ae3-Bd3+w', 'r:Ae1-Ee1+w', 'N:Ba4-Da3+w', 'b:Ae2-Be3+w', 'U:Dc4-Ed3+w', 'n:Dd2-Cd4+w', 'B:De2-Dd3+w', 'k:Ad5-Ac5+w', 'P:Ec4-Ec5+w', 'u:Bc3-Da5+w', 'B:Ec5-Ea3+w', 'r:Ee1-Ec1+w', 'B:Dd3-Bd1+w', 'u:Ad1-Da4+w', 'B:Bd1-Ed4+w', 'r:Dd5-Db5+w', 'R:Eb1-Eb5+w', 'k:Ac5-Bb5+w', 'N:Ee5-Ce4+w', 'n:Cd4-Cc2+w', 'R:Eb5-Ed5+w', 'u:Cc4-Dd5', 'Q:Db4-Bd2', 'b:Be3xBd2', 'U:Ed3-Cb5', 'b:De4-Ee5', 'U:Cb5xDa4', 'k:Bb5-Ca5+b', 'N:Da3-Dc4', 'r:Ba5-Ba3+w', 'R:Ed5-Ec5+w', 'r:Ba3-Ba4', 'N:Dc4-Ee4', 'p:Ba1-Aa1', 'N:Ce4-Ae5', 'b:Ee5xEd4', 'N:Ee4-Ce5', 'n:Cc2-Ca3', 'B:Ea3-Ca1', 'k:Ca5xDa4', 'N:Ae5-Ac4', 'k:Da4-Eb3', 'B:Ca1-Ea3', 'b:Ed4-Ea1', 'N:Ac4-Cd4', 'p:Cc1-Bc1', 'N:Cd4-Ad3', 'b:Bd2-Dd4', 'N:Ad3-Bb3', 'r:Db5-Eb5', 'N:Ce5-Ed5', 'u:Da5-Eb4', 'B:Ea3-Ca1', 'b:Dd4xEd5', 'N:Bb3-Ab1', 'u:Dd5-Ce4+w', 'B:Ca1-Ea3+w', 'r:Ec1-Ed1+w', 'R:Ec5xEb5+w', 'r:Ba4-Ca4+w', 'N:Ab1-Cc1+w', 'u:Eb4-Da3++', 'B:Ea3-Eb4+w', 'b:Ed5-Dd4+w', 'K:Bd3-Ad4+w', 'u:Da3-Eb2+w', 'N:Cc1-Ad1+w', 'b:Dd4-De3+w', 'N:Ad1-Ab2', 'u:Eb2-Da1+w', 'R:Eb5-Ab5+w', 'b:De3-Dc5+w', 'B:Eb4-Bb1+w', 'k:Eb3-Ea2+w', 'R:Ab5-Eb5+w', 'r:Ca4-Cb4+w', 'R:Eb5-Ee5+w', 'r:Ed1-Ed5+w', 'R:Ee5-Ae5+w', 'p:Bc1-Ac1+w', 'N:Ab2-Ac4+w', 'q:Aa1-Ca1+w', 'K:Ad4-Be4', 'b:Dc5-Ec4', 'K:Be4xCe4+w', 'b:Ec4-Eb3+w', 'B:Bb1-Eb4+w', 'u:Da1-Cb2+w', 'K:Ce4-Be3', 'k:Ea2-Eb1', 'N:Ac4-Cc3', 'b:Eb3-Db2', 'B:Eb4xCb2', 'q:Ca1-Ac3', 'K:Be3-Ce3+w', 'u:Ac1-Bb2', 'R:Ae5-Ae4', 'q:Ac3-Bb4', 'B:Cb2-Bb3', 'r:Cb4-Cb3', 'K:Ce3-De4', 'q:Bb4xCc3', 'K:De4-Dd3', 'n:Ca3-Cc2', 'B:Bb3-Ab2', 'k:Eb1-Da2', 'B:Ab2-Ae5', 'n:Cc2-Ba2', 'B:Ae5-Ee1', 'n:Ba2-Bb4', 'R:Ae4-Ab4', 'u:Bb2-Cc1', 'B:Ee1-Ce3', 'n:Bb4-Bc2', 'B:Ce3xCc1', 'r:Ed5-Ee5', 'K:Dd3-Ce3+w', 'k:Da2-Cb1+w', 'B:Cc1-Dc2+w', 'r:Ee5-De5+w', 'B:Dc2-Cc1+w', 'b:Ea1-Aa5+w', 'R:Ab4-Eb4+w', 'r:De5-Ce5+w', 'K:Ce3-Cd3+w', 'r:Cb3-Cb4+w', 'R:Eb4-Eb2+w', 'r:Ce5-Ae5+w', 'B:Cc1-Ce3+w', 'r:Cb4-Ca4+w', 'R:Eb2-Ed2+w', 'k:Cb1-Cc2++', 'K:Cd3-Be2', 'r:Ca4-Cc4', 'R:Ed2-Dd2', 'r:Cc4-Ec4', 'B:Ce3-Be4', 'b:Db2-Cb3', 'B:Be4-Ce3', 'q:Cc3-Ec1', 'K:Be2-Be3+w', 'k:Cc2-Dd1++', 'R:Dd2-Cd2+w', 'r:Ec4-Ec3+w', 'R:Cd2-Ca2+w', 'r:Ec3-Ec2+w', 'K:Be3-Ad4', 'b:Cb3-Bb2', 'K:Ad4-Ac4+w', 'k:Dd1-Dc1+w', 'B:Ce3-Be2+w', 'r:Ec2-Ec5+w', 'R:Ca2-Ca5+w', 'r:Ec5-Ac5+w', 'B:Be2-De4+w', 'b:Aa5-Ca3+w', 'R:Ca5-Ba5+w', 'n:Bc2-Ce2+w', 'R:Ba5-Ea5+w', 'r:Ac5-Ec5', 'B:De4-Ee3', 'k:Dc1-Cd2', 'B:Ee3-Ce5', 'b:Ca3xEa5', 'K:Ac4-Ad5+w', 'b:Ea5-Eb4+w', 'B:Ce5-Be4+w', 'n:Ce2-Cd4+w', 'K:Ad5-Bd5', 'b:Eb4-Ee1', 'B:Be4-Ae3', 'r:Ae5xAe3', 'K:Bd5-Ac4+w', 'n:Cd4-Cb3', 'K:Ac4-Ad4', 'b:Ee1-Ce3', 'K:Ad4-Be5+w', 'n:Cb3-Ab4+w', 'K:Be5-Ce5', 'r:Ec5-Ec3', 'K:Ce5-Dd4', 'q:Ec1-Eb2', 'K:Dd4-Ed4', 'r:Ec3-Cc3+w', 'K:Ed4-Dc5', 'r:Cc3-Cc1', 'K:Dc5-Ed5', 'b:Bb2-Ba1', 'K:Ed5-Ed4+w', 'k:Cd2-Dc3++', 'K:Ed4xDc3+w']

# p1 = ConsolePlayer("P1")
# p1 = RandomPlayer("P1")
# p1 = DummyPlayer("P1")

# p2 = ConsolePlayer("P2")
# p2 = RandomPlayer("P2")
# p2 = DummyPlayer("P2")

# game = ChessGame(p1, p2, 5)
# game.play()
# game.play_script(script)

# game = ChessGame(RandomPlayer("P1"), RandomPlayer("P2"), 5)
# print(game.play())



n = 100
counter = [0, 0, 0]
start_time = datetime.datetime.now()
for i in range(n):
    print(i)
    game = ChessGame(RandomPlayer("P1"), RandomPlayer("P2"), 5)
    win_player = game.play()
    counter[1+win_player] += 1
stop_time = datetime.datetime.now()
print(f"Black wins: {counter[0]} Draws: {counter[1]} White wins: {counter[2]} -- Time taken for {n} runs: {(stop_time - start_time).total_seconds()} s")


# threefold_repetition_script = ['N:Ab1-Aa3', 'n:Eb5-Ea3', 'N:Aa3-Ab1', 'n:Ea3-Eb5', 'N:Ab1-Aa3', 'n:Eb5-Ea3', 'N:Aa3-Ab1', 'n:Ea3-Eb5', 'N:Ab1-Aa3']
# game = ChessGame(DummyPlayer("P1"), DummyPlayer("P2"), 5)
# game.play_script(threefold_repetition_script)