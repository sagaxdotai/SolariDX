import time
import warnings
from qiskit import transpile
from qiskit import QuantumCircuit
from qiskit_ionq import IonQProvider, ErrorMitigation
from qiskit.providers.jobstatus import JobStatus

# Suppress warnings (error mitigation on simulator produces user warning).
warnings.filterwarnings("ignore")

# Define the needed constants.
N = 5
ITER = 30
SHOTS = 8192

# Load the account with the provided API token.
with open('../IonQ_API.txt', 'r') as file:
    token = file.read()
provider = IonQProvider(token)

# Get the IonQ Aria1 noisy backend.
backend = provider.get_backend('ionq_simulator')
backend.set_options(noise_model='harmony')

# For each iteration:
for i in range(1, ITER+1):
    print(f'Iteration {i} of {ITER}:')    

    # For each problem size:
    for n in range(2, N+1):
        print(f'\t{n} qubits')

        # Create the circuit for this run on Simon's algorithm.
        circuit = QuantumCircuit(2*n)
        for m in range(n):
            circuit.h(m)
        circuit.barrier()
        for m in range(n):
            circuit.cx(m, n+m)
        for m in range(n):
            circuit.cx(0, n+m)
        circuit.barrier()
        for m in range(n):
            circuit.h(m)
        circuit.barrier()
        circuit.measure_all()

        # Transpile the ideal circuit to an executable circuit.
        transpiled_circuit = transpile(circuit, backend)

        # Run the transpiled circuit using the simulated fake backend with EM.
        job = backend.run(
            transpiled_circuit,
            shots=SHOTS,
            error_mitigation = ErrorMitigation.DEBIASING
        )

        # Check if job is done.
        while job.status() is not JobStatus.DONE:
            print('\t\tJob status is', job.status() )
            time.sleep(5)

        # When it is done, save the results with sharpening.
        print('\t\tJob status is', job.status())
        result = job.result(sharpen=True).get_counts()
        with open(
            f'IonQHarmonySimulator/n{n}i{i}e1s1.txt', 'w+'
        ) as file:
            file.write(str(result))

        # Also save the results without sharpening.
        result = job.result().get_counts()
        with open(
            f'IonQHarmonySimulator/n{n}i{i}e1s0.txt', 'w+'
        ) as file:
            file.write(str(result))

        # Repeat the job submission without error mitigation (EM).
        job = backend.run(transpiled_circuit, shots=SHOTS)
        while job.status() is not JobStatus.DONE:
            print('\t\tJob status is', job.status() )
            time.sleep(5)
        print('\t\tJob status is', job.status())
        result = job.result(sharpen=True).get_counts()
        with open(
            f'IonQHarmonySimulator/n{n}i{i}e0s1.txt', 'w+'
        ) as file:
            file.write(str(result))
        result = job.result().get_counts()
        with open(
            f'IonQHarmonySimulator/n{n}i{i}e0s0.txt', 'w+'
        ) as file:
            file.write(str(result))
