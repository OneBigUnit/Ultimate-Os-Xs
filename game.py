from formatting import Text, Terminal
import errors


class Board:

    def __init__(self, game, _type="Sub", board_tile=" "):
        self.empty_tile = board_tile
        self._type = _type
        self.board = [[Board(game) if _type.lower() == "super" else board_tile for row_n in range(3)] for column_n in
                      range(3)]
        self.active_master = None
        self.game = game
        self.occupied_space_error = errors.CustomError("OccupiedSpaceError", "The requested space is already occupied")
        self.is_completed = False
        self.winning_tile = None

    def game_is_over(self):
        if self._type != "Super": return
        checks = []
        board = [item.winning_tile for sublist in self.board for item in sublist]
        board = [board[idx: idx + 3] for idx in range(0, len(board), 3)]
        for row in board:
            checks.append(row)
        checks.append([board[0][0], board[1][1], board[2][2]])
        checks.append([board[2][0], board[1][1], board[0][2]])
        for i in range(3):
            checks.append([board[x][i] for x in range(3)])
        for check in checks:
            if self.empty_tile not in check and len(set(check)) == 1:
                return True

    def get_slot(self, idx):
        if idx < 1 or idx > 9:
            raise IndexError("Invalid Square")

        row, column = (idx - 1) // 3, (idx - 1) % 3
        return self.board[row][column]

    def set_slot(self, idx, character):
        if idx < 1:
            raise IndexError("Invalid Square")

        if self.get_slot(idx) != self.empty_tile:
            self.occupied_space_error.throw()

        row, column = (idx - 1) // 3, (idx - 1) % 3
        self.board[row][column] = character

        if not self.is_completed:
            self.game.board.active_master = idx
        else:
            self.game.board.active_master = None

        if self.is_won():
            self.is_completed = True

    def get_list_conversion(self):
        boards = []
        for super_triplet in self.board:
            for idx in range(3):
                for sub_board in super_triplet:
                    boards.append(sub_board.board[idx])
        return [boards[idx: idx + 3] for idx in range(0, len(boards), 3)]

    def is_won(self):
        if self._type != "Sub": return
        checks = []
        for row in self.board:
            checks.append(row)
        checks.append([self.board[0][0], self.board[1][1], self.board[2][2]])
        checks.append([self.board[2][0], self.board[1][1], self.board[0][2]])
        for i in range(3):
            checks.append([self.board[x][i] for x in range(3)])
        for check in checks:
            if self.empty_tile not in check and len(set(check)) == 1:
                self.winning_tile = check[0]
                return True

    def __str__(self):
        boards = self.get_list_conversion()

        lst_rep = []
        for board in boards:
            temp = []
            for i, triplet in enumerate(board):
                temp.append(Text.dim(Text.green(" | ")).join(board[i]))
            lst_rep.append(temp)

        result = " "
        for idx, triplet in enumerate(lst_rep):
            result += Text.bold(Text.red(" | ")).join(triplet) + "\n"
            if (idx + 1) % 3 == 0 and (idx != 0 and idx != 8):
                result += f"{Text.bold(Text.red('- ')) * 18}" + "\n "
            else:
                if idx != 8:
                    result += Text.dim(Text.green(f"{'- ' * 18}"[:-1])) + "\n "

        return result


class Player:

    def __init__(self, _id):
        self._id = _id
        self.character = ["O", "X"][self._id]

    def play_turn(self, board, active_master):
        original_active_master = active_master
        if active_master is None:
            try:
                active_master = int(input("\nGive the number of the board you would like to place in:\t"))
            except ValueError:
                input(Text.warning("\nThat is not an integer! Please pick again. Press enter to continue...\t"))
                return self.play_turn(board, original_active_master)
        try:
            slot = board.get_slot(active_master)
        except IndexError:
            input(Text.warning("\nThat square does not exist! Please pick again. Press enter to continue...\t"))
            return self.play_turn(board, original_active_master)
        if slot.is_completed:
            if original_active_master is None:
                input(
                    Text.warning("\nThat square is already occupied! Please pick again. Press enter to continue...\t"))
            return self.play_turn(board, None)
        try:
            slot.set_slot(int(input("\nGive the number of the square you would like to place in:\t")), self.character)
        except board.get_slot(active_master).occupied_space_error.exception:
            input(Text.warning("\nThat square is already occupied! Please pick again. Press enter to continue...\t"))
            return self.play_turn(board, original_active_master)
        except ValueError:
            input(Text.warning("\nThat is not an integer! Please pick again. Press enter to continue...\t"))
            return self.play_turn(board, original_active_master)
        except IndexError:
            input(Text.warning("\nThat square does not exist! Please pick again. Press enter to continue...\t"))
            return self.play_turn(board, original_active_master)


class Game:

    def __init__(self):
        self.board = Board(self, _type="Super", board_tile=None)
        self.players = [Player(n) for n in range(2)]
        self.game_over = False

    def play_round(self):
        for player in self.players:
            print(Text.underline(Text.bold(f"\nPlayer {player._id + 1}'s Turn!")))
            player.play_turn(self.board, self.board.active_master)
            if self.board.game_is_over():
                self.game_over = True
            yield player

    @Terminal.click_clear
    def print_board(self):
        print(self.board)

    def play(self):
        self.print_board()
        while not self.game_over:
            for active_player in self.play_round():
                self.print_board()
                if self.game_over:
                    print(Text.bold(Text.success(f"\nGame Over!\n\nPlayer {active_player._id + 1} wins!")))
