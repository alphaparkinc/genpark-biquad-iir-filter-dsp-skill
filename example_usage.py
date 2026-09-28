from client import BiquadIIRFilterEngine

def main():
    engine = BiquadIIRFilterEngine(sample_rate=44100)
    coeffs = engine.design_filter("lowpass", cutoff_freq=1000.0, q_factor=0.7071)
    bode = engine.frequency_response(coeffs, [100.0, 500.0, 1000.0, 2000.0, 10000.0])
    print("Biquad IIR Lowpass Filter Verification:")
    print(f"Coefficients: {coeffs}")
    print("Frequency Response:")
    for pt in bode:
        print(f"  {pt['freq_hz']} Hz: {pt['mag_db']} dB, Phase: {pt['phase_deg']} deg")

if __name__ == "__main__":
    main()
