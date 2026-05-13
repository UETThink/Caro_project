# Caro Project

Game Cờ Caro với AI thông minh sử dụng thuật toán Minimax và Alpha-Beta Pruning.

## Giới thiệu

Đây là ứng dụng chơi game Cờ Caro với đối thủ là AI. Game được xây dựng bằng Python với giao diện đồ họa Neon đẹp mắt sử dụng Tkinter.

### Tính năng

- Giao diện Neon hiện đại, bắt mắt
- AI đối thủ với thuật toán Minimax kết hợp Alpha-Beta Pruning
- Hỗ trợ chọn độ sâu AI (1-5)
- Hiển thị lượt chơi và thông tin người chơi
- Hiệu ứng hover và click đẹp mắt
- Tự động phát hiện thắng/thua/hòa

## Cấu trúc dự án

```
caro project/
├── source/
│   ├── ai_agent.py      # Agent AI với Minimax/Alpha-Beta Pruning
│   ├── caro_game.py     # Logic game Caro
│   ├── evaluation.py    # Hàm đánh giá bàn cờ
│   └── utils.py         # Tiện ích (patterns, hash)
├── gui/
│   ├── button.py        # Class Button cho Tkinter
│   ├── caro_gui_neon.py # Giao diện Neon (Tkinter)
│   └── interface.py     # Giao diện Pygame
├── assets/              # Hình ảnh và tài nguyên
├── play_caro.py         # File chạy game Caro
└── requirements.txt     # Thư viện cần thiết
```

## Cài đặt và chạy

### 1. Cài đặt thư viện

```bash
pip install -r requirements.txt
```

### 2. Chạy game

```bash
python play_caro.py
```

## Cách chơi

1. Chọn độ khó AI (1-5) từ menu chính
2. Người chơi đi trước với quân X (màu xanh dương)
3. AI đi sau với quân O (màu hồng)
4. Click vào ô trống trên bàn cờ để đánh
5. Win khi có 4 quân liên tiếp theo hàng ngang, dọc hoặc chéo

## Yêu cầu hệ thống

- Python 3.8 trở lên
- tkinter (có sẵn với Python)
- pygame (tùy chọn)

## Thuật toán AI

### Minimax với Alpha-Beta Pruning

AI sử dụng thuật toán Minimax để tìm nước đi tối ưu, kết hợp với Alpha-Beta Pruning để tối ưu hóa tốc độ tìm kiếm.

### Đánh giá bàn cờ

Hàm đánh giá dựa trên các pattern có thể tạo thành chuỗi 5:
- 5 quân liên tiếp: chiến thắng tuyệt đối
- 4 quân liên tiếp (hở 2 đầu): rất nguy hiểm
- 4 quân liên tiếp (hở 1 đầu): nguy hiểm
- 3 quân liên tiếp: có tiềm năng
- 2 quân liên tiếp: cơ hội phát triển

## Tùy chỉnh

Có thể điều chỉnh độ sâu tìm kiếm AI để thay đổi độ khó:
- Độ sâu 1: Dễ
- Độ sâu 2: Trung bình
- Độ sâu 3: Khó 
- Độ sâu 4: Cực khó

## Tác giả

Project học tập về AI và Game
