"""
Agentic ML Marketing Core v5.0.0
Thompson Sampling (MAB) + MCTS + RAG Semantic Memory + DFS Navigation
"""
import numpy as np
import networkx as nx
from scipy.stats import beta
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, field
import json
import os

# ============================================================
# Agent State
# ============================================================
@dataclass
class AgentState:
    budget: float = 10000.0
    channels: Dict[str, float] = field(default_factory=lambda: {
        'email': 0.2, 'social': 0.3, 'seo': 0.3, 'ads': 0.2
    })
    memories: List = field(default_factory=list)
    beliefs: Dict[str, float] = field(default_factory=dict)
    total_reward: float = 0.0
    n_actions: int = 0


# ============================================================
# Thompson Sampling - Multi-Armed Bandit
# ============================================================
class ThompsonSampling:
    """Production Thompson Sampling MAB for channel allocation."""

    def __init__(self, channels: List[str], redis_client=None):
        self.channels = {ch: {'alpha': 2.0, 'beta': 2.0} for ch in channels}
        self.redis = redis_client
        self._load_beliefs()

    def _load_beliefs(self):
        if self.redis:
            data = self.redis.hgetall('thompson_beliefs')
            for ch, params in data.items():
                ch_str = ch.decode() if isinstance(ch, bytes) else ch
                params_str = params.decode() if isinstance(params, bytes) else params
                self.channels[ch_str].update(json.loads(params_str))

    def sample_action(self) -> Tuple[str, Dict[str, float]]:
        """Sample from all posteriors, return best action."""
        posteriors = {}
        for ch, params in self.channels.items():
            theta = np.random.beta(max(params['alpha'], 1), max(params['beta'], 1))
            posteriors[ch] = float(theta)
        best_action = max(posteriors, key=posteriors.get)
        return best_action, posteriors

    def update(self, action: str, reward: float):
        """Bayesian update after observation."""
        params = self.channels[action]
        params['alpha'] += reward
        params['beta'] += (1 - reward)
        if self.redis:
            self.redis.hset('thompson_beliefs', action, json.dumps({
                'alpha': float(params['alpha']),
                'beta': float(params['beta'])
            }))


# ============================================================
# MCTS Planner
# ============================================================
class MCTSNode:
    """MCTS tree node."""
    def __init__(self, state: Dict, parent=None):
        self.state = state
        self.parent = parent
        self.children: List['MCTSNode'] = []
        self.visits = 0
        self.value = 0.0
        self.untried = ['email', 'social', 'seo', 'ads']

    def best_child(self, c_param=1.414):
        choices = [c for c in self.children if c.visits > 0]
        if not choices:
            return None
        ucb_values = []
        for child in choices:
            exploitation = child.value / child.visits
            exploration = c_param * np.sqrt(np.log(self.visits) / child.visits)
            ucb_values.append(exploitation + exploration)
        return choices[np.argmax(ucb_values)]

    def add_child(self, action: str, state: Dict):
        child = MCTSNode(state, parent=self)
        child.untried = []
        self.children.append(child)
        return child


class MCTSPlanner:
    """Monte Carlo Tree Search for marketing budget optimization."""

    def __init__(self, budget: float = 10000, iterations: int = 5000,
                 c_param: float = 1.414):
        self.budget = budget
        self.iterations = iterations
        self.c_param = c_param
        self.channels = ['email', 'social', 'seo', 'ads']
        self.roi_map = {'email': 5.5, 'social': 2.8, 'seo': 4.1, 'ads': 3.2}
        self.root = MCTSNode({'budget': budget, 'allocation': {}})

    def _simulate(self, node: MCTSNode) -> float:
        """Rollout simulation."""
        remaining = node.state['budget']
        total_roi = 0.0
        alloc = dict(node.state.get('allocation', {}))
        for ch in self.channels:
            if ch not in alloc and remaining > 0:
                spend = min(remaining * np.random.uniform(0.1, 0.4), remaining)
                alloc[ch] = spend
                remaining -= spend
                total_roi += spend * self.roi_map[ch] / 100
        return total_roi

    def _backpropagate(self, node: MCTSNode, reward: float):
        while node is not None:
            node.visits += 1
            node.value += reward
            node = node.parent

    def search(self) -> Tuple[Dict[str, float], float]:
        """Run MCTS and return best allocation."""
        for _ in range(self.iterations):
            node = self.root
            state_budget = node.state['budget']
            alloc = dict(node.state.get('allocation', {}))

            # Selection
            while node.untried == [] and node.children:
                node = node.best_child(self.c_param) or node
                if node is None:
                    break
                state_budget = node.state['budget']
                alloc = dict(node.state.get('allocation', {}))

            # Expansion
            if node.untried and state_budget > 0:
                action = np.random.choice(node.untried)
                node.untried.remove(action)
                spend = min(state_budget * np.random.uniform(0.15, 0.35), state_budget)
                new_alloc = dict(alloc)
                new_alloc[action] = new_alloc.get(action, 0) + spend
                child_state = {'budget': state_budget - spend, 'allocation': new_alloc}
                node = node.add_child(action, child_state)

            # Simulation + Backpropagation
            reward = self._simulate(node)
            self._backpropagate(node, reward)

        # Extract best allocation
        best_child = self.root.best_child(self.c_param) if self.root.children else None
        if best_child:
            return best_child.state['allocation'], best_child.value / max(best_child.visits, 1)
        return {}, 0.0


