import json
from qiskit import *
from qiskit.circuit.library import *
from qiskit.providers.aer import *

def read_json_file(filepath, default_value=None):
    try:
        with open(filepath) as f:
            return json.load(f)
    except:
        return default_value


# Read the input files
input_data = read_json_file('/var/input/data.json') or read_json_file('./input/data.json')
input_params = read_json_file('/var/input/params.json') or read_json_file('./input/params.json', {'round_up': False})

if not input_data:
    print('Error: data.json file not found')
    exit(1)

print("Setting up simulator backend...")

if input_params.get('gpu', False) is True:
    print("Trying to use GPU")
    try:
        sim = Aer.get_backend('aer_simulator')
        sim.set_options(device='GPU')
    except AerError as e:
        print("No CUDA device available, falling back to CPU")
        sim = Aer.get_backend('aer_simulator')

else:
    print("Use CPU")
    sim = Aer.get_backend('aer_simulator')

shots = input_params.get('shots', 100)
depth = input_params.get('depth', 10)
qubits = input_params.get('qubits', 25)

circuit = transpile(QuantumVolume(qubits, depth, seed=0),
        backend=sim,
        optimization_level=0)
circuit.measure_all()
result = execute(circuit,sim,shots=shots,seed_simulator=12345).result()

print("PlanQK:Job:Result:", json.dumps(result.get_counts()))
