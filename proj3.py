from __future__ import annotations
from dataclasses import dataclass, field

@dataclass(order=True, frozen=True)
class Node:
    freq: int
    char: str
    left: Node | None = None
    right: Node | None  = None

    def __str__(self):
        return f"Node: {self.char}, Freq: {self.freq}"

@dataclass(frozen=True)
class MinHeap:
    data: list[Node] = field(default_factory=list)

def heapify_up(heap: MinHeap, index: int) -> MinHeap:
    new_heap = MinHeap(heap.data)

    if index == 0:
        return new_heap

    parent = (index - 1) // 2

    if new_heap[index].freq < new_heap[parent].freq:
        temp = new_heap[index]
        new_heap[index] = new_heap[parent]
        new_heap[parent] = temp
        return heapify_up(new_heap, parent)

    return new_heap

def insert(heap: MinHeap, element: Node) -> MinHeap:
    new_heap = MinHeap(heap.data + [element])
    new_heap = heapify_up(new_heap, len(new_heap.data) - 1)
    return MinHeap(data=new_heap.data)


def heapify_down(heap: MinHeap, index: int) -> MinHeap:
    new_heap = MinHeap(heap.data)
    left = 2 * index + 1
    right = 2 * index + 2
    size = len(new_heap.data)

    if left >= size:
        return new_heap

    smallest = left

    if right < size and new_heap.data[right] < new_heap.data[left]:
        smallest = right

    if new_heap.data[smallest] < new_heap.data[index]:
        temp = new_heap.data[index]
        new_heap[index] = new_heap[smallest]
        new_heap.data[smallest] = temp
        return heapify_down(new_heap, smallest)

    return new_heap


def extract_min(heap: MinHeap) -> tuple[MinHeap, Node]:
    new_heap = MinHeap(heap.data)
    new_heap.data[0] = new_heap.data[len(new_heap.data)-1]
    return heapify_down(new_heap, 0), heap.data[0]


        
def count_frequency(s: str)-> dict[str,int]:
    freq = {}
    for ch in s:
        if ch not in freq:
            freq[ch] = 1
        else:
            freq[ch] +=1
    return freq


def create_priority_queue(frequency: dict[str, int]) -> MinHeap:
    new_data = []
    new_heap = MinHeap(new_data)
    for k in frequency:
        new_node = Node(freq = frequency[k], char = k, left = None, right = None)
        insert(new_heap, new_node)

    return new_heap


def build_tree(priority_queue: MinHeap) -> Node:
    new_heap = MinHeap(priority_queue.data)
    if len(new_heap.data) == 1:
        return new_heap.data[0]
    m1 = extract_min(new_heap)[1]
    m2 = extract_min(new_heap)[1]
    sum_min = m1.freq + m2.freq
    new_node = Node(freq=sum_min, char=m2.char, left=m2, right=m1)
    insert(new_heap, new_node)
    return build_tree(new_heap)






def generate_codes(node: Node | None, prefix="", code: dict | None =None)-> dict:
    new_dict = {}
    if code is None:
        code = {}
    generate_codes(node)
    pass


def encode(s: str, codes: dict)-> str:
    pass


def decode(encoded_string: str, root: Node):
    pass

def huffman_encoding(s:str):
    #Do Not Change this function
    frequency = count_frequency(s)
    pq = create_priority_queue(frequency)
    root = build_tree_from_queue(pq)
    codes = generate_codes(root)
    encoded_string = encode(s, codes)
    decoded_string = decode(encoded_string,root)
    return encoded_string, decoded_string, codes

