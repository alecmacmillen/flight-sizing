import itertools
import random

class Flight(object):
    """
    This object represents a flight of trainees at BMT or airmen at tech school
    and demonstrates the number of total "moves" (exchanges in place) as the
    flight "sizes" itself through the "taller-tap" method.
    """
    def __init__(self, ranks=12, elements=4):
        """
        Initialize an object of the Flight class. Default is 12 ranks (rows)
        and 4 elements (columns).

        The unsized attribute is a randomly generated 48-airman flight that
        draws from two different normal distributions: mean 62.8" and stdev 2.8"
        for females, and mean 70" and stdev 3" for males.

        The sized flight is a shallow copy of the unsized flight, to allow for
        comparisons after the fact.
        """
        self.unsized = [[round(random.gauss(mu=62.8,sigma=2.8),1) if random.random()<.5 
                            else round(random.gauss(mu=70,sigma=3),1) for i in range(ranks)] for j in range(elements)]
        self.sized = [[x for x in y] for y in self.unsized]
        self.primary_moves = 0
        self.secondary_moves = 0
        self.total_moves = 0
    
    def facing_movement(self):
        """
        Transposes the matrix that represents the flight, to correspond with a
        facing movement that transforms rows into columns (ranks into elements)
        and vice versa.
        """
        return list(map(list, itertools.zip_longest(*self.sized,fillvalue=None)))
    
    def taller_tap(self, l, i, j):
        """
        Inefficient but realistic sorting method that mirrors the process airmen
        go through when sizing the flight. An airman is instructed to switch places
        with the airman in front of them if they are taller by tapping them on the
        shoulder. The overall sorting process happens as the amalgamation of many
        piecewise comparisons of adjacent airmen's heights.

        Inputs:
            l (list): the element/column of airmen being sorted
            i (int): the index position of one airman being compared (v1)
            j (int): the index position of the other airman being compared (v2)
        
        Outputs:
            (l, k): a tuple that contains the element/column as it began (l)
                and as it ended (k) after the comparison took place. Can either
                have the two airmen (v1 and v2) remaining in the same position if
                the airman closer to the front of the line (i.e. with a lower index
                number) is taller, or with the two airmen switched if the airman
                closer to the front of the line is shorter.
        """
        k = [i for i in l]
        v1=l[i]
        v2=l[j]
        if v1>v2:
            k[i]=v2
            k[j]=v1
        return (l, k)
    
    def size_element(self, element):
        """
        Iteratively moves through an element and performs the taller-tap
        comparison sort method repeatedly until the element is correctly
        sized (i.e. sorted in descending order). Also tracks the number of
        "moves" (place trades) that take place.

        Inputs:
            element (list): the element/column of airmen's heights to be sorted
        
        Outputs:
            (l, moves): tuple of the newly sorted element (l) and the total
                number of individual comparisons and place trades it took to
                reach that sorted state (moves)
        """
        r = len(element)
        moves = 0
        l = [i for i in element]
        for p in range(r):
            for i in range(1, r):
                (k, l) = self.taller_tap(l,r-i,r-i-1)
                if k != l:
                    moves += 1
        return (l, moves)
    
    def size_flight(self):
        """
        Go through the entire flight sizing process. First, do primary sizing
        by running the taller-tap method on each element/column and tracking
        the number of moves made there. Next, perform the "facing movement"
        (by transposing the list of lists that represent the airmen's heights)
        and repeat the taller-tap method on the ranks/rows, then undo the 
        facing movement to get the flight back to its original orientation.

        Inputs:
            None, takes the flight's starting "unsized" attribute (which was
                copied over to "sized") automatically
        
        Outputs:
            None, updates the self.sized attribute in-place, along with the 
                self.total_moves, self.primary_moves, and self.secondary_moves
                attributes.
        """
        # Primary sizing
        for idx, elem in enumerate(self.sized):
            (sort_elem, moves) = self.size_element(elem)
            self.sized[idx] = sort_elem
            self.primary_moves += moves
        self.sized = self.facing_movement()

        # Secondary sizing
        for idx, elem in enumerate(self.sized):
            (sort_elem, moves) = self.size_element(elem)
            self.sized[idx] = sort_elem
            self.secondary_moves += moves
        self.sized = self.facing_movement()
            
        self.total_moves = self.primary_moves + self.secondary_moves


# A Class where the instance is instantiated by a list of lits
# that represents an unsized flight with all random heights distributed
# as population heights are (normally?)

# "Sizing the flight" means sort top up vertically, face right and sort up horizontally,
# face forward and sort up horizontally. Must COUNT the number of transactions 
# taken to get to a corectly sized endpoint! Will involve a lot of repeated transpositions

# Is the number of moves required to size the flight distributed normally?
# Is the average # of moves across several supergroups of flight itself have to be distributed normally?