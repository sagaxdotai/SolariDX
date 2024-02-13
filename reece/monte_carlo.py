# montecarlo_integration.py
"""Volume 1: Monte Carlo Integration.
Reece Robertson
Section 1
February 23, 2021
"""
import numpy as np
from scipy import linalg as la
from scipy import stats
from matplotlib import pyplot as plt

# Problem 1
def ball_volume(n, N=10000):
    """Estimate the volume of the n-dimensional unit ball.

    Parameters:
        n (int): The dimension of the ball. n=2 corresponds to the unit circle,
            n=3 corresponds to the unit sphere, and so on.
        N (int): The number of random points to sample.

    Returns:
        (float): An estimate for the volume of the n-dimensional unit ball.
    """
    points = np.random.uniform(-1,1,(n,N))      #Randomly sample points.
    lengths = la.norm(points, axis=0)           #Calculate the norm of each point.
    num_within = np.count_nonzero(lengths < 1)  #Count those with norm < 1.
    volume = 2**n * (num_within / N)            #Use that to compute the volume of the unit ball.
    return volume                               #Return the volume.


# Problem 2
def mc_integrate1d(f, a, b, N=10000):
    """Approximate the integral of f on the interval [a,b].

    Parameters:
        f (function): the function to integrate. Accepts and returns scalars.
        a (float): the lower bound of interval of integration.
        b (float): the lower bound of interval of integration.
        N (int): The number of random points to sample.

    Returns:
        (float): An approximation of the integral of f over [a,b].

    Example:
        >>> f = lambda x: x**2
        >>> mc_integrate1d(f, -4, 2)    # Integrate from -4 to 2.
        23.734810301138324              # The true value is 24.
    """
    points = np.random.uniform(a,b,N)   #Randomly sample points.
    average = np.mean(f(points))        #Get the average value of f over the points.
    volume = b - a                      #Get the length of the interval.
    return volume * average             #Return the area (width * heigth).


# Problem 3
def mc_integrate(f, mins, maxs, N=10000):
    """Approximate the integral of f over the box defined by mins and maxs.

    Parameters:
        f (function): The function to integrate. Accepts and returns
            1-D NumPy arrays of length n.
        mins (list): the lower bounds of integration.
        maxs (list): the upper bounds of integration.
        N (int): The number of random points to sample.

    Returns:
        (float): An approximation of the integral of f over the domain.

    Example:
        # Define f(x,y) = 3x - 4y + y^2. Inputs are grouped into an array.
        >>> f = lambda x: 3*x[0] - 4*x[1] + x[1]**2

        # Integrate over the box [1,3]x[-2,1].
        >>> mc_integrate(f, [1, -2], [3, 1])
        53.562651072181225              # The true value is 54.
    """
    #Set up the mins, maxs, n, and points.
    mins, maxs = np.array(mins), np.array(maxs)
    n = len(mins)
    points = np.random.uniform(0,1,(n,N))
    #Scale the points so the samples are from mins[i] to maxs[i] for each i.
    for i in range(n):
        points[i] = points[i] * (maxs[i] - mins[i]) + mins[i]
    #Compute the average of f and the volume of the region.
    average = np.mean(f(points))
    volume = np.prod(maxs - mins)
    #Return an approximation of the integral of the function.
    return float(volume * average)


# Problem 4
def prob4():
    """Let n=4 and Omega = [-3/2,3/4]x[0,1]x[0,1/2]x[0,1].
    - Define the joint distribution f of n standard normal random variables.
    - Use SciPy to integrate f over Omega.
    - Get 20 integer values of N that are roughly logarithmically spaced from
        10**1 to 10**5. For each value of N, use mc_integrate() to compute
        estimates of the integral of f over Omega with N samples. Compute the
        relative error of estimate.
    - Plot the relative error against the sample size N on a log-log scale.
        Also plot the line 1 / sqrt(N) for comparison.
    """
    #Define the needed values and functions.
    n = 4
    mins = [-3/2, 0, 0, 0]
    maxs = [3/4, 1, 1/2, 1]
    f = lambda x: (1/ (2 * np.pi)**(n/2)) * np.exp(-(x[0]**2 + x[1]**2 + x[2]**2 + x[3]**2) / 2)
    #Get the exact integral of f using numpy.
    means, cov = np.zeros(n), np.eye(n)
    exact = stats.mvn.mvnun(mins, maxs, means, cov)[0]
    #Extimate the integral using Monte Carlo integration for various values of N.
    domain = np.logspace(1, 5, 20, dtype=np.int64)
    error = []
    for N in domain:
        estimate = mc_integrate(f, mins, maxs, N)
        error.append(abs(exact - estimate)/abs(exact))
    #Plot the error in the estimation on a log plot.
    #Note that the error in Monte Carlo is proportional to 1/sqrt(N).
    plt.loglog(domain, error, "ro-", label="Relative Error")
    plt.loglog(domain, 1/np.sqrt(domain), "ko-", label="1/sqrt(N)")
    plt.title("Monte Carlo Integration Error for Various Values of N")
    plt.legend(loc="best")
    plt.show()


def test1():
    for n in range(1, 15):
        print("n =", n, ":", ball_volume(n))

def test2():
    f = lambda x: x**2
    print(mc_integrate1d(f, -4, 2))
    f = lambda x: np.sin(x)
    print(mc_integrate1d(f, -2*np.pi, 2*np.pi))
    f = lambda x: 1/x
    print(mc_integrate1d(f, 1, 10))
    f = lambda x: np.abs(np.sin(10*x)*np.cos(10*x)+np.sqrt(x)*np.sin(3*x))
    print(mc_integrate1d(f, 1, 5))

def test3():
    f = lambda x: x[0]**2 + x[1]**2
    print("{:.4f}".format(mc_integrate(f, [0,0], [1,1])))
    f = lambda x: 3*x[0] - 4*x[1] + x[1]**2
    print("{:.4f}".format(mc_integrate(f, [1,-2], [3,1])))
    f = lambda x: x[0] + x[1] - x[3] * x[2]**2
    print("{:.4f}".format(mc_integrate(f, [-1,-2,-3,-4], [1,2,3,4], 10000000)))
    f0 = lambda x: x**4
    print(mc_integrate(f0, [-4], [2]))

if __name__ == '__main__':
    test1()
