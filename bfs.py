def bfs(start, end, grid, is_valid_move):
    from collections import deque

    queue = deque([(start, [])])  
    visited = set()  # Set of visited nodes

    while queue:
        current, path = queue.popleft()  # Dequeue current node and path so far
        visited.add(current)

        # If we reached the target
        if current == end:
            return path + [current]

        # Get neighbors
        neighbors = grid.get_neighborhood(current, moore=False, include_center=False)

        for neighbor in neighbors:
            if neighbor not in visited and grid.is_cell_empty(neighbor):
                if is_valid_move(current, neighbor):  # Validate movement rules
                    queue.append((neighbor, path + [current]))

    return []  
