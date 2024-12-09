from manim import *
import numpy as np
 

class FFT(Scene):
    def construct(self):
        # Helper functions for signal processing
        def get_signal_points(t):
            """Generate a complex signal composed of three sine waves"""
            return (np.sin(2 * np.pi * 2 * t) +      # Base frequency: 2 Hz
                   0.5 * np.sin(2 * np.pi * 5 * t) + # Higher frequency: 5 Hz, half amplitude
                   0.3 * np.sin(2 * np.pi * 8 * t))  # Highest frequency: 8 Hz, 0.3 amplitude

        def get_component_points(t, freq, amplitude=1):
            """Generate a single sine wave with given frequency and amplitude"""
            return amplitude * np.sin(2 * np.pi * freq * t)

        def get_fft(signal, sample_rate):
            """Compute the Fast Fourier Transform of the signal
            Returns positive frequencies and their magnitudes"""
            fft_vals = np.fft.fft(signal)  # Compute FFT
            fft_freqs = np.fft.fftfreq(len(signal), 1/sample_rate)  # Get frequency bins
            pos_mask = fft_freqs > 0  # Only keep positive frequencies
            return fft_freqs[pos_mask], np.abs(fft_vals)[pos_mask]

        # Setup sampling parameters
        sample_rate = 100  # Reduced from 1000 to 100 Hz - still sufficient for visualization
        t = np.linspace(0, 2, sample_rate * 2)  # 2 seconds of time points
        components = [(2, 1), (5, 0.5), (8, 0.3)]  # Keeping the same components

        # Adjust axes for better visibility
        time_axes = Axes(
            x_range=[0, 2, 0.5],
            y_range=[-2, 2, 1],
            x_length=8,  # Increased from 6 to 8 for better visibility
            y_length=4,  # Increased from 3 to 4
            axis_config={"color": BLUE, "include_numbers": True},  # Added numbers
        ).to_edge(UP)

        freq_axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 1.2, 0.2],
            x_length=8,  # Increased from 6 to 8
            y_length=4,  # Increased from 3 to 4
            axis_config={"color": BLUE, "include_numbers": True},  # Added numbers
        ).to_edge(DOWN)

        # Create small axes for individual frequency components
        component_axes_group = VGroup()
        component_plots = VGroup()
        component_labels = VGroup()

        # Create a small display for each frequency component
        for i, (freq, amp) in enumerate(components):
            # Create small axes for this component
            ax = Axes(
                x_range=[0, 1, 0.5],
                y_range=[-1, 1, 0.5],
                x_length=2,
                y_length=1,
                axis_config={"color": GREY_B, "stroke_width": 1}
            ).to_edge(RIGHT, buff=0.5)
            ax.shift(UP * (i - 1) * 1.5)  # Stack vertically
            
            # Plot the individual sine wave
            component_signal = get_component_points(t[:sample_rate], freq, amp)
            plot = ax.plot_line_graph(
                x_values=t[:sample_rate],
                y_values=component_signal,
                line_color=YELLOW,
                stroke_width=2
            )
            
            # Add frequency and amplitude label
            label = Text(f"{freq}Hz × {amp}", font_size=16).next_to(ax, LEFT)
            
            # Group elements for animation
            component_axes_group.add(ax)
            component_plots.add(plot)
            component_labels.add(label)

        # Create the main signal visualization
        signal = get_signal_points(t)
        time_plot = time_axes.plot_line_graph(
            x_values=t,
            y_values=signal,
            line_color=YELLOW,
            stroke_width=2
        )

        # Create sliding window for FFT analysis
        window_width = 0.5  # Window width in seconds
        window = Rectangle(
            width=window_width * time_axes.get_x_unit_size(),
            height=time_axes.height,
            stroke_color=RED,
            stroke_width=2,
            fill_color=RED,
            fill_opacity=0.2
        ).align_to(time_axes, LEFT)

        # Initialize frequency spectrum visualization
        freq_dots = VGroup()
        freq_stems = VGroup()
        freqs, magnitudes = get_fft(signal[:int(window_width * sample_rate)], sample_rate)
        
        # Create dots and stems for frequency spectrum
        for freq, mag in zip(freqs[:50], magnitudes[:50]):  # Only show first 50 frequencies
            dot = Dot(freq_axes.c2p(freq, mag), color=RED)
            stem = Line(
                freq_axes.c2p(freq, 0),
                freq_axes.c2p(freq, mag),
                color=RED,
                stroke_width=2
            )
            freq_dots.add(dot)
            freq_stems.add(stem)

        # Add phase visualization circle
        phase_circle = Circle(radius=0.5, color=BLUE).to_edge(RIGHT, buff=0.5)
        phase_dot = Dot(color=YELLOW).move_to(phase_circle.point_from_proportion(0))
        phase_line = Line(phase_circle.get_center(), phase_dot.get_center(), color=YELLOW)
        phase_group = VGroup(phase_circle, phase_dot, phase_line)

        # New interactive element: Frequency Control Sliders
        class FrequencySlider(VGroup):
            def __init__(self, freq, amplitude, **kwargs):
                super().__init__(**kwargs)
                self.slider = Rectangle(width=2, height=0.1, fill_color=BLUE, fill_opacity=1)
                self.knob = Dot(color=YELLOW).move_to(self.slider.get_center())
                self.label = Text(f"{freq}Hz", font_size=16).next_to(self.slider, LEFT)
                self.value = DecimalNumber(
                    amplitude,
                    num_decimal_places=2,
                    font_size=16
                ).next_to(self.slider, RIGHT)
                self.add(self.slider, self.knob, self.label, self.value)

        # Create interactive sliders
        sliders = VGroup(*[
            FrequencySlider(freq, amp).shift(UP * i)
            for i, (freq, amp) in enumerate(components)
        ]).to_edge(LEFT, buff=1)

        # New educational annotations
        annotations = VGroup(
            # Time Domain Annotations
            Arrow(start=LEFT, end=RIGHT).scale(0.5),
            Text("Time →", font_size=16),
            
            # Frequency Domain Annotations
            Arrow(start=LEFT, end=RIGHT).scale(0.5),
            Text("Frequency →", font_size=16),
            
            # Window Explanation
            Text("Sliding Window", font_size=16),
            Text("(Analyzes signal segment)", font_size=14),
            
            # Phase Information
            Text("Phase Circle", font_size=16),
            Text("Shows signal rotation", font_size=14)
        )

        # New interactive element: Time-Frequency Correlation Lines
        def create_correlation_lines():
            lines = VGroup()
            for freq, mag in zip(freqs[:50], magnitudes[:50]):
                if mag > 0.1:  # Only show significant frequencies
                    line = DashedLine(
                        start=time_axes.c2p(0, mag),
                        end=freq_axes.c2p(freq, mag),
                        color=YELLOW,
                        stroke_opacity=0.3
                    )
                    lines.add(line)
            return lines

        # New interactive element: Real-time Frequency Indicator
        freq_indicator = Triangle(
            fill_color=YELLOW,
            fill_opacity=1
        ).scale(0.1).rotate(-PI/2)
        
        # New educational element: Frequency Components Breakdown
        def create_component_breakdown():
            breakdown = VGroup()
            for freq, amp in components:
                wave = time_axes.plot(
                    lambda x: amp * np.sin(2 * PI * freq * x),
                    color=BLUE_C
                ).set_opacity(0.5)  # Set opacity after creating the plot
                breakdown.add(wave)
            return breakdown

        # Add new mathematical visualization
        def create_fourier_equation():
            return MathTex(
                "F(\\omega) = \\int_{-\\infty}^{\\infty} f(t)e^{-i\\omega t}dt",
                font_size=24
            ).to_edge(UP)

        # Interactive tooltip system
        class Tooltip(VGroup):
            def __init__(self, text, target, **kwargs):
                super().__init__(**kwargs)
                self.bubble = RoundedRectangle(height=0.5, width=1, corner_radius=0.1)
                self.text = Text(text, font_size=12)
                self.text.move_to(self.bubble)
                self.add(self.bubble, self.text)
                self.next_to(target, UP)

        # Add before the animation sequence
        # Define window positions for animation
        window_positions = np.linspace(0, 2 - window_width, 20)  # Reduced from 50 to 20 positions

        # Define spectrum update function
        def update_spectrum(wx):
            start_idx = int(wx * sample_rate)
            end_idx = int((wx + window_width) * sample_rate)
            window_signal = signal[start_idx:end_idx]
            freqs, magnitudes = get_fft(window_signal, sample_rate)
            
            # Update frequency spectrum visualization
            for i, (freq, mag) in enumerate(zip(freqs[:50], magnitudes[:50])):
                freq_dots[i].move_to(freq_axes.c2p(freq, mag))
                freq_stems[i].put_start_and_end_on(
                    freq_axes.c2p(freq, 0),
                    freq_axes.c2p(freq, mag)
                )

        # Position the labels and annotations properly
        annotations.arrange(DOWN, buff=0.5).to_edge(RIGHT)

        # Animation sequence with new elements
        self.play(
            Create(time_axes),
            Create(freq_axes),
            run_time=1
        )
        
        self.play(
            Create(time_plot),
            Create(window),
            Create(freq_dots),
            Create(freq_stems),
            run_time=1
        )

        # Simplified window sliding animation
        for wx in window_positions:
            self.play(
                window.animate.move_to(
                    time_axes.c2p(wx + window_width/2, 0),
                    aligned_edge=ORIGIN
                ),
                *[
                    UpdateFromFunc(freq_dots[i], lambda m, i=i, f=freq, mag=mag: m.move_to(freq_axes.c2p(f, mag)))
                    for i, (freq, mag) in enumerate(zip(freqs[:50], magnitudes[:50]))
                ],
                run_time=0.2,  # Faster animation
            )
            update_spectrum(wx)

        self.wait(1)  # Reduced wait time

