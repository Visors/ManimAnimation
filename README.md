# 数学公开课动画演示项目

## 项目简介
为高中数学公开课创建的计算机图形学教学演示，展示三角形和四面体在2D/3D动画中的基础作用。

## 快速开始

### 1. 环境安装
```bash
pip install -r requirements.txt
```

### 2. 生成教学视频
```bash
# 2D三角形分解演示
manim -pql manim_scripts/triangle_scenes.py TriangleDecomposition

# 3D四面体构建演示  
manim -pql manim_scripts/tetrahedron_scenes.py TetrahedronConstruction

# 物理模拟演示
manim -pql manim_scripts/physics_scenes.py PhysicsSimulation
```

### 3. 运行交互演示
```bash
python -m http.server 8000
# 然后访问 http://localhost:8000/interactive/
```

## 文件结构
- `videos/` - 生成的教学视频
- `interactive/` - 交互式网页演示
- `manim_scripts/` - 视频源代码
- `assets/` - 共用资源

## 课堂使用
1. 播放`videos/`中的MP4文件进行主要讲解
2. 打开`interactive/`中的HTML文件进行互动演示