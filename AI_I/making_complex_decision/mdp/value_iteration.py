# mdp_ch17/value_iteration.py
from __future__ import annotations
from typing import Dict, Tuple, List, Iterable, Callable, Any
from dataclasses import dataclass, field
import math

State = Tuple[int, int]      # (x, y) with x in [1..cols], y in [1..rows]
Action = str                 # 'U','D','L','R'

@dataclass
class MDP:
    states: List[State]
    actions_fn: Callable[[State], Iterable[Action]]
    transition_fn: Callable[[State, Action], List[Tuple[State, float]]]
    reward_fn: Callable[[State, Action, State], float]
    gamma: float

def q_value(mdp: MDP, s: State, a: Action, U: Dict[State, float]) -> float:
    """Q-VALUE(mdp, s, a, U) = sum_{s'} P(s'|s,a) * [ R(s,a,s') + gamma * U[s'] ]"""
    total = 0.0
    for s2, p in mdp.transition_fn(s, a):
        r = mdp.reward_fn(s, a, s2)
        total += p * (r + mdp.gamma * U.get(s2, 0.0))
    return total

def value_iteration(mdp: MDP, eps: float) -> Dict[State, float]:
    """
    VALUE-ITERATION(mdp, ε) per the book:
        repeat
            U ← U′ ; δ ← 0
            for each s in S:
                U′[s] ← max_a Q(s,a)
                δ ← max(δ, |U′[s] − U[s]|)
        until δ ≤ ε*(1−γ)/γ
        return U
    """
    U: Dict[State, float] = {s: 0.0 for s in mdp.states}
    U_prime: Dict[State, float] = {s: 0.0 for s in mdp.states}

    threshold = eps * (1.0 - mdp.gamma) / mdp.gamma if mdp.gamma < 1.0 else eps
    while True:
        U, U_prime = U_prime, U  # swap
        delta = 0.0
        for s in mdp.states:
            actions = list(mdp.actions_fn(s))
            if not actions:
                # terminal: utility is just expected immediate reward of staying (often 0)
                U_prime[s] = U[s]
                continue
            best = -math.inf
            for a in actions:
                q = q_value(mdp, s, a, U)
                if q > best:
                    best = q
            U_prime[s] = best
            delta = max(delta, abs(U_prime[s] - U[s]))
        if delta <= threshold:
            return U_prime

def extract_policy(mdp: MDP, U: Dict[State, float]) -> Dict[State, Action]:
    """π*(s) = argmax_a Q(s,a)"""
    policy: Dict[State, Action] = {}
    for s in mdp.states:
        actions = list(mdp.actions_fn(s))
        if not actions:
            continue
        best_a, best_q = None, -math.inf
        for a in actions:
            q = q_value(mdp, s, a, U)
            if q > best_q:
                best_q = q
                best_a = a
        if best_a is not None:
            policy[s] = best_a
    return policy

def pretty_print_grid(
    rows: int,
    cols: int,
    U: Dict[State, float],
    policy: Dict[State, Action],
    walls: set[State],
    terminals: Dict[State, float],
) -> None:
    """render utility 和 policy。coordinates：(1,1) bottom left；(cols, rows) top right"""
    arrow = {'U': '↑', 'D': '↓', 'L': '←', 'R': '→'}
    print("\nUtilities:")
    for y in range(rows, 1 - 1, -1):
        line = []
        for x in range(1, cols + 1):
            s = (x, y)
            if s in walls:
                line.append("#####".rjust(8))
            elif s in terminals:
                line.append(f"{terminals[s]: .2f}".rjust(8))
            else:
                line.append(f"{U.get(s, 0.0): .4f}".rjust(8))
        print(" ".join(line))

    print("\nPolicy:")
    for y in range(rows, 1 - 1, -1):
        line = []
        for x in range(1, cols + 1):
            s = (x, y)
            if s in walls:
                cell = "#####"
            elif s in terminals:
                cell = "TERM"
            else:
                a = policy.get(s, ' ')
                cell = arrow.get(a, '·')
            line.append(cell.center(6))
        print(" ".join(line))