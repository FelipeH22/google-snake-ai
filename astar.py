import heapq

came_from=dict()

def heuristic(position,final_position):
    return abs(position[0] - final_position[0]) + abs(position[1] - final_position[1])

def a_star(initial_position,final_position,game_board):
    open_set=list()
    closed_set=set()
    heapq.heappush(open_set,(0, initial_position))
    g_score = {initial_position:0}
    f_score = {initial_position:heuristic(initial_position,final_position)}
    while open_set:
        current_position = heapq.heappop(open_set)[1]
        if current_position == final_position:
            path=list()
            while current_position in came_from:
                path.append(current_position)
                current_position=came_from[current_position]
            path.reverse()
            return path

        closed_set.add(current_position)
        for neighbor in [(current_position[0]+1, current_position[1]), (current_position[0]-1, current_position[1]),
                         (current_position[0], current_position[1]+1), (current_position[0], current_position[1]-1)]:
            if not (0<=neighbor[0]<18 and 0<=neighbor[1]<16):
                continue

            if game_board[neighbor[0]][neighbor[1]]==1:
                continue

            tentative_g_score = g_score[current_position]+1
            if neighbor in closed_set and tentative_g_score>=g_score.get(neighbor,float('inf')):
                continue

            if tentative_g_score<g_score.get(neighbor, float('inf')):
                g_score[neighbor]=tentative_g_score
                f_score[neighbor]=tentative_g_score +heuristic(neighbor,final_position)
                heapq.heappush(open_set,(f_score[neighbor],neighbor))
                came_from[neighbor]=current_position
    return None