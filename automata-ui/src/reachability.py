import sys
from collections import defaultdict

def read_input():
    initial_state = input().strip()
    final_states = set(input().strip().split(','))
    probability_threshold = float(input().strip())
    
    transitions = defaultdict(list)
    for line in sys.stdin:
        source, target, action, probability = line.strip().split(',')
        transitions[source].append((target, action, float(probability)))
    
    return initial_state, final_states, probability_threshold, transitions

def create_graph(transitions):
    graph = defaultdict(lambda: defaultdict(dict))
    
    for source, trans_list in transitions.items():
        outgoing_probs = defaultdict(float)
        for target, action, prob in trans_list:
            graph[source][target][action] = prob
            outgoing_probs[action] += prob
        
        # Add self-edges
        for action, total_prob in outgoing_probs.items():
            if total_prob < 1:
                graph[source][source][action] = 1 - total_prob
    
    # Convert defaultdict to regular dict
    return {s: dict(t) for s, t in graph.items()}

def create_transition_matrices(transitions):
    states = set()
    actions = set()
    for source, trans_list in transitions.items():
        states.add(source)
        for target, action, _ in trans_list:
            states.add(target)
            actions.add(action)
    
    states = sorted(states)
    state_index = {state: i for i, state in enumerate(states)}
    matrices = {action: [[0 for _ in states] for _ in states] for action in actions}
    
    for source, trans_list in transitions.items():
        for target, action, prob in trans_list:
            i, j = state_index[source], state_index[target]
            matrices[action][i][j] = prob
    
    # Add self-loops to make matrices stochastic
    for action in actions:
        for i, state in enumerate(states):
            row_sum = sum(matrices[action][i])
            if row_sum < 1:
                matrices[action][i][i] += 1 - row_sum
    
    return matrices

def main():
    initial_state, final_states, probability_threshold, transitions = read_input()
    graph = create_graph(transitions)
    matrices = create_transition_matrices(transitions)
    
    print("Graph:")
    print(graph)
    print("\nTransition Matrices:")
    for action, matrix in matrices.items():
        print(f"Action {action}:")
        for row in matrix:
            print(row)
        print()

if __name__ == "__main__":
    main()