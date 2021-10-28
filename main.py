class ECDH:
    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p

    def double_point(self, x, y):
        s = ((3*(x**2)+self.a) * pow(2*y, -1, self.p)) % self.p
        x_new = (s**2 - 2*x) % self.p
        y_new = (-y + s*(x - x_new)) % self.p
        return x_new, y_new

    def add_points(self, xG, yG, xH, yH):
        try:
            s = ((yH - yG) * pow(xH - xG, -1, self.p)) % self.p
        except ValueError:
            return None, None
        x_new = (s**2 - xH - xG) % self.p
        y_new = (-yH + s*(xH - x_new)) % self.p
        return x_new, y_new

    def generate_subgroup(self, generator_x, generator_y):
        x, y = generator_x, generator_y
        counter = 1
        points = []
        while x is not None:
            points.append((x, y))
            if (x, y) == (generator_x, generator_y):
                x, y = self.double_point(x, y)
            else:
                x, y = self.add_points(x, y, generator_x, generator_y)
            counter += 1
        return points, counter

    def print_subgroup(self, generator_x, generator_y):
        subgroup = self.generate_subgroup(generator_x, generator_y)
        for index, point in enumerate(subgroup[0]):
            print('Key value ' + str(index + 1) + ': ' + str(point))
        print('Key value ' + str(len(subgroup[0]) + 1) + ': infinity')
        print('Subgroup Order: ' + str(subgroup[1]))

    def print_shared_key(self, public_x, public_y, secret_key):
        subgroup = self.generate_subgroup(public_x, public_y)
        print('Shared secret: ' + str(subgroup[0][secret_key - 1]))


if __name__ == '__main__':
    # G = 5, 9
    # a = 5
    # b = 9
    # p = 13
    # ecdh = ECDH(a, b, p)
    # ecdh.print_subgroup(G[0], G[1])

    a = 5
    b = 9
    p = 13
    ecdh = ECDH(a, b, p)

    G = 5, 9
    combined_secret = 11
    ecdh.print_shared_key(G[0], G[1], combined_secret)
