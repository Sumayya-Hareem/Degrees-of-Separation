import itertools
import random


class Minesweeper:
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


class Sentence:
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
        # If the number of cells equals the count of mines,
        # then every cell in this sentence MUST be a mine.
        if len(self.cells) == self.count and self.count != 0:
            return self.cells
        return set()

    def known_safes(self):
        # If the count is 0, every cell in this sentence MUST be safe.
        if self.count == 0:
            return self.cells
        return set()

    def mark_mine(self, cell):
        # If cell is in sentence, remove it and decrease count
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        # If cell is in sentence, just remove it (count stays same)
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI:
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

    def add_knowledge(self, cell, count):
        # 1. Mark move as made and safe
        self.moves_made.add(cell)
        self.mark_safe(cell)

        # 2. Add new sentence to knowledge base
        neighbors = set()
        mine_count = count

        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                neighbor = (i, j)
                if neighbor == cell:
                    continue

                if 0 <= i < self.height and 0 <= j < self.width:
                    if neighbor in self.mines:
                        mine_count -= 1
                    elif neighbor not in self.safes:
                        neighbors.add(neighbor)

        new_sentence = Sentence(neighbors, mine_count)
        self.knowledge.append(new_sentence)

        # 3. Recursive Inference Loop
        # We loop because marking a safe cell might simplify another sentence
        # which might reveal a new mine, and so on.
        made_progress = True
        while made_progress:
            made_progress = False

            # Collect all known safes/mines from sentences
            safes = set()
            mines = set()
            for sentence in self.knowledge:
                safes.update(sentence.known_safes())
                mines.update(sentence.known_mines())

            if safes:
                made_progress = True
                for s in safes:
                    self.mark_safe(s)
            if mines:
                made_progress = True
                for m in mines:
                    self.mark_mine(m)

            # Subset Inference: set2 - set1 = count2 - count1
            for s1 in self.knowledge:
                for s2 in self.knowledge:
                    if s1.cells and s2.cells and s1.cells < s2.cells:
                        new_s = Sentence(s2.cells - s1.cells, s2.count - s1.count)
                        if new_s not in self.knowledge:
                            self.knowledge.append(new_s)
                            made_progress = True

            # Clean up empty sentences
            self.knowledge = [s for s in self.knowledge if s.cells]

    def make_safe_move(self):
        # Return a safe cell that hasn't been clicked yet
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        return None

    def make_random_move(self):
        # List all possible coordinates
        candidates = []
        for i in range(self.height):
            for j in range(self.width):
                cell = (i, j)
                if cell not in self.moves_made and cell not in self.mines:
                    candidates.append(cell)

        return random.choice(candidates) if candidates else None
