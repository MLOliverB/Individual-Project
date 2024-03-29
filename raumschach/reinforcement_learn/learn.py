import os
import torch
from torch import optim
from torch import nn
import numpy as np
from raumschach.raumschach_game.data.figures import FIGURE_ID_MAP, FIGURES, Colour
from raumschach.raumschach_game.engine.game import ChessGame
from raumschach.raumschach_game.players.algorithmic_player import AlphaBetaPlayer, MiniMaxTreeSearchPlayer
from raumschach.raumschach_game.players.basic_player import RandomPlayer
from raumschach.raumschach_game.players.neural_net_player import NNPlayer
from raumschach.reinforcement_learn.const import DRAW_STATE_VALUE, LOSS_STATE_VALUE, WIN_STATE_VALUE

from raumschach.reinforcement_learn.deep_NN import ValueNN
from raumschach.reinforcement_learn.replay_memory import StateMemory


# https://pytorch.org/tutorials/intermediate/reinforcement_q_learning.html



def network_setup(cb_size, rand_seed=None):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    rng = np.random.default_rng(rand_seed)

    LR = 1e-4 # learning rate

    value_net = ValueNN(cb_size, len(FIGURES), [ fig.id for fig in FIGURES ]).to(device)
    optimizer = optim.Adam(value_net.parameters(), lr=LR, amsgrad=True)
    memory = StateMemory()

    return (rng, device, value_net, optimizer, memory)

def learn_simple_value_function(cb_size):
    rng, device, model, optimizer, memory = network_setup(cb_size)
    
    vectorized_value_transform = np.vectorize((lambda x: 0 if x == 0 else FIGURE_ID_MAP[x][0].value*(x/np.abs(x))), otypes='f')

    for i in range(0, 50000):
        print(f"\n\n\nIteration {i}")
        white_player, black_player = None, None
        if i%3 == 0:
            white_player, black_player = RandomPlayer(memory=memory), RandomPlayer(memory=memory)
        elif i%3 == 1:
            white_player, black_player = AlphaBetaPlayer(search_depth=2, play_to_lose=False, memory=memory), RandomPlayer(memory=memory)
        else:
            white_player, black_player = RandomPlayer(memory=memory), AlphaBetaPlayer(search_depth=2, play_to_lose=True, memory=memory)

        game = ChessGame(white_player, black_player, cb_size)
        win_player = game.play()

        if i%50 == 0:
            input_target_lst = []
            for k, stats in memory.iter():
                b = stats.board_state
                tensor_board, tensor_meta_data = model.sparsify_board_state(b.board_a, b.colour, b.state_repetition_count, b.no_progress_count)
                tensor_board, tensor_meta_data = tensor_board.float().to(device), tensor_meta_data.float().to(device)
                value_board = vectorized_value_transform(b.board_a)
                if np.sum(np.isinf(value_board)) > 1:
                    value_board[np.isinf(value_board)] = 0
                target_val = np.sum(value_board) * b.colour
                input_target_lst.append((tensor_board, tensor_meta_data, torch.tensor(target_val, dtype=tensor_board.dtype)))
            memory.clear()

            optimize(model, optimizer, device, input_target_lst)

        if i%100 == 0:
            dir_path = "res/NN_simple_val_func/"
            fn = f"model_{i//100}.ptm"
            os.makedirs(dir_path, exist_ok=True)
            torch.save(model, dir_path + fn)

def learn_RL(cb_size):
    rng, device, model, optimizer, memory = network_setup(cb_size)

    # pre-train on games between algorithm-based players
    for i in range(5000):
        print(f"\n\n\nPre-train Iteration {i}")
        white_player, black_player = None, None
        if i%5 == 0:
            white_player, black_player = RandomPlayer(memory=memory), RandomPlayer(memory=memory)
        elif i%5 == 1:
            white_player, black_player = AlphaBetaPlayer(search_depth=2, play_to_lose=False, memory=memory), RandomPlayer(memory=memory)
        elif i%5 == 2:
            white_player, black_player = RandomPlayer(memory=memory), AlphaBetaPlayer(search_depth=2, play_to_lose=False, memory=memory)
        elif i%5 == 3:
            white_player, black_player = AlphaBetaPlayer(search_depth=2, play_to_lose=True, memory=memory), RandomPlayer(memory=memory)
        else:
            white_player, black_player = RandomPlayer(memory=memory), AlphaBetaPlayer(search_depth=2, play_to_lose=True, memory=memory)

        game = ChessGame(white_player, black_player, cb_size)
        win_player = game.play()

        if i%50 == 0:
            input_target_lst = []
            for k, stats in memory.iter():
                b = stats.board_state
                tensor_board, tensor_meta_data = model.sparsify_board_state(b.board_a, b.colour, b.state_repetition_count, b.no_progress_count)
                tensor_board, tensor_meta_data = tensor_board.float().to(device), tensor_meta_data.float().to(device)

                board_stats = np.array([stats.win_count, stats.draw_count, stats.loss_count])
                state_values = np.array([WIN_STATE_VALUE, DRAW_STATE_VALUE, LOSS_STATE_VALUE])
                target_val = np.dot(board_stats, state_values)/np.sum(board_stats)
                
                input_target_lst.append((tensor_board, tensor_meta_data, torch.tensor(target_val, dtype=tensor_board.dtype)))
            memory.clear()

            optimize(model, optimizer, device, input_target_lst)

        if i%100 == 0:
            dir_path = "res/NN_RL/pre-train/"
            fn = f"model_{i//100}.ptm"
            os.makedirs(dir_path, exist_ok=True)
            torch.save(model, dir_path + fn)

