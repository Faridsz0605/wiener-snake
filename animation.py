"""
Wiener Snake AI — LinkedIn Explainer Animation
Manim Community Edition | 1920x1080 @ 60fps

Render:
    manim -pqh --fps 60 animation.py SnakeAIExplainer
"""

from manim import *
import numpy as np


# ── Color palette (matches the game's retro aesthetic) ───────────────
BG = "#0F0F1A"
GRID_LINE = "#1E1E30"
SNAKE_GREEN = "#50DC64"
SNAKE_BODY_GREEN = "#228B22"
FOOD_RED = "#FF3C3C"
GOLD = "#F0C850"
MUTED_TEXT = "#8C8CAA"
ACCENT_CYAN = "#32DCFF"
ACCENT_PURPLE = "#8250FF"
NODE_FILL = "#1A1A2E"
SUBTLE_BORDER = "#3C3C5A"

# ── Fonts ────────────────────────────────────────────────────────────
FONT_SANS = "Liberation Sans"
FONT_SERIF = "Test Tiempos Text"
FONT_MONO = "JetBrainsMono Nerd Font"


class SnakeAIExplainer(MovingCameraScene):
    def construct(self):
        self.camera.background_color = BG
        self.scene_01_title()
        self.scene_02_the_game()
        self.scene_03_state()
        self.scene_04_network()
        self.scene_05_training()
        self.scene_06_closing()

    # ── Zoom helpers ─────────────────────────────────────────────────
    def _zoom_in(self, target, scale=0.75, run_time=1.2):
        """Smooth zoom into a target mobject."""
        self.play(
            self.camera.frame.animate.set(width=self.camera.frame.get_width() * scale)
            .move_to(target),
            run_time=run_time,
            rate_func=smooth,
        )

    def _zoom_reset(self, run_time=1.0):
        """Smooth zoom back to default framing."""
        self.play(
            self.camera.frame.animate.set(width=14.222).move_to(ORIGIN),
            run_time=run_time,
            rate_func=smooth,
        )

    # ── Scene 1: Title Card (~8s) ────────────────────────────────────
    def scene_01_title(self):
        title = Text(
            "I Built an AI That Learned\nto Play Snake",
            font=FONT_SANS,
            font_size=46,
            color=WHITE,
            line_spacing=1.4,
        ).move_to(UP * 0.3)

        subtitle = Text(
            "Deep Q-Learning  ·  From Scratch",
            font=FONT_SANS,
            font_size=22,
            color=MUTED_TEXT,
        ).next_to(title, DOWN, buff=0.5)

        line = Line(
            LEFT * 2, RIGHT * 2, color=ACCENT_CYAN, stroke_width=1.5
        ).next_to(subtitle, DOWN, buff=0.4)

        # Start slightly zoomed out, settle in
        self.camera.frame.set(width=16).move_to(ORIGIN)
        self.play(
            FadeIn(title, shift=UP * 0.3),
            self.camera.frame.animate.set(width=14.222).move_to(ORIGIN),
            run_time=1.4,
            rate_func=smooth,
        )
        self.wait(0.5)
        self.play(
            FadeIn(subtitle, shift=UP * 0.2),
            Create(line),
            run_time=1.0,
        )
        self.wait(3.5)
        self.play(FadeOut(Group(title, subtitle, line)), run_time=0.8)
        self.wait(0.4)

    # ── Scene 2: The Game (~8s) ──────────────────────────────────────
    def scene_02_the_game(self):
        heading = Text(
            "The Game", font=FONT_SERIF, font_size=34, color=GOLD
        ).to_edge(UP, buff=0.6)

        grid = self._build_grid(rows=8, cols=12, cell=0.45).move_to(ORIGIN)

        snake_cells = [(4, 6), (4, 5), (4, 4), (4, 3)]
        snake_rects = VGroup()
        for i, (r, c) in enumerate(snake_cells):
            color = SNAKE_GREEN if i == 0 else SNAKE_BODY_GREEN
            opacity = 1.0 if i == 0 else max(0.4, 1.0 - i * 0.2)
            rect = Square(
                0.40, fill_color=color, fill_opacity=opacity, stroke_width=0
            ).move_to(grid[r * 12 + c].get_center())
            snake_rects.add(rect)

        food = Square(
            0.40, fill_color=FOOD_RED, fill_opacity=1, stroke_width=0
        ).move_to(grid[2 * 12 + 9].get_center())

        desc = Text(
            "The classical snake game - but no human is playing.",
            font=FONT_SERIF,
            font_size=20,
            color=MUTED_TEXT,
        ).next_to(grid, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(Create(grid), run_time=1.0)
        self.play(FadeIn(snake_rects), FadeIn(food), run_time=0.8)
        self.play(FadeIn(desc, shift=UP * 0.15), run_time=0.6)
        # Gentle zoom into the snake on the grid
        self._zoom_in(snake_rects, scale=0.8, run_time=1.5)
        self.wait(1.5)
        self._zoom_reset(run_time=0.8)
        self.play(
            FadeOut(Group(heading, grid, snake_rects, food, desc)), run_time=0.6
        )
        self.wait(0.3)

    # ── Scene 3: How the AI Sees the Game (~10s) ─────────────────────
    def scene_03_state(self):
        heading = Text(
            "What the AI Sees", font=FONT_SANS, font_size=34, color=GOLD
        ).to_edge(UP, buff=0.6)

        state_labels = [
            "Danger ahead",
            "Danger right",
            "Danger left",
            "Moving left",
            "Moving right",
            "Moving up",
            "Moving down",
            "Food is left",
            "Food is right",
            "Food is up",
            "Food is down",
        ]

        col1 = VGroup()
        col2 = VGroup()
        for i, label in enumerate(state_labels):
            val = "1" if i in [1, 4, 8, 10] else "0"
            color = ACCENT_CYAN if val == "1" else MUTED_TEXT
            row = VGroup(
                Text(f"[{val}]", font=FONT_MONO, font_size=18, color=color),
                Text(label, font=FONT_SANS, font_size=16, color=color),
            ).arrange(RIGHT, buff=0.3)
            if i < 6:
                col1.add(row)
            else:
                col2.add(row)

        col1.arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        col2.arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        columns = VGroup(col1, col2).arrange(RIGHT, buff=1.2).move_to(DOWN * 0.2)

        caption = Text(
            "11 binary signals — the entire world, compressed.",
            font=FONT_SANS,
            font_size=20,
            color=MUTED_TEXT,
        ).next_to(columns, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(
            LaggedStart(
                *[FadeIn(row, shift=RIGHT * 0.2) for row in [*col1, *col2]],
                lag_ratio=0.08,
            ),
            run_time=1.8,
        )
        self.play(FadeIn(caption, shift=UP * 0.15), run_time=0.6)
        # Slow zoom into the active signals
        active_rows = VGroup(col1[1], col1[4], col2[2], col2[4])
        self._zoom_in(columns, scale=0.85, run_time=1.5)
        self.wait(2.5)
        self._zoom_reset(run_time=0.8)
        self.play(FadeOut(Group(heading, columns, caption)), run_time=0.6)
        self.wait(0.3)

    # ── Scene 4: Neural Network Architecture (~12s) ──────────────────
    def scene_04_network(self):
        heading = Text(
            "The Brain", font=FONT_SANS, font_size=34, color=GOLD
        ).to_edge(UP, buff=0.6)

        # Layers — reduced hidden to 6 nodes to fix overlap
        input_nodes = self._node_column(6, x=-4.0, color=ACCENT_CYAN, label="11")
        hidden_nodes = self._node_column(6, x=0, color=ACCENT_PURPLE, label="256")
        output_nodes = self._node_column(3, x=4.0, color=SNAKE_GREEN, label="3")

        lbl_in = Text(
            "State", font=FONT_SANS, font_size=16, color=MUTED_TEXT
        ).next_to(input_nodes, DOWN, buff=0.4)
        lbl_hid = Text(
            "Hidden (ReLU)", font=FONT_SANS, font_size=16, color=MUTED_TEXT
        ).next_to(hidden_nodes, DOWN, buff=0.4)
        lbl_out = Text(
            "Actions", font=FONT_SANS, font_size=16, color=MUTED_TEXT
        ).next_to(output_nodes, DOWN, buff=0.4)

        # Connections
        connections = VGroup()
        for i_node in input_nodes:
            if not isinstance(i_node, Circle):
                continue
            for h_node in hidden_nodes:
                if not isinstance(h_node, Circle):
                    continue
                connections.add(
                    Line(
                        i_node.get_right(),
                        h_node.get_left(),
                        stroke_width=0.4,
                        stroke_opacity=0.15,
                        color=WHITE,
                    )
                )
        for h_node in hidden_nodes:
            if not isinstance(h_node, Circle):
                continue
            for o_node in output_nodes:
                if not isinstance(o_node, Circle):
                    continue
                connections.add(
                    Line(
                        h_node.get_right(),
                        o_node.get_left(),
                        stroke_width=0.5,
                        stroke_opacity=0.2,
                        color=WHITE,
                    )
                )

        action_labels = ["Straight", "Turn Right", "Turn Left"]
        a_labels = VGroup()
        output_circles = [m for m in output_nodes if isinstance(m, Circle)]
        for circle, lbl in zip(output_circles, action_labels):
            t = Text(
                lbl, font=FONT_SANS, font_size=14, color=SNAKE_GREEN
            ).next_to(circle, RIGHT, buff=0.3)
            a_labels.add(t)

        # Reward annotation
        reward_text = VGroup(
            Text(
                "+10  eat food", font=FONT_MONO, font_size=16, color=SNAKE_GREEN
            ),
            Text(
                "-10  collision", font=FONT_MONO, font_size=16, color=FOOD_RED
            ),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).to_edge(DOWN, buff=0.7)

        reward_heading = Text(
            "Rewards", font=FONT_SANS, font_size=18, color=GOLD
        ).next_to(reward_text, UP, buff=0.25)

        # Network group for zoom targeting
        network = Group(
            connections, input_nodes, hidden_nodes, output_nodes,
            lbl_in, lbl_hid, lbl_out, a_labels,
        )

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(connections), run_time=0.6)
        self.play(FadeIn(input_nodes), FadeIn(lbl_in), run_time=0.6)
        self.play(FadeIn(hidden_nodes), FadeIn(lbl_hid), run_time=0.6)
        self.play(
            FadeIn(output_nodes), FadeIn(lbl_out), FadeIn(a_labels),
            run_time=0.6,
        )
        # Zoom into the network architecture
        self._zoom_in(network, scale=0.85, run_time=1.2)
        self.wait(1.0)
        self._zoom_reset(run_time=0.8)
        self.play(FadeIn(reward_heading), FadeIn(reward_text), run_time=0.8)
        self.wait(3.5)
        self.play(
            FadeOut(
                Group(
                    heading, connections, input_nodes, hidden_nodes,
                    output_nodes, lbl_in, lbl_hid, lbl_out, a_labels,
                    reward_heading, reward_text,
                )
            ),
            run_time=0.6,
        )
        self.wait(0.3)

    # ── Scene 5: Training Progression (~14s) ─────────────────────────
    def scene_05_training(self):
        heading = Text(
            "Training", font=FONT_SANS, font_size=34, color=GOLD
        ).to_edge(UP, buff=0.6)

        axes = Axes(
            x_range=[0, 500, 100],
            y_range=[0, 60, 10],
            x_length=9,
            y_length=4,
            axis_config={
                "color": MUTED_TEXT,
                "stroke_width": 1.5,
                "include_ticks": True,
                "tick_size": 0.05,
            },
            tips=False,
        ).move_to(DOWN * 0.2)

        x_label = Text(
            "Games Played", font=FONT_SANS, font_size=16, color=MUTED_TEXT
        ).next_to(axes.x_axis, DOWN, buff=0.3)
        y_label = Text(
            "Score", font=FONT_SANS, font_size=16, color=MUTED_TEXT
        ).next_to(axes.y_axis, LEFT, buff=0.3)

        np.random.seed(42)
        n = 500
        x_vals = np.arange(n)
        base = 2 + 45 * (1 - np.exp(-x_vals / 150))
        noise = np.random.normal(0, 4, n)
        raw_scores = np.clip(base + noise, 0, 60)

        window = 30
        mean_scores = np.convolve(
            raw_scores, np.ones(window) / window, mode="valid"
        )
        mean_x = x_vals[window - 1:]

        score_dots = VGroup()
        for i in range(0, n, 5):
            dot = Dot(
                axes.c2p(x_vals[i], raw_scores[i]),
                radius=0.02,
                color=ACCENT_CYAN,
                fill_opacity=0.3,
            )
            score_dots.add(dot)

        mean_points = [
            axes.c2p(mean_x[i], mean_scores[i]) for i in range(len(mean_x))
        ]
        mean_line = VMobject(color=GOLD, stroke_width=2.5)
        mean_line.set_points_smoothly(mean_points[::3])

        phase_explore = Text(
            "Exploring", font=FONT_SANS, font_size=16, color=ACCENT_CYAN
        ).move_to(axes.c2p(80, 55))
        phase_learn = Text(
            "Learning", font=FONT_SANS, font_size=16, color=ACCENT_PURPLE
        ).move_to(axes.c2p(250, 55))
        phase_exploit = Text(
            "Exploiting", font=FONT_SANS, font_size=16, color=SNAKE_GREEN
        ).move_to(axes.c2p(420, 55))

        eps_note = Text(
            "Exploration rate decays over 500 games",
            font=FONT_SANS,
            font_size=14,
            color=MUTED_TEXT,
        ).to_edge(DOWN, buff=0.5)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(
            Create(axes), FadeIn(x_label), FadeIn(y_label), run_time=1.0
        )

        chunk = len(score_dots) // 3
        self.play(
            LaggedStart(
                *[FadeIn(d) for d in score_dots[:chunk]], lag_ratio=0.02
            ),
            FadeIn(phase_explore),
            run_time=1.2,
        )
        self.play(
            LaggedStart(
                *[FadeIn(d) for d in score_dots[chunk: 2 * chunk]],
                lag_ratio=0.02,
            ),
            FadeIn(phase_learn),
            run_time=1.2,
        )
        self.play(
            LaggedStart(
                *[FadeIn(d) for d in score_dots[2 * chunk:]], lag_ratio=0.02
            ),
            FadeIn(phase_exploit),
            run_time=1.2,
        )

        self.play(Create(mean_line), run_time=2.0)
        self.play(FadeIn(eps_note), run_time=0.5)
        # Zoom into the late-stage performance
        late_zone = VGroup(phase_exploit)
        self._zoom_in(axes, scale=0.9, run_time=1.2)
        self.wait(2.0)
        self._zoom_reset(run_time=0.8)
        self.play(
            FadeOut(
                Group(
                    heading, axes, x_label, y_label, score_dots, mean_line,
                    phase_explore, phase_learn, phase_exploit, eps_note,
                )
            ),
            run_time=0.6,
        )
        self.wait(0.3)

    # ── Scene 6: Closing (~10s) ──────────────────────────────────────
    def scene_06_closing(self):
        line1 = Text(
            "From random moves to intelligent navigation.",
            font=FONT_SANS,
            font_size=28,
            color=WHITE,
        ).move_to(UP * 1.0)

        line2 = Text(
            "No rules programmed — only rewards.",
            font=FONT_SANS,
            font_size=22,
            color=MUTED_TEXT,
        ).next_to(line1, DOWN, buff=0.4)

        divider = Line(
            LEFT * 1.5, RIGHT * 1.5, color=SUBTLE_BORDER, stroke_width=1
        ).next_to(line2, DOWN, buff=0.5)

        tech = Text(
            "Python  ·  PyTorch  ·  Pygame",
            font=FONT_SANS,
            font_size=18,
            color=ACCENT_CYAN,
        ).next_to(divider, DOWN, buff=0.4)

        built = Text(
            "Built from scratch.",
            font=FONT_SANS,
            font_size=20,
            color=GOLD,
        ).next_to(tech, DOWN, buff=0.35)

        # Start slightly zoomed out for cinematic feel
        self.camera.frame.set(width=15.5)
        self.play(
            FadeIn(line1, shift=UP * 0.2),
            self.camera.frame.animate.set(width=14.222).move_to(ORIGIN),
            run_time=1.2,
            rate_func=smooth,
        )
        self.wait(0.5)
        self.play(FadeIn(line2, shift=UP * 0.15), run_time=0.8)
        self.wait(0.3)
        self.play(Create(divider), run_time=0.5)
        self.play(FadeIn(tech), run_time=0.6)
        self.play(FadeIn(built), run_time=0.6)
        self.wait(5.5)
        self.play(
            FadeOut(Group(line1, line2, divider, tech, built)), run_time=1.0
        )

    # ── Helpers ──────────────────────────────────────────────────────
    def _build_grid(self, rows, cols, cell):
        grid = VGroup()
        for r in range(rows):
            for c in range(cols):
                sq = Square(
                    side_length=cell,
                    stroke_color=GRID_LINE,
                    stroke_width=0.8,
                    fill_opacity=0,
                ).move_to(
                    np.array([
                        (c - cols / 2 + 0.5) * cell,
                        (rows / 2 - r - 0.5) * cell,
                        0,
                    ])
                )
                grid.add(sq)
        return grid

    def _node_column(self, n, x, color, label):
        group = VGroup()
        spacing = 0.5
        total_h = (n - 1) * spacing

        for i in range(n):
            y = total_h / 2 - i * spacing
            circle = Circle(
                radius=0.18,
                stroke_color=color,
                stroke_width=1.5,
                fill_color=NODE_FILL,
                fill_opacity=0.9,
            ).move_to(np.array([x, y, 0]))
            group.add(circle)

        # Count label above with enough clearance
        count = Text(
            label, font=FONT_MONO, font_size=18, color=color
        ).next_to(group, UP, buff=0.35)
        group.add(count)
        return group
