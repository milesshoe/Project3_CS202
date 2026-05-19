import unittest
from proj3 import (
    Node,
    MinHeap,
    heapify_up,
    insert,
    extract_min,
    count_frequency,
    create_priority_queue,
    build_tree,
    generate_codes,
    encode,
    decode,
    huffman_encoding,
)


class TestHeapFunctions(unittest.TestCase):

    def test_heapify_up(self):
        heap = MinHeap([
            Node(3, "c"),
            Node(5, "e"),
            Node(4, "d"),
            Node(1, "a"),
        ])

        result = heapify_up(heap, 3)

        self.assertEqual(result.data[0].char, "a")
        self.assertEqual(result.data[0].freq, 1)
        self.assertEqual(len(result.data), 4)

    def test_insert(self):
        heap = MinHeap([
            Node(2, "b"),
            Node(4, "d"),
            Node(3, "c"),
        ])

        result = insert(heap, Node(1, "a"))

        self.assertEqual(result.data[0], Node(1, "a"))
        self.assertEqual(len(result.data), 4)

    def test_extract_min(self):
        heap = MinHeap([
            Node(1, "a"),
            Node(3, "c"),
            Node(2, "b"),
        ])

        new_heap, minimum = extract_min(heap)

        self.assertEqual(minimum, Node(1, "a"))
        self.assertEqual(len(new_heap.data), 2)
        self.assertEqual(new_heap.data[0], Node(2, "b"))


class TestHuffmanFunctions(unittest.TestCase):

    def test_count_frequency(self):
        result = count_frequency("aabbc")

        self.assertEqual(result, {"a": 2, "b": 2, "c": 1})

    def test_generate_codes_simple_tree(self):
        tree = Node(
            2,
            "ab",
            left=Node(1, "a"),
            right=Node(1, "b"),
        )

        codes = generate_codes(tree)

        self.assertEqual(codes, {"a": "0", "b": "1"})

    def test_encode_decode_simple_tree(self):
        tree = Node(
            2,
            "ab",
            left=Node(1, "a"),
            right=Node(1, "b"),
        )

        codes = generate_codes(tree)
        encoded = encode("abba", codes)
        decoded = decode(encoded, tree)

        self.assertEqual(encoded, "0110")
        self.assertEqual(decoded, "abba")

    def test_single_character(self):
        encoded, decoded, codes = huffman_encoding("aaaa")

        self.assertEqual(decoded, "aaaa")
        self.assertIn("a", codes)
        self.assertEqual(len(codes), 1)

    def test_repeated_characters(self):
        encoded, decoded, codes = huffman_encoding("bbbbbb")

        self.assertEqual(decoded, "bbbbbb")
        self.assertEqual(len(codes), 1)
        self.assertIn("b", codes)

    def test_empty_string_raises_error(self):
        with self.assertRaises(ValueError):
            huffman_encoding("")

    def test_tree_shape_two_characters(self):
        frequency = count_frequency("ABBA")
        pq = create_priority_queue(frequency)
        root = build_tree(pq)

        self.assertEqual(root.freq, 4)
        self.assertIsNotNone(root.left)
        self.assertIsNotNone(root.right)
        self.assertEqual(root.left.char, "A")
        self.assertEqual(root.right.char, "B")

    def test_code_lengths(self):
        encoded, decoded, codes = huffman_encoding("hello")

        self.assertEqual(decoded, "hello")
        self.assertEqual(codes["l"], "0")
        self.assertEqual(len(codes["l"]), 1)
        self.assertGreaterEqual(len(codes["h"]), 2)
        self.assertGreaterEqual(len(codes["e"]), 2)
        self.assertGreaterEqual(len(codes["o"]), 2)


if __name__ == "__main__":
    unittest.main()