from manim import *
import numpy as np

# Part 1: Introduction
class IntroductionScene(Scene):
    def construct(self):
        title = Text("Understanding Fourier Transform", font_size=48)
        subtitle = Text("From Time Domain to Frequency Domain", font_size=32)
        subtitle.next_to(title, DOWN)

        # Create fancy animation for title
        self.play(Write(title))
        self.play(FadeIn(subtitle))
        self.wait()

        # Introduction text
        intro_text = Text(
            "Fourier Transform decomposes complex signals\n"
            "into simple sine waves",
            font_size=24
        ).move_to(DOWN)
        
        self.play(
            title.animate.scale(0.7).to_edge(UP),
            FadeOut(subtitle),
            Write(intro_text)
        )
        self.wait(2)

# Part 2: Basic Sine Wave Explanation
class SineWaveScene(Scene):
    def construct(self):
        # Create axes
        axes = Axes(
            x_range=[-4, 4],
            y_range=[-2, 2],
            axis_config={"color": BLUE}
        )

        # Create sine wave
        sine_wave = axes.plot(lambda x: np.sin(x), color=YELLOW)
        
        # Labels
        labels = axes.get_axis_labels(x_label="Time", y_label="Amplitude")

        # Animation
        self.play(Create(axes), Create(labels))
        self.play(Create(sine_wave))
        
        # Add frequency and amplitude explanation
        explanation = VGroup(
            Text("Frequency: Rate of oscillation", font_size=24),
            Text("Amplitude: Height of the wave", font_size=24)
        ).arrange(DOWN).to_edge(RIGHT)
        
        self.play(Write(explanation))
        self.wait(2)

# Part 3: Complex Signal Composition
class ComplexSignalScene(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-4, 4],
            y_range=[-3, 3],
        )

        # Create multiple sine waves with different frequencies
        wave1 = axes.plot(lambda x: np.sin(x), color=RED)
        wave2 = axes.plot(lambda x: 0.5 * np.sin(2*x), color=BLUE)
        wave3 = axes.plot(lambda x: 0.25 * np.sin(4*x), color=GREEN)
        
        # Combined wave
        combined = axes.plot(
            lambda x: np.sin(x) + 0.5 * np.sin(2*x) + 0.25 * np.sin(4*x),
            color=YELLOW
        )

        # Animations
        self.play(Create(axes))
        self.play(Create(wave1))
        self.play(Create(wave2))
        self.play(Create(wave3))
        self.play(
            Transform(
                VGroup(wave1, wave2, wave3),
                combined
            )
        )
        self.wait(2)

# Continue with more parts...

# Continuing from previous code...

# Part 4: Fourier Transform Visualization
class FourierTransformScene(Scene):
    def construct(self):
        # Helper functions for signal processing
        def get_signal_points(t):
            """Generate a complex signal composed of three sine waves"""
            return (np.sin(2 * np.pi * 2 * t) +      # Base frequency: 2 Hz
                   0.5 * np.sin(2 * np.pi * 5 * t) + # Higher frequency: 5 Hz
                   0.3 * np.sin(2 * np.pi * 8 * t))  # Highest frequency: 8 Hz

        # Setup sampling parameters
        duration = 2  # 2 seconds
        sample_rate = 1000  # 1000 Hz
        t = np.linspace(0, duration, int(duration * sample_rate))
        signal = get_signal_points(t)

        # Create axes
        time_axes = Axes(
            x_range=[0, duration, 0.5],
            y_range=[-2, 2, 1],
            x_length=6,
            y_length=3,
            axis_config={"color": BLUE}
        ).to_edge(UP)

        # Add labels separately
        time_labels = time_axes.get_axis_labels(
            x_label="Time (s)",
            y_label="Amplitude"
        )

        freq_axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 1.2, 0.2],
            x_length=6,
            y_length=3,
            axis_config={"color": BLUE}
        ).to_edge(DOWN)

        freq_labels = freq_axes.get_axis_labels(
            x_label="Frequency (Hz)",
            y_label="Magnitude"
        )

        # Plot time domain signal
        time_plot = time_axes.plot_line_graph(
            x_values=t,
            y_values=signal,
            line_color=YELLOW
        )

        # Calculate and plot frequency spectrum
        n_samples = len(signal)
        fft_values = np.fft.fft(signal)
        freqs = np.fft.fftfreq(n_samples, 1/sample_rate)
        
        # Only use positive frequencies and normalize magnitudes
        pos_mask = freqs >= 0
        freqs = freqs[pos_mask]
        magnitudes = 2.0/n_samples * np.abs(fft_values[pos_mask])

        # Create frequency domain plot
        freq_plot = VGroup()
        for freq, mag in zip(freqs[freqs <= 10], magnitudes[freqs <= 10]):
            stem = Line(
                freq_axes.c2p(freq, 0),
                freq_axes.c2p(freq, mag),
                color=RED
            )
            dot = Dot(freq_axes.c2p(freq, mag), color=RED)
            freq_plot.add(stem, dot)

        # Labels
        time_label = Text("Time Domain Signal", font_size=24).next_to(time_axes, UP)
        freq_label = Text("Frequency Spectrum", font_size=24).next_to(freq_axes, UP)

        # Animations
        self.play(
            Create(time_axes),
            Create(freq_axes),
            Create(time_labels),
            Create(freq_labels),
            Write(time_label),
            Write(freq_label)
        )
        self.play(Create(time_plot))
        self.play(Create(freq_plot))
        
        # Add component frequencies labels
        component_labels = VGroup()
        for freq, amp in [(2, 1.0), (5, 0.5), (8, 0.3)]:
            label = Text(f"{freq}Hz", font_size=20).move_to(
                freq_axes.c2p(freq, amp + 0.1)
            )
            component_labels.add(label)
        
        self.play(Write(component_labels))
        self.wait(2)

