import random
import uuid

SIZE = 540
PIECE = 32
N = 9
MARGIN = 23
GRID = (SIZE - 2 * MARGIN) / (N-1)

def pos_pixel2map(x, y):
    # Tính toán trực tiếp tọa độ logic (i, j) từ tọa độ chuột (x, y)
    j = round((x - MARGIN) / GRID)
    i = round((y - MARGIN) / GRID)
    
    # Ép nó nằm trong giới hạn bàn cờ từ 0 đến N-1 để tránh lỗi click ra ngoài rìa
    j = max(0, min(N - 1, j))
    i = max(0, min(N - 1, i))
    
    return (i, j)

def pos_map2pixel(i, j):
    return (MARGIN + j * GRID - PIECE/2, MARGIN + i * GRID - PIECE/2)


def create_mapping():
    pos_mapping = {}
    for i in range(N):
        for j in range(N):
            spacing = [r for r in range(MARGIN, SIZE-MARGIN+1, int(GRID))]
            pos_mapping[(i,j)] = (spacing[j],spacing[i])
    
    return pos_mapping



def create_pattern_dict():
    x = -1
    patternDict = {}
    
    # Vòng lặp chạy 2 lần: x = -1 (Người chơi O), sau đó x = 1 (AI X)
    while (x < 2):
        y = -x # y là kẻ thù của x
        
        # --- BẬC 1: CHIẾN THẮNG TUYỆT ĐỐI (4 QUÂN) ---
        # Điểm cực cao để AI lập tức đánh luôn nếu có cơ hội, hoặc phải chặn ngay lập tức
        patternDict[(x, x, x, x)] = 1000000 * x
        
        # --- BẬC 2: NGUY HIỂM TỘT ĐỘ (MỞ 3 QUÂN) ---
        # Có 3 quân liên tiếp và 2 đầu đều trống. Đạt được thế này là 100% thắng.
        patternDict[(0, x, x, x, 0)] = 100000 * x
        # 3 quân bị lủng 1 lỗ nhưng 2 đầu vẫn mở (đánh vào giữa sẽ thành 4)
        patternDict[(0, x, 0, x, x, 0)] = 100000 * x
        patternDict[(0, x, x, 0, x, 0)] = 100000 * x
        
        # --- BẬC 3: ĐE DỌA TRỰC TIẾP (BỊ CHẶN 1 ĐẦU NHƯNG ĐÃ CÓ 3) ---
        # Bắt buộc đối thủ phải chặn đầu còn lại ngay lập tức
        patternDict[(y, x, x, x, 0)] = 10000 * x
        patternDict[(0, x, x, x, y)] = 10000 * x
        patternDict[(y, x, 0, x, x, 0)] = 10000 * x
        patternDict[(0, x, x, 0, x, y)] = 10000 * x
        patternDict[(y, x, x, 0, x, 0)] = 10000 * x
        patternDict[(0, x, 0, x, x, y)] = 10000 * x
        
        # --- BẬC 4: XÂY DỰNG NỀN TẢNG (MỞ 2 QUÂN) ---
        # Tiềm năng tạo thành thế Mở 3
        patternDict[(0, 0, x, x, 0)] = 1000 * x
        patternDict[(0, x, x, 0, 0)] = 1000 * x
        patternDict[(0, x, 0, x, 0)] = 1000 * x
        
        # --- BẬC 5: CÁC THẾ CỜ YẾU HƠN / ĐANG PHÁT TRIỂN ---
        # Bị chặn 1 đầu nhưng mới có 2 quân
        patternDict[(y, x, x, 0, 0)] = 100 * x
        patternDict[(0, 0, x, x, y)] = 100 * x
        patternDict[(y, 0, x, x, 0)] = 100 * x
        patternDict[(0, x, x, 0, y)] = 100 * x
        patternDict[(y, x, 0, x, 0)] = 100 * x
        patternDict[(0, x, 0, x, y)] = 100 * x

        # --- BẬC 6: THẾ CỜ CHẾT (BỊ CHẶN CẢ 2 ĐẦU) ---
        # Điểm âm nhẹ để AI hạn chế tốn nước đi vào những chỗ không thể kéo dài thêm
        patternDict[(y, x, x, x, y)] = -10 * x 
        patternDict[(y, x, x, y)] = -10 * x

        x += 2 # Tăng lên 1 để chấm điểm cho phe AI
        
    return patternDict



def init_zobrist():
    zTable = [[[uuid.uuid4().int  for _ in range(2)] \
                        for j in range(N)] for i in range(N)]
    return zTable

def update_TTable(table, hash, score, depth):
    table[hash] = [score, depth]
