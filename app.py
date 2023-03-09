from raumschach.figures import FIGURES
from raumschach.players.basic_player import *
from raumschach.players.algorithmic_player import *

from raumschach.board import INITIAL_5_5_BOARD_SETUP, ChessBoard
from raumschach.game import ChessGame

import sys
import datetime
import numpy as np
import torch

from raumschach.players.neural_net_player import MoveValueClassifierPlayer
from raumschach.reinforcement_learn.deep_NN import ValueNN
from raumschach.reinforcement_learn.learn import learn_RL, learn_simple_value_function, test_network, train_reward_RL

ChessGame(ConsolePlayer(), RandomPlayer(), 5).play()

""" Function to continue training a pre-trained neural network using a reward-based function """
# train_reward_RL(5, sys.argv[1], save_dir=sys.argv[2])

# game = ChessGame(AlphaBetaPlayer(search_depth=4, play_to_lose=True), AlphaBetaPlayer(search_depth=4), 5)
# winner = game.play()

# model = ValueNN(5, len(FIGURES), [ fig.id for fig in FIGURES ])
# model = model.to("cuda")
# player = MiniMaxTreeSearchPlayer(search_depth=2, value_function=model.get_board_state_moves_value_function("cuda"))
# # player = AlphaBetaPlayer(search_depth=2)
# game = ChessGame(player, RandomPlayer(), 5).play()


# test_network("C:/Users/Oliver/Desktop/UofG/University-of-Glasgow/Codebases/Lvl4_COMPSCI4025P_Individual-Project-H/Individual-Project/res/NN_RL/pre-train/model_49.ptm", 5, tree_search=True, num_test=5)
# test_network("C:/Users/Oliver/Downloads/res/NN_RL/pre-train/model_14.ptm", 5)
# train_reward_RL(5, "C:/Users/Oliver/Desktop/UofG/University-of-Glasgow/Codebases/Lvl4_COMPSCI4025P_Individual-Project-H/Individual-Project/res/NN_RL/pre-train/model_49.ptm")
# learn_RL(5)
# learn_simple_value_function(5)