# Part 5: Mathematical Foundation
class MathematicalFoundationScene(Scene):
    def construct(self):
        # Fourier Transform Equation
        fourier_eq = MathTex(
            "F(\\omega) = \\int_{-\\infty}^{\\infty} f(t)e^{-i\\omega t}dt"
        )
        
        # Euler's Formula
        euler_eq = MathTex(
            "e^{ix} = \\cos(x) + i\\sin(x)"
        )

        # Arrange equations
        equations = VGroup(fourier_eq, euler_eq).arrange(DOWN, buff=1)
        
        # Explanatory text
        explanation = Text(
            "The Fourier Transform converts a time-domain signal\n"
            "into its frequency components using complex exponentials",
            font_size=24
        ).next_to(equations, DOWN)

        # Animations
        self.play(Write(fourier_eq))
        self.play(Write(euler_eq))
        self.play(Write(explanation))
        self.wait(2)

# Signal Decomposition Visualization
class SignalDecompositionScene(Scene):
    def construct(self):
        # Create a more compact layout with 2x2 grid
        axes_group = VGroup()
        
        # Create 4 smaller axes in a grid layout
        for i in range(2):
            for j in range(2):
                ax = Axes(
                    x_range=[-2, 2],
                    y_range=[-1.5, 1.5],
                    x_length=4,
                    y_length=2,
                    axis_config={
                        "color": BLUE,
                        "stroke_width": 2,
                        "tip_length": 0.2
                    }
                ).scale(0.8)
                
                # Position axes in 2x2 grid
                ax.move_to(
                    RIGHT * (j * 5 - 2.5) +  # Horizontal spacing
                    UP * (i * (-3) + 1.5)    # Vertical spacing
                )
                axes_group.add(ax)

        # Define component signals
        signals = [
            (lambda x: np.sin(x), "First Harmonic"),
            (lambda x: 0.5 * np.sin(2*x), "Second Harmonic"),
            (lambda x: 0.3 * np.sin(3*x), "Third Harmonic"),
            (lambda x: np.sin(x) + 0.5*np.sin(2*x) + 0.3*np.sin(3*x), "Combined Signal")
        ]

        # Create waves and labels
        waves = VGroup()
        labels = VGroup()

        for i, (signal_func, label_text) in enumerate(signals):
            wave = axes_group[i].plot(signal_func, color=YELLOW)
            waves.add(wave)
            
            label = Text(
                label_text,
                font_size=24,
                color=WHITE
            ).next_to(axes_group[i], UP, buff=0.2)
            labels.add(label)

        # Title
        title = Text("Signal Decomposition", font_size=36).to_edge(UP)

        # Animations
        self.play(Write(title))
        self.play(Create(axes_group))
        
        # Animate each component separately
        for wave, label in zip(waves, labels):
            self.play(
                Create(wave),
                Write(label),
                run_time=1
            )
        
        # Add highlighting animation to show relationship
        highlight = SurroundingRectangle(waves[-1], color=RED)
        self.play(Create(highlight))
        self.play(FadeOut(highlight))
        
        self.wait(2)

# Part 6: Conclusion with Voice Analysis
class ConclusionScene(Scene):
    def construct(self):
        # Title
        title = Text("Voice Frequency Analysis", font_size=36).to_edge(UP)
        
        # Create frequency ranges visualization
        def create_range_viz(name, fund_range, harm_range):
            return VGroup(
                Text(name, font_size=24),
                Line(
                    start=LEFT*3,
                    end=RIGHT*3,
                    color=BLUE
                ),
                Text(f"Fundamental: {fund_range}", font_size=20),
                Text(f"Harmonics: {harm_range}", font_size=20)
            ).arrange(DOWN, buff=0.2)

        # Create visualizations for each singer
        singers = VGroup(
            create_range_viz("Fayrouz", "250-450 Hz", "up to 5000 Hz"),
            create_range_viz("Asmahan", "450 Hz", "Complex spectrum"),
            create_range_viz("Laila Morad", "200-300 Hz", "up to 3000 Hz"),
            create_range_viz("Shaban Abd Elraheem", "150-300 Hz", "Limited harmonics")
        ).arrange(DOWN, buff=0.5)

        # Animations
        self.play(Write(title))
        for singer in singers:
            self.play(FadeIn(singer))
        self.wait(2)
