#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <unordered_map>
#include <queue>
#include <algorithm>

struct Transition {
    std::string target;
    double probability;
};

struct Automaton {
    std::unordered_map<std::string, std::vector<Transition>> transitions;
    std::string initialState;
    std::vector<std::string> finalStates;
    double probabilityThreshold;
};

Automaton readAutomaton(std::istream &input) {
    Automaton automaton;
    std::string line;

    // Read initial state
    getline(input, automaton.initialState);
    std::cout << "Initial State: " << automaton.initialState << std::endl;

    // Read final states
    getline(input, line);
    std::istringstream finalStatesStream(line);
    std::string state;
    while (getline(finalStatesStream, state, ',')) {
        automaton.finalStates.push_back(state);
        std::cout << "Final State: " << state << std::endl;
    }

    // Read probability threshold
    getline(input, line);
    automaton.probabilityThreshold = std::stod(line);
    std::cout << "Probability Threshold: " << automaton.probabilityThreshold << std::endl;

    // Read transitions
    while (getline(input, line)) {
        std::istringstream iss(line);
        std::string source, target, action;
        double probability;
        getline(iss, source, ',');
        getline(iss, target, ',');
        getline(iss, action, ',');
        iss >> probability;
        automaton.transitions[source].push_back({target, probability});
        std::cout << "Transition: " << source << " -> " << target << " with probability " << probability << std::endl;
    }

    return automaton;
}

bool isReachable(const Automaton &automaton) {
    std::unordered_map<std::string, double> probabilities;
    probabilities[automaton.initialState] = 1.0;

    std::queue<std::string> queue;
    queue.push(automaton.initialState);

    while (!queue.empty()) {
        std::string current = queue.front();
        queue.pop();

        std::cout << "Current state: " << current << " with probability " << probabilities[current] << std::endl;

        if (automaton.transitions.find(current) == automaton.transitions.end()) {
            std::cout << "No transitions from state: " << current << std::endl;
            continue;
        }

        for (const Transition &transition : automaton.transitions.at(current)) {
            double newProbability = probabilities[current] * transition.probability;

            std::cout << "Transition to " << transition.target 
                      << " with probability " << transition.probability 
                      << " resulting in new probability " << newProbability << std::endl;

            if (newProbability >= automaton.probabilityThreshold) {
                std::cout << "New probability " << newProbability << " is above threshold " << automaton.probabilityThreshold << std::endl;

                if (std::find(automaton.finalStates.begin(), automaton.finalStates.end(), transition.target) != automaton.finalStates.end()) {
                    std::cout << "Final state " << transition.target << " reachable with probability " << newProbability << std::endl;
                    return true;
                }

                if (probabilities.find(transition.target) == probabilities.end() || newProbability > probabilities[transition.target]) {
                    probabilities[transition.target] = newProbability;
                    queue.push(transition.target);
                }
            }
        }
    }

    return false;
}

int main() {
    Automaton automaton = readAutomaton(std::cin);
    bool reachable = isReachable(automaton);

    std::cout << (reachable ? "Reachable" : "Not reachable") << std::endl;

    return 0;
}


