import numpy as np
import torch


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
        zeeman_tot = -torch.sum(
            torch.sum(torch.tensor(self.s.array) * torch.tensor(self.B), dim=2)
        )  # see source 1 and source 2 in references

        return float(zeeman_tot.item())

    def anisotropy(self):
        """
        This function calculates the total anisotropy of the system

        Returns:
            float_: a floating point number
        """

        if not isinstance(self.u, torch.Tensor):
            self.u = torch.tensor(self.u, dtype=torch.float32)
        if torch.norm(self.u) > 1:
            magnitude = torch.norm(self.u)
            self.u = torch.tensor(self.u) / magnitude
        anisotropy = (
            torch.sum(
                torch.square(torch.sum(torch.tensor(self.s.array) * self.u, axis=2))
            )
            * -self.K
        )  # see source 1 and source 2 in references

        return anisotropy.cpu().numpy()

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
        s_array = torch.tensor(self.s.array)
        horizontal_pairs = s_array[:, :-1] * s_array[:, 1:]
        component1 = torch.einsum("ijk->", horizontal_pairs) * self.J * -1

        # Calculate vertical component
        vertical_pairs = s_array[:-1, :] * s_array[1:, :]
        component2 = torch.einsum("ijk->", vertical_pairs) * self.J * -1

        e_exchange_tot = component1 + component2
        return e_exchange_tot.item()

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
        s_array = torch.tensor(self.s.array, dtype=torch.float32)

        # Generate unit vectors in the x and y directions
        rij_x = torch.tensor([1, 0, 0], dtype=torch.float32)
        rij_y = torch.tensor([0, 1, 0], dtype=torch.float32)

        # Horizontal comparison
        cross_product_x = torch.cross(s_array[:, :-1], s_array[:, 1:])
        x_component = torch.einsum("ijk,k->", cross_product_x, rij_x) * self.D

        # Vertical comparison
        cross_product_y = torch.cross(s_array[:-1, :], s_array[1:, :])
        y_component = torch.einsum("ijk,k->", cross_product_y, rij_y) * self.D

        return (x_component + y_component).item()