def train_reward_RL(cb_size, disk_path, save_dir=None):
    rng, device, model, optimizer, memory = network_setup(cb_size)

    model = torch.load(disk_path, map_location=torch.device('cpu')).to(device)


    for i in range(50000):
        print(f"Iteration {i}")
        white_player, black_player = None, None

        players = [
            (RandomPlayer(memory=memory), AlphaBetaPlayer(search_depth=2, play_to_lose=False, memory=memory)),
            (RandomPlayer(memory=memory), MiniMaxTreeSearchPlayer(search_depth=2, branching_factor=10, random_action_p=0, value_function=model.get_board_state_moves_value_function(device))),
            (AlphaBetaPlayer(search_depth=2, play_to_lose=False, memory=memory), MiniMaxTreeSearchPlayer(search_depth=2, branching_factor=10, random_action_p=0.25, value_function=model.get_board_state_moves_value_function(device))),
            (MiniMaxTreeSearchPlayer(search_depth=2, branching_factor=10, random_action_p=0.05, value_function=model.get_board_state_moves_value_function(device)), MiniMaxTreeSearchPlayer(search_depth=2, branching_factor=10, random_action_p=0.5, value_function=model.get_board_state_moves_value_function(device))),
            (MiniMaxTreeSearchPlayer(search_depth=2, branching_factor=10, random_action_p=0, value_function=model.get_board_state_moves_value_function(device)), MiniMaxTreeSearchPlayer(search_depth=2, branching_factor=10, random_action_p=0, value_function=model.get_board_state_moves_value_function(device)))
        ]
        probas = normalize(np.array([
            0.05,
            0.05,
            0.4,
            0.45,
            0.05,
        ]))

        # players = [
        #     (RandomPlayer(memory=memory), AlphaBetaPlayer(search_depth=2, play_to_lose=False, memory=memory)),
        #     (RandomPlayer(memory=memory), MiniMaxTreeSearchPlayer(search_depth=2, branching_factor=10, random_action_p=0.02, value_function=model.get_board_state_moves_value_function(device))),
        #     (AlphaBetaPlayer(search_depth=2, play_to_lose=False, memory=memory), MiniMaxTreeSearchPlayer(search_depth=2, branching_factor=10, random_action_p=0.02, value_function=model.get_board_state_moves_value_function(device))),
        #     (MiniMaxTreeSearchPlayer(search_depth=2, branching_factor=10, random_action_p=0.2, value_function=model.get_board_state_moves_value_function(device)), MiniMaxTreeSearchPlayer(search_depth=2, branching_factor=10, random_action_p=0.2, value_function=model.get_board_state_moves_value_function(device))),
        #     (MiniMaxTreeSearchPlayer(search_depth=2, branching_factor=10, random_action_p=0.02, value_function=model.get_board_state_moves_value_function(device)), MiniMaxTreeSearchPlayer(search_depth=2, branching_factor=10, random_action_p=0.02, value_function=model.get_board_state_moves_value_function(device)))
        # ]
        # probas = normalize(np.array([
        #     0.05,
        #     0.1,
        #     0.1,
        #     0.3,
        #     0.45,
        # ]))

        if rng.choice([True, False]):
            white_player, black_player = players[rng.choice(np.arange(0, len(players)), p=probas)]
        else:
            black_player, white_player = players[rng.choice(np.arange(0, len(players)), p=probas)]

        print(white_player, black_player)
        game = ChessGame(white_player, black_player, cb_size)
        win_player = game.play()

        if i%50 == 0:
            input_target_lst = []
            for k, stats in memory.iter():
                b = stats.board_state
                tensor_board, tensor_meta_data = model.sparsify_board_state(b.board_a, b.colour, b.state_repetition_count, b.no_progress_count)
                tensor_board, tensor_meta_data = tensor_board.float().to(device), tensor_meta_data.float().to(device)

                board_stats = np.array([stats.win_count, stats.draw_count, stats.loss_count])

                target_val = None
                if board_stats[1] == np.sum(board_stats): # This board state only draws
                    target_val = - 0.01
                elif board_stats[0] >= board_stats[2]: # This board state has potential for winning
                    target_val = 1
                else: # This board state is losing very frequently
                    target_val = -1

                # target_val = None
                # max_ix = np.argmax(board_stats)
                # if max_ix == 0: #Frequently winning
                #     target_val = 1
                # elif max_ix == 1: #Frequently drawing
                #     target_val = -0.01
                # elif max_ix == 2: # Frequently losing
                #     target_val = -1
                
                input_target_lst.append((tensor_board, tensor_meta_data, torch.tensor(target_val, dtype=tensor_board.dtype)))
            memory.clear()

            optimize_reward(model, optimizer, device, input_target_lst)

        if i%100 == 0:
            dir_path = "res/NN_RL/reward-train/"
            if save_dir:
                dir_path = save_dir
            fn = f"model_{i//100}.ptm"
            os.makedirs(dir_path, exist_ok=True)
            torch.save(model, dir_path + fn)


