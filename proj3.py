from __future__ import annotations
from dataclasses import dataclass, field


@dataclass(order=True, frozen=True)
class Node:
    freq: int
    char: str
    left: "Node | None" = None
    right: "Node | None" = None

    def __str__(self):
        return f"Node: {self.char}, Freq: {self.freq}"


@dataclass(frozen=True)
class MinHeap:
    data: list[Node] = field(default_factory=list)


def heapify_up(heap: MinHeap, index: int) -> MinHeap:
    new_data = heap.data[:]

    if index == 0:
        return MinHeap(new_data)

    parent = (index - 1) // 2

    if new_data[index] < new_data[parent]:
        temp = new_data[index]
        new_data[index] = new_data[parent]
        new_data[parent] = temp
        return heapify_up(MinHeap(new_data), parent)

    return MinHeap(new_data)


def insert(heap: MinHeap, element: Node) -> MinHeap:
    new_data = heap.data + [element]
    return heapify_up(MinHeap(new_data), len(new_data) - 1)


def heapify_down(heap: MinHeap, index: int) -> MinHeap:
    new_data = heap.data[:]

    left = 2 * index + 1
    right = 2 * index + 2
    size = len(new_data)

    if left >= size:
        return MinHeap(new_data)

    smallest = left

    if right < size and new_data[right] < new_data[left]:
        smallest = right

    if new_data[smallest] < new_data[index]:
        temp = new_data[index]
        new_data[index] = new_data[smallest]
        new_data[smallest] = temp
        return heapify_down(MinHeap(new_data), smallest)

    return MinHeap(new_data)


def extract_min(heap: MinHeap) -> tuple[MinHeap, Node]:
    if len(heap.data) == 0:
        raise IndexError

    min_value = heap.data[0]

    if len(heap.data) == 1:
        return MinHeap([]), min_value

    last_value = heap.data[-1]
    new_data = [last_value] + heap.data[1:-1]
    new_heap = heapify_down(MinHeap(new_data), 0)

    return new_heap, min_value


def count_frequency(s: str) -> dict[str, int]:
    freq = {}

    for ch in s:
        if ch not in freq:
            freq[ch] = 1
        else:
            freq[ch] += 1

    return freq


def create_priority_queue(frequency: dict[str, int]) -> MinHeap:
    new_heap = MinHeap([])

    for k in frequency:
        new_node = Node(freq=frequency[k], char=k)
        new_heap = insert(new_heap, new_node)

    return new_heap


def build_tree(priority_queue: MinHeap) -> Node:
    new_heap = MinHeap(priority_queue.data[:])

    if len(new_heap.data) == 0:
        raise ValueError

    if len(new_heap.data) == 1:
        return new_heap.data[0]

    new_heap, m1 = extract_min(new_heap)
    new_heap, m2 = extract_min(new_heap)

    sum_min = m1.freq + m2.freq
    new_node = Node(freq=sum_min, char=m1.char + m2.char, left=m1, right=m2)

    new_heap = insert(new_heap, new_node)

    return build_tree(new_heap)


def generate_codes(node: Node | None, prefix: str = "", code: dict | None = None) -> dict:
    if code is None:
        code = {}

    if node is None:
        return code

    if node.left is None and node.right is None:
        if prefix == "":
            code[node.char] = "0"
        else:
            code[node.char] = prefix
        return code
    generate_codes(node.left, prefix + "0", code)
    generate_codes(node.right, prefix + "1", code)

    return code


def encode(s: str, codes: dict) -> str:
    result = ""

    for char in s:
        result += codes[char]

    return result


def decode(encoded_string: str, root: Node) -> str:
    if root.left is None and root.right is None:
        return root.char * len(encoded_string)

    result = ""
    current = root

    for bit in encoded_string:
        if bit == "0":
            current = current.left
        else:
            current = current.right

        if current.left is None and current.right is None:
            result += current.char
            current = root

    return result


def huffman_encoding(s: str):
    # Do Not Change this function
    frequency = count_frequency(s)
    pq = create_priority_queue(frequency)
    root = build_tree(pq)
    codes = generate_codes(root)
    encoded_string = encode(s, codes)
    decoded_string = decode(encoded_string, root)
    return encoded_string, decoded_string, codes