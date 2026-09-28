"""Second-Order Biquad IIR Digital Audio Filter Engine
100% Python Standard Library (math, cmath).
"""

import math
import cmath

class BiquadIIRFilterEngine:
    """Biquad IIR filter implementing Low-Pass, High-Pass, Band-Pass, Notch, and Peaking EQ."""
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate

    def design_filter(self, filter_type="lowpass", cutoff_freq=1000.0, q_factor=0.7071, gain_db=0.0):
        omega = 2.0 * math.pi * cutoff_freq / self.sample_rate
        sn = math.sin(omega)
        cs = math.cos(omega)
        alpha = sn / (2.0 * q_factor)
        A = 10.0 ** (gain_db / 40.0)

        if filter_type == "lowpass":
            b0 = (1.0 - cs) / 2.0
            b1 = 1.0 - cs
            b2 = (1.0 - cs) / 2.0
            a0 = 1.0 + alpha
            a1 = -2.0 * cs
            a2 = 1.0 - alpha
        elif filter_type == "highpass":
            b0 = (1.0 + cs) / 2.0
            b1 = -(1.0 + cs)
            b2 = (1.0 + cs) / 2.0
            a0 = 1.0 + alpha
            a1 = -2.0 * cs
            a2 = 1.0 - alpha
        elif filter_type == "bandpass":
            b0 = alpha
            b1 = 0.0
            b2 = -alpha
            a0 = 1.0 + alpha
            a1 = -2.0 * cs
            a2 = 1.0 - alpha
        elif filter_type == "notch":
            b0 = 1.0
            b1 = -2.0 * cs
            b2 = 1.0
            a0 = 1.0 + alpha
            a1 = -2.0 * cs
            a2 = 1.0 - alpha
        else: # peaking
            b0 = 1.0 + alpha * A
            b1 = -2.0 * cs
            b2 = 1.0 - alpha * A
            a0 = 1.0 + alpha / A
            a1 = -2.0 * cs
            a2 = 1.0 - alpha / A

        return {
            "b0": b0 / a0,
            "b1": b1 / a0,
            "b2": b2 / a0,
            "a1": a1 / a0,
            "a2": a2 / a0
        }

    def process_signal(self, signal, coeffs):
        b0, b1, b2 = coeffs["b0"], coeffs["b1"], coeffs["b2"]
        a1, a2 = coeffs["a1"], coeffs["a2"]
        y = []
        x1 = x2 = y1 = y2 = 0.0
        for x0 in signal:
            y0 = b0 * x0 + b1 * x1 + b2 * x2 - a1 * y1 - a2 * y2
            y.append(y0)
            x2 = x1
            x1 = x0
            y2 = y1
            y1 = y0
        return y

    def frequency_response(self, coeffs, freqs):
        b0, b1, b2 = coeffs["b0"], coeffs["b1"], coeffs["b2"]
        a1, a2 = coeffs["a1"], coeffs["a2"]
        response = []
        for f in freqs:
            w = 2.0 * math.pi * f / self.sample_rate
            z1 = cmath.exp(complex(0, -w))
            z2 = cmath.exp(complex(0, -2 * w))
            num = b0 + b1 * z1 + b2 * z2
            den = 1.0 + a1 * z1 + a2 * z2
            h = num / den
            mag_db = 20.0 * math.log10(max(abs(h), 1e-9))
            phase_deg = math.degrees(cmath.phase(h))
            response.append({"freq_hz": f, "mag_db": round(mag_db, 2), "phase_deg": round(phase_deg, 2)})
        return response