# script = ['N:Ab1-Aa3', 'n:Eb5-Ea3', 'N:Aa3-Ab1', 'n:Ea3-Eb5', 'N:Ab1-Aa3', 'n:Eb5-Ea3', 'N:Aa3-Ab1', 'n:Ea3-Eb5', 'N:Ab1-Aa3'] # Testing threefold repetition rule
# script = ['P:Ad2-Ad3', 'p:Ee4-Ee3', 'B:Ba1-Ca2', 'q:Dc5-Cc5', 'B:Ca2-Cb1', 'u:Db5-Cc4', 'N:Ab1-Bb3', 'p:Ed4-Ed3', 'B:Bd1-Cd2', 'p:Ed3-Dd3', 'P:Ad3-Bd3', 'p:Ea4-Ea3', 'B:Cb1-Db2', 'p:Dd4-Cd4', 'N:Bb3-Cb1', 'p:Dd3-Cd3', 'B:Db2-Dd4', 'u:De5-Ed4', 'P:Ac2-Ac3', 'n:Ed5-Db5', 'P:Ab2-Ab3', 'q:Cc5-Ca5', 'B:Dd4-Dc5', 'p:Da4-Da3', 'P:Ab3-Ab4', 'r:Ee5-Ae5', 'R:Aa1-Ca1', 'p:Cd4-Bd4', 'R:Ca1-Ca3', 'n:Eb5-Cb4', 'U:Bb1-Ee4', 'p:Eb4-Eb3', 'P:Ab4-Ab5', 'p:De4-De3', 'P:Ac3-Bc3', 'q:Ca5-Aa5', 'P:Ae2-Ae3', 'p:Bd4xBc3', 'N:Cb1-Cc3', 'n:Cb4xBb2', 'P:Be2-Ce2', 'p:Ec4-Ec3', 'B:Cd2-Bd1', 'q:Aa5-Aa3+w', 'U:Ee4-Cc2+w', 'n:Db5-Cd5+w', 'P:Aa2xBb2+w', 'p:Ea3-Ea2+w', 'Q:Bc1-Bb1+w', 'p:Ea2-Da2+w', 'P:Bb2-Bb3+w', 'p:Dc4-Dc3+w', 'R:Ca3xAa3', 'p:De3-De2', 'B:Bd1-Be2', 'p:Db4-Db3', 'B:Dc5-Ec4', 'p:Da3-Ca3', 'B:Ec4-Dc5', 'u:Ed4-De5', 'R:Ae1-Ae2', 'r:Ea5-Ea3', 'P:Ae3-Ae4', 'b:Dd5-Cd4', 'R:Ae2-Ab2', 'p:Dc3-Dc2', 'B:Dc5-Dd4', 'p:Cd3xCe2', 'P:Bd3-Cd3', 'p:Dc2-Dc1', 'P:Ab5-Bb5', 'u:De5-Ed4', 'Q:Bb1-Db1', 'p:Da2-Da1', 'B:Dd4-De5', 'p:Ec3-Dc3', 'P:Bb5-Cb5', 'p:Dc1-Cc1', 'Q:Db1-Dc1', 'k:Ec5-Dd5', 'P:Bd2-Bd3', 'n:Cd5-Db5', 'R:Aa3-Ba3', 'b:Da5-Ea4', 'B:De5-Be3', 'p:Ce2-Ce1', 'U:Cc2-Db1', 'r:Ea3-Ea1', 'P:Bc2-Cc2', 'u:Ed4-Dc5', 'N:Cc3-Ac2', 'u:Cc4-Dd3', 'U:Db1-Ec2', 'u:Dc5xBa3', 'P:Bb3-Cb3', 'n:Db5-Da3', 'B:Be3-Bc1', 'p:Da1-Ca1', 'R:Ab2-Cb2', 'k:Dd5-Ed5', 'U:Ec2xDb3', 'p:De2-Ce2', 'P:Cb5-Db5', 'r:Ea1-Ea3', 'U:Db3-Cc4', 'n:Da3-Ea1', 'P:Ba2-Ca2', 'p:Dc3-Cc3', 'N:Ac2-Cd2', 'p:Ca3xCb2', 'U:Be1-Ad2', 'n:Ea1xCa2', 'B:Be2-Ee5', 'b:Cd4xBd3', 'K:Ac1-Bb1+w', 'b:Bd3-Dd5+w', 'K:Bb1-Aa1+w', 'k:Ed5-Dd4++', 'N:Cd2-Ed1+w', 'k:Dd4-Ed3+w', 'U:Ad2xBc3+w', 'n:Ca2-Cb4', 'K:Aa1-Ab1', 'k:Ed3-Ed4+b', 'B:Ee5-Be2', 'u:Dd3-Ee4', 'P:Ae4-Be4', 'r:Ea3-Ca3', 'B:Bc1-Ac2', 'n:Cb4xCd3', 'N:Ad1-Ae3', 'p:Ca1-Ba1+w', 'K:Ab1-Ac1', 'u:Ee4-Dd3', 'B:Be2-Ce3', 'p:Cb2-Bb2', 'P:Cb3-Cb4', 'u:Ba3-Ab2', 'U:Bc3-Ad2', 'p:Eb3-Eb2', 'P:Be4-Ce4', 'p:Ce1-Be1', 'K:Ac1-Bb1+w', 'r:Ae5-De5+w', 'P:Ce4-Ce5+w', 'k:Ed4-Dc3++', 'Q:Dc1-Db1+w', 'k:Dc3xCc4++', 'N:Ae3-Bc3+w', 'p:Be1-Ae1+w', 'Q:Db1xEb2+w', 'p:Bb2xAc2+w', 'P:Ce5xDd5+w', 'p:Ac2-Ac1+w', 'P:Cb4-Db4+w', 'k:Cc4-Bd5++', 'N:Bc3-Db3+w', 'r:Ca3-Ca5+w', 'Q:Eb2-Ed2+w', 'p:Ee3xEd2+w', 'P:Db4xEa4+w', 'p:Cc3-Bc3+w', 'B:Ce3-De2+w', 'r:Ca5-Ba5+w', 'P:Ea4-Ea5+w', 'p:Ed2-Dd2+w', 'P:Cc2-Dc2+w', 'p:Bc3-Ac3+w', 'P:Dc2-Ec2+w', 'p:Dd2-Cd2+w', 'P:Db5-Eb5+w', 'k:Bd5-Be5+w', 'N:Db3-Cb1+w', 'b:Ae1-Be2+w', 'P:Dd5-Ed5+w', 'n:Cd3-Bd1+w', 'N:Ed1-Eb2+w', 'p:Ac3xAd2+w', 'N:Cb1-Db3+w', 'u:Dd3-Ee4+w', 'K:Bb1-Ac2', 'n:Ac1-Aa2', 'B:De2-Ee1', 'u:Ee4-Dd5', 'K:Ac2-Bc2+w', 'p:Ad2-Ad1+w', 'U:Ed5-Ba2+w', 'u:Dd5-Ce4+w', 'N:Db3-Da5+w', 'p:Cd2-Bd2+w', 'N:Da5-Ec5+w', 'u:Ab2-Bc3+w', 'K:Bc2-Ad3+w', 'p:Ce2-Ce1+w', 'N:Ec5-Cd5+w', 'b:Ad1-Ae2+w', 'N:Cd5-Ee5+w', 'b:Ae2-Be1+w', 'N:Eb2-Ea4+w', 'u:Ce4-Dd3+w', 'N:Ea4-Ec5+w', 'b:Be2-De4+w', 'P:Ec2-Ec3+w', 'b:Be1-Ae2+w', 'B:Ee1-De2+w', 'p:Ce1-Be1+w', 'N:Ec5-Da5+w', 'k:Be5-Ad5+w', 'Q:Ea5-Db4+w', 'n:Bd1-Dd2+w', 'U:Ba2-Dc4+w', 'b:De4-Ce5+w', 'N:Da5-Ba4+w', 'r:De5-Dd5+w', 'K:Ad3-Ae3+w', 'p:Bd2-Ad2+w', 'N:Ba4xAa2+w', 'p:Ad2-Ad1+w', 'R:Eb5-Eb1+w', 'b:Ce5-De4', 'N:Aa2-Ba4', 'u:Dd3-Cc4', 'P:Ec3-Ec4', 'p:Be1-Ae1', 'K:Ae3-Bd3+w', 'r:Ae1-Ee1+w', 'N:Ba4-Da3+w', 'b:Ae2-Be3+w', 'U:Dc4-Ed3+w', 'n:Dd2-Cd4+w', 'B:De2-Dd3+w', 'k:Ad5-Ac5+w', 'P:Ec4-Ec5+w', 'u:Bc3-Da5+w', 'B:Ec5-Ea3+w', 'r:Ee1-Ec1+w', 'B:Dd3-Bd1+w', 'u:Ad1-Da4+w', 'B:Bd1-Ed4+w', 'r:Dd5-Db5+w', 'R:Eb1-Eb5+w', 'k:Ac5-Bb5+w', 'N:Ee5-Ce4+w', 'n:Cd4-Cc2+w', 'R:Eb5-Ed5+w', 'u:Cc4-Dd5', 'Q:Db4-Bd2', 'b:Be3xBd2', 'U:Ed3-Cb5', 'b:De4-Ee5', 'U:Cb5xDa4', 'k:Bb5-Ca5+b', 'N:Da3-Dc4', 'r:Ba5-Ba3+w', 'R:Ed5-Ec5+w', 'r:Ba3-Ba4', 'N:Dc4-Ee4', 'p:Ba1-Aa1', 'N:Ce4-Ae5', 'b:Ee5xEd4', 'N:Ee4-Ce5', 'n:Cc2-Ca3', 'B:Ea3-Ca1', 'k:Ca5xDa4', 'N:Ae5-Ac4', 'k:Da4-Eb3', 'B:Ca1-Ea3', 'b:Ed4-Ea1', 'N:Ac4-Cd4', 'p:Cc1-Bc1', 'N:Cd4-Ad3', 'b:Bd2-Dd4', 'N:Ad3-Bb3', 'r:Db5-Eb5', 'N:Ce5-Ed5', 'u:Da5-Eb4', 'B:Ea3-Ca1', 'b:Dd4xEd5', 'N:Bb3-Ab1', 'u:Dd5-Ce4+w', 'B:Ca1-Ea3+w', 'r:Ec1-Ed1+w', 'R:Ec5xEb5+w', 'r:Ba4-Ca4+w', 'N:Ab1-Cc1+w', 'u:Eb4-Da3++', 'B:Ea3-Eb4+w', 'b:Ed5-Dd4+w', 'K:Bd3-Ad4+w', 'u:Da3-Eb2+w', 'N:Cc1-Ad1+w', 'b:Dd4-De3+w', 'N:Ad1-Ab2', 'u:Eb2-Da1+w', 'R:Eb5-Ab5+w', 'b:De3-Dc5+w', 'B:Eb4-Bb1+w', 'k:Eb3-Ea2+w', 'R:Ab5-Eb5+w', 'r:Ca4-Cb4+w', 'R:Eb5-Ee5+w', 'r:Ed1-Ed5+w', 'R:Ee5-Ae5+w', 'p:Bc1-Ac1+w', 'N:Ab2-Ac4+w', 'q:Aa1-Ca1+w', 'K:Ad4-Be4', 'b:Dc5-Ec4', 'K:Be4xCe4+w', 'b:Ec4-Eb3+w', 'B:Bb1-Eb4+w', 'u:Da1-Cb2+w', 'K:Ce4-Be3', 'k:Ea2-Eb1', 'N:Ac4-Cc3', 'b:Eb3-Db2', 'B:Eb4xCb2', 'q:Ca1-Ac3', 'K:Be3-Ce3+w', 'u:Ac1-Bb2', 'R:Ae5-Ae4', 'q:Ac3-Bb4', 'B:Cb2-Bb3', 'r:Cb4-Cb3', 'K:Ce3-De4', 'q:Bb4xCc3', 'K:De4-Dd3', 'n:Ca3-Cc2', 'B:Bb3-Ab2', 'k:Eb1-Da2', 'B:Ab2-Ae5', 'n:Cc2-Ba2', 'B:Ae5-Ee1', 'n:Ba2-Bb4', 'R:Ae4-Ab4', 'u:Bb2-Cc1', 'B:Ee1-Ce3', 'n:Bb4-Bc2', 'B:Ce3xCc1', 'r:Ed5-Ee5', 'K:Dd3-Ce3+w', 'k:Da2-Cb1+w', 'B:Cc1-Dc2+w', 'r:Ee5-De5+w', 'B:Dc2-Cc1+w', 'b:Ea1-Aa5+w', 'R:Ab4-Eb4+w', 'r:De5-Ce5+w', 'K:Ce3-Cd3+w', 'r:Cb3-Cb4+w', 'R:Eb4-Eb2+w', 'r:Ce5-Ae5+w', 'B:Cc1-Ce3+w', 'r:Cb4-Ca4+w', 'R:Eb2-Ed2+w', 'k:Cb1-Cc2++', 'K:Cd3-Be2', 'r:Ca4-Cc4', 'R:Ed2-Dd2', 'r:Cc4-Ec4', 'B:Ce3-Be4', 'b:Db2-Cb3', 'B:Be4-Ce3', 'q:Cc3-Ec1', 'K:Be2-Be3+w', 'k:Cc2-Dd1++', 'R:Dd2-Cd2+w', 'r:Ec4-Ec3+w', 'R:Cd2-Ca2+w', 'r:Ec3-Ec2+w', 'K:Be3-Ad4', 'b:Cb3-Bb2', 'K:Ad4-Ac4+w', 'k:Dd1-Dc1+w', 'B:Ce3-Be2+w', 'r:Ec2-Ec5+w', 'R:Ca2-Ca5+w', 'r:Ec5-Ac5+w', 'B:Be2-De4+w', 'b:Aa5-Ca3+w', 'R:Ca5-Ba5+w', 'n:Bc2-Ce2+w', 'R:Ba5-Ea5+w', 'r:Ac5-Ec5', 'B:De4-Ee3', 'k:Dc1-Cd2', 'B:Ee3-Ce5', 'b:Ca3xEa5', 'K:Ac4-Ad5+w', 'b:Ea5-Eb4+w', 'B:Ce5-Be4+w', 'n:Ce2-Cd4+w', 'K:Ad5-Bd5', 'b:Eb4-Ee1', 'B:Be4-Ae3', 'r:Ae5xAe3', 'K:Bd5-Ac4+w', 'n:Cd4-Cb3', 'K:Ac4-Ad4', 'b:Ee1-Ce3', 'K:Ad4-Be5+w', 'n:Cb3-Ab4+w', 'K:Be5-Ce5', 'r:Ec5-Ec3', 'K:Ce5-Dd4', 'q:Ec1-Eb2', 'K:Dd4-Ed4', 'r:Ec3-Cc3+w', 'K:Ed4-Dc5', 'r:Cc3-Cc1', 'K:Dc5-Ed5', 'b:Bb2-Ba1', 'K:Ed5-Ed4+w', 'k:Cd2-Dc3++', 'K:Ed4xDc3+w']
# script = ['B:Ba1-Ca2', 'p:Da4-Da3', 'P:Be2-Ce2', 'p:De4-Ce4', 'R:Aa1-Da1', 'p:Db4-Db3', 'P:Bc2-Bc3', 'b:Da5-De1', 'B:Ca2-Cb3', 'b:Dd5-De4', 'P:Ab2-Ab3', 'n:Ed5-Cc5', 'P:Bd2-Cd2', 'p:Dc4-Dc3', 'P:Ad2-Bd2', 'p:Db3-Db2', 'P:Bd2-Bd3', 'p:Ec4-Dc4', 'B:Bd1-Bb3', 'u:De5xBc3', 'R:Da1-Aa1', 'p:Da3-Da2', 'N:Ad1-Ce1', 'q:Dc5-Be3', 'P:Cd2-Cd3', 'p:Db2-Cb2', 'P:Aa2-Aa3', 'p:Dc4-Cc4', 'R:Aa1-Ea1', 'b:De1-Dd2', 'U:Be1-Ad2', 'p:Cb2xBa2', 'U:Bb1xEe4', 'p:Ea4-Da4', 'B:Bb3-Ba4', 'p:Ed4-Ed3', 'K:Ac1-Ad1', 'p:Ed3-Ed2', 'B:Cb3xCc4', 'p:Da4-Da3', 'Q:Bc1-Cc2', 'n:Eb5-Ca5', 'U:Ee4-Dd5', 'u:Bc3-Da5', 'P:Aa3-Aa4', 'q:Be3-Be5', 'U:Ad2-Be3', 'n:Ca5-Cb3', 'P:Cd3xDc3', 'b:De4-Ee3', 'B:Ba4-Bb5', 'k:Ec5-Ed5', 'P:Ce2-Ce3', 'p:Dd4xCc4', 'P:Ce3-De3', 'n:Cb3-Ca1', 'U:Dd5-Ec4', 'p:Ba2-Ba1', 'B:Bb5-Bc4', 'p:Da3-Ca3', 'P:Ab3-Bb3', 'u:Db5-Ca4', 'P:Ac2-Bc2', 'p:Ca3-Ba3', 'P:Ae2-Be2', 'n:Ca1-Aa2', 'R:Ae1-Be1', 'p:Ed2-Ed1', 'P:De3-De4', 'u:Da5-Cb4', 'K:Ad1-Bd1', 'u:Cb4-Ad2', 'P:Be2-Ce2', 'n:Aa2-Ca3', 'U:Be3-Cd2', 'p:Ed1-Dd1', 'R:Ea1-Ea4', 'k:Ed5-Ec5', 'U:Ec4-Dd5', 'b:Dd2-Dc1', 'P:Dc3-Ec3', 'r:Ee5-Ee4', 'N:Ce1-Ed1', 'r:Ea5-Eb5', 'P:Bd3-Bd4', 'b:Ee3xDe4', 'K:Bd1-Ad1', 'r:Ee4-Ed4', 'P:Ce2-De2', 'p:Da2-Da1', 'B:Bc4-Ac3', 'q:Be5-Be3', 'K:Ad1-Ac2', 'q:Be3-Ee3', 'U:Cd2-Bc1', 'p:Ce4xBd4', 'N:Ed1-Db1', 'b:De4-Ce3', 'N:Ab1-Aa3', 'p:Eb4-Eb3', 'R:Ea4-Ea5', 'k:Ec5-Ed5', 'R:Be1-Ae1', 'u:Ca4-Bb5', 'B:Ac3-Aa5', 'p:Dd1-Cd1', 'P:Bc2-Bc3', 'p:Eb3-Db3', 'N:Aa3-Ab5', 'r:Eb5xEa5', 'U:Bc1-Ab2', 'r:Ea5-Ea4', 'Q:Cc2-Cb1', 'n:Ca3-Ba5', 'K:Ac2xAd2', 'p:Db3-Cb3', 'P:De2-De3', 'p:Cd1-Bd1', 'P:Bb3-Bb4', 'b:Ce3xAe1+', 'K:Ad2-Bd2', 'p:Da1xCb1', 'N:Ab5xCc5+', 'n:Ba5xCc5', 'K:Bd2-Ac2', 'p:Cb3xBc3', 'K:Ac2-Bc2', 'r:Ea4-Ba4', 'K:Bc2xBd1', 'n:Cc5-Be5', 'U:Dd5-Ee4', 'p:Bc3xBb2', 'P:Bb4-Cb4', 'b:Dc1-Db2', 'N:Db1-Da3', 'n:Be5-Bc4', 'P:De3-De4', 'r:Ed4-Dd4', 'K:Bd1-Ad1', 'p:Ba1-Aa1=r+', 'K:Ad1-Bc2', 'u:Bb5xAa4', 'U:Ab2xBa3', 'n:Bc4-Be5', 'N:Da3-Ca1', 'n:Be5-Ae3', 'P:Cb4-Cb5', 'b:Db2-Da3', 'P:De4-De5+', 'k:Ed5-Ec5', 'B:Aa5xBa4', 'r:Aa1-Ab1', 'B:Ba4-Aa3', 'b:Ae1-De4', 'B:Aa3-Ab4', 'b:De4-Ee5', 'P:Cb5-Db5+', 'k:Ec5-Dc4', 'N:Ca1-Cb3', 'k:Dc4-Eb5', 'K:Bc2xAb1', 'p:Bd4-Bd3', 'P:Ec3-Ec4+', 'k:Eb5-Ea4', 'N:Cb3xBd3', 'q:Ee3-Be3', 'K:Ab1-Bc2', 'q:Be3-Be2+', 'K:Bc2-Bb1', 'p:Bb2-Ab2', 'B:Ab4-Ad2', 'b:Ee5-De4', 'P:Db5-Eb5=R', 'r:Dd4-Ad4', 'B:Ad2-Ae1', 'p:Ab2-Ab1=b', 'P:Ec4-Ec5=Q', 'r:Ad4-Ae4', 'Q:Ec5-Ec1', 'r:Ae4-Ab4', 'R:Eb5-Ec5', 'p:Cc4-Cc3', 'K:Bb1-Aa1', 'r:Ab4-Eb4', 'R:Ec5-Eb5', 'k:Ea4-Eb3', 'B:Ae1-Aa5', 'k:Eb3-Da4', 'K:Aa1-Ab2', 'b:Ab1xEb5', 'U:Ba3-Dc1', 'p:Cb1-Bb1', 'U:Ee4-Dd3', 'q:Be2-Ce2', 'K:Ab2-Ba2', 'p:Cc3-Bc3', 'U:Dd3xCe2', 'r:Eb4-Eb2', 'K:Ba2-Aa3', 'b:De4-Be2', 'K:Aa3xAa4', 'b:Be2-Ae1', 'U:Dc1-Cd2', 'k:Da4-Cb5', 'U:Cd2-Eb4', 'b:Eb5-Cb3', 'K:Aa4-Bb3', 'p:Bb1-Ab1=n+', 'K:Bb3-Ca3', 'k:Cb5-Dc4', 'U:Eb4-Dc5', 'b:Cb3-Ca2', 'Q:Ec1-Ac1+', 'k:Dc4-Eb5', 'K:Ca3-Db3', 'b:Ca2-Cb3', 'U:Ce2-Ec4', 'r:Eb2-Ab2', 'P:De5-Ee5=B', 'b:Da3-Ca4', 'B:Aa5-Ad2', 'n:Ab1-Bd1', 'B:Ee5-Ea1', 'b:Ae1-Ee5', 'N:Bd3-Dd2', 'k:Eb5-Ea5', 'Q:Ac1-Dc1', 'b:Ca4-Aa2', 'B:Ad2-Ab4', 'b:Ee5-Ae1', 'U:Ec4-Db5', 'b:Aa2-Da5', 'K:Db3-Da3', 'b:Ae1-Be2', 'Q:Dc1-Eb2', 'p:Bc3-Ac3', 'U:Db5-Ec4', 'n:Bd1-Cb1', 'N:Dd2-Bd1', 'b:Da5-Dc3', 'K:Da3-Cb4', 'k:Ea5-Ea4', 'U:Ec4-Db3+', 'n:Cb1xDb3', 'B:Ea1-Aa5', 'b:Dc3-Bc1', 'U:Dc5-Eb4', 'p:Ac3-Ac2', 'K:Cb4-Dc4', 'b:Be2-Bb5', 'K:Dc4-Ed5', 'n:Db3-Cb1', 'K:Ed5-Dd4', 'r:Ab2-Cb2', 'B:Ab4-Aa3', 'b:Cb3-Cc2', 'N:Bd1-Dd2', 'r:Cb2xEb2', 'N:Dd2-Cd4', 'n:Ae3-Ce2', 'N:Cd4-Ed5', 'b:Bc1-Bd2+', 'K:Dd4-Ce3', 'n:Ce2-Cd4', 'U:Eb4-Dc3', 'b:Bb5-Cb4', 'K:Ce3xCd4', 'b:Cb4-Cd2', 'U:Dc3-Cb2', 'n:Cb1-Ac1', 'B:Aa3-Ca5', 'k:Ea4-Db4', 'U:Cb2-Ba3', 'n:Ac1-Aa2', 'U:Ba3-Cb2', 'r:Eb2-Eb1', 'U:Cb2-Ed4', 'b:Cd2-Dd3+', 'K:Cd4-Be5', 'n:Aa2-Ab4', 'U:Ed4-De5', 'n:Ab4-Cb3', 'B:Aa5-Ba4', 'p:Ac2-Ac1=q', 'K:Be5-Ad4', 'b:Dd3-Cd2+', 'K:Ad4-Bc5', 'b:Cc2-Cd3', 'N:Ed5-Ce5', 'n:Cb3-Db1', 'K:Bc5-Bc4', 'q:Ac1-Cc1', 'B:Ba4-Ca3', 'q:Cc1-Cc2', 'N:Ce5-Ee4', 'b:Cd3-Ed5', 'K:Bc4-Bc5', 'b:Cd2-Cc1', 'U:De5-Ed4', 'k:Db4-Da5', 'K:Bc5-Bd4', 'b:Ed5-Cd3+', 'K:Bd4-Bc4', 'r:Eb1-Eb5', 'K:Bc4-Ac5', 'k:Da5-Db5', 'B:Ca3-Da2', 'b:Cd3-Dd2', 'K:Ac5-Ab4', 'b:Bd2-Be1', 'K:Ab4-Bb5', 'r:Eb5-Ee5', 'U:Ed4-Ba1', 'b:Be1-Ce2', 'B:Da2-Db3', 'b:Cc1-Dc2', 'U:Ba1-Cb2', 'b:Dd2-Cd1', 'B:Ca5-Ba4', 'q:Cc2-Cb3', 'N:Ee4-Ce3', 'k:Db5-Eb5', 'B:Db3-Eb4', 'k:Eb5xEb4', 'N:Ce3-Ee2', 'r:Ee5-Ea5', 'B:Ba4-Aa3', 'b:Cd1-Bd2', 'B:Aa3-Ac1', 'b:Bd2-Ba5', 'K:Bb5-Aa5', 'k:Eb4-Dc5', 'K:Aa5-Ab4', 'r:Ea5-Da5', 'B:Ac1-Ab2', 'n:Db1-Bb2+', 'K:Ab4-Bb5', 'r:Da5-Da2', 'B:Ab2-Ac3', 'n:Bb2-Bd3', 'N:Ee2-Ed4', 'q:Cb3-Db4', 'B:Ac3-Ae1', 'b:Ce2-Be1', 'K:Bb5-Ac4', 'n:Bd3-Ad5', 'U:Cb2-Dc3', 'b:Ba5-Bb4', 'N:Ed4-Dd2', 'n:Ad5-Cc5+', 'K:Ac4-Bb5', 'r:Da2-Aa2', 'B:Ae1-Ac3', 'k:Dc5-Dd4', 'B:Ac3-Ad2', 'n:Cc5xDc3', 'B:Ad2-Ac3', 'k:Dd4-Ee3', 'N:Dd2-Db3', 'b:Dc2xDb3+', 'K:Bb5-Ca4', 'k:Ee3-Dd4', 'B:Ac3-Ad4', 'r:Aa2-Aa4+', 'K:Ca4xDb4', 'b:Db3-Da4', 'B:Ad4-Aa1', 'r:Aa4-Ab4', 'B:Aa1xDa4', 'r:Ab4-Ad4', 'K:Db4-Eb5', 'r:Ad4-Ad2', 'K:Eb5-Ea4', 'b:Bb4-Cb3', 'B:Da4-Ca5', 'k:Dd4-Cc4', 'B:Ca5-Cd2', 'n:Dc3-Bb3', 'B:Cd2-Dd3', 'b:Cb3-Db4', 'B:Dd3-Dc2', 'n:Bb3-Ab5', 'B:Dc2-Db1', 'r:Ad2-Cd2', 'B:Db1-Cb2', 'b:Be1-Ee4', 'K:Ea4-Ea5', 'k:Cc4-Bb5', 'K:Ea5-Db5', 'k:Bb5-Aa5', 'B:Cb2-Cd4', 'b:Db4-Eb3', 'K:Db5-Dc5', 'k:Aa5-Bb5', 'B:Cd4-Ce5', 'n:Ab5-Ca5+', 'K:Dc5-Ed4', 'r:Cd2-Ad2', 'K:Ed4xEe4', 'n:Ca5-Cc4', 'B:Ce5-Ee3', 'k:Bb5-Aa4', 'B:Ee3-Ed4', 'n:Cc4-Eb4', 'B:Ed4-Eb2', 'b:Eb3-Ea2', 'K:Ee4-Dd3', 'r:Ad2-Ad4', 'B:Eb2-Ec1', 'n:Eb4-Ed3', 'K:Dd3-Ee2', 'n:Ed3-Eb2', 'K:Ee2-De3', 'k:Aa4-Ba5', 'K:De3-De4', 'n:Eb2-Ca2', 'K:De4-Dd5', 'n:Ca2-Da4', 'K:Dd5-Dc4', 'r:Ad4-Ad2', 'B:Ec1-Ac5', 'k:Ba5-Ba4', 'B:Ac5-Aa3+', 'k:Ba4-Ba5', 'K:Dc4-Cd4', 'n:Da4-Bb4+', 'K:Cd4-Bd4', 'n:Bb4-Db3', 'K:Bd4-Cd4', 'n:Db3-Da5', 'B:Aa3-Ab4', 'n:Da5-Cc5', 'K:Cd4-Cd5', 'r:Ad2-Bd2', 'B:Ab4-Ac5', 'k:Ba5-Cb4', 'B:Ac5-Bc4', 'k:Cb4-Da3', 'B:Bc4-Bd5', 'k:Da3-Ca4', 'K:Cd5-Be4', 'r:Bd2-Bd3', 'B:Bd5-Ad4', 'k:Ca4-Ba4', 'B:Ad4-Ac3', 'k:Ba4-Aa3', 'K:Be4xBd3', 'n:Cc5-Ad5+', 'K:Bd3-Bd2', 'n:Ad5xAc3', 'K:Bd2-Ce2', 'b:Ea2-Ed5', 'K:Ce2-Ce3', 'n:Ac3-Be3', 'K:Ce3-Be4', 'k:Aa3-Ab2', 'K:Be4-Ad5', 'k:Ab2-Ab1', 'K:Ad5-Ac5', 'b:Ed5-Ea2', 'K:Ac5-Bd4', 'k:Ab1-Ac2', 'K:Bd4-Ae3', 'k:Ac2-Bc3', 'K:Ae3-Be4', 'n:Be3-Ce5', 'K:Be4xCe5', 'b:Ea2-Eb1', 'K:Ce5-Ce4', 'b:Eb1-Ed3', 'K:Ce4-Be5', 'b:Ed3-Ee4', 'K:Be5-Cd5', 'k:Bc3-Cc3', 'K:Cd5-Be4', 'k:Cc3-Bb4', 'K:Be4-Bd4', 'k:Bb4-Cb5', 'K:Bd4-Ad3', 'b:Ee4-De3', 'K:Ad3-Ae4', 'b:De3-Dd4', 'K:Ae4-Bd4', 'k:Cb5-Ba4', 'K:Bd4-Ae5', 'b:Dd4-Db2', 'K:Ae5-Ad4', 'k:Ba4-Ba5', 'K:Ad4-Bd3', 'k:Ba5-Cb4', 'K:Bd3-Be3', 'b:Db2-Dd4', 'K:Be3-Ad4', 'k:Cb4-Ca5', 'K:Ad4-Bd4', 'k:Ca5-Ba5', 'K:Bd4-Ad3', 'b:Dd4-Cd5+', 'K:Ad3-Ac3', 'b:Cd5-Ce4', 'K:Ac3-Bc4', 'k:Ba5-Ca5', 'K:Bc4-Cb3', 'b:Ce4-De5', 'K:Cb3-Db3', 'b:De5-Be3', 'K:Db3-Da3', 'k:Ca5-Cb5', 'K:Da3-Cb2', 'k:Cb5-Ca5', 'K:Cb2-Cc1', 'b:Be3-Ae2', 'K:Cc1-Bb1', 'b:Ae2-Ce4', 'K:Bb1-Ac1', 'k:Ca5-Db5', 'K:Ac1-Bb1', 'k:Db5-Cb4 ½-½']
# script = ['Q:Bc1-Ec1']
# script = ['P:Be2-Be3', 'n:Ed5-Ee3', 'P:Ac2-Ac3', 'q:Dc5-Bc5', 'P:Ae2-Be2', 'n:Ee3-Ed1', 'U:Bb1-Ac2', 'q:Bc5-Bb5', 'P:Be3-Ce3', 'u:De5xAb2', 'N:Ad1-Bb1', 'q:Bb5-Dd3', 'U:Ac2-Ca4', 'q:Dd3-Db3', 'Q:Bc1-Ec1', 'n:Ed1-Cd2', 'N:Bb1-Bc3', 'u:Ab2-Ba3', 'N:Bc3-Cc5', 'q:Db3-Cb2', 'U:Ca4-Ec2', 'q:Cb2-Eb2', 'K:Ac1-Bb1', 'n:Cd2xEc2', 'N:Ab1-Cc1', 'q:Eb2-Da1', 'R:Ae1-Ac1', 'n:Eb5-Cb4', 'N:Cc5-Ad5', 'q:Da1-Da3', 'B:Bd1xEd4+b', 'n:Ec2xEd4', 'Q:Ec1-Ee3', 'u:Ba3-Ab4', 'P:Ce3-De3', 'u:Ab4-De1', 'Q:Ee3xEd4+b', 'k:Ec5-Eb5', 'P:Be2-Ce2', 'p:Dc4-Dc3', 'N:Cc1-Ec2', 'n:Cb4-Ab3+w', 'K:Bb1-Cc1', 'u:Db5-Ca4', 'K:Cc1-Cd1', 'q:Da3-Ea2', 'B:Ba1-Da3', 'n:Ab3-Bd3+w', 'P:Ac3xBd3', 'b:Dd5-Dc4', 'P:Ba2-Ba3', 'q:Ea2-Db3', 'P:De3-Ee3', 'r:Ee5-Ed5', 'R:Ac1-Cc1', 'q:Db3-Db1', 'N:Ad5-Cd4', 'q:Db1-Bb3', 'R:Aa1-Ab1', 'q:Bb3-Bc3', 'N:Ec2-Ea1', 'p:Dc3-Dc2', 'Q:Ed4-Dd5', 'r:Ed5-Ed1+w', 'K:Cd1xDc2', 'u:Ca4-Db3', 'N:Ea1-Dc1', 'u:Db3-Bd5', 'B:Da3xDb4+b', 'p:Ec4xDb4', 'R:Ab1-Bb1', 'q:Bc3-Cc3+w', 'N:Dc1xCc3', 'r:Ed1-Dd1', 'P:Ce2-Ce3', 'u:De1-Cd2', 'N:Cd4-Ad5', 'b:Dc4-Ec5', 'N:Ad5-Cc5# 1-0'] # White checkmates black
# game = ChessGame(DummyPlayer(), DummyPlayer(), 5)
# game.play_script(script)

