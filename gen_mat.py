from math import comb

class BitCombinations:
    def __init__(self, k: int, n: int, m: int):
        self.k = k
        self.n = n
        self.m = m
        self.zeros = k - 1
        self.ones = n - self.zeros
        self.total_comb = comb(n, k - 1)
        self.matrix = []      # Will store combinations as lists of bits
        self.mand_mask = []   # Will store mandatory mask
        self.combined_mat = []

    def mandatory_mask(self):
        """Create identity + zero rows as mandatory mask"""
        identity = [[1 if i == j else 0 for j in range(self.m)] for i in range(self.m)]
        zeros = [[0] * self.m for _ in range(self.n - self.m)]
        mask_matrix = identity + zeros
        self.mand_mask = mask_matrix

        print("\nMandatory Matrix:")
        for row in mask_matrix:
            print(row)

    def generate(self):
        """Generate all bit combinations with (k-1) zeros"""
        total_bits = self.n
        zeros = self.zeros
        ones = self.ones

        x = (1 << ones) - 1
        limit = 1 << total_bits

        while x < limit:
            binary_str = f"{x:0{total_bits}b}"
            if binary_str.count('0') == zeros:
                self.matrix.append([int(b) for b in binary_str])

            c = x & -x
            r = x + c
            x = (((r ^ x) >> 2) // c) | r

    def get_matrix(self):
        return self.matrix

    def get_transpose(self):
        if not self.matrix:
            raise ValueError("Matrix not generated yet. Call generate() first.")
        return [list(row) for row in zip(*self.matrix)]

    def combine_with_mandatory(self, transposed_matrix):
        """Combine each row of the transposed matrix with the mandatory mask"""
        if not self.mand_mask:
            self.mandatory_mask()

        combined_matrix = [
            transposed_matrix[i] + self.mand_mask[i]
            for i in range(len(transposed_matrix))
        ]

        return combined_matrix


if __name__ == "__main__":
    combo = BitCombinations(k=5, n=7, m=3)
    combo.generate()

    # Transpose and print
    transposed = combo.get_transpose()
    print("\nMask Matrix:")
    for row in transposed:
        print(row)

    combo.mandatory_mask()
    combo.combined_mat = combo.combine_with_mandatory(transposed)

    print("\nActual Mask Matrix:")
    for row in combo.combined_mat:
        print(row)
