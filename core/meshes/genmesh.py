import math

LAT = 20
LON = 30   # 10 * 15 * 2 triangles = 300

vertices = []
faces = []

# top pole
vertices.append((0, 1, 0))

# rings
for i in range(1, LAT):
    phi = math.pi * i / LAT
    y = math.cos(phi)
    r = math.sin(phi)

    for j in range(LON):
        theta = 2 * math.pi * j / LON
        x = r * math.cos(theta)
        z = r * math.sin(theta)
        vertices.append((x, y, z))

# bottom pole
bottom_index = len(vertices)
vertices.append((0, -1, 0))

def ring_start(i):
    return 1 + (i - 1) * LON

# top cap
for j in range(LON):
    a = 0
    b = ring_start(1) + j
    c = ring_start(1) + (j + 1) % LON
    faces.append((a, c, b))

# middle
for i in range(1, LAT - 1):
    r1 = ring_start(i)
    r2 = ring_start(i + 1)

    for j in range(LON):
        a = r1 + j
        b = r1 + (j + 1) % LON
        c = r2 + j
        d = r2 + (j + 1) % LON

        faces.append((a, b, c))
        faces.append((b, d, c))

# bottom cap
last_ring = ring_start(LAT - 1)

for j in range(LON):
    a = last_ring + j
    b = last_ring + (j + 1) % LON
    faces.append((a, bottom_index, b))

# output in your format
for v in vertices:
    print(f"v {v[0]:.6f} {v[1]:.6f} {v[2]:.6f}")

print()

for f in faces:
    print(f"f {f[0]} {f[1]} {f[2]}")

print("\n# triangles:", len(faces))