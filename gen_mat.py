from math import comb
from itertools import combinations
from typing import List

class BitCombinations:
    """
    Parameters:
        n       : number of total participants
        m       : number of mandatory shares
        k       : minimum number shares essential for reconstruction of the secret (must satisfy m < k < n)
        sec_txt : character string of the secret
    """
    def __init__(self, k: int, n: int, m: int, sec_txt: str):
        if not (m < k < n):
            raise ValueError("Must satisfy m < k < n")
        
        self.k = k
        self.n = n
        self.m = m
        self.sec_txt = sec_txt

        # self.binary_sec_txt = []
        # self.sec_len = None 

        self.zeros = k - 1
        self.ones = n - self.zeros
        self.total_comb = comb(n, k - 1)

        self.combo_matrix: List[List[int]] = []                 # Will store combinations as lists of bits
        self.mand_mask: List[List[int]] = []                    # Will store mandatory mask
        self.combined_matrix: List[List[int]] = []              # Will store combinations combined with mandatory mask
        self.repeated_combined_matrix: List[List[int]] = []     # Will store repeated combined matrix to match secret length
        self.combined_AND_mask: List[List[int]] = []            # Will store final AND-ed matrix with secret bits

        self.string_to_bits()


    # ------------------------------------------------------------------
    # Secret <-> bits
    # ------------------------------------------------------------------
        
    def string_to_bits(self) -> None :
        """Convert secret text to list of bits."""
        binary = ''.join(format(ord(c), '08b') for c in self.sec_txt)
        self.secret_bits = [int(b) for b in binary]
        self.secret_len = len(self.secret_bits)

    @staticmethod
    def bits_to_string(bits: List[int]) -> str:
        """Convert list of bits back to string."""
        if len(bits) % 8 != 0:
            raise ValueError("Binary length must be divisible by 8")

        chars: List[str] = []
        for i in range(0, len(bits), 8):
            byte_str = ''.join(str(b) for b in bits[i:i + 8])
            chars.append(chr(int(byte_str, 2)))
        return ''.join(chars)


    # ------------------------------------------------------------------
    # Combination / mask construction
    # ------------------------------------------------------------------

    def generate_combinations(self) -> None:
        """
        Generate all length-n bit strings with exactly (k-1) zeros
        """
        self.combo_matrix = []
        total_bits = self.n
        zeros = self.zeros
        ones = self.ones

        x = (1 << ones) - 1
        limit = 1 << total_bits

        while x < limit:
            binary_str = f"{x:0{total_bits}b}"
            # This condition is always true if ones+zeros==total_bits, but
            # kept to match original logic exactly.
            if binary_str.count('0') == zeros:
                self.combo_matrix.append([int(b) for b in binary_str])

            # Gosper's hack: next combination with same popcount
            c = x & -x
            r = x + c
            x = (((r ^ x) >> 2) // c) | r

    @staticmethod
    def transpose(matrix: List[List[int]]) -> List[List[int]]:
        return [list(row) for row in zip(*matrix)]
    
    def build_mandatory_mask(self):
        """Create identity + zero rows as mandatory mask"""
        identity = [[1 if i == j else 0 for j in range(self.m)] for i in range(self.m)]
        zeros_block = [[0] * self.m for _ in range(self.n - self.m)]
        self.mand_mask = identity + zeros_block

    def build_combined_with_mandatory(self) -> None:
        """Combine each row of the transposed matrix with the mandatory mask"""
        if not self.mand_mask:
            self.build_mandatory_mask()
        if not self.combo_matrix:
            self.generate_combinations()

        transposed = self.transpose(self.combo_matrix)

        self.combined_matrix = [
            transposed[i] + self.mand_mask[i]
            for i in range(self.n)
        ]

    
    def build_repeated_mask(self):
        """Repeat each combined row to reach the secret length."""
        # print("\nrepeated combined mask\n")
        if not self.combined_matrix:
            self.build_combined_with_mandatory()

        base_len = len(self.combined_matrix[0])

        repeats, remainder = divmod(self.secret_len, base_len)

        self.repeated_combined_matrix = [
            row * repeats + row[:remainder]
            for row in self.combined_matrix
        ]
    
    

    # ------------------------------------------------------------------
    # Share generation / reconstruction
    # ------------------------------------------------------------------

    def share_generation(self) -> None:
        """AND each bit with the corresponding bit in binary_sec_txt"""
        if not self.repeated_combined_matrix:
            self.build_repeated_mask()

        self.combined_AND_mask = [
            [a & b for a, b in zip(row, self.secret_bits)]
            for row in self.repeated_combined_matrix
        ]

    def reconstruct_bits(self):
        """
        Reconstruct bits by OR-ing a subset of rows.
        """
        if not self.combined_AND_mask:
            self.share_generation()

        start = self.n - self.k
        chosen_row = self.combined_AND_mask[start:]
        result: List[int] = []

        for i in range(self.secret_len):
            bit = 0
            for row in chosen_row:
                bit |= row[i]
            result.append(bit)
        
        return result
    
    def reconstruct_secret(self) -> str:
        """Full reconstruction pipeline: combined_AND_mask -> bits -> secret_string."""
        return self.bits_to_string(self.reconstruct_bits())


    # ------------------------------------------------------------------
    # Printing methods
    # ------------------------------------------------------------------            

    @staticmethod
    def print_row(row: List[int]) -> None:
        print(''.join(str(x) for x in row))  

    def print_combined_matrix(self) -> None:
        for row in self.combined_matrix:
            self.print_row(row)  

    def print_repeated_combined_matrix(self) -> None:
        for row in self.repeated_combined_matrix:
            self.print_row(row)

    def print_combined_AND_mask(self) -> None:
        for row in self.combined_AND_mask:
            self.print_row(row)  

    # def get_matrix(self):
    #     return self.matrix

    # def print_list(self, l):
    #     for element in l:
    #         print(element, end = "")
    #     print("")
         
    # def print_mask_matrix(self):
    #     for row in self.combined_mat:
    #         self.print_list(row)

    # def get_ith_mask(self, i, length):
    #     mask_i = self.combined_mat[i]
    #     return mask_i * (length // len(mask_i)) + mask_i[0:length % len(mask_i)]

    # def print_repeated_mask_matrix(self):
    #     for row in self.repeated_combined_matrix:
    #         self.print_list(row)

    # def print_combined_AND_mask(self):
    #     for row in self.combined_AND_mask:
    #         self.print_list(row)
  




if __name__ == "__main__":
    combo = BitCombinations(k=5, n=7, m=3, sec_txt="secr_t")

    combo.generate_combinations()
    combo.build_mandatory_mask()
    combo.build_combined_with_mandatory()
    combo.build_repeated_mask()
    combo.share_generation()

    print("binary msg: ")
    BitCombinations.print_row(combo.secret_bits)

    print("\nafter combining with mandatory mask (combined_matrix):")
    combo.print_combined_matrix()

    print("\nafter repeating (repeated_combined_matrix):")
    combo.print_repeated_combined_matrix()

    print("\nafter AND-ing (combined_AND_mask):")
    combo.print_combined_AND_mask()

    print("\nreconstructed msg:", combo.reconstruct_secret())