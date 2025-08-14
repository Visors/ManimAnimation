from manim import *
import numpy as np

class TetrahedronPhysics(ThreeDScene):
    def construct(self):
        # 设置3D场景
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)
        
        # 标题
        title = Text("四面体软体物理模拟", font_size=36, color=BLUE)
        title.to_edge(UP, buff=0.3)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))
        self.wait(1)
        
        # 创建3D坐标轴
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1], 
            z_range=[-1, 4, 1],
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
        
        # 1. 四面体结构介绍
        intro_text = Text("四面体：软体物理模拟的基础", font_size=20, color=YELLOW)
        intro_text.to_corner(UL, buff=0.5)
        self.add_fixed_in_frame_mobjects(intro_text)
        self.play(Write(intro_text))
        
        # 创建一个单独的四面体（放大并放在坐标轴平面上）
        tetra_vertices = [
            np.array([0, 0, 3.5]),      # 顶点
            np.array([2.5, 0, 0]),      # 底面1（放在z=0平面上）
            np.array([-1.25, 2.2, 0]), # 底面2（放在z=0平面上）
            np.array([-1.25, -2.2, 0]) # 底面3（放在z=0平面上）
        ]
        
        # 显示四面体顶点
        tetra_dots = []
        tetra_labels = []
        
        for i, vertex in enumerate(tetra_vertices):
            dot = Dot3D(vertex, color=RED, radius=0.08)
            label = Text(f"V{i+1}", font_size=16, color=RED)
            label.rotate(PI/2, axis=RIGHT)
            if i == 0:
                label.next_to(vertex, UP, buff=0.2)
            else:
                label.next_to(vertex, DOWN, buff=0.2)
            tetra_dots.append(dot)
            tetra_labels.append(label)
        
        for dot, label in zip(tetra_dots, tetra_labels):
            self.play(Create(dot), Write(label), run_time=0.5)
        
        # 创建四面体的边（弹簧系统）
        tetra_edges = [
            (0, 1), (0, 2), (0, 3),  # 从顶点到底面
            (1, 2), (2, 3), (3, 1)   # 底面边
        ]
        
        spring_lines = []
        for edge in tetra_edges:
            start, end = edge
            line = Line3D(tetra_vertices[start], tetra_vertices[end], 
                         color=BLUE, stroke_width=4)
            spring_lines.append(line)
        
        # 显示弹簧连接
        spring_text = Text("弹簧连接系统", font_size=16, color=BLUE)
        spring_text.to_corner(UR, buff=0.5)
        self.add_fixed_in_frame_mobjects(spring_text)
        self.play(Write(spring_text))
        
        for line in spring_lines:
            self.play(Create(line), run_time=0.3)
        
        self.wait(1.5)
        
        # 2. 软体物理原理
        self.play(FadeOut(intro_text), FadeOut(spring_text))
        
        physics_text = Text("胡克定律：F = -k × Δx", font_size=20, color=GREEN)
        physics_text.to_corner(UL, buff=0.5)
        self.add_fixed_in_frame_mobjects(physics_text)
        self.play(Write(physics_text))
        
        # 显示力的计算公式
        force_formula = MathTex(r"F = -k(|d| - L_0) \frac{\vec{d}}{|d|}", font_size=18, color=GREEN)
        force_formula.to_corner(DR, buff=0.5)
        self.add_fixed_in_frame_mobjects(force_formula)
        self.play(Write(force_formula))
        
        explanation_text = Text("k:弹性系数 L₀:静息长度 d:当前距离", font_size=14, color=WHITE)
        explanation_text.to_corner(DR, buff=1.0)
        self.add_fixed_in_frame_mobjects(explanation_text)
        self.play(Write(explanation_text))
        
        self.wait(2)
        
        # 3. 变形演示1：顶点受力
        self.play(FadeOut(physics_text), FadeOut(force_formula), FadeOut(explanation_text))
        
        deform_text = Text("演示1：顶点受力变形", font_size=20, color=ORANGE)
        deform_text.to_corner(UL, buff=0.5)
        self.add_fixed_in_frame_mobjects(deform_text)
        self.play(Write(deform_text))
        
        # 在顶点添加力的箭头
        force_arrow = Arrow3D(tetra_vertices[0], tetra_vertices[0] + np.array([0, 1, -0.5]), 
                             color=RED, thickness=0.1)
        self.play(Create(force_arrow))
        
        force_label = Text("外力", font_size=14, color=RED)
        force_label.rotate(PI/2, axis=RIGHT)
        force_label.next_to(tetra_vertices[0] + np.array([0, 1.2, -0.3]), UP, buff=0.1)
        self.add(force_label)
        
        # 模拟顶点移动
        new_top_vertex = tetra_vertices[0] + np.array([0, 1.2, -0.5])
        
        # 更新四面体
        new_vertices = tetra_vertices.copy()
        new_vertices[0] = new_top_vertex
        
        # 重新创建变形后的四面体
        new_spring_lines = []
        for edge in tetra_edges:
            start, end = edge
            line = Line3D(new_vertices[start], new_vertices[end], 
                         color=BLUE, stroke_width=4)
            new_spring_lines.append(line)
        
        # 移动顶点和重绘弹簧
        self.play(
            tetra_dots[0].animate.move_to(new_top_vertex),
            tetra_labels[0].animate.next_to(new_top_vertex, UP, buff=0.2),
            *[Transform(old_line, new_line) for old_line, new_line in zip(spring_lines, new_spring_lines)],
            run_time=2
        )
        
        self.wait(1.5)
        
        # 弹性恢复
        recovery_text = Text("弹性恢复", font_size=16, color=GREEN)
        recovery_text.to_corner(UR, buff=0.5)
        self.add_fixed_in_frame_mobjects(recovery_text)
        self.play(Write(recovery_text))
        
        # 恢复原形 - 直接恢复到原始四面体状态
        original_spring_lines = []
        for edge in tetra_edges:
            start, end = edge
            line = Line3D(tetra_vertices[start], tetra_vertices[end], 
                         color=BLUE, stroke_width=4)
            original_spring_lines.append(line)
        
        self.play(
            tetra_dots[0].animate.move_to(tetra_vertices[0]),
            tetra_labels[0].animate.next_to(tetra_vertices[0], UP, buff=0.2),
            *[Transform(new_line, original_line) for new_line, original_line in zip(new_spring_lines, original_spring_lines)],
            FadeOut(force_arrow),
            FadeOut(force_label),
            run_time=2
        )
        
        self.wait(1)
        
        # 4. 演示2：多四面体软体
        self.play(FadeOut(deform_text), FadeOut(recovery_text))
        
        multi_text = Text("演示2：多四面体软体模拟", font_size=20, color=PURPLE)
        multi_text.to_corner(UL, buff=0.5)
        self.add_fixed_in_frame_mobjects(multi_text)
        self.play(Write(multi_text))
        
        # 移除单个四面体（包括变形后的边线）
        self.play(
            *[FadeOut(obj) for obj in tetra_dots + tetra_labels + original_spring_lines],
            run_time=1
        )
        
        # 创建2x2的四面体网格模拟软体（放大并放在平面上）
        grid_tetras = []
        grid_positions = [
            (-1.5, -1.5, 0), (1.5, -1.5, 0),  # 底层前排（z=0平面）
            (-1.5, 1.5, 0), (1.5, 1.5, 0),    # 底层后排（z=0平面）
            (-1.5, -1.5, 3), (1.5, -1.5, 3),  # 顶层前排
            (-1.5, 1.5, 3), (1.5, 1.5, 3)     # 顶层后排
        ]
        
        # 定义四面体连接（每个立方体分成5个四面体）
        tetra_connections = [
            # 底面四面体
            [0, 1, 2, 4],  # 左前底
            [1, 2, 3, 5],  # 右前底
            [2, 3, 6, 7],  # 右后底
            [0, 2, 4, 6],  # 左后底
            [2, 4, 5, 6],  # 中央连接
            # 顶面四面体  
            [4, 5, 6, 7]   # 顶面
        ]
        
        # 创建软体的顶点
        soft_dots = []
        for pos in grid_positions:
            dot = Dot3D(np.array(pos), color=YELLOW, radius=0.06)
            soft_dots.append(dot)
        
        # 创建软体的边
        soft_edges = []
        edge_set = set()
        edge_list = []  # 保持顺序的边列表
        
        for tetra in tetra_connections:
            # 为每个四面体创建所有边
            for i in range(4):
                for j in range(i+1, 4):
                    edge = tuple(sorted([tetra[i], tetra[j]]))
                    if edge not in edge_set:
                        edge_set.add(edge)
                        edge_list.append(edge)
        
        for edge in edge_list:
            start_pos = np.array(grid_positions[edge[0]])
            end_pos = np.array(grid_positions[edge[1]])
            line = Line3D(start_pos, end_pos, color=TEAL, stroke_width=2)
            soft_edges.append(line)
        
        # 显示软体结构
        for dot in soft_dots:
            self.add(dot)
        for edge in soft_edges:
            self.add(edge)
        
        self.wait(1)
        
        # 5. 重力作用演示
        gravity_text = Text("重力作用下的变形", font_size=18, color=RED)
        gravity_text.to_corner(UR, buff=0.5)
        self.add_fixed_in_frame_mobjects(gravity_text)
        self.play(Write(gravity_text))
        
        # 模拟重力作用：顶部顶点向下移动，底部固定
        gravity_deformation = []
        for i, pos in enumerate(grid_positions):
            if pos[2] > 1:  # 顶层顶点
                new_pos = np.array(pos) + np.array([0, 0, -1.2])
            else:  # 底层顶点（z=0）
                new_pos = np.array(pos)  # 底部固定在平面上
            gravity_deformation.append(new_pos)
        
        # 执行重力变形动画 - 使用过渡动画而不是突然消失
        animations = []
        for i, (dot, new_pos) in enumerate(zip(soft_dots, gravity_deformation)):
            animations.append(dot.animate.move_to(new_pos))
        
        # 同时更新边线 - 创建动态变形的边线动画
        edge_animations = []
        for i, edge in enumerate(edge_list):
            start_pos = gravity_deformation[edge[0]]
            end_pos = gravity_deformation[edge[1]]
            edge_animations.append(soft_edges[i].animate.put_start_and_end_on(start_pos, end_pos))
        
        # 执行统一的变形动画
        self.play(*animations, *edge_animations, run_time=3)
        self.wait(1.5)
        
        # 6. 碰撞演示
        self.play(FadeOut(gravity_text))
        
        collision_text = Text("碰撞压缩演示", font_size=18, color=RED)
        collision_text.to_corner(UR, buff=0.5)
        self.add_fixed_in_frame_mobjects(collision_text)
        self.play(Write(collision_text))
        
        # 从侧面施加压力
        compression_deformation = []
        for i, pos in enumerate(gravity_deformation):
            if pos[0] > 0.5:  # 右侧顶点向左压缩
                new_pos = pos + np.array([-0.6, 0, 0])
            elif pos[0] < -0.5:  # 左侧顶点向右压缩
                new_pos = pos + np.array([0.6, 0, 0])
            else:
                new_pos = pos  # 中间的点不动
            compression_deformation.append(new_pos)
        
        # 执行压缩动画 - 使用过渡动画
        animations = []
        for i, (dot, new_pos) in enumerate(zip(soft_dots, compression_deformation)):
            animations.append(dot.animate.move_to(new_pos))
        
        # 同时更新边线
        edge_animations = []
        for i, edge in enumerate(edge_list):
            start_pos = compression_deformation[edge[0]]
            end_pos = compression_deformation[edge[1]]
            edge_animations.append(soft_edges[i].animate.put_start_and_end_on(start_pos, end_pos))
        
        # 执行统一的压缩动画
        self.play(*animations, *edge_animations, run_time=2)
        self.wait(1)
        
        # 弹性恢复
        self.play(FadeOut(collision_text))
        
        elastic_text = Text("弹性恢复", font_size=18, color=GREEN)
        elastic_text.to_corner(UR, buff=0.5)
        self.add_fixed_in_frame_mobjects(elastic_text)
        self.play(Write(elastic_text))
        
        # 恢复到重力变形状态 - 使用过渡动画
        animations = []
        for i, (dot, original_pos) in enumerate(zip(soft_dots, gravity_deformation)):
            animations.append(dot.animate.move_to(original_pos))
        
        # 同时恢复边线
        edge_animations = []
        for i, edge in enumerate(edge_list):
            start_pos = gravity_deformation[edge[0]]
            end_pos = gravity_deformation[edge[1]]
            edge_animations.append(soft_edges[i].animate.put_start_and_end_on(start_pos, end_pos))
        
        # 执行统一的恢复动画
        self.play(*animations, *edge_animations, run_time=2)
        self.wait(1.5)
        
        # 7. 总结
        self.play(FadeOut(multi_text), FadeOut(elastic_text))
        
        conclusion = VGroup(
            Text("四面体软体物理总结", font_size=24, color=BLUE),
            Text("• 四面体用于软体物理有限元分析", font_size=18, color=WHITE),
            Text("• 每条边都是弹簧系统(胡克定律)", font_size=18, color=WHITE),
            Text("• 可模拟重力、碰撞、弹性变形", font_size=18, color=WHITE),
            Text("• 广泛用于游戏物理引擎", font_size=18, color=WHITE),
            Text("• 与3D建模完全不同的应用领域", font_size=18, color=WHITE)
        )
        conclusion.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        conclusion.to_corner(DL, buff=0.3)
        self.add_fixed_in_frame_mobjects(conclusion)
        self.play(Write(conclusion))
        self.wait(3)
        
        # 最终展示 - 摄像机环绕
        self.move_camera(phi=45 * DEGREES, theta=0 * DEGREES, run_time=2)
        self.move_camera(phi=75 * DEGREES, theta=PI, run_time=2)
        self.move_camera(phi=75 * DEGREES, theta=PI/2, run_time=2)
        
        # 清场
        all_display_objects = ([title, axes, axis_labels, conclusion] + 
                             soft_dots + soft_edges)
        self.play(*[FadeOut(obj) for obj in all_display_objects])
        self.wait(1)