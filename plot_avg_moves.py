import itertools
import random
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from flight_sizing import Flight

# Create empty lists to store the number of moves in
primary_moves = []
secondary_moves = []
total_moves = []

# Generate 10000 random flights and size them, track the number of 
# primary and secondary moves necessary to properly size
for i in range(10000):
    f = Flight()
    f.size_flight()
    primary_moves.append(f.primary_moves)
    secondary_moves.append(f.secondary_moves)
    total_moves.append(f.total_moves)

# Convert lists to numpy arrays for plotting
pm_arr = np.array(primary_moves)
sm_arr = np.array(secondary_moves)
tm_arr = np.array(total_moves)

# Assuming the number of moves to size flights is normally distributed,
# calculate the mean and standard deviation of this distribution
mu, std = norm.fit(tm_arr)
# Plot histogram
plt.hist(tm_arr, bins=25, density=True, alpha=0.8, color='green')
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
# Fit a normal distribution to the total moves data array
p = norm.pdf(x, mu, std)
# Plot and show
plt.plot(x, p, 'k', linewidth=2)
title = "Fit values: {:.2f} and {:.2f}".format(mu,std)
plt.title(title)
plt.show()

# A little background statistics: the total moves dataset is an example of
# the sum of normally distributed random variables 
# (https://en.wikipedia.org/wiki/Sum_of_normally_distributed_random_variables)
# rather than a mixture distribution that is derived from a collection of two
# random variables. 

# In other words: total_moves = primary_moves + secondary_moves, which are both
# themselves random variables. total_moves is NOT the result of randomly selecting
# a value from EITHER primary_moves OR secondary_moves into a single mixed distribution
# based on some underlying probability (like pulling 25% of values from primary_moves
# and 75% of values from secondary_moves). That's the key difference between the sum
# of normally distributed random variables and a mixture distribution.

# One thing to consider - are primary_moves and secondary_moves actually independent
# random variables? I might argue no because they could be directly correlated. Fewer
# primary_moves MIGHT correlate to fewer_secondary moves - if the flight's random initial
# starting state is a "little more organized", fewer primary_moves necessary to get the
# first taller-tap round finished might mean that fewer secondary_moves are necessary
# to get the second round finished. Quick gut check on the random instance of the 10k
# trials I had running at the time:

# np.corrcoef(pm_arr, sm_arr) 
# yields
# array([[ 1.        , -0.00145469],
#        [-0.00145469,  1.        ]])

# which suggests to me that pm_arr and sm_arr are not actually correlated. I suppose this
# makes sense - the extent to which the columns/elements of the initial unsized flights are
# "closer to organized" shouldn't have anything to do with how the rows/ranks are, especially
# because ALL flights, regardless of how many primary_moves it takes to get to the intermediate
# sized stage (after the first round of taller-tap but before the second round) should be
# roughly the same amount of organized.

# It is in fact the case that if X ~ N(mu1, sigma1) and X ~ N(mu2, sigma2) then Z = X + Y means
# Z ~ N(mu1 + mu2, sigma1 + sigma2)

# More discussion here: https://docs.google.com/document/d/1lp9j98zhtJQJ7qfed0oqK9Qeris2nRmDgMt2j17Rfy8/edit
# and fold some of this into over there