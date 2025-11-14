from math import comb

class BitCombinations:
    def __init__(self, k: int, n: int, m: int, sec_txt: str):
        self.k = k
        self.n = n
        self.m = m
        self.sec_txt = sec_txt
        self.sec_len = None 
        self.zeros = k - 1
        self.ones = n - self.zeros
        self.total_comb = comb(n, k - 1)
        self.matrix = []      # Will store combinations as lists of bits
        self.mand_mask = []   # Will store mandatory mask
        self.combined_mat = []
        self.repeated_combined_mat = []
        
        if not (m < k < n):
            raise ValueError("Must satisfy m < k < n")

    def mandatory_mask(self):
        """Create identity + zero rows as mandatory mask"""
        identity = [[1 if i == j else 0 for j in range(self.m)] for i in range(self.m)]
        zeros = [[0] * self.m for _ in range(self.n - self.m)]
        mask_matrix = identity + zeros
        self.mand_mask = mask_matrix

        # print("\nMandatory Matrix:")
        # for row in mask_matrix:
        #     print(row)

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

    def print_list(self, l):
        for element in l:
            print(element, end = "")
        print("")
         
    def print_mask_matrix(self):
        for row in self.combined_mat:
            self.print_list(row)

    def get_ith_mask(self, i, length):
        mask_i = self.combined_mat[i]
        return mask_i * (length // len(mask_i)) + mask_i[0:length % len(mask_i)]
    
    def repeat_mask(self):
        # for repeating mask
        print("\nrepeated combined mask\n")
        base_len = len(self.combined_mat[0])
        for mask in self.combined_mat:
            repeats = self.sec_len // base_len
            remainder = self.sec_len % base_len
            repeated_mask = mask * repeats + mask[:remainder]
            self.repeated_combined_mat.append(repeated_mask)

        return self.repeated_combined_mat
    
    def print_repeated_mask_matrix(self):
        for row in self.repeated_combined_mat:
            self.print_list(row)

    def string_to_binary(self):
        binary = ''.join(format(ord(c), '08b') for c in self.sec_txt)
        self.sec_len = len(binary)
        return self.sec_len

if __name__ == "__main__":
    combo = BitCombinations(k=5, n=7, m=3, sec_txt="secret")
    combo.generate()
    combo.string_to_binary()

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

    #combo.print_list([1, 2, 3])
    combo.print_mask_matrix()
    combo.print_list(combo.get_ith_mask(0, 80))

    combo.repeated_mask = combo.repeat_mask()
    combo.print_repeated_mask_matrix()