# game = ChessGame(ConsolePlayer(), ConsolePlayer(), 5)
# game.play()

# game = ChessGame(RandomPlayer(), RandomPlayer(), 5)
# game.play()

# game = ChessGame(ConsolePlayer(), RandomPlayer(), 5)
# game.play()

# game = ChessGame(MiniMaxPlayer(search_depth=2, rand_seed=1), MiniMaxPlayer(search_depth=2, rand_seed=1), 5)
# game.play()

# board = ChessBoard(5, INITIAL_5_5_BOARD_SETUP)

# n = 1000
# start_time = start_time = datetime.datetime.now()
# for i in range(n):
#     for piece_pos in [ (p[0], p[1], p[2]) for p in np.asarray((board.cube > 0).nonzero()).T ]:
#         ChessBoard._generate_figure_passives_captures(board.cube, piece_pos)
# stop_time = datetime.datetime.now()
# print(f"generate figure moves captures avg : {((stop_time - start_time).total_seconds()) / n} s")

# n = 100
# start_time = start_time = datetime.datetime.now()
# for i in range(n):
#     m = np.concatenate(ChessBoard.get_passives_captures(board.cube, simulate_safe_moves=False, colour=Colour.WHITE), axis=0)
#     ChessBoard.get_safe_moves_simulated(board.cube, m, Colour.WHITE)
# stop_time = datetime.datetime.now()
# print(f"generate player moves captures avg : {((stop_time - start_time).total_seconds()) / n} s")


