import cudaq
import numpy as np

# To model quantum noise, we need to utilise the density matrix simulator target.
cudaq.set_target("density-matrix-cpu")

# Let's define a simple kernel that we will add noise to.
qubit_count = 2

# We begin by defining the `Kernel` that we will construct our
# program with.
kernel = cudaq.make_kernel()

# Next, we can allocate qubits to the kernel via `qalloc(qubit_count)`.
# An empty call to `qalloc` will return a single qubit.
qubits = kernel.qalloc(qubit_count)

kernel.x(qubits[0])
kernel.x(qubits[1])

# In the ideal noiseless case, we get |11> 100% of the time.
# Next, we add a measurement to the kernel so that we can sample
# the measurement results on our simulator!
ideal_counts = cudaq.sample(kernel, shots_count=1000)
ideal_counts.dump()

# First, we will define an out of the box noise channel. In this case,
# we choose depolarization noise. This depolarization will result in
# the qubit state decaying into a mix of the basis states, |0> and |1>,
# with our provided probability.
error_probability = 0.1
depolarization_channel = cudaq.DepolarizationChannel(error_probability)

# We can also define our own, custom noise channels through
# Kraus Operator's. Here we will define two operators repsenting
# bit flip errors.

# Define the Kraus Error Operator as a complex ndarray.
kraus_0 = np.sqrt(1 - error_probability) * np.array([[1.0, 0.0], [0.0, 1.0]],
                                                    dtype=np.complex128)
kraus_1 = np.sqrt(error_probability) * np.array([[0.0, 1.0], [1.0, 0.0]],
                                                dtype=np.complex128)

# Add the Kraus Operator to create a quantum channel.
bitflip_channel = cudaq.KrausChannel([kraus_0, kraus_1])

# Add the two channels to our Noise Model.
noise_model = cudaq.NoiseModel()

# Apply the depolarization channel to any X-gate on the 0th qubit.
noise_model.add_channel("x", [0], depolarization_channel)
# Apply the bitflip channel to any X-gate on the 1st qubit.
noise_model.add_channel("x", [1], bitflip_channel)

# Due to the impact of noise, our measurements will no longer be uniformly
# in the |11> state.
noisy_counts = cudaq.sample(kernel, noise_model=noise_model, shots_count=1000)
noisy_counts.dump()
