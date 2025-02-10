import numpy as np
import torch

# from mcsim import system


def random_spin(s0, alpha=0.1):
    """Generate a new random spin based on the original one.

    Parameters
    ----------
    s0: np.ndarray

        The original spin that needs to be changed.

    alpha: float

        Larger alpha, larger the modification of the spin. Defaults to 0.1.

    Returns
    -------
    np.ndarray

        New updated spin, normalised to 1.

    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    delta_s = (2 * torch.rand(3) - 1) * alpha
    delta_s = delta_s.to(device)
    s1 = s0 + delta_s
    return s1 / torch.norm(s1)


class Driver:
    """Driver class.

    Driver class does not take any input parameters at initialisation.

    """

    def __init__(self):
        pass

    def drive(self, system, n, alpha=0.1):
        """ "
        Paramters:
        --------
         n= number of iterations
         system= the systems objects
         alpha= the rate at which the spins are changed

        Return:
        -------
         The updated system with minimized energy


        """
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        systems_array = system.s.array
        if not isinstance(systems_array, torch.Tensor):
            print("Converting to tensor")
            systems_array = torch.tensor(systems_array, dtype=torch.float64).to(device)
            print(device)
        else:
            systems_array = systems_array.to(device)
            print(device)

        for repetition in range(n + 1):
            # create a deep copy of the array, so you can easily revert back to the original state ## see source 7 ##
            systems_copy = systems_array.clone()
            # compute the total energy of the system
            E0 = system.energy()
            # generate random numbers
            res1 = torch.randint(systems_array.shape[0], (1,)).item()
            res2 = torch.randint(systems_array.shape[1], (1,)).item()
            # get the random spin vector
            random_spin_original = systems_array[res1, res2]
            # randomly change the spin of the randomly selected vector
            change_spin = random_spin(random_spin_original, alpha).to(device)
            # assign the randomized spin to the original array
            systems_array[res1, res2] = change_spin
            E1 = system.energy()
            if E1 - E0 >= 0:
                systems_array[res1, res2] = systems_copy[res1, res2]
