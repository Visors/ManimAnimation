from manim import *
import numpy as np

class TriangleMesh3D(ThreeDScene):
    def construct(self):
        # 设置3D场景
        self.set_camera_orientation(phi=60 * DEGREES, theta=-30 * DEGREES)
        
        # 标题
        title = Text("3D三角形网格建模", font_size=36, color=BLUE)
        title.to_edge(UP, buff=0.3)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))
        self.wait(1)
        
        # 创建3D坐标轴
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1], 
            z_range=[-2, 3, 1],
            x_length=6,
            y_length=6,
            z_length=5,
            axis_config={"color": GREY, "stroke_width": 2}
        )
        
        axis_labels = axes.get_axis_labels(
            Text("x", font_size=20),
            Text("y", font_size=20), 
            Text("z", font_size=20)
        )
        
        self.play(Create(axes), Write(axis_labels))
        self.wait(0.5)
        
        # 1. 展示单个三角形在3D空间中的概念
        intro_text = Text("3D图形学基础：三角形网格", font_size=20, color=YELLOW)
        intro_text.to_corner(UL, buff=0.5)
        self.add_fixed_in_frame_mobjects(intro_text)
        self.play(Write(intro_text))
        
        # 创建一个简单的三角形
        triangle_vertices = [
            np.array([1, 0, 1]),
            np.array([-0.5, 1.5, 1]),
            np.array([-0.5, -1.5, 1])
        ]
        
        # 显示三角形顶点
        triangle_dots = []
        triangle_labels = []
        
        for i, vertex in enumerate(triangle_vertices):
            dot = Dot3D(vertex, color=RED, radius=0.08)
            label = Text(f"P{i+1}", font_size=16, color=RED)
            label.rotate(PI/2, axis=RIGHT)
            label.next_to(vertex, UP, buff=0.2)
            triangle_dots.append(dot)
            triangle_labels.append(label)
        
        for dot, label in zip(triangle_dots, triangle_labels):
            self.play(Create(dot), Write(label), run_time=0.5)
        
        # 创建三角形面
        triangle = Polygon(*triangle_vertices, 
                          color=BLUE, 
                          fill_opacity=0.6, 
                          stroke_width=3)
        
        self.play(Create(triangle))
        self.wait(1)
        
        concept_text = Text("三角形是3D图形的基本单元", font_size=16, color=BLUE)
        concept_text.to_corner(DR, buff=0.5)
        self.add_fixed_in_frame_mobjects(concept_text)
        self.play(Write(concept_text))
        self.wait(1.5)
        
        # 2. 构建球体的三角形网格
        self.play(FadeOut(intro_text), FadeOut(concept_text))
        
        mesh_text = Text("构建球体：从粗糙到精细", font_size=20, color=ORANGE)
        mesh_text.to_corner(UL, buff=0.5)
        self.add_fixed_in_frame_mobjects(mesh_text)
        self.play(Write(mesh_text))
        
        # 移除单个三角形演示
        self.play(
            *[FadeOut(obj) for obj in triangle_dots + triangle_labels + [triangle]],
            run_time=1
        )
        
        # 阶段1：4个三角形构成四面体（最粗糙）
        stage1_text = Text("阶段1：4个三角形（四面体）", font_size=18, color=GREEN)
        stage1_text.to_corner(UR, buff=0.5)
        self.add_fixed_in_frame_mobjects(stage1_text)
        self.play(Write(stage1_text))
        
        # 四面体顶点
        tetra_vertices = [
            np.array([0, 0, 1.5]),      # 顶点
            np.array([1.2, 0, -0.5]),   # 底面1
            np.array([-0.6, 1.0, -0.5]), # 底面2
            np.array([-0.6, -1.0, -0.5]) # 底面3
        ]
        
        # 四面体的4个三角形面
        tetra_faces = [
            [0, 1, 2],  # 前面
            [0, 2, 3],  # 左面
            [0, 3, 1],  # 右面
            [1, 2, 3]   # 底面
        ]
        
        tetra_triangles = []
        colors = [YELLOW, PINK, TEAL, PURPLE]
        
        for i, face_indices in enumerate(tetra_faces):
            vertices = [tetra_vertices[j] for j in face_indices]
            triangle = Polygon(*vertices, 
                              color=colors[i], 
                              fill_opacity=0.5, 
                              stroke_width=2)
            tetra_triangles.append(triangle)
        
        # 逐个显示四面体的4个面
        count_text = Text("三角形数量：4", font_size=16, color=WHITE)
        count_text.to_corner(DL, buff=0.5)
        self.add_fixed_in_frame_mobjects(count_text)
        self.play(Write(count_text))
        
        for triangle in tetra_triangles:
            self.play(Create(triangle), run_time=0.6)
        
        self.wait(2)
        
        # 阶段2：8个三角形（八面体，更细致）
        self.play(FadeOut(stage1_text))
        stage2_text = Text("阶段2：8个三角形（八面体）", font_size=18, color=GREEN)
        stage2_text.to_corner(UR, buff=0.5)
        self.add_fixed_in_frame_mobjects(stage2_text)
        self.play(Write(stage2_text))
        
        # 移除四面体
        self.play(*[FadeOut(triangle) for triangle in tetra_triangles], run_time=1)
        
        # 八面体顶点（6个顶点）
        octa_vertices = [
            np.array([0, 0, 1.5]),    # 上顶点
            np.array([0, 0, -1.5]),   # 下顶点
            np.array([1.2, 0, 0]),    # 前顶点
            np.array([-1.2, 0, 0]),   # 后顶点
            np.array([0, 1.2, 0]),    # 右顶点
            np.array([0, -1.2, 0])    # 左顶点
        ]
        
        # 八面体的8个三角形面
        octa_faces = [
            [0, 2, 4], [0, 4, 3], [0, 3, 5], [0, 5, 2],  # 上半部分
            [1, 4, 2], [1, 3, 4], [1, 5, 3], [1, 2, 5]   # 下半部分
        ]
        
        octa_triangles = []
        octa_colors = [YELLOW, PINK, TEAL, PURPLE, ORANGE, GREEN, BLUE, RED]
        
        for i, face_indices in enumerate(octa_faces):
            vertices = [octa_vertices[j] for j in face_indices]
            triangle = Polygon(*vertices, 
                              color=octa_colors[i], 
                              fill_opacity=0.4, 
                              stroke_width=2)
            octa_triangles.append(triangle)
        
        # 更新计数
        new_count_text = Text("三角形数量：8", font_size=16, color=WHITE)
        new_count_text.to_corner(DL, buff=0.5)
        self.play(Transform(count_text, new_count_text))
        
        # 逐个显示八面体的8个面
        for triangle in octa_triangles:
            self.play(Create(triangle), run_time=0.4)
        
        self.wait(2)
        
        # 阶段3：细分球体（更多三角形）
        self.play(FadeOut(stage2_text))
        stage3_text = Text("阶段3：细分球体（更精细）", font_size=18, color=GREEN)
        stage3_text.to_corner(UR, buff=0.5)
        self.add_fixed_in_frame_mobjects(stage3_text)
        self.play(Write(stage3_text))
        
        # 移除八面体
        self.play(*[FadeOut(triangle) for triangle in octa_triangles], run_time=1)
        
        # 创建更精细的球体网格（使用正确的球面三角化）
        def sphere_point(u, v, radius=1.2):
            return radius * np.array([
                np.sin(v) * np.cos(u),
                np.sin(v) * np.sin(u),
                np.cos(v)
            ])
        
        # 生成球体网格顶点
        u_segments = 6  # 经度方向6段  
        v_segments = 4  # 纬度方向4段
        
        sphere_vertices = []
        # 添加北极点
        sphere_vertices.append(sphere_point(0, 0, 1.2))
        
        # 添加中间纬度圈的顶点
        for i in range(1, v_segments):
            v = i * np.pi / v_segments
            for j in range(u_segments):
                u = j * 2 * np.pi / u_segments
                vertex = sphere_point(u, v)
                sphere_vertices.append(vertex)
        
        # 添加南极点
        sphere_vertices.append(sphere_point(0, np.pi, 1.2))
        
        # 生成三角形面
        sphere_triangles = []
        triangle_count = 0
        
        # 北极帽三角形
        for j in range(u_segments):
            next_j = (j + 1) % u_segments
            triangle = Polygon(
                sphere_vertices[0],  # 北极点
                sphere_vertices[1 + j],  # 当前经度线上的点
                sphere_vertices[1 + next_j],  # 下一个经度线上的点
                color=BLUE, fill_opacity=0.4, stroke_width=1
            )
            sphere_triangles.append(triangle)
            triangle_count += 1
        
        # 中间带的四边形（分成两个三角形）
        for i in range(1, v_segments - 1):
            for j in range(u_segments):
                next_j = (j + 1) % u_segments
                
                # 当前四边形的四个顶点索引
                top_left = 1 + (i - 1) * u_segments + j
                top_right = 1 + (i - 1) * u_segments + next_j
                bottom_left = 1 + i * u_segments + j
                bottom_right = 1 + i * u_segments + next_j
                
                # 第一个三角形 (左上 -> 右上 -> 左下)
                triangle1 = Polygon(
                    sphere_vertices[top_left],
                    sphere_vertices[top_right], 
                    sphere_vertices[bottom_left],
                    color=TEAL if (i + j) % 2 == 0 else BLUE, 
                    fill_opacity=0.4, stroke_width=1
                )
                sphere_triangles.append(triangle1)
                triangle_count += 1
                
                # 第二个三角形 (右上 -> 右下 -> 左下)
                triangle2 = Polygon(
                    sphere_vertices[top_right],
                    sphere_vertices[bottom_right],
                    sphere_vertices[bottom_left], 
                    color=TEAL if (i + j) % 2 == 0 else BLUE,
                    fill_opacity=0.4, stroke_width=1
                )
                sphere_triangles.append(triangle2)
                triangle_count += 1
        
        # 南极帽三角形
        south_pole_idx = len(sphere_vertices) - 1
        for j in range(u_segments):
            next_j = (j + 1) % u_segments
            triangle = Polygon(
                sphere_vertices[south_pole_idx],  # 南极点
                sphere_vertices[1 + (v_segments - 2) * u_segments + next_j],  # 下一个经度线上的点
                sphere_vertices[1 + (v_segments - 2) * u_segments + j],  # 当前经度线上的点
                color=BLUE, fill_opacity=0.4, stroke_width=1
            )
            sphere_triangles.append(triangle)
            triangle_count += 1
        
        # 更新计数
        final_count_text = Text(f"三角形数量：{triangle_count}", font_size=16, color=WHITE)
        final_count_text.to_corner(DL, buff=0.5)
        self.play(Transform(count_text, final_count_text))
        
        # 快速显示所有三角形
        for triangle in sphere_triangles:
            self.add(triangle)
        
        self.wait(2)
        
        # 3. 实时变形演示
        self.play(FadeOut(stage3_text), FadeOut(mesh_text))
        
        transform_text = Text("3D变形：顶点坐标变换", font_size=20, color=PURPLE)
        transform_text.to_corner(UL, buff=0.5)
        self.add_fixed_in_frame_mobjects(transform_text)
        self.play(Write(transform_text))
        
        # 显示变换矩阵（用英文避免LaTeX中文问题）
        matrix_text = MathTex(r"Transform: \begin{bmatrix} a & b & c \\ d & e & f \\ g & h & i \end{bmatrix}", 
                             font_size=16, color=BLUE)
        matrix_text.to_corner(DR, buff=0.5)
        self.add_fixed_in_frame_mobjects(matrix_text)
        self.play(Write(matrix_text))
        
        all_mesh_objects = VGroup(*sphere_triangles)
        
        # 变形1：拉伸
        stretch_text = Text("拉伸变形", font_size=16, color=ORANGE)
        stretch_text.to_corner(UR, buff=0.5)
        self.add_fixed_in_frame_mobjects(stretch_text)
        self.play(Write(stretch_text))
        
        self.play(
            all_mesh_objects.animate.apply_function(
                lambda p: [p[0], p[1], p[2] * 1.5]  # Z方向拉伸
            ),
            run_time=2
        )
        self.wait(1)
        
        # 变形2：压缩
        self.play(FadeOut(stretch_text))
        compress_text = Text("压缩变形", font_size=16, color=ORANGE)
        compress_text.to_corner(UR, buff=0.5)
        self.add_fixed_in_frame_mobjects(compress_text)
        self.play(Write(compress_text))
        
        self.play(
            all_mesh_objects.animate.apply_function(
                lambda p: [p[0] * 0.8, p[1] * 0.8, p[2] * 0.7]  # 整体压缩
            ),
            run_time=2
        )
        self.wait(1)
        
        # 变形3：旋转
        self.play(FadeOut(compress_text))
        rotate_text = Text("旋转变形", font_size=16, color=ORANGE)
        rotate_text.to_corner(UR, buff=0.5)
        self.add_fixed_in_frame_mobjects(rotate_text)
        self.play(Write(rotate_text))
        
        angle = PI/4
        self.play(
            all_mesh_objects.animate.apply_function(
                lambda p: [
                    p[0] * np.cos(angle) - p[1] * np.sin(angle),
                    p[0] * np.sin(angle) + p[1] * np.cos(angle),
                    p[2]
                ]
            ),
            run_time=2
        )
        self.wait(2)
        
        # 4. 总结
        self.play(FadeOut(transform_text), FadeOut(matrix_text), FadeOut(rotate_text))
        
        conclusion = VGroup(
            Text("3D三角形网格建模总结", font_size=24, color=BLUE),
            Text("• 三角形是3D图形学的基础单元", font_size=18, color=WHITE),
            Text("• 从粗糙到精细：4 → 8 → 数十个三角形", font_size=18, color=WHITE),
            Text("• 顶点坐标变换实现3D变形", font_size=18, color=WHITE),
            Text("• 真实游戏和电影都使用此方法", font_size=18, color=WHITE),
            Text("• 这是计算机图形学的核心技术", font_size=18, color=WHITE)
        )
        conclusion.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        conclusion.to_corner(DL, buff=0.3)
        self.add_fixed_in_frame_mobjects(conclusion)
        self.play(Write(conclusion))
        self.wait(3)
        
        # 最终展示 - 摄像机环绕
        self.move_camera(phi=30 * DEGREES, theta=0 * DEGREES, run_time=2)
        self.move_camera(phi=60 * DEGREES, theta=PI, run_time=2)
        self.move_camera(phi=60 * DEGREES, theta=PI/2, run_time=2)
        
        # 清场
        all_display_objects = ([title, axes, axis_labels, count_text, conclusion] + 
                             sphere_triangles)
        self.play(*[FadeOut(obj) for obj in all_display_objects])
        self.wait(1)