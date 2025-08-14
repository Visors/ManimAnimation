from manim import *
import numpy as np

class TriangleDecomposition(Scene):
    def construct(self):
        # 标题
        title = Text("2D三角形分解", font_size=36, color=BLUE)
        title.to_edge(UP, buff=0.3)
        
        self.play(Write(title))
        self.wait(1)
        
        # 创建坐标轴
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=8,
            y_length=6,
            axis_config={"color": GREY, "stroke_width": 2},
            tips=False
        )
        
        x_label = axes.get_x_axis_label("x", edge=RIGHT, direction=DOWN, buff=0.1)
        y_label = axes.get_y_axis_label("y", edge=UP, direction=LEFT, buff=0.1)
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.wait(0.5)
        
        # 1. 绘制平滑的人脸轮廓 - 通过关键点的样条曲线
        # 定义人脸关键点（整数坐标，便于后续采样）
        face_key_points = [
            [0, 2.5],      # 头顶
            [1, 2.3],      # 右上额头
            [1.8, 1.5],    # 右太阳穴
            [2.0, 0.5],    # 右脸颊上
            [1.8, -0.5],   # 右脸颊下
            [1.2, -1.2],   # 右下颌
            [0, -1.5],     # 下巴
            [-1.2, -1.2],  # 左下颌
            [-1.8, -0.5],  # 左脸颊下
            [-2.0, 0.5],   # 左脸颊上
            [-1.8, 1.5],   # 左太阳穴
            [-1, 2.3],     # 左上额头
        ]
        
        # 使用这些点创建平滑的人脸轮廓
        face_points_3d = [[p[0], p[1], 0] for p in face_key_points]
        
        # 创建平滑的样条曲线轮廓
        head_smooth = VMobject()
        head_smooth.set_points_smoothly([np.array(p) for p in face_points_3d])
        head_smooth.close_path()  # 闭合路径
        head_smooth.set_stroke(YELLOW, 4)
        
        head_label = Text("平滑原图形", font_size=18, color=WHITE)
        head_label.to_corner(UL, buff=0.5)
        
        self.play(Create(head_smooth))
        self.play(Write(head_label))
        self.wait(1.5)
        
        # 2. 粗糙拟合对比 - 从人脸关键点采样
        self.play(FadeOut(head_label))
        
        rough_text = Text("拟合1: 6个三角形", font_size=18, color=BLUE)
        rough_text.to_corner(UL, buff=0.5)
        self.play(Write(rough_text))
        
        center = [0, 0, 0]
        # 从人脸关键点中采样6个点（粗糙拟合）
        rough_indices = [0, 2, 4, 6, 8, 10]  # 每隔2个点采样
        rough_points = [face_key_points[i] for i in rough_indices]
        rough_points_3d = [[p[0], p[1], 0] for p in rough_points]
        
        triangles_rough = []
        colors = [RED, GREEN, ORANGE, PURPLE, PINK, TEAL]
        
        for i in range(len(rough_points_3d)):
            next_i = (i + 1) % len(rough_points_3d)
            triangle = Polygon(center, rough_points_3d[i], rough_points_3d[next_i],
                             color=colors[i], fill_opacity=0.5, stroke_width=2)
            triangles_rough.append(triangle)
        
        # 保留原图形，显示拟合对比
        for triangle in triangles_rough:
            self.play(Create(triangle), run_time=0.3)
        
        error_text = Text("误差较大", font_size=16, color=RED)
        error_text.to_corner(UR, buff=0.5)
        self.play(Write(error_text))
        self.wait(2)
        
        # 3. 精细拟合 - 使用所有人脸关键点
        self.play(FadeOut(rough_text), FadeOut(error_text), 
                  *[FadeOut(tri) for tri in triangles_rough])
        
        fine_text = Text("拟合2: 12个三角形", font_size=18, color=BLUE)
        fine_text.to_corner(UL, buff=0.5)
        self.play(Write(fine_text))
        
        # 使用所有人脸关键点（精细拟合）
        fine_points = face_key_points.copy()
        fine_points_3d = [[p[0], p[1], 0] for p in fine_points]
        
        triangles = []
        colors_extended = colors + [MAROON, GOLD, BLUE_A, YELLOW_A, LIGHT_PINK, LIGHT_BROWN]
        
        for i in range(len(fine_points_3d)):
            next_i = (i + 1) % len(fine_points_3d)
            triangle = Polygon(center, fine_points_3d[i], fine_points_3d[next_i],
                             color=colors_extended[i % len(colors_extended)], 
                             fill_opacity=0.6, stroke_width=2)
            triangles.append(triangle)
        
        for triangle in triangles:
            self.play(Create(triangle), run_time=0.2)
        
        better_text = Text("精度提升", font_size=16, color=GREEN)
        better_text.to_corner(UR, buff=0.5)
        self.play(Write(better_text))
        self.wait(1)
        
        summary = Text("精度 ∝ 三角形数量", font_size=20, color=YELLOW)
        summary.to_corner(DR, buff=0.5)
        self.play(Write(summary))
        self.wait(1.5)
        
        # 4. 隐藏原图形，开始变换演示
        self.play(FadeOut(head_smooth), FadeOut(fine_text), FadeOut(better_text), FadeOut(summary))
        self.wait(1)
        
        # 5. 显示关键顶点坐标
        coord_text = Text("关键顶点", font_size=20, color=GREEN)
        coord_text.to_corner(UL, buff=0.5)
        self.play(Write(coord_text))
        
        # 选择更有代表性的关键点：中心、右脸颊上、左下颌
        key_points = [center, fine_points_3d[3], fine_points_3d[7]]  # 中心、右脸颊上、左下颌
        key_coords = ["(0, 0)", "(2.0, 0.5)", "(-1.2, -1.2)"]
        
        dots = []
        labels = []
        
        for point, coord_label in zip(key_points, key_coords):
            dot = Dot(point, color=WHITE, radius=0.05)
            label = Text(coord_label, font_size=14, color=WHITE)
            
            if point[0] < -1:
                label.next_to(dot, LEFT, buff=0.1)
            elif point[0] > 1:
                label.next_to(dot, RIGHT, buff=0.1)
            else:
                label.next_to(dot, DOWN, buff=0.1)
            
            dots.append(dot)
            labels.append(label)
        
        for dot, label in zip(dots, labels):
            self.play(Create(dot), Write(label), run_time=0.4)
        
        self.wait(1.5)
        
        # 6. 多种线性变换演示
        self.play(FadeOut(coord_text))
        
        # 第一种变换：抬头效果（实际的旋转变换）
        transform_text1 = Text("变换1: 抬头（旋转）", font_size=20, color=ORANGE)
        transform_text1.to_corner(UL, buff=0.5)
        
        # 抬头是绕X轴的旋转，在2D中表现为头部向上倾斜
        matrix_text1 = MathTex(r"\begin{bmatrix} 1 & -0.2 \\ 0 & 1 \end{bmatrix}", font_size=24, color=BLUE)
        matrix_text1.to_corner(DR, buff=0.5)
        
        self.play(Write(transform_text1), Write(matrix_text1))
        
        # 创建抬头变形：实际的旋转+平移效果
        lift_points = []
        for p in fine_points:
            x, y = p[0], p[1]
            # 抬头变换：头部区域向后倾斜（负的剪切）+ 上部区域向上平移
            if y > 0:
                # 头部向后倾斜
                new_x = x - y * 0.2  # 剪切变换，头部向后倾
                new_y = y + 0.3      # 头部向上抬起
            else:
                # 下巴区域保持相对稳定
                new_x = x - y * 0.1  # 轻微剪切
                new_y = y
            lift_points.append([new_x, new_y, 0])
        
        lift_key_points = [center, lift_points[3], lift_points[7]]  # 对应右脸颊上、左下颌
        lift_coords = ["(0, 0)", f"({lift_points[3][0]:.1f}, {lift_points[3][1]:.1f})", f"({lift_points[7][0]:.1f}, {lift_points[7][1]:.1f})"]
        
        new_triangles1 = []
        for i in range(len(lift_points)):
            next_i = (i + 1) % len(lift_points)
            triangle = Polygon(center, lift_points[i], lift_points[next_i],
                             color=colors_extended[i % len(colors_extended)], 
                             fill_opacity=0.6, stroke_width=2)
            new_triangles1.append(triangle)
        
        new_dots1 = []
        new_labels1 = []
        for point, coord_label in zip(lift_key_points, lift_coords):
            dot = Dot(point, color=WHITE, radius=0.05)
            label = Text(coord_label, font_size=14, color=WHITE)
            
            if point[0] < -1:
                label.next_to(dot, LEFT, buff=0.1)
            elif point[0] > 1:
                label.next_to(dot, RIGHT, buff=0.1)
            else:
                label.next_to(dot, DOWN, buff=0.1)
            
            new_dots1.append(dot)
            new_labels1.append(label)
        
        # 执行抬头变形
        transforms1 = [Transform(old, new) for old, new in zip(triangles, new_triangles1)]
        dot_transforms1 = [Transform(old, new) for old, new in zip(dots, new_dots1)]
        label_transforms1 = [Transform(old, new) for old, new in zip(labels, new_labels1)]
        
        self.play(*transforms1, *dot_transforms1, *label_transforms1, run_time=2)
        self.wait(1.5)
        
        # 第二种变换：扭头（侧向旋转）
        self.play(FadeOut(transform_text1), FadeOut(matrix_text1))
        
        transform_text2 = Text("变换2: 扭头（侧转）", font_size=20, color=ORANGE)
        transform_text2.to_corner(UL, buff=0.5)
        
        matrix_text2 = MathTex(r"\begin{bmatrix} 1 & 0.3 \\ 0 & 1 \end{bmatrix}", font_size=24, color=BLUE)
        matrix_text2.to_corner(DR, buff=0.5)
        
        self.play(Write(transform_text2), Write(matrix_text2))
        
        # 创建扭头变形：头部向右转动
        twist_points = []
        for p in lift_points:
            x, y = p[0], p[1]
            # 扭头效果：头部区域向右偏移，模拟侧向转动
            if y > 0:
                # 头部区域向右扭转
                new_x = x + y * 0.3  # 上半部分向右移动
                new_y = y
            else:
                # 下巴区域保持稳定
                new_x = x
                new_y = y
            twist_points.append([new_x, new_y, p[2]])
        
        compress_points = twist_points
        compress_key_points = [center, compress_points[3], compress_points[7]]
        compress_coords = ["(0, 0)", f"({compress_points[3][0]:.1f}, {compress_points[3][1]:.1f})", f"({compress_points[7][0]:.1f}, {compress_points[7][1]:.1f})"]
        
        new_triangles2 = []
        for i in range(len(compress_points)):
            next_i = (i + 1) % len(compress_points)
            triangle = Polygon(center, compress_points[i], compress_points[next_i],
                             color=colors_extended[i % len(colors_extended)], 
                             fill_opacity=0.6, stroke_width=2)
            new_triangles2.append(triangle)
        
        new_dots2 = []
        new_labels2 = []
        for point, coord_label in zip(compress_key_points, compress_coords):
            dot = Dot(point, color=WHITE, radius=0.05)
            label = Text(coord_label, font_size=14, color=WHITE)
            
            if point[0] < -1:
                label.next_to(dot, LEFT, buff=0.1)
            elif point[0] > 1:
                label.next_to(dot, RIGHT, buff=0.1)
            else:
                label.next_to(dot, DOWN, buff=0.1)
            
            new_dots2.append(dot)
            new_labels2.append(label)
        
        transforms2 = [Transform(tri, new_tri) for tri, new_tri in zip(triangles, new_triangles2)]
        dot_transforms2 = [Transform(dot, new_dot) for dot, new_dot in zip(dots, new_dots2)]
        label_transforms2 = [Transform(label, new_label) for label, new_label in zip(labels, new_labels2)]
        
        self.play(*transforms2, *dot_transforms2, *label_transforms2, run_time=2)
        self.wait(1.5)
        
        # 第三种变换：转头（水平旋转）
        self.play(FadeOut(transform_text2), FadeOut(matrix_text2))
        
        transform_text3 = Text("变换3: 转头（水平旋转）", font_size=20, color=ORANGE)
        transform_text3.to_corner(UL, buff=0.5)
        
        matrix_text3 = MathTex(r"\begin{bmatrix} 0.8 & 0 \\ -0.2 & 1 \end{bmatrix}", font_size=24, color=BLUE)
        matrix_text3.to_corner(DR, buff=0.5)
        
        self.play(Write(transform_text3), Write(matrix_text3))
        
        # 创建转头变形：头部水平旋转效果
        turn_points = []
        for p in compress_points:
            x, y = p[0], p[1]
            # 转头效果：模拟头部向右水平转动，右侧收缩，左侧拉伸
            if x > 0:
                # 右侧脸颊收缩
                new_x = x * 0.8
                new_y = y - x * 0.2  # 右侧略微向下
            else:
                # 左侧脸颊拉伸
                new_x = x * 1.1
                new_y = y - x * 0.15  # 左侧略微向上（x为负，所以实际是向下）
            turn_points.append([new_x, new_y, p[2]])
        
        shear_points = turn_points
        
        shear_key_points = [center, shear_points[3], shear_points[7]]
        shear_coords = ["(0, 0)", f"({shear_points[3][0]:.1f}, {shear_points[3][1]:.1f})", f"({shear_points[7][0]:.1f}, {shear_points[7][1]:.1f})"]
        
        new_triangles3 = []
        for i in range(len(shear_points)):
            next_i = (i + 1) % len(shear_points)
            triangle = Polygon(center, shear_points[i], shear_points[next_i],
                             color=colors_extended[i % len(colors_extended)], 
                             fill_opacity=0.6, stroke_width=2)
            new_triangles3.append(triangle)
        
        new_dots3 = []
        new_labels3 = []
        for point, coord_label in zip(shear_key_points, shear_coords):
            dot = Dot(point, color=WHITE, radius=0.05)
            label = Text(coord_label, font_size=14, color=WHITE)
            
            if point[0] < -1:
                label.next_to(dot, LEFT, buff=0.1)
            elif point[0] > 1:
                label.next_to(dot, RIGHT, buff=0.1)
            else:
                label.next_to(dot, DOWN, buff=0.1)
            
            new_dots3.append(dot)
            new_labels3.append(label)
        
        transforms3 = [Transform(tri, new_tri) for tri, new_tri in zip(triangles, new_triangles3)]
        dot_transforms3 = [Transform(dot, new_dot) for dot, new_dot in zip(dots, new_dots3)]
        label_transforms3 = [Transform(label, new_label) for label, new_label in zip(labels, new_labels3)]
        
        self.play(*transforms3, *dot_transforms3, *label_transforms3, run_time=2)
        self.wait(2)
        
        # 清理变换标签
        self.play(FadeOut(transform_text3), FadeOut(matrix_text3))
        
        # 7. 总结
        conclusion = VGroup(
            Text("三角形分解与线性变换", font_size=24, color=BLUE),
            Text("• 平滑曲线的离散近似", font_size=18, color=WHITE),
            Text("• 精度随三角形数量提升", font_size=18, color=WHITE),
            Text("• 矩阵变换控制几何形变", font_size=18, color=WHITE),
            Text("• 计算机图形学的数学基础", font_size=18, color=WHITE)
        )
        conclusion.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        conclusion.to_corner(DR, buff=0.3)
        
        self.play(Write(conclusion))
        self.wait(3)
        
        # 清场
        all_objects = [title, axes, x_label, y_label, conclusion] + triangles + dots + labels
        self.play(*[FadeOut(obj) for obj in all_objects])
        self.wait(1)