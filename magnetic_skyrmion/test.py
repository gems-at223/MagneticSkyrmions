import matplotlib.pyplot as plt
import numpy as np
import mcsim
import numbers

# rtol = 0.01
# atol = 0.01
# n = (5, 5)
# s = mcsim.Spins(n=n)
# s.randomise()
# B = (1, 0, 0)
# K = 0
# u = (0, 1, 0)
# J = 0
# D = 0
# system = mcsim.System(s=s, B=B, K=K, u=u, J=J, D=D)
# driver = mcsim.Driver()
# driver.drive(system, n=100)
# print(s.mean)
# system.s.plot()
# print(abs(system.s))

# assert np.allclose(system.s.mean, (1, 0, 0), rtol=rtol, atol=atol)
# assert np.allclose(abs(system.s), 1, rtol=rtol, atol=atol)
n = (10, 10)  # define the dimensions of the lattice 6x7 in this case
spin_system = mcsim.Spins(n=n)  # create the 2d lattice
spin_system.randomise()  # randomise all the spins in the lattice
# B = (1, 1, 1)  # add the magnetic field direction
# K = 1  # add the anisotropy constant
# u = (0, 1, 0)  # add the anisotropy axis
# J = 1  # add the coupling constant
# D = 1  # add the DMI constant
# create an instance of the system you want to simulate
# system = mcsim.System(s=s, B=B, K=K, u=u, J=J, D=D)
system_to_simulate = mcsim.System(s=spin_system, B=(0, 0, 0.1),
                                  K=0.01, u=(0, 0, 1), J=0.5, D=0.5)

driver = mcsim.Driver()  # create an instance of the druver class
# run the Metrpolis Monte Carlo simulation
driver.drive(system_to_simulate, n=10)
# print(system.anisotropy())
# plt.savefig('figure.jpeg')
system_to_simulate.s.plot()
print(spin_system.mean)
print(system_to_simulate.anisotropy())
print(system_to_simulate.zeeman())
print(system_to_simulate.dmi())
print(system_to_simulate.exchange())
print(system_to_simulate.energy())
