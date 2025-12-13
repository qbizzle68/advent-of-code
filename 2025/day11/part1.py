import sys
import re


class Node:
    def __init__(self, name: str) -> None:
        self.name = name
        self.links = []

    def add(self, node: 'Node') -> None:
        self.links.append(node)


def parse_input(filepath: str) -> dict[str, list[str]]:
    with open(filepath) as f:
        data = f.readlines()

    connections = {}
    for d in data:
        match = re.findall('[a-zA-Z]{3}', d)
        if match == []:
            raise Exception(f'Unable to parse line {d}')
        
        connections[match[0]] = set(match[1:])
    connections['out'] = []

    return connections


def build_tree(data: dict[str, list[str]]) -> Node:
    nodes = {name: Node(name) for name in data}
    
    for name, node in nodes.items():
        for link_name in data[name]:
            node.add(nodes[link_name])

    return nodes['you']


def count_out(node: Node) -> int:
    out_links = [link for link in node.links if link.name == 'out']
    node_links = [link for link in node.links if link.name != 'out']

    result = len(out_links) + sum(count_out(link) for link in node_links)
    return result


def main(root: Node) -> int:
    return count_out(root)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} FILEPATH')
    filepath = sys.argv[1]

    data = parse_input(filepath)
    root = build_tree(data)
    print(main(root))
