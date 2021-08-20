import copy
import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """
    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # Ignore the cell itself
                if (i, j) == cell:
                    continue
                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1
        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:  # all cells must be mines
            return set(self.cells)
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:  # none of the cells can be mines
            return set(self.cells)
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1  # we removed one of the mines, so count should decrease

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)  # no need to change count as no. of mines is same


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def get_neighbours(self, cell):
        """
        Returns the list of neighbours for any given cell
        """
        neighbours = set()
        x, y = cell
        for row in range(x - 1, x + 2):
            if (row >= 0) and (row < self.height):
                for col in range(y - 1, y + 2):
                    if (col >= 0) and (col < self.width) and (row, col) != cell and (row, col) not in self.safes:
                        neighbours.add((row, col))
        return neighbours

    def get_count_and_remove_mines(self, neighbours):
        """
        Finds the number of mines and subsequently removes mines from a list of neighbours
        """
        count = 0
        new_neighbours = neighbours.copy()
        for neighbour in neighbours:
            if neighbour in self.mines:
                count += 1
                new_neighbours.remove(neighbour)
        return count, new_neighbours

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # 1) mark the cell as a move that has been made
        self.moves_made.add(cell)
        # 2) mark the cell as safe
        self.mark_safe(cell)
        # 3) add a new sentence to the AI's knowledge base based on the value of 'cell' and 'count'
        neighbours = self.get_neighbours(cell)
        num_mines, neighbours = self.get_count_and_remove_mines(neighbours)
        count -= num_mines
        updated_sentence = Sentence(neighbours, count)
        if updated_sentence not in self.knowledge:  # we don't want to add a sentence that already exists
            self.knowledge.append(updated_sentence)
        # 4) mark any additional cells as safe or as mines if it can be concluded based on the AI's knowledge base
        for sentence in self.knowledge:
            safes = sentence.known_safes()
            mines = sentence.known_mines()
            for safe in safes:
                self.mark_safe(safe)  # marking known safes as safe in MineSweeperAI
            for mine in mines:
                self.mark_mine(mine)
        # 5) add any new sentences to the AI's knowledge base if they can be inferred from existing knowledge
        sentences = self.knowledge.copy()  # Copy
        for sentence1 in sentences:
            sentences.remove(sentence1)
            for sentence2 in sentences:
                if len(sentence1.cells) != 0 and len(sentence2.cells) != 0:
                    if len(sentence1.cells) > len(sentence2.cells):  # sentence 2 is a subset since its shorter that sentence 1
                        parent_set = sentence1.cells
                        subset = sentence2.cells
                        mine_count_diff = sentence1.count - sentence2.count  # checking for whether there are any mines in the subset not in the parent set by comparing the numbers of mines in each
                    elif len(sentence1.cells) < len(sentence2.cells):
                        parent_set = sentence2.cells
                        subset = sentence1.cells
                        mine_count_diff = sentence2.count - sentence1.count
                    else:
                        continue
                    if subset <= parent_set:  # subset needs to be smaller
                        diff = parent_set - subset  # get non-overlapping elements (exclusive to the parent set)
                        if len(diff) == 1:
                            if mine_count_diff == 0:
                                self.mark_safe(diff.pop())
                            elif mine_count_diff == 1:
                                self.mark_mine(diff.pop())
                        else:
                            self.knowledge.append(Sentence(diff, mine_count_diff))

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.
        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        move = None
        for safe_move in self.safes:
            if safe_move not in self.moves_made:  # we dont want to make a move we've already made
                move = safe_move
                self.moves_made.add(move)
                return move
        return move

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        moves_to_make = []
        for r in range(self.height):
            for c in range(self.width):
                cell = (r, c)
                if not(cell in self.moves_made or cell in self.mines):  # we don't want cells that have already been chosen or are mines
                    moves_to_make.append(cell)
            if not len(moves_to_make) == 0:  # choose a random move as long as there are still moves that can be made
                move = moves_to_make[random.randint(0, len(moves_to_make)-1)]  # select a random move form the moves that we can make
                self.moves_made.add(move)
                return move
