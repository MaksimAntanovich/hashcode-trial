from point import Point


class Cut:
    begin = Point(0, 0)
    end = Point(0, 0)

    def __init__(self, begin, end):
        self.begin = begin
        self.end = end

    def count(self, char):
        from main import pizza
        count = 0
        for i in range(self.begin.x, self.end.x + 1):
            for j in range(self.begin.y, self.end.y + 1):
                if pizza[j, i] == char:
                    count += 1
        return count

    def square(self):
        return (self.end.x - self.begin.x + 1) * (self.end.y - self.begin.y + 1)

    def valid(self):
        from main import L, H
        return self.count('M') >= L and self.count('T') >= L and self.square() <= H
