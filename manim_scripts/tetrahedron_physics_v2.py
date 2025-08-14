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
        
        # 阶段1：单四面体弹簧系统演示
        self.single_tetrahedron_demo()
        
        # 阶段2：多四面体软体演示
        self.multi_tetrahedron_demo()
        
        # 总结
        self.show_conclusion()
        
        # 清场
        self.play(*[FadeOut(obj) for obj in [title, axes, axis_labels]])
        self.wait(1)
    
    def single_tetrahedron_demo(self):
        """单四面体弹簧系统演示"""
        # 介绍文本
        intro_text = Text("四面体：软体物理模拟的基础", font_size=20, color=YELLOW)
        intro_text.to_corner(UL, buff=0.5)
        self.add_fixed_in_frame_mobjects(intro_text)
        self.play(Write(intro_text))
        
        # 创建四面体顶点（放大并放在坐标轴平面上）
        vertices = [
            np.array([0, 0, 3.5]),      # 顶点
            np.array([2.5, 0, 0]),      # 底面1（z=0平面）
            np.array([-1.25, 2.2, 0]), # 底面2（z=0平面）
            np.array([-1.25, -2.2, 0]) # 底面3（z=0平面）
        ]
        
        # 创建顶点
        dots = []
        labels = []
        for i, vertex in enumerate(vertices):
            dot = Dot3D(vertex, color=RED, radius=0.08)
            label = Text(f"V{i+1}", font_size=16, color=RED)
            label.rotate(PI/2, axis=RIGHT)
            if i == 0:
                label.next_to(vertex, UP, buff=0.2)
            else:
                label.next_to(vertex, DOWN, buff=0.2)
            dots.append(dot)
            labels.append(label)
        
        # 显示顶点
        for dot, label in zip(dots, labels):
            self.play(Create(dot), Write(label), run_time=0.5)
        
        # 创建弹簧连接
        edges = [(0, 1), (0, 2), (0, 3), (1, 2), (2, 3), (3, 1)]
        spring_lines = []
        for start, end in edges:
            line = Line3D(vertices[start], vertices[end], color=BLUE, stroke_width=4)
            spring_lines.append(line)
        
        # 显示弹簧系统
        spring_text = Text("弹簧连接系统", font_size=16, color=BLUE)
        spring_text.to_corner(UR, buff=0.5)
        self.add_fixed_in_frame_mobjects(spring_text)
        self.play(Write(spring_text))
        
        for line in spring_lines:
            self.play(Create(line), run_time=0.3)
        
        self.wait(1.5)
        
        # 物理原理
        self.play(FadeOut(intro_text), FadeOut(spring_text))
        
        physics_text = Text("胡克定律：F = -k × Δx", font_size=20, color=GREEN)
        physics_text.to_corner(UL, buff=0.5)
        self.add_fixed_in_frame_mobjects(physics_text)
        self.play(Write(physics_text))
        
        force_formula = MathTex(r"F = -k(|d| - L_0) \frac{\vec{d}}{|d|}", font_size=18, color=GREEN)
        force_formula.to_corner(DR, buff=0.5)
        self.add_fixed_in_frame_mobjects(force_formula)
        self.play(Write(force_formula))
        
        self.wait(2)
        
        # 变形演示
        self.play(FadeOut(physics_text), FadeOut(force_formula))
        
        deform_text = Text("演示：顶点受力变形", font_size=20, color=ORANGE)
        deform_text.to_corner(UL, buff=0.5)
        self.add_fixed_in_frame_mobjects(deform_text)
        self.play(Write(deform_text))
        
        # 添加力箭头
        force_arrow = Arrow3D(vertices[0], vertices[0] + np.array([0, 1.2, -0.5]), 
                             color=RED, thickness=0.1)
        self.play(Create(force_arrow))
        
        # 变形：顶点移动
        new_top = vertices[0] + np.array([0, 1.2, -0.5])
        new_vertices = vertices.copy()
        new_vertices[0] = new_top
        
        # 创建新的弹簧线
        new_springs = []
        for start, end in edges:
            line = Line3D(new_vertices[start], new_vertices[end], color=BLUE, stroke_width=4)
            new_springs.append(line)
        
        # 执行变形动画
        animations = [dots[0].animate.move_to(new_top)]
        animations.append(labels[0].animate.next_to(new_top, UP, buff=0.2))
        for old_line, new_line in zip(spring_lines, new_springs):
            animations.append(Transform(old_line, new_line))
        
        self.play(*animations, run_time=2)
        self.wait(1)
        
        # 弹性恢复
        recovery_text = Text("弹性恢复", font_size=16, color=GREEN)
        recovery_text.to_corner(UR, buff=0.5)
        self.add_fixed_in_frame_mobjects(recovery_text)
        self.play(Write(recovery_text))
        
        # 恢复原形
        original_springs = []
        for start, end in edges:
            line = Line3D(vertices[start], vertices[end], color=BLUE, stroke_width=4)
            original_springs.append(line)
        
        recovery_animations = [dots[0].animate.move_to(vertices[0])]
        recovery_animations.append(labels[0].animate.next_to(vertices[0], UP, buff=0.2))
        recovery_animations.append(FadeOut(force_arrow))
        for new_line, original_line in zip(new_springs, original_springs):
            recovery_animations.append(Transform(new_line, original_line))
        
        self.play(*recovery_animations, run_time=2)
        self.wait(1)
        
        # 完全清除单四面体演示的所有对象
        self.play(FadeOut(deform_text), FadeOut(recovery_text))
        single_tetra_objects = dots + labels + original_springs
        self.play(*[FadeOut(obj) for obj in single_tetra_objects], run_time=1)
        self.wait(0.5)
    
    def multi_tetrahedron_demo(self):
        """多四面体软体演示"""
        multi_text = Text("演示：多四面体软体模拟", font_size=20, color=PURPLE)
        multi_text.to_corner(UL, buff=0.5)
        self.add_fixed_in_frame_mobjects(multi_text)
        self.play(Write(multi_text))
        
        # 创建软体网格顶点（放大并放在平面上）
        positions = [
            (-1.5, -1.5, 0), (1.5, -1.5, 0),  # 底层前排
            (-1.5, 1.5, 0), (1.5, 1.5, 0),    # 底层后排
            (-1.5, -1.5, 3), (1.5, -1.5, 3),  # 顶层前排
            (-1.5, 1.5, 3), (1.5, 1.5, 3)     # 顶层后排
        ]
        
        # 创建顶点
        soft_dots = []
        for pos in positions:
            dot = Dot3D(np.array(pos), color=YELLOW, radius=0.06)
            soft_dots.append(dot)
        
        # 定义连接关系
        connections = [
            # 底面连接
            (0, 1), (0, 2), (1, 3), (2, 3),
            # 顶面连接
            (4, 5), (4, 6), (5, 7), (6, 7),
            # 垂直连接
            (0, 4), (1, 5), (2, 6), (3, 7),
            # 对角连接
            (0, 3), (1, 2), (4, 7), (5, 6),
            # 交叉连接
            (0, 5), (1, 4), (2, 7), (3, 6)
        ]
        
        # 创建边线
        soft_edges = []
        for start, end in connections:
            start_pos = np.array(positions[start])
            end_pos = np.array(positions[end])
            line = Line3D(start_pos, end_pos, color=TEAL, stroke_width=2)
            soft_edges.append(line)
        
        # 显示软体结构
        for dot in soft_dots:
            self.add(dot)
        for edge in soft_edges:
            self.add(edge)
        
        self.wait(1)
        
        # 重力变形
        gravity_text = Text("重力作用下的变形", font_size=18, color=RED)
        gravity_text.to_corner(UR, buff=0.5)
        self.add_fixed_in_frame_mobjects(gravity_text)
        self.play(Write(gravity_text))
        
        # 计算重力变形后的位置
        gravity_positions = []
        for i, pos in enumerate(positions):
            if pos[2] > 1:  # 顶层顶点下降
                new_pos = np.array(pos) + np.array([0, 0, -1.2])
            else:  # 底层固定
                new_pos = np.array(pos)
            gravity_positions.append(new_pos)
        
        # 执行重力变形
        gravity_animations = []
        for i, (dot, new_pos) in enumerate(zip(soft_dots, gravity_positions)):
            gravity_animations.append(dot.animate.move_to(new_pos))
        
        for i, (start, end) in enumerate(connections):
            start_pos = gravity_positions[start]
            end_pos = gravity_positions[end]
            gravity_animations.append(soft_edges[i].animate.put_start_and_end_on(start_pos, end_pos))
        
        self.play(*gravity_animations, run_time=3)
        self.wait(1.5)
        
        # 侧向压缩
        self.play(FadeOut(gravity_text))
        
        collision_text = Text("碰撞压缩演示", font_size=18, color=RED)
        collision_text.to_corner(UR, buff=0.5)
        self.add_fixed_in_frame_mobjects(collision_text)
        self.play(Write(collision_text))
        
        # 计算压缩变形
        compression_positions = []
        for pos in gravity_positions:
            if pos[0] > 0.5:  # 右侧压缩
                new_pos = pos + np.array([-0.6, 0, 0])
            elif pos[0] < -0.5:  # 左侧压缩
                new_pos = pos + np.array([0.6, 0, 0])
            else:
                new_pos = pos
            compression_positions.append(new_pos)
        
        # 执行压缩变形
        compression_animations = []
        for i, (dot, new_pos) in enumerate(zip(soft_dots, compression_positions)):
            compression_animations.append(dot.animate.move_to(new_pos))
        
        for i, (start, end) in enumerate(connections):
            start_pos = compression_positions[start]
            end_pos = compression_positions[end]
            compression_animations.append(soft_edges[i].animate.put_start_and_end_on(start_pos, end_pos))
        
        self.play(*compression_animations, run_time=2)
        self.wait(1)
        
        # 弹性恢复
        self.play(FadeOut(collision_text))
        
        elastic_text = Text("弹性恢复", font_size=18, color=GREEN)
        elastic_text.to_corner(UR, buff=0.5)
        self.add_fixed_in_frame_mobjects(elastic_text)
        self.play(Write(elastic_text))
        
        # 恢复到重力状态
        recovery_animations = []
        for i, (dot, original_pos) in enumerate(zip(soft_dots, gravity_positions)):
            recovery_animations.append(dot.animate.move_to(original_pos))
        
        for i, (start, end) in enumerate(connections):
            start_pos = gravity_positions[start]
            end_pos = gravity_positions[end]
            recovery_animations.append(soft_edges[i].animate.put_start_and_end_on(start_pos, end_pos))
        
        self.play(*recovery_animations, run_time=2)
        self.wait(1.5)
        
        # 清除多四面体演示
        self.play(FadeOut(multi_text), FadeOut(elastic_text))
        multi_objects = soft_dots + soft_edges
        self.play(*[FadeOut(obj) for obj in multi_objects], run_time=1)
    
    def show_conclusion(self):
        """显示总结"""
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
        
        self.play(FadeOut(conclusion))
        self.wait(1)