# ============================================================
# RAG Semantic Memory
# ============================================================
class SemanticMemory:
    """Simple RAG-like semantic memory using cosine similarity."""

    def __init__(self, max_memories: int = 10000):
        self.max_memories = max_memories
        self.memories: List[Dict] = []

    def add(self, query: str, result: Dict):
        if len(self.memories) >= self.max_memories:
            self.memories.pop(0)
        self.memories.append({'query': query, 'result': result, 'timestamp': str(np.datetime64('now'))})

    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        """Simple keyword-based retrieval (cosine sim placeholder)."""
        query_words = set(query.lower().split())
        scored = []
        for mem in self.memories:
            mem_words = set(mem['query'].lower().split())
            overlap = len(query_words & mem_words) / max(len(query_words | mem_words), 1)
            scored.append((overlap, mem))
        scored.sort(reverse=True)
        return [m for _, m in scored[:top_k]]

    def get_stats(self) -> Dict:
        return {'total_memories': len(self.memories), 'max_capacity': self.max_memories}


# ============================================================
# DFS Navigation Tree (Permission Filtered)
# ============================================================
def dfs_nav_build(role: str = "user") -> Dict:
    """Build navigation tree with permission filtering."""
    nav = {
        "🏠 Dashboard": ["Overview", "Live Metrics", "Alerts"],
        "🧠 ML Models": ["Training", "Predictions", "Feature Analysis"],
        "📊 Campaigns": ["Optimizer", "Strategy Tree", "A/B Tests"],
        "📈 Reports": ["ROI", "Attribution", "Forecasts"]
    }
    if role == "admin":
        nav["⚙️ Admin"] = ["API Keys", "User Management", "System Logs", "Model Registry"]
    return nav


def dfs_traverse(node, path=None, results=None):
    """DFS traversal of navigation tree."""
    if path is None:
        path = []
    if results is None:
        results = []
    if isinstance(node, dict):
        for key, value in node.items():
            dfs_traverse(value, path + [key], results)
    elif isinstance(node, list):
        for item in node:
            dfs_traverse(item, path, results)
    else:
        results.append(" → ".join(path + [str(node)]))
    return results


# ============================================================
# Unified Agentic Pipeline
# ============================================================
class AgenticMarketingPipeline:
    """Complete self-learning marketing agent pipeline."""

    def __init__(self, redis_client=None, budget: float = 10000):
        self.state = AgentState(budget=budget)
        self.thompson = ThompsonSampling(['email', 'social', 'seo', 'ads'], redis_client)
        self.mcts = MCTSPlanner(budget=budget, iterations=5000)
        self.memory = SemanticMemory()
        self.nav_tree = dfs_nav_build("user")

    def run_cycle(self) -> Dict:
        """Run one full agentic cycle."""
        # Thompson Sampling action
        action, posteriors = self.thompson.sample_action()

        # MCTS optimization
        mcts_alloc, mcts_roi = self.mcts.search()

        # Store in memory
        self.memory.add(f"{action} campaign", {
            'action': action, 'posteriors': posteriors,
            'mcts_roi': mcts_roi, 'mcts_alloc': mcts_alloc
        })

        self.state.n_actions += 1
        self.state.total_reward += mcts_roi

        return {
            'thompson_action': action,
            'thompson_posteriors': {k: round(v, 3) for k, v in posteriors.items()},
            'mcts_allocation': {k: round(v, 2) for k, v in mcts_alloc.items()},
            'mcts_predicted_roi': round(mcts_roi, 2),
            'total_actions': self.state.n_actions,
            'cumulative_reward': round(self.state.total_reward, 2)
        }

    def get_accessible_pages(self) -> List[str]:
        return dfs_traverse(self.nav_tree)
