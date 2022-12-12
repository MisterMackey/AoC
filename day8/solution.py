def get_grid(test = False) -> list[list[int]]:
    if test:
        with open('./input') as f:
            lines = f.read().splitlines()
    else:
        with open('./input_full') as f:
            lines = f.read().splitlines()
    output = list[list[int]]()
    for line in lines:
        row = list[int]()
        for digit in line:
            row.append(int(digit))
        output.append(row)
    return output

class Tree:
    def __init__(self, height: int) -> None:
        self.height = height
        self.visible_from_left = False
        self.visible_from_right = False
        self.visible_from_top = False
        self.visible_from_bottom = False
        self.scenic_score = 0
    
    def __str__(self) -> str:
        def letter(x: bool):
            if x:
                return 'o'
            else:
                return 'x'
        return ' {0} \n{1}{2}{3}\n {4} '.format(letter(self.visible_from_top), 
                                                       letter(self.visible_from_left),
                                                       self.height,
                                                       letter(self.visible_from_right),
                                                       letter(self.visible_from_bottom))

def create_tree_grid(grid : list[list[int]]) -> list[list[Tree]]:
    #form basic grid
    x = list[list[Tree]]()
    for row in grid:
        nrow = list[Tree]()
        for column in row:
            nrow.append(Tree(column))
        x.append(nrow)
    #visible from left or top
    max_height_top = list[int]()
    for i_row in range(len(x)):
        max_height_left = 0
        for i_column in range(len(x[i_row])):
            tree = x[i_row][i_column]
            if i_row == 0:
                tree.visible_from_top = True
                max_height_top.append(tree.height)
            else:
                if tree.height > max_height_top[i_column]:
                    max_height_top[i_column] = tree.height
                    tree.visible_from_top = True
            if i_column == 0:
                tree.visible_from_left = True
                max_height_left = tree.height
            else:
                if tree.height > max_height_left:
                    max_height_left = tree.height
                    tree.visible_from_left = True

    #visible from right or bottom
    max_height_bottom = list[int]()
    for row in x[0]:
        max_height_bottom.append(0)
    for i_row in range(len(x)-1, -1, -1):
        max_height_right = 0
        for i_column in range(len(x[i_row])-1, -1, -1):
            tree = x[i_row][i_column]
            if i_row == len(x)-1:
                tree.visible_from_bottom = True
                max_height_bottom[i_column] = tree.height
            else:
                if tree.height > max_height_bottom[i_column]:
                    max_height_bottom[i_column] = tree.height
                    tree.visible_from_bottom = True
            if i_column == len(x[i_row])-1:
                tree.visible_from_right = True
                max_height_right = tree.height
            else:
                if tree.height > max_height_right:
                    max_height_right = tree.height
                    tree.visible_from_right = True
    return x
            
def count_visible_trees(tree_grid: list[list[Tree]]) -> int:
    num = 0
    for y in tree_grid:
        for x in y:
            if x.visible_from_top or x.visible_from_bottom or x.visible_from_left or x.visible_from_right:
                num += 1
    return num

def get_anwer():
    x = get_grid()
    y = create_tree_grid(x)
    count = count_visible_trees(y)
    print(count)
    
def compute_scenic_score(tree_grid : list[list[Tree]]):
    #only 99 X 99, should fit in cache easily right?
    for i_row, row in enumerate(tree_grid):
        for i_col, tree in enumerate(row):
            #count left, mininum of 1
            trees_left = 0
            for i in range(i_col, -1, -1):
                if i == 0:
                    break;
                trees_left += 1
                if row[i-1].height >= tree.height:
                    break;
            #repeat for other directions
            trees_right = 0
            for i in range(i_col, len(row)):
                if i == len(row)-1:
                    break;
                trees_right += 1
                if row[i+1].height >= tree.height:
                    break;
            trees_top = 0
            for i in range(i_row, -1, -1):
                if i == 0:
                    break;
                trees_top += 1
                if tree_grid[i-1][i_col].height >= tree.height:
                    break;
            trees_bottom = 0
            for i in range(i_row, len(tree_grid)):
                if i == len(tree_grid)-1:
                    break;
                trees_bottom += 1
                if tree_grid[i+1][i_col].height >= tree.height:
                    break;
            score = trees_left * trees_right * trees_top * trees_bottom
            tree.scenic_score = score
            
def get_part_2_answer():
    x = get_grid()
    y = create_tree_grid(x)
    compute_scenic_score(y)
    flat_scores = [tree.scenic_score for row in y for tree in row]
    print(max(flat_scores))