"""Generate the Empirical bell-curve path (Gaussian, matched to the original logo).

Usage: python3 tools/curve.py [width] [base_y] [peak_y] [points]
Prints an SVG path 'd' string: a closed Gaussian from (0, base) to (width, base).
"""
import math, sys

def curve(width=1400, base=533, peak=4, n=48):
    sigma = width * 0.15          # measured from the original logo
    amp = base - peak
    cx = width / 2
    # denser sampling near the centre
    xs = sorted({round(cx + (width / 2) * math.copysign(abs(t) ** 1.6, t), 2)
                 for t in [i / n * 2 - 1 for i in range(n + 1)]})
    pts = [(x, base - amp * math.exp(-((x - cx) ** 2) / (2 * sigma ** 2))) for x in xs]
    # Catmull-Rom -> cubic Bezier for a smooth outline
    d = [f"M{pts[0][0]:.1f} {base:.1f}L{pts[0][0]:.1f} {pts[0][1]:.1f}"]
    for i in range(len(pts) - 1):
        p0 = pts[i - 1] if i else pts[i]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[i + 2] if i + 2 < len(pts) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d.append(f"C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}")
    d.append(f"L{pts[-1][0]:.1f} {base:.1f}Z")
    return "".join(d)

if __name__ == "__main__":
    a = [float(x) for x in sys.argv[1:4]]
    n = int(sys.argv[4]) if len(sys.argv) > 4 else 48
    print(curve(*a, n=n) if a else curve(n=n))
