import json
import time
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
input_data = read_json_file(
    '/var/input/data.json') or read_json_file('./input/data.json')

default_params = {"gpu": False,
                  "shots": 100,
                  "depth": 10,
                  "qubits": 5,
                  "simulator_seed": 12345,
                  "quantum_volume_seed": 0,
                  "return_counts": False
                  }

input_params = read_json_file(
    '/var/input/params.json') or read_json_file('./input/params.json', default_params)

if not input_data:
    print('Error: data.json file not found')
    exit(1)

print("Setting up simulator backend...")

if input_params.get('gpu', False) is True:
    print("Trying to use GPU...")
    try:
        sim = Aer.get_backend('aer_simulator')
        sim.set_options(device='GPU')
        print("Using GPU")
    except AerError as e:
        print("No CUDA device available, falling back to CPU")
        sim = Aer.get_backend('aer_simulator')

else:
    print("Using CPU")
    sim = Aer.get_backend('aer_simulator')

shots = input_params.get('shots')
depth = input_params.get('depth')
qubits = input_params.get('qubits')
simulator_seed = input_params.get('simulator_seed')
quantum_volume_seed = input_params.get('quantum_volume_seed')
return_counts = input_params.get('return_counts')

print(f"Simulating with following parameters: shots={shots}, depth={depth}, qubits={qubits}, simulator_seed={simulator_seed}, quantum_volume_seed={quantum_volume_seed}")

circuit = transpile(QuantumVolume(qubits, depth, seed=quantum_volume_seed),
                    backend=sim,
                    optimization_level=0)
circuit.measure_all()

start_time = time.perf_counter()
result = execute(circuit, sim, shots=shots,
                 seed_simulator=simulator_seed).result()
end_time = time.perf_counter()
elapsed_time = end_time - start_time
elapsed_time_ms = elapsed_time * 1000
elapsed_seconds = int(elapsed_time_ms // 1000)
elapsed_milliseconds = elapsed_time_ms % 1000

result_obj = {
          "elapsed_seconds": elapsed_seconds,
          "elapsed_milliseconds": elapsed_milliseconds,
          "duration_message": f"Elapsed time: {elapsed_seconds} seconds, {elapsed_milliseconds:.2f} milliseconds"
      }

if return_counts is True:
    result_obj["counts"] = result.get_counts()

print("PlanQK:Job:Result:", json.dumps(result_obj))
