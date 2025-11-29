from collections import deque

# 외부 공기(바깥에서 통하는 0)를 BFS로 찾고,
# 그 외부 공기와 맞닿은 치즈(1)의 통계치를 구하는 함수
def compute_surface_stats(board):
    n = len(board)
    m = len(board[0])

    # 패딩 추가 (바깥 한 줄 0으로 둘러싸기)
    padded = [[0] * (m + 2) for _ in range(n + 2)]
    for i in range(n):
        for j in range(m):
            padded[i + 1][j + 1] = board[i][j]

    # 외부 공기 표시 배열
    outside = [[False] * (m + 2) for _ in range(n + 2)]

    # (0,0)에서 BFS 시작 → 바깥 공기와 연결된 모든 0 탐색
    dq = deque()
    dq.append((0, 0))
    outside[0][0] = True
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    while dq:
        x, y = dq.popleft()
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n + 2 and 0 <= ny < m + 2:
                if not outside[nx][ny] and padded[nx][ny] == 0:
                    outside[nx][ny] = True
                    dq.append((nx, ny))

    total_cheese = 0           # 전체 치즈 칸 수 (부피 개념)
    surface_cells = 0          # 외부 공기와 최소 1면 이상 맞닿은 치즈 칸 수
    contact_sides = 0          # 외부 공기와 맞닿은 변(모서리 아님, 면) 총 개수

    # 실제 격자 영역(1~n, 1~m)에서 치즈 주변을 조사
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if padded[i][j] == 1:
                total_cheese += 1
                cnt = 0
                for dx, dy in dirs:
                    nx, ny = i + dx, j + dy
                    if outside[nx][ny]:
                        cnt += 1
                if cnt > 0:
                    surface_cells += 1
                    contact_sides += cnt

    # 비율 계산 (0으로 나누는 것 방지)
    surface_ratio = surface_cells / total_cheese if total_cheese > 0 else 0.0
    contact_ratio = contact_sides / total_cheese if total_cheese > 0 else 0.0

    return {
        "total_cheese": total_cheese,
        "surface_cells": surface_cells,
        "contact_sides": contact_sides,
        "surface_ratio": surface_ratio,   # 외부와 맞닿은 치즈 칸 / 전체 치즈 칸
        "contact_ratio": contact_ratio,   # 외부와 맞닿은 변 개수 / 전체 치즈 칸
    }

def print_stats(name, stats):
    print(f"[{name}]")
    print(f"전체 치즈 칸 수: {stats['total_cheese']}")
    print(f"외부 공기와 맞닿은 치즈 칸 수: {stats['surface_cells']}")
    print(f"외부 공기와 맞닿은 변의 총 개수: {stats['contact_sides']}")
    print(f"표면적/부피 비율(칸 기준): {stats['surface_ratio']:.3f}")
    print(f"표면 접촉 변/부피 비율: {stats['contact_ratio']:.3f}")
    print()

if __name__ == "__main__":
    # 예시 1: 한 덩어리로 모여 있는 경우 (부피 = 8)
    # 0 = 빈칸(체액), 1 = 치즈(세포 덩어리)
    one_cluster = [
        [0,0,0,0,0,0,0,0],
        [0,1,1,1,1,0,0,0],
        [0,1,1,1,1,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
    ]

    # 예시 2: 두 덩어리로 나뉜 경우 (부피 = 8, 개수는 동일)
    two_clusters = [
        [0,0,0,0,0,0,0,0],
        [0,1,1,0,0,1,1,0],
        [0,1,1,0,0,1,1,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
    ]

    stats_one = compute_surface_stats(one_cluster)
    stats_two = compute_surface_stats(two_clusters)

    print_stats("한 덩어리", stats_one)
    print_stats("두 덩어리", stats_two)
