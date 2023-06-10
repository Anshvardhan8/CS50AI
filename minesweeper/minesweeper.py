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
        # This function returns a set of all the cells in self.cells known to be mines by confirming that the count of mines in the sentence is equal to the number of cells in the sentence.

        if len(self.cells) == self.count and self.count != 0:
            return self.cells
        else:
            return set()
 
    def known_safes(self):
    # This function returns a set of all the cells in self.cells known to be safe by confirming that the count of mines in the sentence is equal to 0.
        if self.count == 0:
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
    #If cell is in the sentence, the function should update the sentence if cell is mine by removing the cell and decreasing count.
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
        else:
            return
        
    def mark_safe(self, cell):
    #If cell is in the sentence, the function should update the sentence if cell is safe by removing the cell and count remains same.
        if cell in self.cells:
            self.cells.remove(cell)
        else:
            return

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

    def add_knowledge(self, cell, count):
    #The function should mark the cell as a move that has been made and mark the cell as safe and update any sentences that contain the cell as well. If any of the sentences become empty, they should be removed from the knowledge base. If any of the sentences become safes, then the cell should be marked as safe, and any sentences that contain the cell should be updated. Similarly, if any of the sentences become mines, then the cell should be marked as a mine, and any sentences that contain the cell should be updated.
        mines = 0
        undet = []
        self.moves_made.add(cell)
        self.mark_safe(cell)
        for i in range (cell[0] - 1, cell[0] + 2): # We go through all the cells around the cell we clicked on
            for j in range (cell[1] - 1, cell[1] + 2):
                if (i,j) in self.mines:# If the cell is a mine, we add 1 to the mines counter
                    mines += 1
                if (i,j) not in self.mines and (i,j) not in self.safes and 0 <= i < self.height and 0 <= j < self.width: # If the cell is not a mine and not a safe cell, we add it to the undetected cells list
                    undet.append((i,j))
        self.knowledge.append(Sentence(undet, count - mines))# We add the new sentence to the knowledge base that contains the undetected cells and the number of mines around the cell we clicked on minus the number of mines we already know about
        newsentence = Sentence(undet, count - mines)

        for sentence in self.knowledge: # we go through all the sentences in the knowledge base to update them
            if sentence.known_mines(): # If the sentence contains mines, we update the mines
                for cell in sentence.known_mines().copy():
                    self.mark_mine(cell)
            if sentence.known_safes():# If the sentence contains safes, we update the safes
                for cell in sentence.known_safes().copy():
                    self.mark_safe(cell)

        for sentence in self.knowledge: # We go through all the sentences in the knowledge base to update them by 
            if newsentence.cells.issubset(sentence.cells) and sentence.count > 0 and newsentence.count > 0 and newsentence != sentence:
                news = sentence.cells.difference(newsentence.cells)
                newc = Sentence(list(news), sentence.count - newsentence.count)
                self.knowledge.append(newc)


    def make_safe_move(self):
        #This function should return a move (i, j) that is known to be safe by going through the set of safe moves, and returning the first safe move that hasn't already been made.
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        else:
            return None

    def make_random_move(self):
    # This function should return a random move (i, j) from the set of cells that are not known to be mines or safe. The move should be returned as a tuple of (i, j).
        moves = []
        for i in range (self.height):
            for j in range (self.width):
                if (i,j) not in self.moves_made and (i,j) not in self.mines:
                    moves.append((i,j))
        if len(moves) == 0:
            return None
        else:
            return random.choice(moves)
        





