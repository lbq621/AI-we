"""
创建竖屏短视频 - 铜陵天气新闻
"""
from moviepy import *
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os

# 视频参数
WIDTH, HEIGHT = 1080, 1920  # 竖屏
FPS = 30
BG_COLOR = (24, 24, 32)  # 深色背景
ACCENT_COLOR = (0, 150, 255)  # 蓝色强调色
TEXT_COLOR = (255, 255, 255)  # 白色文字

def create_text_clip(text, duration, font_size=60, color=TEXT_COLOR, position='center', bg_color=None):
    """创建文字片段"""
    # 创建文字图片
    img = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("msyh.ttc", font_size)
    except:
        font = ImageFont.load_default()

    # 计算文字位置
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    if isinstance(position, str):
        if position == 'center':
            x = (WIDTH - text_width) // 2
            y = (HEIGHT - text_height) // 2
        elif position == 'top':
            x = (WIDTH - text_width) // 2
            y = 100
        elif position == 'bottom':
            x = (WIDTH - text_width) // 2
            y = HEIGHT - text_height - 100
    else:
        # position 是元组 (x_pos, y_pos)
        x_pos, y_pos = position
        if x_pos == 'center':
            x = (WIDTH - text_width) // 2
        else:
            x = x_pos
        if y_pos == 'center':
            y = (HEIGHT - text_height) // 2
        else:
            y = y_pos

    # 绘制背景
    if bg_color:
        padding = 20
        draw.rectangle([x-padding, y-padding, x+text_width+padding, y+text_height+padding], fill=bg_color)

    # 绘制文字
    draw.text((x, y), text, font=font, fill=color)

    # 转换为numpy数组
    img_array = np.array(img)

    return ImageClip(img_array).with_duration(duration)

def create_image_clip(image_path, duration, resize=None):
    """创建图片片段"""
    img = Image.open(image_path)

    if resize:
        img = img.resize(resize, Image.Resampling.LANCZOS)

    # 创建黑色背景
    bg = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)

    # 将图片居中放置
    x = (WIDTH - img.width) // 2
    y = (HEIGHT - img.height) // 2

    if img.mode == 'RGBA':
        bg.paste(img, (x, y), img)
    else:
        bg.paste(img, (x, y))

    return ImageClip(np.array(bg)).with_duration(duration)

def create_animated_clip(image_path, duration, zoom_start=1.0, zoom_end=1.2):
    """创建带动画效果的图片片段"""
    img = Image.open(image_path)

    # 创建黑色背景
    bg = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)

    frames = []
    for i in range(int(FPS * duration)):
        progress = i / (FPS * duration)
        zoom = zoom_start + (zoom_end - zoom_start) * progress

        # 缩放图片
        new_size = (int(img.width * zoom), int(img.height * zoom))
        resized = img.resize(new_size, Image.Resampling.LANCZOS)

        # 居中裁剪
        x = (new_size[0] - WIDTH) // 2
        y = (new_size[1] - HEIGHT) // 2
        cropped = resized.crop((x, y, x + WIDTH, y + HEIGHT))

        frames.append(np.array(cropped))

    return ImageSequenceClip(frames, fps=FPS)

