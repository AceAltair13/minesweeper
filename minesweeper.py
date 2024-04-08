"""
Minesweeper

Group Members:

╔═══════╦════════════════════════════╦════════════╗
║ Sr No ║            Name            ║ Student ID ║
╠═══════╬════════════════════════════╬════════════╣
║   1   ║ Tirth Shailesh Thoria      ║ 031149064  ║
║   2   ║ Avantika Singh             ║ 031376590  ║
║   3   ║ Laksh Chandrabhan Jadhwani ║ 032166249  ║
╚═══════╩════════════════════════════╩════════════╝

"""

import copy
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
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        return self.cells if self.count == len(self.cells) else None

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        return self.cells if self.count == 0 else None

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.count -= 1
            self.cells.remove(cell)

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)
        else:
            pass


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
        # Record the move
        self.moves_made.add(cell)

        # Mark the cell as safe and update the knowledge base
        self.mark_safe(cell)

        # Create a new sentence based on the cell's neighbors and the count of mines
        cells = set()
        adjusted_count = copy.deepcopy(count)
        neighbors = self.get_adjacent_cells(cell)

        for neighbor in neighbors:
            if neighbor in self.mines:
                adjusted_count -= 1
            elif neighbor not in self.safes:
                cells.add(neighbor)

        # Add the new sentence to the knowledge base if it's not empty
        if cells:
            self.knowledge.append(Sentence(cells, adjusted_count))

        # Update the knowledge base and perform additional inference
        self.knowledge_verification()
        self.inference_helper()

    def get_adjacent_cells(self, target_cell):
        """
        This method returns a set of cells that are adjacent to the given cell.
        """
        # returns cells close to arg cell by 1 cell
        neighboring_cells = set()

        for row in range(self.height):
            for column in range(self.width):
                if max(abs(target_cell[0] - row), abs(target_cell[1] - column)) == 1:
                    neighboring_cells.add((row, column))

        return neighboring_cells

    def knowledge_verification(self):
        """
        Check the knowledge base for new safe cells and mines, and update the knowledge base if possible.
        """
        # Create a copy of the knowledge base to avoid modifying the original while iterating
        knowledge_clone = copy.deepcopy(self.knowledge)

        # Iterate through each statement in the copied knowledge base
        for statement in knowledge_clone:
            # If the statement has no cells, remove it from the knowledge base
            if not statement.cells:
                if statement in self.knowledge:
                    self.knowledge.remove(statement)

            # Identify potential mines and safe cells
            potential_mines = statement.known_mines()
            potential_safes = statement.known_safes()

            # If a mine or safe cell is found, mark it and recheck the knowledge base
            if potential_mines:
                for mine in potential_mines:
                    self.mark_mine(mine)
                    self.knowledge_verification()
            if potential_safes:
                for safe in potential_safes:
                    self.mark_safe(safe)
                    self.knowledge_verification()

    def inference_helper(self):
        """
        This method performs additional inference by looking for sentences in the knowledge base
        that are subsets of other sentences, and then creating new sentences based on the differences.
        """
        # Create a copy of the knowledge base to avoid modifying it while iterating over it
        for sentence1 in self.knowledge:
            for sentence2 in self.knowledge:
                # check if sentence 1 is subset of sentence 2
                if sentence1.cells.issubset(sentence2.cells):
                    new_cells = sentence2.cells - sentence1.cells
                    new_count = sentence2.count - sentence1.count
                    new_sentence = Sentence(new_cells, new_count)
                    mines = new_sentence.known_mines()
                    safes = new_sentence.known_safes()
                    if mines:
                        for mine in mines:
                            self.mark_mine(mine)
                    if safes:
                        for safe in safes:
                            self.mark_safe(safe)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for cell in self.safes - self.moves_made:
            return cell

        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """

        # Calculate the total number of cells on the board
        total_cells = self.width * self.height

        # Try to find a valid move
        while total_cells > 0:
            total_cells -= 1

            # Choose a random cell
            row = random.randrange(self.height)
            column = random.randrange(self.width)
            cell = (row, column)

            # If the cell has not been chosen yet and is not known to be a mine, return it
            if cell not in self.moves_made | self.mines:
                return cell

        # If there are no valid moves left, return None
        return None