def test_network(disk_path, cb_size, num_test=25, tree_search=False):
    rng, device, _, optimizer, memory = network_setup(cb_size)
    model = torch.load(disk_path, map_location=torch.device('cpu')).to(device)

    test_random = [0, 0, 0]

    for i in range(num_test):

        nn_player = None
        if tree_search:
            # nn_player = AlphaBetaTreeSearchPlayer(search_depth=2, value_function=model.get_board_state_value_function(device))
            nn_player = MiniMaxTreeSearchPlayer(search_depth=2, branching_factor=10, value_function=model.get_board_state_moves_value_function(device))
            # nn_player = MiniMaxTreeSearchPlayer(search_depth=2, value_function=None)
        else:
            nn_player = NNPlayer(model, device)
        enemy = RandomPlayer()
        # enemy = MiniMaxTreeSearchPlayer(search_depth=2, value_function=model.get_board_state_moves_value_function(device))

        if i%2 == 0:
            white_player, black_player = nn_player, enemy
        else:
            black_player, white_player = enemy, nn_player

        game = ChessGame(white_player, black_player, cb_size)
        win_player = game.play()

        if i%2 == 0:
            test_random[1+win_player] += 1
        else:
            test_random[2-(1+win_player)] += 1

        print(f"Testing against random - Iteration  : {i:5,d} | Wins: {test_random[2]} Draws: {test_random[1]} Losses: {test_random[0]}")


def optimize(model, optimizer: optim.Optimizer, device, input_target_lst, batch_size=128):
    print(f"\nOptimize...    ({len(input_target_lst)} inputs)")
    model.train()

    rng = np.random.default_rng()
    rng.shuffle(input_target_lst)

    counter = 0
    while input_target_lst:
        counter += 1
        print(f"\rbatch {counter}     ", end="")
        batch, input_target_lst = input_target_lst[:batch_size], input_target_lst[batch_size:]

        inputs_board = torch.stack([t[0] for t in batch]).to(device)
        input_meta_data = torch.stack([t[1] for t in batch]).to(device)
        targets = torch.stack([t[2] for t in batch], dim=-1)[:, None].to(device)

        vals = model(inputs_board, input_meta_data)

        criterion = nn.SmoothL1Loss()
        loss = criterion(vals, targets)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    print("\r            ")

def optimize_reward(model, optimizer: optim.Optimizer, device, input_target_lst, batch_size=128):
    print(f"\nOptimize [reward addition]...    ({len(input_target_lst)} inputs)")
    model.train()

    rng = np.random.default_rng()
    rng.shuffle(input_target_lst)

    counter = 0
    while input_target_lst:
        counter += 1
        print(f"\rbatch {counter}     ", end="")
        batch, input_target_lst = input_target_lst[:batch_size], input_target_lst[batch_size:]

        inputs_board = torch.stack([t[0] for t in batch]).to(device)
        input_meta_data = torch.stack([t[1] for t in batch]).to(device)
        targets = torch.stack([t[2] for t in batch], dim=-1)[:, None].to(device)

        vals = model(inputs_board, input_meta_data)
        vals_detach = vals.detach()

        criterion = nn.SmoothL1Loss()
        loss = criterion(vals, vals_detach+targets)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    print("\r            ")



def neural_net_player_random_weighted_enemy(rng, value_net, memory, device):
    ally_player = NNPlayer(value_net, memory, device)

    enemy_players = [
        AlphaBetaPlayer(search_depth=2, play_to_lose=True),
        AlphaBetaPlayer(search_depth=1, play_to_lose=True),
        RandomPlayer(),
        AlphaBetaPlayer(search_depth=1),
        AlphaBetaPlayer(search_depth=2),
        "NNPlayer"
        ]
    enemy_player_weights = np.array([
        0.17,
        0.17,
        0.27,
        0.17,
        0.17,
        0.05
    ])
    enemy_player_weights = enemy_player_weights / np.sum(enemy_player_weights) # Sum to 1
    enemy_player = rng.choice(enemy_players, p=enemy_player_weights)
    if enemy_player == "NNPlayer":
        enemy_player = NNPlayer(value_net, memory, device)

    ally_colour = rng.choice(np.array([Colour.WHITE, Colour.BLACK]))

    if ally_colour == Colour.WHITE:
        return (ally_player, enemy_player)
    else:
        return (enemy_player, ally_player)

def normalize(a: np.ndarray):
    return a / np.sum(a)