# board = ChessBoard(5, ["P Eb4", "p Ea5", "p Ec5"]) # , "P Dc3"
# board.get_moves()
# render_board_ascii(board.cube)
# board._generate_figure_passives_captures((4, 3, 1)) # Promotion Pawn
# board._generate_figure_passives_captures((3, 2, 3)) # Promotion Pawn
# board._generate_figure_passives_captures((1, 0, 1)) # Unicorn
# board._generate_figure_passives_captures((1, 1, 0)) # Pawn
# board._generate_figure_passives_captures((3, 3, 4)) # pawn

# ChessGame(MoveValueClassifierPlayer(5, len(FIGURES)), RandomPlayer(rand_seed=1), 5).play()
# player1 = MoveValueClassifierPlayer(5, len(FIGURES))

# n = 100
# counter = [0, 0, 0]
# start_time = datetime.datetime.now()
# for i in range(1, n+1):
#     print("Game", i)
#     # game = ChessGame(RandomPlayer(rand_seed=i-1), RandomPlayer(rand_seed=i+1), 5)
#     # game = ChessGame(MiniMaxPlayer(search_depth=3, rand_seed=i-1), MiniMaxPlayer(search_depth=3, rand_seed=i-1), 5)
#     # game = ChessGame(AlphaBetaPlayer(search_depth=3, rand_seed=i-1), AlphaBetaPlayer(search_depth=3, rand_seed=i+1), 5)
#     # game = ChessGame(AlphaBetaPlayer(search_depth=2, rand_seed=i-1), RandomPlayer(rand_seed=i+1), 5)
#     # game = ChessGame(AlphaBetaPlayer(search_depth=4, rand_seed=i-1), RandomPlayer(rand_seed=i+1), 5)
#     game = ChessGame(player1, RandomPlayer(rand_seed=i+1), 5)
#     win_player = game.play()
#     if (i-1)%10 == 0:
#         player1.test()
#     else:
#         player1.train()
#     counter[1+win_player] += 1
# stop_time = datetime.datetime.now()
# print(f"Black wins: {counter[0]} Draws: {counter[1]} White wins: {counter[2]} -- Time taken for {n} runs: {(stop_time - start_time).total_seconds()} s")


# threefold_repetition_script = ['N:Ab1-Aa3', 'n:Eb5-Ea3', 'N:Aa3-Ab1', 'n:Ea3-Eb5', 'N:Ab1-Aa3', 'n:Eb5-Ea3', 'N:Aa3-Ab1', 'n:Ea3-Eb5', 'N:Ab1-Aa3']
# game = ChessGame(DummyPlayer("P1"), DummyPlayer("P2"), 5)
# game.play_script(threefold_repetition_script)