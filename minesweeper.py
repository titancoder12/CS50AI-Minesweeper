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
        prints a text-based representation
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
        self.safes = set()
        self.mines = set()

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        mines = self.mines

        raise NotImplementedError

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        raise NotImplementedError

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.mines.add(cell)
            self.cells.remove(cell)
            self.count = self.count - 1
        return True
    
        # raise NotImplementedError

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.safes.add(cell)
            self.cells.remove(cell)
        return True
        #raise NotImplementedError


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
        # [1] Mark the cell as a move that has been made
        countc = count
        self.moves_made.add(cell)

        # [2] Mark the cell as safe
        self.safes.add(cell)

        # [3] Add a new sentence to the AI's knowledge base
        attempt_cellfield = {(cell[0]-1, cell[1]-1), (cell[0]-1, cell[1]), (cell[0]-1, cell[1]+1), (cell[0], cell[1]-1), (cell[0], cell[1]), (cell[0], cell[1]+1), (cell[0]+1, cell[1]-1), (cell[0]+1, cell[1]), (cell[0]+1, cell[1]+1)}
        cellfield = set()
        for cellf in attempt_cellfield:
            if not(cellf[0] < 0 or cellf[0] > 7) and not(cellf[1] < 0 or cellf[1] > 7):
                #print("CORNER")
                cellfield.add(cellf)

        sentence = Sentence(cells=cellfield, count=countc)
        self.knowledge.append(sentence)

        # [4] Mark any additional cells as safe or as mines
        safe_cells = set()
        mine_cells = set()
        """

        # See if any conclusions can be drawn from knowledge
        self.check_knowledge()

        # Mark mines
        if count == len(cellfield):
            mine_cells = cellfield
        
        for mine in mine_cells:
            self.mark_mine(mine)
        #print("mine:")
        #print(self.mines)
        
        # Mark safes
        surroundingmines_c = 0
        surroundingmines = set()
        for surroundingmine in cellfield:
            if surroundingmine in self.mines:
                surroundingmines_c += 1
                surroundingmines.add(surroundingmine)
        #print("mines:")
        #print(surroundingmines)
        if count == surroundingmines_c:
            #("reached condition")
            safe_cells = cellfield
            cellfield_c = cellfield.copy()
            for cellf in cellfield_c:
                if cellf in surroundingmines:
                    safe_cells.remove(cellf)
        if count == 0:
            for cell_l in cellfield:
                self.mark_safe(cell_l)
        for safe_cell in safe_cells:
            self.mark_safe(safe_cell)"""
        #print("safe:")
        #print(self.safes)

        # Set and Subset Division
        while True:
            # Mark mines
            if count == len(cellfield):
                mine_cells = cellfield
        
            for mine in mine_cells:
                self.mark_mine(mine)
            #print("mine:")
            #print(self.mines)
        
            # Mark safes
            surroundingmines_c = 0
            surroundingmines = set()
            for surroundingmine in cellfield:
                if surroundingmine in self.mines:
                    surroundingmines_c += 1
                    surroundingmines.add(surroundingmine)
            #print("mines:")
            #print(surroundingmines)
            if count == surroundingmines_c:
                #print("reached condition")
                safe_cells = cellfield
                cellfield_c = cellfield.copy()
                for cellf in cellfield_c:
                    if cellf in surroundingmines:
                        safe_cells.remove(cellf)
            if count == 0:
                for cell_l in cellfield:
                    self.mark_safe(cell_l)
            for safe_cell in safe_cells:
                self.mark_safe(safe_cell)

            old_knowledge = self.knowledge.copy()
            self.check_knowledge()

            for i in range(len(self.knowledge)):
                for j in range(len(self.knowledge) - 1):
                    j += 1
                    set1 = self.knowledge[i]
                    set2 = self.knowledge[j]
                    if (set1.cells != set2.cells):
                        if (set1.cells).issubset(set2.cells):
                            #print("found subset")
                            #print(str(set1.cells) +" issubset" + str(set2.cells))
                            newset = (set2.cells).difference(set1.cells)
                            newcount = set2.count - set1.count
                            newsentence = Sentence(cells=newset, count=newcount)
                            if (newsentence != set1) and (newsentence != set2) and (newsentence not in self.knowledge):
                                self.knowledge.append(newsentence)      
                        elif (set2.cells).issubset(set1.cells):
                            #print("found subset")
                            #print(str(set2.cells) + "issubset" + str(set1.cells))
                            newset = (set1.cells).difference(set2.cells)
                            newcount = set1.count - set2.count
                            newsentence = Sentence(cells=newset, count=newcount)
                            if (newsentence != set1) and (newsentence != set2) and (newsentence not in self.knowledge):
                                self.knowledge.append(newsentence)   
            if old_knowledge == self.knowledge:
                break

        # Return status
        #print(self.safes.difference(self.moves_made))
        return True
                        
        #raise NotImplementedError
    
    def check_knowledge(self):
        for sentence in self.knowledge:
            if len(sentence.cells) == 1:
                if sentence.count == 0:
                    #print("safe found")
                    self.mark_safe(list(sentence.cells)[0])
                if sentence.count >= 1:
                    #print("mine found")
                    self.mark_mine(list(sentence.cells)[0])
            elif len(sentence.cells) == sentence.count:
                for cell in sentence.cells.copy():
                    self.mark_mine(cell)
            elif sentence.count == 0:
                for cell in sentence.cells.copy():
                    self.mark_safe(cell)
        return True

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for safe in self.safes:
            if safe not in self.moves_made:
                return safe
        return None
        #raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        available_moves = [(i, j) for i in range(8) for j in range(8) if (i, j) not in self.moves_made and (i, j) not in self.mines]
        if available_moves:
            return random.choice(available_moves)
        return None


        #raise NotImplementedError
