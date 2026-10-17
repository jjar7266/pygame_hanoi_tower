# This function generates the moves needed to solve Tower of Hanoi.
# It supports any number of disks from 3 to 8.
# Each move is sorted as a tuple: (disk_number, from_rod, to_rod).
# We use a simple recursive approach:
#  - Move n-1 disks from source to auxiliary
#  - Move the largest disk from source to target
#  - Move n-1 disks from auxiliary to target

def generate_hanoi_moves(n):
    moves = []

    def solve(num, source, target, auxiliary):
        # Base case: only one disk
        if num == 1:
            moves.append((1, source, target))
            return

        # Move n-1 disks to auxiliary
        solve(num - 1, source, auxiliary, target)

        # Move the largest disk to target
        moves.append((num, source, target))

        # Move n-1 disks from auxiliary to target
        solve(num -1, auxiliary, target, source)

    solve(n, "A", "C", "B")
    return moves

# Quick test: print moves for 3 disks
if __name__ == "__main__":
    result = generate_hanoi_moves(3)
    for move in result:
        print(move)
        
