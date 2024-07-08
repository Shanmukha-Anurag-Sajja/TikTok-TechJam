
import random, os

global mine_values, mine_values_copy, numbers, mine_no, n


def set_mines():
    global mine_values
    global numbers
    global mine_no
    global n
    # Track of number of mines already set up
    count = 0
    while count < mine_no:
 
        # Random number from all possible grid positions 
        val = random.randint(0, n*n-1)
 
        # Generating row and column from the number
        r = val // n
        col = val % n
 
        # Place the mine, if it doesn't already have one
        if mine_values[r][col] != 'M':
            count = count + 1
            numbers[r][col] = -1
            mine_values[r][col] = 'M'

def set_values():
    global mine_values
    global numbers
    global n
    for r in range(n):
        for col in range(n):
 
            # Skip, if it contains a mine
            if numbers[r][col] == -1:
                continue
 
            # Check up  
            if r > 0 and numbers[r-1][col] == -1:
                numbers[r][col] = numbers[r][col] + 1
            # Check down    
            if r < n-1  and numbers[r+1][col] == -1:
                numbers[r][col] = numbers[r][col] + 1
            # Check left
            if col > 0 and numbers[r][col-1] == -1:
                numbers[r][col] = numbers[r][col] + 1
            # Check right
            if col < n-1 and numbers[r][col+1] == -1:
                numbers[r][col] = numbers[r][col] + 1
            # Check top-left    
            if r > 0 and col > 0 and numbers[r-1][col-1] == -1:
                numbers[r][col] = numbers[r][col] + 1
            # Check top-right
            if r > 0 and col < n-1 and numbers[r-1][col+1] == -1:
                numbers[r][col] = numbers[r][col] + 1
            # Check below-left  
            if r < n-1 and col > 0 and numbers[r+1][col-1] == -1:
                numbers[r][col] = numbers[r][col] + 1
            # Check below-right
            if r < n-1 and col < n-1 and numbers[r+1][col+1] == -1:
                numbers[r][col] = numbers[r][col] + 1
            if numbers[r][col]!=0:
                mine_values[r][col] = str(numbers[r][col])

def show_mines():
    global mine_values_copy
    global numbers
    global n
 
    for r in range(n):
        for col in range(n):
            if numbers[r][col] == -1:
                mine_values_copy[r][col] = 'M'

def neighbours(r, col):
     
    global mine_values_copy
    global numbers
    global vis
 
    # If the cell already not visited
    if [r,col] not in vis:
 
        # Mark the cell visited
        vis.append([r,col])
 
        # If the cell is zero-valued
        if numbers[r][col] == 0:
 
            # Display it to the user
            mine_values_copy[r][col] = str(numbers[r][col])
 
            # Recursive calls for the neighbouring cells
            if r > 0:
                neighbours(r-1, col)
            if r < n-1:
                neighbours(r+1, col)
            if col > 0:
                neighbours(r, col-1)
            if col < n-1:
                neighbours(r, col+1)    
            if r > 0 and col > 0:
                neighbours(r-1, col-1)
            if r > 0 and col < n-1:
                neighbours(r-1, col+1)
            if r < n-1 and col > 0:
                neighbours(r+1, col-1)
            if r < n-1 and col < n-1:
                neighbours(r+1, col+1)  
 
        # If the cell is not zero-valued            
        if numbers[r][col] != 0:
                mine_values_copy[r][col] = str(numbers[r][col])

    
def validate(r, col):
    global vis, numbers, mine_values_copy
    print("validate received r: ", r)
    print("validate received col: ", col)
    if(r == None and col == None):
        return
    
    if numbers[r][col]==-1:
        mine_values_copy[r][col] = 'M'
        show_mines()
        return [True,mine_values_copy]
    elif numbers[r][col]==0:
        vis = []
        mine_values_copy[r][col]='0'
        neighbours(r,col)
        return [False, mine_values_copy]
    else:
        mine_values_copy[r][col] = str(numbers[r][col])
        return [False, mine_values_copy]

def initialize():
    global mine_values, mine_values_copy, numbers, mine_no, n
    n = 8
    mine_values = [['0' for i in range(n)] for j in range(n)]
    mine_values_copy = [['X' for i in range(n)] for j in range(n)]
    numbers = [[0 for x in range(n)] for y in range(n)]
    mine_no = 8
    set_mines()
    set_values()


# print_layout(n,numbers)
# over = False

# while not over:
#     print_layout(n,mine_values_copy)
#     inp = input("Enter row number followed by space and column number: ")
#     if len(inp)==3:
#         try:
#             x = inp.split()
#             x = [int(i) for i in x]
#             val = x
#         except ValueError:
#             print("Wrong Input1")
#             continue
#     else:
#         print("Wrong Input2")
#         continue

#     if val[0]>n or val[0]<1 or val[1]>n or val[1]<1:
#         print("Wrong Input3")
#         continue
#     r = val[0]-1
#     col = val[1]-1

#     if numbers[r][col]==-1:
#         mine_values_copy[r][col] = 'M'
#         show_mines()
#         print_layout(n,mine_values)
#         print("Landed on a mine . GAME OVER !!")
#         over = True
#         continue
#     elif numbers[r][col]==0:
#         vis = []
#         mine_values_copy[r][col]='0'
#         neighbours(r,col)
#     else:
#         mine_values_copy[r][col] = str(numbers[r][col])
#     #os.system("clear")
#     if(mine_values_copy[r][col])!='X':
#         print("type again since you opened an opened box")
#     if(check_over()):
#         show_mines()
#         print_layout(n,mine_values_copy)
#         print("Congratulations !! YOU WIN")
#         over = True
#         continue
#     #os.system("clear")
