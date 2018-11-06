class Distance:
    '''
    Cálculo de distâncias em um grid hexagonal
    '''

    @staticmethod
    def axial_to_cube(q, r):
        x = r
        z = q
        y = -x - z
        return (x, y, z)

    def hex_distance(self, p0, p1):
        x0, y0 = p0
        x1, y1 = p1
        first = Distance.axial_to_cube(x0, y0)
        second = Distance.axial_to_cube(x1, y1)
        return Distance.cube_distance(first[0], first[1], first[2], second[0], second[1], second[2])

    @staticmethod
    def cube_distance(ax, ay, az, bx, by, bz):
        return (abs(ax - bx) + abs(ay - by) + abs(az - bz)) / 2