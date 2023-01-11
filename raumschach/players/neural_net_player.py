import random
from torch import cuda
from torch import nn
import numpy as np
import torch
from raumschach.board import ChessBoard

from raumschach.board_state import BoardState
from raumschach.figures import FIGURES
from raumschach.players.player import Player


class MoveValueClassifierPlayer(Player):

    cb_size: int
    num_piece_types: int

    is_train: bool
    device: str
    model: nn.Module
    # loss_fn
    optimizer: torch.optim
    fig_id_map: dict
    sparse_legal: list
    sparse_illegal: list

    def __init__(self, cb_size: int, num_piece_types: int, is_training: bool=True, use_cuda: bool=True):
        super().__init__()
        self.cb_size = cb_size
        self.num_piece_types = num_piece_types
        self.is_train = is_training
        self.device = "cuda" if (use_cuda and cuda.is_available()) else "cpu"
        self.model = CombinedValueClassifierNN(cb_size, num_piece_types)
        self.model.to(self.device)
        
        self.loss_fn = nn.MSELoss()
        self.optimizer = torch.optim.SGD(self.model.parameters(), lr=1e-5)

        self.sparse_legal = []
        self.sparse_illegal = []

        self.fig_id_map = dict()
        for i in range(len(FIGURES)):
            self.fig_id_map[FIGURES[i].id] = i
            self.model.train()

    def send_action(self, board_state: BoardState):
        legal_moves = np.concatenate((board_state.passives, board_state.captures), axis=0)
        for sparse_move in self.sparsify(board_state, legal_moves):
            self.sparse_legal.append(sparse_move)
        all_passives, all_captures = ChessBoard.get_passives_captures(board_state.board_a, colour=board_state.colour, simulate_safe_moves=False)
        illegal_moves = []
        for move in np.concatenate((all_passives, all_captures), axis=0):
            if not np.any(np.all(move == legal_moves, axis=1), axis=0):
                illegal_moves.append(move)
        if illegal_moves:
            for sparse_move in self.sparsify(board_state, illegal_moves):
                self.sparse_illegal.append(sparse_move)

        self.model.eval()
        vals, legal_probas = self.model(self.sparsify(board_state, legal_moves))

        max_value = np.argmax(vals.detach().numpy())
        if type(max_value) == type(np.ndarray):
            max_value = max_value[0]
        move = legal_moves[max_value]
        return move

    def receive_reward(self, reward_value, move_history):
        pass

    def train(self):
        self.model.train()

        all_sparse_moves = []
        for move in self.sparse_legal:
            all_sparse_moves.append((1.0, move))
        for move in self.sparse_illegal:
            all_sparse_moves.append((0.0, move))
        self.sparse_legal = []
        self.sparse_illegal = []

        random.shuffle(all_sparse_moves)

        class_vals, moves = [ x[0] for x in all_sparse_moves ], [ x[1] for x in all_sparse_moves ]

        # class_vals = torch.tensor(class_vals, device=self.device)
        # moves = torch.tensor(moves, device=self.device)
        class_vals = torch.from_numpy(np.array(class_vals, dtype=np.single))
        class_vals = class_vals.to(self.device)
        moves = torch.from_numpy(np.stack(moves, axis=0))
        moves = moves.to(self.device)

        len_moves = len(moves)
        batch_size = 1000
        # batch_size = 10
        i = 0
        while i < len_moves:
            vals, legal_probas = self.model(moves[i:i+batch_size])
            loss = torch.nn.functional.mse_loss(legal_probas[:, 0], class_vals[i:i+batch_size])
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
            i += batch_size

    def test(self):
        self.model.eval()

        all_sparse_moves = []
        for move in self.sparse_legal:
            all_sparse_moves.append((1.0, move))
        for move in self.sparse_illegal:
            all_sparse_moves.append((0.0, move))
        self.sparse_legal = []
        self.sparse_illegal = []

        random.shuffle(all_sparse_moves)

        class_vals, moves = [ x[0] for x in all_sparse_moves ], [ x[1] for x in all_sparse_moves ]

        # class_vals = torch.tensor(class_vals, device=self.device)
        # moves = torch.tensor(moves, device=self.device)
        class_vals = torch.from_numpy(np.array(class_vals, dtype=np.single))
        class_vals = class_vals.to(self.device)
        moves = torch.from_numpy(np.stack(moves, axis=0))
        moves = moves.to(self.device)

        vals, legal_probas = self.model(moves)

        moves = moves.detach().numpy()
        class_vals = class_vals.detach().numpy()
        legal_probas = legal_probas.detach().numpy()
        vals = vals.detach().numpy()

        legal_proba_lst = []
        legal_val_lst = []
        illegal_proba_lst = []
        illegal_val_lst = []

        for i in range(len(moves)):
            if (class_vals[i]) == 0:
                illegal_proba_lst.append(np.average(np.array(legal_probas[i])))
                illegal_val_lst.append(np.average(np.array(vals[i])))
            else:
                legal_proba_lst.append(np.average(np.array(legal_probas[i])))
                legal_val_lst.append(np.average(np.array(vals[i])))

        print()
        print("Test Result")
        print("Average probability given to legal moves:  ", np.average(np.array(legal_proba_lst)))
        print("Average probability given to illegal moves:", np.average(np.array(illegal_proba_lst)))
        print()
        print("Average value given to legal moves:  ", np.average(np.array(legal_val_lst)))
        print("Average value given to illegal moves:", np.average(np.array(illegal_val_lst)))
        print()


    def sparsify(self, board_state: BoardState, moves: np.ndarray):
        len_figures = len(FIGURES)
        ally_colour = board_state.colour
        enemy_colour = ally_colour*-1
        cb_arrays_shape = tuple([len_figures] + list(board_state.board_a.shape))

        sparse_arrays = []

        ally_arrays = np.zeros(cb_arrays_shape, dtype=np.single)
        enemy_arrays = np.zeros(cb_arrays_shape, dtype=np.single)
        board_state_arrays = np.zeros(tuple([2] + list(board_state.board_a.shape)), np.single)
        from_move_arrays = np.zeros(cb_arrays_shape, dtype=np.single)
        to_move_arrays = np.zeros(cb_arrays_shape, dtype=np.single)

        for figure in FIGURES:
            ally_arrays[self.fig_id_map[figure.id]][board_state.board_a == figure.id*ally_colour] = 1
            enemy_arrays[self.fig_id_map[figure.id]][board_state.board_a == figure.id*enemy_colour] = 1

        board_state_arrays[0] = board_state.state_repetition_count/3
        board_state_arrays[1] = board_state.no_progress_count/50

        for move in moves:
            from_move_arrays = np.zeros(cb_arrays_shape, dtype=np.single)
            to_move_arrays = np.zeros(cb_arrays_shape, dtype=np.single)
            from_move_arrays[self.fig_id_map[abs(move[0])]][move[2]][move[3]][move[4]] = 1.0
            to_move_arrays[self.fig_id_map[abs(move[1])]][move[5]][move[6]][move[7]] = 1.0
            sparse_array = np.concatenate((ally_arrays, enemy_arrays, board_state_arrays, from_move_arrays, to_move_arrays), axis=0)
            sparse_arrays.append(sparse_array)

        
        return torch.from_numpy(np.stack(sparse_arrays, axis=0)).to(self.device)

