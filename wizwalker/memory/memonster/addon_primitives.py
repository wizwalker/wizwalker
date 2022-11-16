import math

class XYZ:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __sub__(self, other):
        return self.distance(other)

    def __str__(self):
        return f"<XYZ ({self.x}, {self.y}, {self.z})>"

    def __repr__(self):
        return str(self)

    def __iter__(self):
        return iter((self.x, self.y, self.z))

    def distance(self, other):
        """
        Calculate the distance between two points
        this does not account for z axis
        """
        if not isinstance(other, type(self)):
            raise ValueError(
                f"Can only calculate distance between instances of {type(self)} not {type(other)}"
            )

        return math.dist((self.x, self.y), (other.x, other.y))

    def calculate_perfect_yaw(self, target_xyz: "XYZ") -> float:
        """
        Calculates the perfect yaw to reach an xyz in a stright line

        Args:
            current_xyz: Starting position xyz
            target_xyz: Ending position xyz
        """
        target_line = math.dist(
            (self.x, self.y), (target_xyz.x, target_xyz.y)
        )
        origin_line = math.dist(
            (self.x, self.y), (self.x, self.y - 1)
        )
        target_to_origin_line = math.dist(
            (target_xyz.x, target_xyz.y), (self.x, self.y - 1)
        )
        # target_angle = math.cos(origin_line / target_line)
        target_angle = math.acos(
            (pow(target_line, 2) + pow(origin_line, 2) - pow(target_to_origin_line, 2))
            / (2 * origin_line * target_line)
        )

        if target_xyz.x > self.x:
            # outside
            target_angle_degres = math.degrees(target_angle)
            perfect_yaw = math.radians(360 - target_angle_degres)
        else:
            # inside
            perfect_yaw = target_angle

        return perfect_yaw

    def yaw(self, other):
        """Calculate perfect yaw to reach another xyz"""
        if not isinstance(other, type(self)):
            raise ValueError(
                f"Can only calculate yaw between instances of {type(self)} not {type(other)}"
            )

        return self.calculate_perfect_yaw(other)

    def relative_yaw(self, *, x: float = None, y: float = None):
        """Calculate relative yaw to reach another x and/or y relative to current"""
        if x is None:
            x = self.x
        if y is None:
            y = self.y

        other = type(self)(x, y, self.z)
        return self.yaw(other)


class Orient:
    def __init__(self, pitch: float, roll: float, yaw: float):
        self.pitch = pitch
        self.roll = roll
        self.yaw = yaw

    def __str__(self):
        return f"<Orient (Pitch: {self.pitch}, roll: {self.roll}, yaw: {self.yaw})>"

    def __repr__(self):
        return str(self)

    def __iter__(self):
        return iter((self.pitch, self.roll, self.yaw))


class Rectangle:
    def __init__(self, x1: int, y1: int, x2: int, y2: int):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def __str__(self):
        return f"<Rectangle ({self.x1}, {self.y1}, {self.x2}, {self.y2})>"

    def __repr__(self):
        return str(self)

    def __iter__(self):
        return iter((self.x1, self.x2, self.y1, self.y2))

    def scale_to_client(self, parents: list["Rectangle"], factor: float) -> "Rectangle":
        """
        Scale this rectangle base on parents and a scale factor

        Args:
            parents: List of other rectangles
            factor: Factor to scale by

        Returns:
            The scaled rectangle
        """
        x1_sum = self.x1
        y1_sum = self.y1

        for rect in parents:
            x1_sum += rect.x1
            y1_sum += rect.y1

        converted = Rectangle(
            int(x1_sum * factor),
            int(y1_sum * factor),
            int(((self.x2 - self.x1) * factor) + (x1_sum * factor)),
            int(((self.y2 - self.y1) * factor) + (y1_sum * factor)),
        )

        return converted

    def center(self):
        """
        Get the center point of this rectangle

        Returns:
            The center point
        """
        center_x = ((self.x2 - self.x1) // 2) + self.x1
        center_y = ((self.y2 - self.y1) // 2) + self.y1

        return center_x, center_y


    # TODO:
    # def paint_on_screen(self, window_handle: int, *, rgb: tuple = (255, 0, 0)):
    #     """
    #     Paint this rectangle to the screen for debugging

    #     Args:
    #         rgb: Red, green, blue tuple to define the color of the rectangle
    #         window_handle: Handle to the window to paint the rectangle on
    #     """
    #     paint_struct = PAINTSTRUCT()
    #     # https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getdc
    #     device_context = user32.GetDC(window_handle)
    #     brush = gdi32.CreateSolidBrush(ctypes.wintypes.RGB(*rgb))

    #     user32.BeginPaint(window_handle, ctypes.byref(paint_struct))

    #     # left, top = top left corner; right, bottom = bottom right corner
    #     draw_rect = ctypes.wintypes.RECT()
    #     draw_rect.left = self.x1
    #     draw_rect.top = self.y1
    #     draw_rect.right = self.x2
    #     draw_rect.bottom = self.y2

    #     # https://docs.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-createrectrgnindirect
    #     region = gdi32.CreateRectRgnIndirect(ctypes.byref(draw_rect))
    #     # https://docs.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-fillrgn
    #     gdi32.FillRgn(device_context, region, brush)

    #     user32.EndPaint(window_handle, ctypes.byref(paint_struct))
    #     user32.ReleaseDC(window_handle, device_context)
    #     gdi32.DeleteObject(brush)
    #     gdi32.DeleteObject(region)
