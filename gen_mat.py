def generate_combinations(k, n):
    total_bits = n
    zeros = k - 1
    ones = total_bits - zeros 


    x = (1 << ones) - 1
    limit = 1 << total_bits

    count = 0

    print(f"All {total_bits}-bit numbers with {zeros} zeros ({ones} ones):\n")

    while x < limit:
        binary_str = f"{x:0{total_bits}b}"
        if binary_str.count('0') == zeros: 
            print(f"{x:>3}  ->  {binary_str}")
            count += 1


        c = x & -x
        r = x + c
        x = (((r ^ x) >> 2) // c) | r

    print(f"\nGenerated {count} numbers with {zeros} zeros ({ones} ones)")


def main():
    n = 7
    k = 5
    generate_combinations(k, n)


if __name__ == "__main__":
    main()
