import numbers
import torch
import numpy as np
import matplotlib.pyplot as plt


class Spins:
    """Field of spins on a two-dimensional lattice.

    Each spin is a three-dimensional vector s = (sx, sy, sz). Underlying data
    stucture (``self.array``) is a numpy array (``np.ndarray``) with shape
    ``(nx, ny, 3)``, where ``nx`` and ``ny`` are the number of spins in the x
    and y directions, respectively, and 3 to hold all three vector components of
    the spin.

    Parameters
    ----------
    n: Iterable

        Dimensions of a two-dimensional lattice ``n = (nx, ny)``, where ``nx``
        and ``ny`` are the number of atoms in x and y directions, respectively.
        Values of ``nx`` and ``ny`` must be positive integers.

    value: Iterable

        The value ``(sx, sy, sz)`` that is used to initialise all spins in the
        lattice. All elements of ``value`` must be real numbers. Defaults to
        ``(0, 0, 1)``.

    """

    def __init__(self, n, value=(0, 0, 1)):
        # Checks on input parameters.
        if len(n) != 2:
            raise ValueError(f"Length of iterable n must be 2, not {len(n)=}.")
        if any(i <= 0 or not isinstance(i, int) for i in n):
            raise ValueError("Elements of n must be positive integers.")

        if len(value) != 3:
            raise ValueError(f"Length of iterable value must be 3, not {len(n)=}.")
        if any(not isinstance(i, numbers.Real) for i in n):
            raise ValueError("Elements of value must be real numbers.")

        self.n = n
        self.array = np.empty((*self.n, 3), dtype=np.float64)
        self.array[..., :] = value

        if not np.isclose(value[0] ** 2 + value[1] ** 2 + value[2] ** 2, 1):
            # we ensure all spins' magnitudes are normalised to 1.
            self.normalise()

    @property
    def mean(self):
        """
        Calculate the mean for the individual components (x,y,z) of the lattice.

        Returns:
            np.ndarray: a 1D array [x,y,z] containing the mean values of the individual components of the spins

        """

        if not isinstance(self.array, torch.Tensor):
            self.array = torch.tensor(self.array, dtype=torch.float64)

        # calculate the mean for the x component
        mx = torch.sum(self.array[:, :, 0]) / (
            self.n[0] * self.n[1]
        )  # See source 3 in refrences
        # calculate the mean for the y component
        my = torch.sum(self.array[:, :, 1]) / (self.n[0] * self.n[1])
        # calculate the mean for the z component
        mz = torch.sum(self.array[:, :, 2]) / (self.n[0] * self.n[1])
        return torch.tensor([mx, my, mz]).cpu().numpy()

    def __abs__(self):
        """
        Calculate the norm of every vector in self.array of dimension (nx,ny,3)


        Returns:
            np.ndarray: An array if dimensions (nx,ny,1)
        """
        # create an array (nx,ny,1)
        if not isinstance(self.array, torch.Tensor):
            self.array = torch.tensor(self.array, dtype=torch.float64)

        norm = torch.norm(self.array, dim=2, keepdim=True)
        return norm.cpu().numpy()

    def normalise(self):
        """Normalise the magnitude of all spins to 1."""
        self.array = self.array / abs(self)
        # This computation will be failing until you implement __abs__.

        return self.array

    def randomise(self):
        """Initialise the lattice with random spins.

        Components of each spin are between -1 and 1: -1 <= si <= 1, and all
        spins are normalised to 1.

        """
        self.array = 2 * torch.rand((*self.n, 3)) - 1
        self.normalise()

    def plot(self):
        x, y = np.meshgrid(
            np.arange(self.array.shape[0]), np.arange(self.array.shape[1])
        )  # see source 4

        u = self.array[:, :, 0]  # Extract the x-components of the vectors
        v = self.array[:, :, 1]  # Extract the y-components of the vectors
        # see source 5; create arrows of different color based on magnitude
        magnitude = np.hypot(u, v)

        # plot spins as arrows ## see source 4 and source 5
        plt.quiver(x, y, u, v, magnitude, width=0.005)
        plt.xlabel("ny")
        plt.ylabel("xy")
        plt.grid(linewidth=0.3)  # create a grid to represent the lattice
        plt.title("Directions of Spins on a 2D lattice")
        plt.colorbar(label="Spin Magnitude")  # see source 6
        plt.scatter(x, y, color="red", s=2)  # create the lattice points
        plt.show()
