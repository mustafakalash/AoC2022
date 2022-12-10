class Tree:
    def __init__(self, x, y, height):
        self.x = x
        self.y = y
        self.height = height
        self.visible = True
        self.visibility_checked = False
        self.scenic_score = 0
        self.left_visibility = 0
        self.right_visibility = 0
        self.up_visibility = 0
        self.down_visibility = 0

    def check_visibility(self, grid):
        if not self.visibility_checked:
            if not self.is_edge_tree(grid):
                self.left_visibility = self.x
                self.right_visibility = len(grid[0]) - self.x - 1
                self.up_visibility = self.y
                self.down_visibility = len(grid) - self.y - 1
                left_blocked = False
                right_blocked = False
                up_blocked = False
                down_blocked = False

                for other in grid[self.y]:
                    if other == self:
                        continue

                    if other.height >= self.height:
                        if other.x < self.x:
                            self.left_visibility = self.x - other.x
                            left_blocked = True
                        elif other.x > self.x:
                            self.right_visibility = other.x - self.x
                            right_blocked = True
                            break

                for y, _ in enumerate(grid):
                    if y == self.y:
                        continue

                    other = grid[y][self.x]
                    if other.height >= self.height:
                        if other.y < self.y:
                            self.up_visibility = self.y - other.y
                            up_blocked = True
                        elif other.y > self.y:
                            self.down_visibility = other.y - self.y
                            down_blocked = True
                            break

                self.visible = not (
                    left_blocked and right_blocked and up_blocked and down_blocked)

                self.scenic_score = (self.up_visibility * self.down_visibility *
                                     self.left_visibility * self.right_visibility)

            self.visibility_checked = True

        return self.visible

    def is_edge_tree(self, grid):
        return (self.x == 0 or self.x == len(grid[0]) - 1
                or self.y == 0 or self.y == len(grid) - 1)


def __main__():
    visible_trees = 0
    best_scenic_score = 0
    with open("8/input", "r", encoding = "UTF-8") as f:
        grid = list()
        for y, line in enumerate(f):
            line = line.strip()

            row = list()
            for x, height in enumerate(line):
                row.append(Tree(x, y, int(height)))
            grid.append(row)

        for row in grid:
            for tree in row:
                if tree.check_visibility(grid):
                    visible_trees += 1
                best_scenic_score = max(best_scenic_score, tree.scenic_score)

    print(visible_trees)
    print(best_scenic_score)


__main__()
