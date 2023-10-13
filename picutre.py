import os
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from tqdm import tqdm

"""
文件功能描述：
将指定文件夹中的所有jpg图片以指定行数和列数拼接到A4大小的纸张上，然后以PDF文件的形式储存
input_folder：包含所有jpg图片的文件夹
output_pdf：输出PDF的路径
"""

# 指定输入图片文件夹和输出PDF文件
input_folder = r"C:\Users\10164\Desktop\phone"
output_pdf = r"C:\Users\10164\Desktop\phone\output.pdf"

# 获取文件夹中的所有jpg文件
jpg_files = [f for f in os.listdir(input_folder) if f.endswith(".jpg")]

# 计算每张纸上的图片数量和排列方式
rows = 5
cols = 4
images_per_page = rows * cols # 5行4列，共20张图片

# 计算每张图片在A4纸上的宽度和高度
page_width, page_height = A4  # 使用A4纸的尺寸
image_width = page_width / cols
image_height = page_height / rows

# 创建一个PDF文件并开始绘制
c = canvas.Canvas(output_pdf, pagesize=A4)  # 使用A4纸的尺寸

for i, jpg_file in enumerate(tqdm(jpg_files, desc="生成PDF进度")):
    if i % images_per_page == 0 and i > 0:
        c.showPage()  # 创建新的一页

    # 计算当前图片在本页的位置
    row_index = (i // cols) % rows
    col_index = i % cols

    x_offset = col_index * image_width
    y_offset = (rows - 1 - row_index) * image_height

    image = Image.open(os.path.join(input_folder, jpg_file))

    # 计算图片的缩放比例，以适应单元格并保持原始宽高比
    width_ratio = image_width / image.width
    height_ratio = image_height / image.height
    scale_ratio = min(width_ratio, height_ratio)

    scaled_width = image.width * scale_ratio
    scaled_height = image.height * scale_ratio

    x_centered = x_offset + (image_width - scaled_width) / 2
    y_centered = y_offset + (image_height - scaled_height) / 2

    c.drawImage(
        os.path.join(input_folder, jpg_file),
        x_centered,
        y_centered,
        width=scaled_width,
        height=scaled_height,
    )

# 确保最后一页也被保存
c.showPage()
c.save()
print(f"已生成PDF文件：{output_pdf}")
