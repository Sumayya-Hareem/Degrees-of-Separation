from collections import deque


class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


class QueueFrontier(StackFrontier):
    def __init__(self):
        self.frontier = deque()
        self.states = set()  # This makes "contains_state" instant

    def add(self, node):
        self.frontier.append(node)
        self.states.add(node.state)

    def contains_state(self, state):
        return state in self.states

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier.popleft()  # Instant removal
            self.states.remove(node.state)
            return node