class CombinedValueClassifierNN(nn.Module):

    cb_size: int
    num_piece_types: int
    
    def __init__(self, cb_size: int, num_piece_types: int):
        super().__init__()
        self.cb_size = cb_size
        self.num_piece_types = num_piece_types

        in_features = ((self.num_piece_types*4)+2)*(self.cb_size**3)

        self.preSplit = nn.Sequential(
            # nn.Linear(in_features, in_features),
            # nn.Tanh(),
            # nn.Conv3d(in_features, self.num_piece_types*(self.cb_size**3), self.cb_size*2),
            nn.Conv3d(30, 15, self.cb_size, padding=self.cb_size//2),
            # nn.Linear(in_features, self.num_piece_types*(self.cb_size**3)),
            nn.Tanh(),
            nn.Conv3d(15, 5, self.cb_size, padding=self.cb_size//2),
            nn.Tanh(),
            nn.Conv3d(5, 1, self.cb_size, padding=self.cb_size//2),
            nn.Tanh()
        )

        self.flatten = nn.Flatten()

        self.classifier = nn.Sequential(
            # nn.Linear(self.num_piece_types*(self.cb_size**3), self.num_piece_types*(self.cb_size**3)),
            # nn.Tanh(),
            nn.Linear(125, 100),
            nn.Sigmoid(),
            nn.Linear(100, 50),
            nn.Sigmoid(),
            nn.Linear(50, 1),
            nn.Sigmoid()
        )

        self.value_function = nn.Sequential(
            # nn.Linear(self.num_piece_types*(self.cb_size**3), self.num_piece_types*(self.cb_size**3)),
            # nn.Tanh(),
            nn.Linear(125, 100),
            nn.ReLU(),
            nn.Linear(100, 50),
            nn.ReLU(),
            nn.Linear(50, 1),
            nn.ReLU()
        )

    def forward(self, x):
        # print(x.shape)
        x = self.preSplit(x)
        # print(x.shape)
        x = self.flatten(x)
        class_proba = self.classifier(x)
        move_val = self.value_function(x)
        # raise Exception("Stop")
        return (move_val, class_proba)