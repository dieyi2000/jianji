from scenedetect import VideoManager, SceneManager
from scenedetect.detectors import ContentDetector
from moviepy.editor import VideoFileClip
import os

# 设置视频文件路径
video_path = "input_video.mp4"
output_dir = "output_scenes"  # 输出文件夹

# 创建输出文件夹（如果不存在）
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 创建视频管理器和场景管理器
video_manager = VideoManager([video_path])
scene_manager = SceneManager()

# 使用内容检测器检测场景变化
scene_manager.add_detector(ContentDetector())

# 开始处理视频
video_manager.set_downscale_factor()
video_manager.start()

# 检测场景
scene_manager.detect_scenes(video_manager)

# 获取检测到的场景列表
scene_list = scene_manager.get_scene_list()

# 加载原始视频
video = VideoFileClip(video_path)

# 根据场景列表裁剪并保存视频片段
for i, scene in enumerate(scene_list):
    start_time = scene[0].get_seconds()  # 起始时间（秒）
    end_time = scene[1].get_seconds()  # 结束时间（秒）

    # 裁剪视频片段
    clip = video.subclip(start_time, end_time)

    # 设置输出文件名
    output_path = os.path.join(output_dir, f"scene_{i + 1}.mp4")

    # 保存裁剪后的视频片段
    clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

    print(f"Saved Scene {i + 1}: {start_time} sec - {end_time} sec as {output_path}")

# 释放资源
video_manager.release()
video.close()