import numpy as np


class System:
    """System object with the spin configuration and necessary parameters.

    Parameters
    ----------
    s: mcsim.Spins

        Two-dimensional spin field.

    B: Iterable

        External magnetic field, length 3.

    K: numbers.Real

        Uniaxial anisotropy constant.

    u: Iterable(float)

        Uniaxial anisotropy axis, length 3. If ``u`` is not normalised to 1, it
        will be normalised before the calculation of uniaxial anisotropy energy.

    J: numbers.Real

        Exchange energy constant.

    D: numbers.Real

        Dzyaloshinskii-Moriya energy constant.

    """

    def __init__(self, s, B, K, u, J, D):
        self.s = s
        self.J = J
        self.D = D
        self.B = B
        self.K = K
        self.u = u

    def energy(self):
        """Total energy of the system.

        The total energy of the system is computed as the sum of all individual
        energy terms.

        Returns
        -------
        float

            Total energy of the system.

        """
        return self.zeeman() + self.anisotropy() + self.exchange() + self.dmi()

    def zeeman(self):
        """Calculate the total zeeman energy of the lattice by summing over all spin vectors

        Returns:
            float: a float number
        """
        zeeman_tot = -np.sum(
            np.sum(self.s.array * self.B, axis=2)
        )  # see source 1 and source 2 in references

        return zeeman_tot

    def anisotropy(self):
        """
        This function calculates the total anisotropy of the system

        Returns:
            float_: a floating point number
        """
        print(self.u.shape)
        if np.linalg.norm(self.u) > 1:
            magnitude = np.linalg.norm(self.u)
            self.u = self.u / magnitude
        anisotropy = (
            np.sum(np.square(np.sum(self.s.array * self.u, axis=2))) * -self.K
        )  # see source 1 and source 2 in references

        return anisotropy

    def exchange(self):
        """Calculates the total exchange energy by taking the dot product of adjacent spins.
           First for loop loops through every row and calculates the dot product for adjacent spins
           within a row. The second for loop also loops through rows but calculates the dot product
           for spins vertically.

        Returns:
            float:float number
        """
        component1 = 0
        component2 = 0
        for i in range(self.s.array.shape[0]):
            for j in range(self.s.array.shape[1] - 1):
                component1 += (
                    np.dot(self.s.array[i, j], self.s.array[i, j + 1]) * self.J * -1
                )
        for i in range(self.s.array.shape[0] - 1):
            for j in range(self.s.array.shape[1]):
                component2 += (
                    np.dot(self.s.array[i, j], self.s.array[i + 1, j]) * self.J * -1
                )

        e_exchange_tot = component1 + component2
        return e_exchange_tot

    def dmi(self):
        """
        This function loops through the lattice. The first for loop loops through every row and compares
        neighbouring spin vectors. The cross product is calculated and then the dot product is computed
        between the cross product and the rij vector, which represents the difference in the x position.
        The same is done in the second for loop, but here vertical comparisons are made. The rij vector
        represents the difference in the y coordinates.

        Returns:
            float: a float number
        """
        x_component = 0
        y_component = 0
        # loop through rows and compare elements within a row (horizontal comparison)
        for i in range(self.s.array.shape[0]):
            for j in range(self.s.array.shape[1] - 1):
                cross_product = np.cross(self.s.array[i, j], self.s.array[i, j + 1])
                # generate a unit vector in the x direction
                rij = np.array([i + 1, j, 0] - np.array([i, j, 0]))
                x_component += np.dot(rij, cross_product) * self.D

        # loop through rows and compare elements in adjacent rows(vertical comparison)
        for i in range(self.s.array.shape[0] - 1):
            for j in range(self.s.array.shape[1]):
                cross_product = np.cross(self.s.array[i, j], self.s.array[i + 1, j])
                # generate a unit vector in the y direction
                rij = np.array([i, j + 1, 0]) - np.array([i, j, 0])
                y_component += np.dot(rij, cross_product) * self.D
        return x_component + y_component
