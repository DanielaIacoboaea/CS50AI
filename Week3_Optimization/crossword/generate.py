import sys
from collections import Counter
import random
import copy

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())


    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        
        for variable in self.domains:
            for word in self.domains[variable].copy():
                if not len(word) == variable.length:
                    self.domains[variable].remove(word)



    def character_match(self, j, x_char, y):
        """
        Check if i'th character of x matches the j'th character of y,
        for each word in y's domain of values
        """
        
        # if we found a match return true
        for word in self.domains[y]:
            if word[j] == x_char:
                return True

        # otherwise signal that we can remove the word from x's domain of values
        # because no corresponding value for y is possible
        return False



    def count_character_no_match(self, j, x_char, x_char_count, y):
        """
        Return how many values from y's domain the current value from x's domain 
        will exclude.
        """
        
        # include in the count how many values the current value from x's domain 
        # already excluded from other variables
        count = x_char_count

        # count the words that should overlap and they don't
        for word in self.domains[y]:
            if word[j] != x_char:
                count += 1

        return count



    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        
        # check if the variables x and y overlap 
        overlap = self.crossword.overlaps[x, y]
        revised = False
        
        # if they don't overlap, nothing will be changed in x's domain
        if overlap is None:
           return revised
        else:
            # otherwise, get the index for the letters that should overlap
            # letter at index i of x should overlap with letter at index j for y
            i = overlap[0]
            j = overlap[1]


        # for every letter at index i for every word in x's domain 
        # check if it has a match (same letter) in any of y's words at index j 
        for word in self.domains[x].copy():
            char = word[i]
            if not self.character_match(j, char, y):
                self.domains[x].remove(word)
                revised = True
        return revised



    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        
        # add all arcs (variables that overlap) in a queue
        queue = []

        if arcs is not None:
            queue = arcs.copy()
        else:
            for variable in self.crossword.variables:
                neighbours = self.crossword.neighbors(variable)
                if neighbours:
                    for neighbor in neighbours:
                        queue.append((variable, neighbor))
        
        # for each arc, enforce arc consistency
        while queue:
            arc = queue.pop(0)
            if self.revise(arc[0], arc[1]):
                if len(self.domains[arc[0]]) == 0:
                    # if a variable's domain becomes empty, the problem has no solution
                    return False
                neighbours = self.crossword.neighbors(arc[0])
                if neighbours:
                    for neighbor in neighbours:
                        queue.append((arc[0], neighbor))
        return True




    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        
        # check if the number of variables within the assigment is the same 
        # as the total number of variables in the crossword
        if len(assignment) != len(self.crossword.variables):
            return False

        return True



    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
           
        # check if the words have duplicates
        # check if they have the same length as their variable
        words = []

        for variable in assignment:
            if variable.length != len(assignment[variable]):
                    return False
            words.append(assignment[variable])
        

        count = Counter(words)

        # if a word appears more than once, then it is a duplicate
        for word in count:
            if count[word] != 1:
                return False

        # check if neighbouring variables have the same letter at the overlap index
        for variable in assignment:
            neighbours = self.crossword.neighbors(variable)
            if neighbours:
                for neighbor in neighbours:
                    # only check if the neighbour is within the assigment as well
                    if neighbor in assignment:
                        overlap = self.crossword.overlaps[variable, neighbor]
                        i = overlap[0]
                        j = overlap[1]
                        if assignment[variable][i] != assignment[neighbor][j]:
                            return False

        return True




    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
       
        values = dict()
        unassigned_variables = []

        # select the variables that don't have anything assigned yet
        for variable in self.crossword.variables:
            if variable not in assignment:
                unassigned_variables.append(variable)
        
        # initialize a count from 0 for each possible value within the var's domain
        for word in self.domains[var]:
            values.update({word: 0})
        
        # check if var has any neighbours
        neighbours = self.crossword.neighbors(var)

        if neighbours:
            for neighbor in neighbours:
                # if the neighbours are not present in the assigment
                # update the count for how many possibile words within the neighbour's domains
                # each word will eliminate
                if neighbor in unassigned_variables:
                    overlap = self.crossword.overlaps[var, neighbor]
                    i = overlap[0]
                    j = overlap[1]
                    for word in values:
                        get_no_matched = self.count_character_no_match(j, word[i], values[word], neighbor)
                        values[word] += get_no_matched
        

        # sort the count for each word so that it will eliminate 
        # the min number of possible words from the neighbour's domains 
        sort_asc = sorted(values.items(), key=lambda value: value[1])
        sorted_values = [value[0] for value in sort_asc]
       
        # if the variable does not have any neighbours
        # sort the list of possibile values randomly
        if not neighbours:
            random.shuffle(sorted_values)

        return sorted_values



    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        
        # keep track of the number of possible values within 
        # each unassigned variable's domain
        unassigned_variables = []
        count_domains = []
        min_equal_domains = []
        degrees = []
        max_equal_degrees = []

        # get the unassigned variables
        for variable in self.crossword.variables:
            if variable not in assignment:
                unassigned_variables.append(variable)
        
        # get the number of values within each unassigned variable's domain
        for variable in unassigned_variables:
            count_domains.append(len(self.domains[variable]))

        # get the minim number of values within each unassigned variable's domain
        min_domain = min(count_domains)

        # check if it's a tie among different variables 
        equal_domains = Counter(count_domains)
       
        # if it's not a tie and only one variable has the min num of values in it's domain
        # return the variable 
        if equal_domains[min_domain] == 1:
            for variable in unassigned_variables:
                if len(self.domains[variable]) == min_domain:
                    return variable
        else:
            # otherwise compute the degree for all the variables that have the min number of values
            # within their domain
            for variable in unassigned_variables:
                if len(self.domains[variable]) == min_domain:
                    min_equal_domains.append(variable)
            for variable in min_equal_domains:
                neighbours = self.crossword.neighbors(variable)
                degrees.append(len(neighbours))

            # get the max number of degrees 
            max_degree = max(degrees)

            # check if more than 1 variable have the same max num of degrees
            equal_degrees = Counter(degrees)

            # if only one variable has the max degree,
            # return the variable 
            if equal_degrees[max_degree] == 1:    
                for variable in min_equal_domains:
                    if len(self.crossword.neighbors(variable)) == max_degree:
                        return variable
            else:
                # otherwise pick a random variable within tied 
                # variables (same min number of values within their domain) and
                # same degree
                for variable in min_equal_domains:
                    if len(self.crossword.neighbors(variable)) == max_degree:
                        max_equal_degrees.append(variable)
                return random.choice(max_equal_degrees)



    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        # if we found a solution, return it
        if self.assignment_complete(assignment):
            return assignment
        
        # pick an anassigned variable
        variable = self.select_unassigned_variable(assignment)

        # get their values
        values = self.order_domain_values(variable, assignment)

        # check for each value if it is a consistent assigment 
        for value in values:
            assignment[variable] = value
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if not result is None:
                    return result
            # otherwise, remove it
            assignment.pop(variable)

        return None



def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