def main():
    print("开始创建视频...")

    # 场景列表
    scenes = []

    # 场景1: 标题
    print("创建场景1: 标题")
    title_clip = create_text_clip("今夜抵达铜陵！", 3, font_size=80, color=ACCENT_COLOR, position='center')
    subtitle_clip = create_text_clip("较强降水即将来袭", 3, font_size=50, position=('center', HEIGHT//2 + 100))
    scenes.append(CompositeVideoClip([title_clip, subtitle_clip]).with_duration(3))

    # 场景2: 天气动图
    print("创建场景2: 天气动图")
    if os.path.exists('D:/AI/we/image_1.gif'):
        try:
            weather_clip = create_animated_clip('D:/AI/we/image_1.gif', 4)
            text_overlay = create_text_clip("安徽进入梅雨期", 4, font_size=45, position=('center', 150), bg_color=(0, 0, 0, 180))
            scenes.append(CompositeVideoClip([weather_clip, text_overlay]).with_duration(4))
        except:
            # 如果GIF处理失败，使用静态图片
            weather_clip = create_image_clip('D:/AI/we/image_1.gif', 4)
            text_overlay = create_text_clip("安徽进入梅雨期", 4, font_size=45, position=('center', 150), bg_color=(0, 0, 0, 180))
            scenes.append(CompositeVideoClip([weather_clip, text_overlay]).with_duration(4))

    # 场景3: 降水预报
    print("创建场景3: 降水预报")
    rain_text = """未来十天多降水
北部晴雨相间
南部有持续强降水过程

大雨到暴雨，局部大暴雨
短时强降水40～60毫米/小时
局地雷暴大风8～10级"""
    rain_clip = create_text_clip(rain_text, 5, font_size=40, position='center')
    scenes.append(rain_clip)

    # 场景4: 预报图片
    print("创建场景4: 预报图片")
    if os.path.exists('D:/AI/we/image_2.jpg'):
        forecast_clip = create_animated_clip('D:/AI/we/image_2.jpg', 4)
        text_overlay = create_text_clip("6月18日-20日累计雨量", 4, font_size=45, position=('center', 100), bg_color=(0, 0, 0, 180))
        scenes.append(CompositeVideoClip([forecast_clip, text_overlay]).with_duration(4))

    # 场景5: 铜陵天气详情
    print("创建场景5: 铜陵天气详情")
    if os.path.exists('D:/AI/we/image_3.jpg'):
        detail_clip = create_animated_clip('D:/AI/we/image_3.jpg', 4)
        text_overlay = create_text_clip("铜陵具体天气预报", 4, font_size=45, position=('center', 100), bg_color=(0, 0, 0, 180))
        scenes.append(CompositeVideoClip([detail_clip, text_overlay]).with_duration(4))

    # 场景6: 具体天气
    print("创建场景6: 具体天气")
    weather_detail = """今天白天：多云转中等雷阵雨
26到30℃，偏东风3级

今天夜里：大雨，局地暴雨
24到27℃，西南风3级

19日：大雨，24到28℃
20日：雷阵雨，24到30℃
21日：大雨，局地暴雨"""
    detail_clip = create_text_clip(weather_detail, 5, font_size=40, position='center')
    scenes.append(detail_clip)

    # 场景7: 提醒建议
    print("创建场景7: 提醒建议")
    reminder = """温馨提示

1. 关注强降雨和强对流天气
   对出行和交通安全的影响

2. 关注城市暴雨积涝
   以及山洪、地质灾害风险

端午期间多降水，请注意安全！"""
    reminder_clip = create_text_clip(reminder, 5, font_size=40, position='center', color=(255, 200, 100))
    scenes.append(reminder_clip)

    # 场景8: 结尾
    print("创建场景8: 结尾")
    end_clip = create_text_clip("来源：铜陵气象 安徽气象", 3, font_size=35, position='center')
    scenes.append(end_clip)

    # 合并所有场景
    print("合并视频...")
    final_video = concatenate_videoclips(scenes)

    # 添加淡入淡出效果
    final_video = final_video.with_effects([
        vfx.FadeIn(0.5),
        vfx.FadeOut(0.5)
    ])

    # 导出视频
    output_path = 'D:/AI/we/铜陵天气新闻.mp4'
    print(f"导出视频到: {output_path}")
    final_video.write_videofile(
        output_path,
        fps=FPS,
        codec='libx264',
        audio=False,
        preset='medium',
        threads=4
    )

    print(f"视频创建完成: {output_path}")
    print(f"视频时长: {final_video.duration}秒")

if __name__ == "__main__":
    main()
