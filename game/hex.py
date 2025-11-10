class Hex:
    def __init__(self, x, y, z):
        self.__x__ = x
        self.__y__ = y
        self.__z__ = z
        self.Coord = (x, y, z)
        self.Terrain = None
    
    def __repr__(self):
        return self.Coord
    
    def SetTer(self, terrain):
        self.Terrain = terrain
    
class Grid:
    def __init__(self, size):
        self.Hexes = {}
        for x in range(-size, size):
            for y in range(-size, size):
                for z in range(-size, size):
                    if x + y + z != 0:
                        continue
                    h = Hex(x, y, z)
                    self.Hexes[h.Coord] = h

    def GetNeighbors(self, coord, radius=1):
        neighbors = []
        x0, y0, z0 = coord
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                dz = -dx - dy
                if abs(dz) > radius:
                    continue
                ncoord = (x0 + dx, y0 + dy, z0 + dz)
                if ncoord == coord:
                    continue
                if ncoord in self.Hexes:
                    neighbors.append(self.Hexes[ncoord])
        return neighbors
    
    def GetLine(self, start, end):
        hexes = []
        x0, y0, z0 = start
        x1, y1, z1 = end

        n = cube_distance(start, end)
        if n == 0:
            return [self.Hexes[start]] if start in self.Hexes else []

        for i in range(n + 1):
            t = 0.0 if n == 0 else i / float(n)
            fx, fy, fz = cube_lerp(start, end, t)
            coord = cube_round(fx, fy, fz)
            if coord in self.Hexes:
                hexes.append(self.Hexes[coord])
        return hexes
    
    def GetDistance(self, start, end):
        if start in self.Hexes and end in self.Hexes:
            return cube_distance(start, end)
        raise Exception("invalid input")



def cube_distance(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]), abs(a[2] - b[2]))

def cube_lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t,
             a[1] + (b[1] - a[1]) * t,
             a[2] + (b[2] - a[2]) * t)

def cube_round(fx, fy, fz):
    rx = round(fx)
    ry = round(fy)
    rz = round(fz)
    x_diff = abs(rx - fx)
    y_diff = abs(ry - fy)
    z_diff = abs(rz - fz)
    if x_diff > y_diff and x_diff > z_diff:
        rx = -ry - rz
    elif y_diff > z_diff:
        ry = -rx - rz
    else:
        rz = -rx - ry
    return (int(rx), int(ry), int(rz))