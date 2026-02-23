import os
from PIL import Image, ImageDraw

def generate_turing_machine_grid(filepath, output_path):
    # --- 配置项 ---
    CELL_SIZE = 4    
    BORDER_SIZE = 1  
    CONTENT_SIZE = 3 
    ROWS = 100       
    COLS = 2500       
    MAX_TABLES = 1   
    GAP = 0          

    # 颜色配置（严格按照“黑0白1”设定）
    # 注：若发现输出的底色是全黑而点是白的（需要反相的话），可以把这两个颜色互相调换
    COLORS = {
        '0': (0, 0, 0),       # 黑0
        '1': (255, 255, 255)  # 白1
    }
    BOUNDARY_COLOR = (128, 128, 128) # 边界线默认给灰色，以免和纯黑/纯白混淆
    BG_COLOR = (20, 20, 20)          # 整个图片的底色
    
    # 确保保存路径所属文件夹存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # --- 1. 读取并预处理数据 ---
    data_lines = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            # 截取或填充至100个字符 (取原磁带中央的100个字符)
            target = ROWS
            n = len(line)
            if n >= target:
                start = (n - target) // 2
                processed_line = line[start : start + target]
            else:
                pad_l = (target - n) // 2
                pad_r = target - n - pad_l
                processed_line = '0' * pad_l + line + '0' * pad_r
                
            data_lines.append(processed_line)
            
            # 至多需要 MAX_TABLES * COLS 等于 2000 行
            if len(data_lines) >= MAX_TABLES * COLS:
                break

    if not data_lines:
        print("未从文件中读取到数据！")
        return

    # --- 2. 逻辑分块（分割成至多5个表格） ---
    tables_data = []
    for i in range(0, len(data_lines), COLS):
        tables_data.append(data_lines[i : i + COLS])
        if len(tables_data) == MAX_TABLES:
            break

    # --- 3. 绘制单独的表格 ---
    table_images = []
    for table_idx, chunk in enumerate(tables_data):
        # 计算当前表格的长宽
        # 转置逻辑：行(chunk的元素) -> 网格的列(X轴) ； 列(字符串长度) -> 网格的行(Y轴)
        width_px = len(chunk) * CELL_SIZE + BORDER_SIZE
        height_px = ROWS * CELL_SIZE + BORDER_SIZE
        
        # 新建立表格图片对象，底色直接铺满边界色
        img_table = Image.new('RGB', (width_px, height_px), BOUNDARY_COLOR)
        draw = ImageDraw.Draw(img_table)
        
        # 遍历数据填充 3x3 内部小方块
        for t, line_data in enumerate(chunk):        # t: 时间步（向右）
            for s, char in enumerate(line_data):     # s: 磁带空间（向下）
                # 网格矩阵中坐标 (起点为边框，向右/下偏移像素即可)
                # x0, y0 包含自己，x1, y1 也包含自己，所以 3x3 画出来的就是右下的3个像素块
                x0 = t * CELL_SIZE + BORDER_SIZE
                y0 = s * CELL_SIZE + BORDER_SIZE
                x1 = x0 + CONTENT_SIZE - 1
                y1 = y0 + CONTENT_SIZE - 1
                
                fill_color = COLORS.get(char, COLORS['0']) # 遇到异常字符默认当0处理
                draw.rectangle([x0, y0, x1, y1], fill=fill_color)
                
        table_images.append(img_table)

    # --- 4. 拼接所有表格 ---
    # 计算大画布的总宽度和总高度 (给四周加上 20px 的留白)
    margin = 20
    total_width = sum(img.width for img in table_images) + GAP * (len(table_images) - 1)
    max_height = max(img.height for img in table_images)
    
    final_img = Image.new('RGB', (total_width + margin * 2, max_height + margin * 2), BG_COLOR)
    
    # 将表格按顺序排版写入
    current_x = margin
    for img in table_images:
        final_img.paste(img, (current_x, margin))
        current_x += img.width + GAP

    # --- 5. 保存并输出 ---
    final_img.save(output_path)
    print(f"图像生成成功！成功合成 {len(table_images)} 个表格，已保存至: {output_path}")

# --- 运行入口 ---
if __name__ == "__main__":
    # 你可以修改为你本地的实际输入/输出路径
    input_file = "resources/bbs_track/BB5.txt"
    output_file = "resources/bbs_track/BB5_grid.png"
    
    generate_turing_machine_grid(input_file, output_file)