from cats.CatFather import CatFather
class BreadthFirstSearchCat(CatFather):
    def __init__(self, start_cell : 'Cell.Cell', objective_cell : 'Cell.Cell' , grid):
        super().__init__(start_cell, objective_cell, grid)

        self.reset()

    def reset(self):
        super().reset()

    def find_path(self):
        pass


def breadth_first_search(problem):

    # a dictionary to maintain meta information (used for path formation)
    # key -> (parent state, action to reach child)
    meta = dict()

    # initialize
    root = problem.get_root()
    meta[root] = (None, None)
    open_set.enqueue(root)

    # For each node on the current level expand and process, if no children
    # (leaf) then unwind
    while not open_set.is_empty():
        subtree_root = open_set.dequeue()
        # We found the node we wanted so stop and emit a path.
        if problem.is_goal(subtree_root):
            return construct_path(subtree_root, meta)
        # For each child of the current tree process
        for (child, action) in problem.get_successors(subtree_root):
            # The node has already been processed, so skip over it
            if child in closed_set:
                continue
            # The child is not enqueued to be processed, so enqueue this level of
            # children to be expanded
            if child not in open_set:
                meta[child] = (subtree_root, action)  # create metadata for these nodes
                open_set.enqueue(child)  # enqueue these nodes
        # We finished processing the root of this subtree, so add it to the closed
        # set
        closed_set.add(subtree_root)