import sys
import numpy as np

def read_input():
    input_data = sys.stdin.read().strip().split('\n')
    initial_state = input_data[0].strip()
    final_states = input_data[1].strip().split(',')
    probability_threshold = float(input_data[2].strip())
    transitions = [line.strip().split(',') for line in input_data[3:]]
    return initial_state, final_states, probability_threshold, transitions

def build_transition_matrices(transitions, states):
    n = len(states)
    transition_matrices = {action: np.zeros((n, n)) for action in set(t[2] for t in transitions)}
    
    for src, tgt, action, prob in transitions:
        i, j = states.index(src), states.index(tgt)
        transition_matrices[action][i, j] = float(prob)
        
    return transition_matrices

import numpy as np

def calculate_reachability(transition_matrices, initial_state, states):
    n = len(states)
    state_vector = np.zeros(n)
    state_vector[states.index(initial_state)] = 1.0

    state_vectors = [state_vector.copy()]
    iteration = 0
    last_nonzero_vector = state_vector.copy()  # Keep track of the last nonzero state vector

    while True:
        new_state_vector = np.zeros(n)
        for action, matrix in transition_matrices.items():
            new_state_vector += np.dot(state_vector, matrix)

        if np.all(new_state_vector == 0) and np.any(last_nonzero_vector > 0):
            # If new vector is all zeros but there was a previous nonzero vector, end iterations
            state_vectors.append(last_nonzero_vector.copy())
            break

        if np.linalg.norm(new_state_vector - state_vector) < 1e-8 and iteration > 0:
            # Convergence is confirmed
            state_vectors.append(new_state_vector.copy())
            break

        state_vector = new_state_vector.copy()
        if np.any(state_vector > 0):
            last_nonzero_vector = state_vector.copy()  # Update the last known nonzero vector

        state_vectors.append(state_vector.copy())

        iteration += 1
        # if iteration > 1000:  # Safeguard against infinite loops
        #     print("Iteration limit reached. Potential non-convergence.")
        #     break

    return state_vectors


def main():
    initial_state, final_states, probability_threshold, transitions = read_input()
    
    states = list(set([t[0] for t in transitions] + [t[1] for t in transitions]))
    
    transition_matrices = build_transition_matrices(transitions, states)
    
    state_vectors = calculate_reachability(transition_matrices, initial_state, states)
    
    # Check reachability
    reachability = False
    final_reachability_vector = state_vectors[-1]
    for state in final_states:
        if final_reachability_vector[states.index(state)] >= probability_threshold:
            reachability = True
            break
    
    # Print detailed logs
    print("Reachability Analysis Logs:")
    print(f"Initial State: {initial_state}")
    print(f"Final States: {final_states}")
    print(f"Probability Threshold: {probability_threshold}")
    print(f"States: {states}")
    print("Transitions:")
    for src, tgt, action, prob in transitions:
        print(f"  {src} --{action}/{prob}--> {tgt}")
    print("\nState Probabilities at Each Step:")
    
    for i, vector in enumerate(state_vectors):
        print(f"Step {i}:")
        for j, state in enumerate(states):
            print(f"  State {state}: {vector[j]}")
    
    print("\nReachability Result:")
    if reachability:
        print("SUCCESS: One or more final states are reachable with the given probability threshold.")
    else:
        print("FAILURE: No final states are reachable with the given probability threshold.")

if __name__ == "__main__":
    main()
