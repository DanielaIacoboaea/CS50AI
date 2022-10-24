import itertools
import random
import copy


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

        # count -> total number of mines in the sentence
        # if len of sentence = count
        # all the cells within the sentence are mines
        if len(self.cells) == self.count:
            return self.cells
        else:
            # otherwise, can't draw a conclusion about the mines in the sentence
            return None
       

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        
        # count -> total number of mines in the sentence
        # if count = 0 and there are cells in the cell
        # all the cells within the sentence are safe cells
        if self.count == 0 and len(self.cells) != 0:
            return self.cells
        else:
            # otherwise, can't draw a conclusion about the safe cells in the sentence
            return None


    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """

        # if the mine (cell) is within the sentence, remove it 
        # and decrease count of known mines for this sentence by 1
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1


    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """

        # if the safe cell is within the sentence, remove it
        # count remains the same because no mine was removed
        if cell in self.cells:
            self.cells.remove(cell)



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


    def neighbour_cells(self, cell):
        """
        Returns a set with all neighbour cells and the total number of 
        neighbours for the cell
        """

        neighbours = set()
        count_neighbours = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # add neighbour
                if 0 <= i < self.height and 0 <= j < self.width:
                    neighbours.add((i, j))
                    count_neighbours += 1
        
        return neighbours, count_neighbours



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

        # mark the cell as a move that has been made
        self.moves_made.add(cell)

        # mark the cell as safe
        self.mark_safe(cell)

        # add a new sentence to the AI's knowledge base
        # based on the value of `cell` and `count`
        new_sentence = set()
        new_count = copy.deepcopy(count)

        neighbours, count_neighbours = self.neighbour_cells(cell)

        # if the count is 0 
        # mark all neighbours as safe
        if new_count == 0:
            for neighbour in neighbours:
                if neighbour not in self.safes:
                    self.mark_safe(neighbour)

        # if the count = the total number of neighbours
        # it means all of them are mines 
        # mark all neighbours as mines
        elif new_count == count_neighbours:
            for neighbour in neighbours:
                if neighbour not in self.mines:
                    self.mark_mine(neighbour)
        else:
            # otherwise, for each neighbour:
            # check if we already know it is a mine cell or a safe cell
            # if true, don't add it to the new sentence for the knowledge base
            # otherwise, add it 
            for neighbour in neighbours:
                if neighbour not in self.mines and neighbour not in self.safes:
                    new_sentence.add(neighbour)
                elif neighbour in self.mines:
                    new_count -= 1
            self.knowledge.append(Sentence(new_sentence, new_count))

        # make inferrences from the AI's knowledge base
        # mark any additional cells as safe or as mines
        get_all_known_safes = set()
        get_all_known_mines = set()
        to_remove = []
        to_add = []

        # Basic idea:
        # for each sentence in the AI's knowledge base
        # if the sentence became safe(or all mines) after changes were made to it 
        # we can mark all cells from the sentence as safe(or mines) 
        # and remove them from other sentences
        # after we're done, we can remove the sentence itself 
        # because all relevant info has been transfered to self.safes(or self.mines)
        for sentence in self.knowledge:
            # if a sentence is empty
            # remove it
            if not sentence.cells:
                to_remove.append(sentence)

            get_known_safes = sentence.known_safes()
            get_known_mines = sentence.known_mines()

            # if the sentence is evaluated to safe
            # mark every cell from it as safe
            if get_known_safes:
                get_all_known_safes = get_all_known_safes.union(get_known_safes)
                for safe_cell in get_known_safes.copy():
                    self.mark_safe(safe_cell)
                to_remove.append(sentence)

            # if the sentence is evaluated to all mines
            # mark every cell from it as mine
            if get_known_mines:
                get_all_known_mines = get_all_known_mines.union(get_known_mines)
                for mine_cell in get_known_mines.copy():
                    self.mark_mine(mine_cell)
                to_remove.append(sentence)

        # update the safe cells and mines that we know about 
        # after inferences on the AI's knowledge base
        self.safes = self.safes.union(get_all_known_safes)
        self.mines = self.mines.union(get_all_known_mines)

        # remove any sentence that we don't need anymore
        if to_remove:
            for sentence in to_remove:
                self.knowledge.remove(sentence)

        # check on the cleaned knowledge base if we can draw some more conclusions 
        # if we know {A, B, C, D, E} = 2 and {D, E} = 1
        # add a new sentence to the knowledge base: 
        # {A, B, C} must be 1
        loop1 = self.knowledge.copy()
        loop2 = self.knowledge.copy()

        for i in range(len(loop1)):
            for j in range(i+1, len(loop2)):
                if loop1[i].cells.issubset(loop2[j].cells):
                    new_knowledge = loop2[j].cells.difference(loop1[i].cells)
                    new_count = loop2[j].count - loop1[i].count
                    to_add.append(Sentence(new_knowledge, new_count))
                elif loop2[j].cells.issubset(loop1[i].cells):
                    new_knowledge = loop1[i].cells.difference(loop2[j].cells)
                    new_count = loop1[i].count - loop2[j].count
                    to_add.append(Sentence(new_knowledge, new_count))

        # add new sentences
        if to_add:
            self.knowledge.extend(to_add)


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """

        # get all safe moves and check if the move has already been made
        # if we have available moves, generate a random one
        # otherwise, return None 
        moves = []

        for move in self.safes:
            if move not in self.moves_made:
                moves.append(move)
        
        if len(moves) == 0:
            return None
        else:
            generate_move = random.randrange(len(moves))
            return moves[generate_move]



    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """

        # get all available moves 
        # check if the cell is marked as mine 
        # if we have available moves, generate a random one
        # otherwise, return None 
        moves = []

        for i in range(0, self.height):
            for j in range(0, self.width):
                if (i, j) not in self.moves_made:
                    if (i, j) not in self.mines:
                        moves.append((i,j))

        if len(moves) == 0:
            return None
        else:
            generate_move = random.randrange(len(moves))
            return moves[generate_move]
