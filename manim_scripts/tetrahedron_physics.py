# tetrahedron_physics.py
from manim import *
import numpy as np


class TetrahedronPhysics(ThreeDScene):
    """
    四面体软体物理模拟演示
    –––––––––––––––––––––––
    1. 单四面体：顶点受力→形变→恢复
    2. 多四面体立方体：重力→碰撞压缩→完整弹性恢复
    3. 总结 + 摄像机环绕
    修复：弹性恢复时回到初始未变形状态（而不是停留在重力形变状态）
    """

    # ----------------------------------------------------------
    # 场景主流程
    # ----------------------------------------------------------
    def construct(self):
        # 1. 场景初始化
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)

        title = Text("四面体软体物理模拟", font_size=36, color=BLUE)
        title.to_edge(DOWN, buff=0.3)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))
        self.wait(1)

        # 2. 坐标系
        axes = ThreeDAxes(
            x_range=[-4, 4, 1], y_range=[-4, 4, 1], z_range=[-2, 4, 1],
            x_length=8, y_length=8, z_length=6,
            axis_config={"color": GREY, "stroke_width": 2}
        )
        axis_labels = axes.get_axis_labels(
            Text("x", font_size=20),
            Text("y", font_size=20),
            Text("z", font_size=20)
        )
        self.play(Create(axes), Write(axis_labels))
        self.wait(0.5)

        # 3. 各演示阶段
        self.single_tetrahedron_demo()
        self.multi_tetrahedron_demo()

        # 4. 清场
        self.play(*[FadeOut(obj) for obj in [title, axes, axis_labels]])
        self.wait(1)

    # ----------------------------------------------------------
    # 1. 单四面体弹簧系统
    # ----------------------------------------------------------
    def single_tetrahedron_demo(self):
        intro_text = Text("四面体：软体物理模拟的基础", font_size=20, color=YELLOW)
        intro_text.to_corner(UL, buff=0.5)
        self.add_fixed_in_frame_mobjects(intro_text)
        self.play(Write(intro_text))

        # 顶点
        vertices = [
            np.array([0, 0, 3]),
            np.array([3, 0, 0]),
            np.array([-2, 2, 0]),
            np.array([-2, -2, 0]),
        ]
        dots, labels = [], []
        for i, v in enumerate(vertices):
            dot = Dot3D(v, color=RED, radius=0.08)
            label = Text(f"V{i+1}", font_size=16, color=RED).rotate(PI / 2, RIGHT)
            label.next_to(v, UP if i == 0 else DOWN, buff=0.2)
            dots.append(dot)
            labels.append(label)
            self.play(Create(dot), Write(label), run_time=0.5)

        # 弹簧边
        edges = [(0, 1), (0, 2), (0, 3), (1, 2), (2, 3), (3, 1)]
        springs = [Line3D(vertices[s], vertices[e], color=BLUE, stroke_width=4) for s, e in edges]
        spring_text = Text("弹簧连接系统", font_size=16, color=BLUE)
        spring_text.to_corner(UR, buff=0.5)
        self.add_fixed_in_frame_mobjects(spring_text)
        self.play(Write(spring_text))
        for ln in springs:
            self.play(Create(ln), run_time=0.3)
        self.wait(1.5)

        # 物理公式
        self.play(FadeOut(intro_text), FadeOut(spring_text))
        physics = Text("胡克定律：F = -k × Δx", font_size=20, color=GREEN)
        physics.to_corner(UL, buff=0.5)
        self.add_fixed_in_frame_mobjects(physics)
        self.play(Write(physics))
        formula = MathTex(r"F = -k(|d| - L_0) \frac{\vec{d}}{|d|}", font_size=18, color=GREEN)
        formula.to_corner(DR, buff=0.5)
        self.add_fixed_in_frame_mobjects(formula)
        self.play(Write(formula))
        self.wait(2)

        # 施加外力
        self.play(FadeOut(physics), FadeOut(formula))
        deform = Text("演示：顶点受力变形", font_size=20, color=ORANGE)
        deform.to_corner(UL, buff=0.5)
        self.add_fixed_in_frame_mobjects(deform)
        self.play(Write(deform))

        force_vec = np.array([0, 1.2, -0.5])
        force_arrow = Arrow3D(vertices[0], vertices[0] + force_vec, color=RED, thickness=0.1)
        self.play(Create(force_arrow))

        # 变形
        new_top = vertices[0] + force_vec
        new_verts = vertices.copy()
        new_verts[0] = new_top
        new_springs = [Line3D(new_verts[s], new_verts[e], color=BLUE, stroke_width=4) for s, e in edges]

        self.play(
            dots[0].animate.move_to(new_top),
            labels[0].animate.next_to(new_top, UP, buff=0.2),
            *[Transform(old, new) for old, new in zip(springs, new_springs)],
            run_time=2
        )
        self.wait(1)

        # 弹性恢复
        recover_text = Text("弹性恢复", font_size=16, color=GREEN)
        recover_text.to_corner(UR, buff=0.5)
        self.add_fixed_in_frame_mobjects(recover_text)
        self.play(Write(recover_text))

        orig_springs = [Line3D(vertices[s], vertices[e], color=BLUE, stroke_width=4) for s, e in edges]
        self.play(
            dots[0].animate.move_to(vertices[0]),
            labels[0].animate.next_to(vertices[0], UP, buff=0.2),
            FadeOut(force_arrow),
            *[Transform(spring, orig) for spring, orig in zip(springs, orig_springs)],
            run_time=2
        )
        self.wait(1)

        # 清场
        self.play(FadeOut(deform), FadeOut(recover_text))
        self.play(*[FadeOut(obj) for obj in (dots + labels + springs)])

    # ----------------------------------------------------------
    # 2. 多四面体软体
    # ----------------------------------------------------------
    def multi_tetrahedron_demo(self):
        multi = Text("演示：多四面体软体模拟", font_size=20, color=PURPLE)
        multi.to_corner(UL, buff=0.5)
        self.add_fixed_in_frame_mobjects(multi)
        self.play(Write(multi))

        # 8 个顶点（2×2×2 网格）
        positions = [
            (-1.5, -1.5, 0), (1.5, -1.5, 0),
            (-1.5, 1.5, 0), (1.5, 1.5, 0),
            (-1.5, -1.5, 3), (1.5, -1.5, 3),
            (-1.5, 1.5, 3), (1.5, 1.5, 3),
        ]
        
        # 逐个创建顶点和标签
        dots, labels = [], []
        for i, p in enumerate(positions):
            dot = Dot3D(np.array(p), color=YELLOW, radius=0.06)
            label = Text(f"P{i+1}", font_size=14, color=YELLOW).rotate(PI / 2, RIGHT)
            label.next_to(np.array(p), UP if p[2] > 1 else DOWN, buff=0.2)
            dots.append(dot)
            labels.append(label)
            self.play(Create(dot), Write(label), run_time=0.3)

        # 立方体所有边的连接关系（12条边 + 4条主对角线用于四面体分解）
        conns = [
            # 底面正方形 (z=0)
            (0, 1), (1, 3), (3, 2), (2, 0),
            # 顶面正方形 (z=3) 
            (4, 5), (5, 7), (7, 6), (6, 4),
            # 垂直边
            (0, 4), (1, 5), (2, 6), (3, 7),
            # 四面体分解的关键对角线
            (0, 3), (0, 7), (1, 6), (2, 5)
        ]
        
        # 弹簧连接系统
        spring_text = Text("多四面体弹簧网络", font_size=16, color=TEAL)
        spring_text.to_corner(UR, buff=0.5)
        self.add_fixed_in_frame_mobjects(spring_text)
        self.play(Write(spring_text))
        
        # 逐个创建边线
        edges = []
        for s, e in conns:
            line = Line3D(np.array(positions[s]), np.array(positions[e]), color=TEAL, stroke_width=2)
            edges.append(line)
            self.play(Create(line), run_time=0.2)
        
        self.play(FadeOut(spring_text))
        self.wait(1)

        # 重力变形
        g_text = Text("重力作用下的变形", font_size=18, color=RED)
        g_text.to_corner(UR, buff=0.5)
        self.add_fixed_in_frame_mobjects(g_text)
        self.play(Write(g_text))

        # 所有顶点都受重力影响，上层顶点下沉更多
        gravity_pos = [
            np.array(p) + np.array([0, 0, -0.8]) if p[2] > 1.5 else 
            np.array(p) + np.array([0, 0, -0.4])
            for p in positions
        ]

        anims = [dot.animate.move_to(np.array(gp)) for dot, gp in zip(dots, gravity_pos)]
        for ln, (s, e) in zip(edges, conns):
            anims.append(ln.animate.put_start_and_end_on(np.array(gravity_pos[s]), np.array(gravity_pos[e])))
        self.play(*anims, run_time=3)
        self.wait(1.5)

        # 碰撞压缩
        self.play(FadeOut(g_text))
        c_text = Text("碰撞压缩演示", font_size=18, color=RED)
        c_text.to_corner(UR, buff=0.5)
        self.add_fixed_in_frame_mobjects(c_text)
        self.play(Write(c_text))

        comp_pos = [
            gp + np.array([-0.6, 0, 0]) if gp[0] > 0.5 else
            gp + np.array([0.6, 0, 0]) if gp[0] < -0.5 else
            gp
            for gp in gravity_pos
        ]

        anims = [dot.animate.move_to(np.array(cp)) for dot, cp in zip(dots, comp_pos)]
        for ln, (s, e) in zip(edges, conns):
            anims.append(ln.animate.put_start_and_end_on(np.array(comp_pos[s]), np.array(comp_pos[e])))
        self.play(*anims, run_time=2)
        self.wait(1)

        # 弹性恢复（回到初始无外力状态）
        self.play(FadeOut(c_text))
        e_text = Text("弹性恢复到初始状态", font_size=18, color=GREEN)
        e_text.to_corner(UR, buff=0.5)
        self.add_fixed_in_frame_mobjects(e_text)
        self.play(Write(e_text))

        # 回到原始未变形状态
        anims = [dot.animate.move_to(np.array(p)) for dot, p in zip(dots, positions)]
        for ln, (s, e) in zip(edges, conns):
            anims.append(ln.animate.put_start_and_end_on(np.array(positions[s]), np.array(positions[e])))
        self.play(*anims, run_time=2.5)
        self.wait(1.5)

        # 清场
        self.play(FadeOut(multi), FadeOut(e_text))

        # ----------------------------------------------------------
        # 3. 总结
        # ----------------------------------------------------------

        conclusion = VGroup(
            Text("四面体软体物理总结", font_size=24, color=BLUE),
            Text("• 四面体用于软体物理有限元分析", font_size=18),
            Text("• 每条边都是弹簧系统(胡克定律)", font_size=18),
            Text("• 可模拟重力、碰撞、弹性变形", font_size=18),
            Text("• 广泛用于游戏物理引擎", font_size=18),
            Text("• 与3D建模完全不同的应用领域", font_size=18),
        )
        conclusion.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        conclusion.to_corner(DL, buff=0.3)
        self.add_fixed_in_frame_mobjects(conclusion)
        self.play(Write(conclusion))
        self.wait(3)

        # 摄像机环绕
        self.move_camera(phi=45 * DEGREES, theta=0, run_time=2)
        self.move_camera(phi=75 * DEGREES, theta=PI, run_time=2)
        self.move_camera(phi=75 * DEGREES, theta=PI / 2, run_time=2)

        self.play(FadeOut(conclusion))
        self.play(*[FadeOut(obj) for obj in (dots + labels + edges)])
        self.wait(1)



