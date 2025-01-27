import pygame
import numpy as np

class MusicGenerator:
    def __init__(self):
        self.sample_rate = 44100
        self.notes = {
            'C3': 130.81, 'D3': 146.83, 'E3': 164.81, 'F3': 174.61,
            'G3': 196.00, 'A3': 220.00, 'B3': 246.94,
            'C4': 261.63, 'D4': 293.66, 'E4': 329.63, 'F4': 349.23,
            'G4': 392.00, 'A4': 440.00, 'B4': 493.88,
            'C5': 523.25, 'D5': 587.33, 'E5': 659.25, 'F5': 698.46,
            'G5': 783.99, 'A5': 880.00
        }
        
    def generate_square_wave(self, frequency, duration, amplitude=0.3, duty_cycle=0.5):
        num_samples = int(duration * self.sample_rate)
        t = np.linspace(0, duration, num_samples, False)
        wave = (np.sin(2 * np.pi * frequency * t) > -duty_cycle) * 2 - 1
        return (wave * amplitude * 32767).astype(np.int16)

    def create_pattern(self, notes_pattern, base_duration=0.125):
        return [(note, duration * base_duration) for note, duration in notes_pattern]

    def generate_song(self):
        # Fast-paced intro
        intro = self.create_pattern([
            ('E4', 1), ('G4', 1), ('A4', 2),
            ('C5', 1), ('B4', 1), ('A4', 2),
            ('G4', 1), ('E4', 1), ('G4', 2),
            ('A4', 1), ('G4', 1), ('E4', 2),
        ], 0.125)  # Sixteenth notes for speed

        # Main verse - energetic and rhythmic
        verse = self.create_pattern([
            ('E4', 1), ('G4', 1), ('A4', 2), ('C5', 2),
            ('B4', 1), ('A4', 1), ('G4', 2), ('E4', 2),
            ('A4', 1), ('G4', 1), ('E4', 2), ('D4', 2),
            ('E4', 1), ('G4', 1), ('A4', 2), ('G4', 2),
        ] * 2, 0.125)

        # Build-up section
        buildup = self.create_pattern([
            ('C5', 1), ('D5', 1), ('E5', 2),
            ('D5', 1), ('C5', 1), ('B4', 2),
            ('C5', 1), ('D5', 1), ('E5', 2),
            ('F5', 1), ('E5', 1), ('D5', 2),
        ] * 2, 0.125)

        # Intense chorus
        chorus = self.create_pattern([
            ('E5', 1), ('D5', 1), ('C5', 1), ('B4', 1),
            ('C5', 1), ('A4', 1), ('G4', 2),
            ('A4', 1), ('B4', 1), ('C5', 1), ('D5', 1),
            ('E5', 1), ('D5', 1), ('C5', 2),
        ] * 2, 0.125)

        # Bridge with variation
        bridge = self.create_pattern([
            ('G4', 1), ('A4', 1), ('B4', 2),
            ('C5', 2), ('D5', 2), ('E5', 2),
            ('D5', 1), ('C5', 1), ('B4', 2),
            ('A4', 2), ('G4', 2), ('F4', 2),
        ] * 2, 0.125)

        # Final chorus with higher intensity
        final_chorus = self.create_pattern([
            ('E5', 1), ('G5', 1), ('A5', 1), ('G5', 1),
            ('E5', 1), ('C5', 1), ('D5', 2),
            ('E5', 1), ('D5', 1), ('C5', 1), ('B4', 1),
            ('C5', 1), ('A4', 1), ('G4', 2),
        ] * 2, 0.125)

        # Outro with dramatic finish
        outro = self.create_pattern([
            ('C5', 2), ('G4', 2), ('E4', 4),
            ('A4', 2), ('E4', 2), ('C4', 4),
            ('G4', 2), ('E4', 2), ('C4', 8),
        ], 0.125)

        # Combine all sections
        melody = (intro + 
                 verse + 
                 buildup + 
                 chorus + 
                 verse + 
                 bridge + 
                 chorus + 
                 buildup + 
                 final_chorus + 
                 outro)

        # Bass line patterns for different sections
        bass_pattern = [
            ('C3', 4), ('G3', 4), 
            ('A3', 4), ('E3', 4),
            ('F3', 4), ('C3', 4), 
            ('G3', 4), ('C3', 4)
        ]
        
        bass_intense = [
            ('C3', 2), ('G3', 2), ('C3', 2), ('G3', 2),
            ('A3', 2), ('E3', 2), ('A3', 2), ('E3', 2),
        ]

        # Create full bass line matching song length
        bass_line = self.create_pattern(bass_pattern * 8 + 
                                      bass_intense * 4 + 
                                      bass_pattern * 12, 0.125)

        # Generate the audio
        total_duration = sum(duration for _, duration in melody)
        buffer = np.zeros((int(total_duration * self.sample_rate), 2), dtype=np.int16)

        # Add melody
        current_time = 0
        for note, duration in melody:
            freq = self.notes[note]
            wave = self.generate_square_wave(freq, duration, amplitude=0.2)
            end_time = current_time + len(wave)
            buffer[current_time:end_time] += np.column_stack((wave, wave))
            current_time = end_time

        # Add bass
        current_time = 0
        for note, duration in bass_line:
            if current_time >= len(buffer):
                break
            freq = self.notes[note]
            wave = self.generate_square_wave(freq, duration, amplitude=0.15, duty_cycle=0.3)
            end_time = min(current_time + len(wave), len(buffer))
            buffer[current_time:end_time] += np.column_stack((wave[:end_time-current_time], wave[:end_time-current_time]))
            current_time = end_time

        # Normalize to prevent clipping
        buffer = (buffer * 0.7).astype(np.int16)
        
        return pygame.sndarray.make_sound(buffer), total_duration

    def generate_hit_sound(self):
        duration = 0.1
        frequency = 880
        wave1 = self.generate_square_wave(frequency, duration, 0.2)
        wave2 = self.generate_square_wave(frequency * 1.5, duration, 0.1)
        combined_wave = wave1 + wave2
        buffer = np.column_stack((combined_wave, combined_wave))
        return pygame.sndarray.make_sound(buffer)

# Make sure the class is available for import
__all__ = ['MusicGenerator']