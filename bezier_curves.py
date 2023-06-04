import numpy as np
import numpy.typing as npt
import pygame
import math

class BezierTools():
    # generate control points from terminal user input. Minimum 2 points
    def gen_controlpoints(self) -> npt.ArrayLike:
        n = int(input("How many Bezier control points? (>= 2):  "))
        ctrl_points = np.random.randint((0, 0), (self.width, self.height), (n, 2))
        return ctrl_points

    # generate Bernstein basis polynomial
    # reference: https://en.wikipedia.org/wiki/Bernstein_polynomial
    def bernstein(self, t, n, i) -> int:
        return math.comb(n, i) * math.pow(t, i) * math.pow((1-t), (n-i))
    
    # generate Bezier curve points
    # reference: [explicit terminology] https://en.wikipedia.org/wiki/B%C3%A9zier_curve
    def bezier(self, points, t) -> tuple[float, float]:
        degree = len(points) - 1
        x = y = 0
        for i, pos in enumerate(points):
            bern_coeff = self.bernstein(t, degree, i)
            x += pos[0] * bern_coeff
            y += pos[1] * bern_coeff
        return (x, y)

class MainWindow(BezierTools):
    def __init__(self) -> None:
        # window dimensions in px
        # origin: top-left
        self.height = 600
        self.width = 800

        # colors are in (r, g, b) format
        self.background_color = (0, 0, 0)
        self.ctrl_point_color = (0, 255, 0)
        self.ctrl_line_color = (100, 100, 100)
        self.beziercurve_color = (255, 174, 0)
        self.boundingbox_color = (255, 0, 255)
        
        # thicknesses are in px
        self.ctrl_point_radius = 4
        self.ctrl_line_thickness = 1
        self.beziercurve_thickness = 2
        self.boundingbox_thickness = 2

        # box edge length = boundingbox_size * 2
        self.bboxes = None
        self.boundingbox_size = 10

        # bezier curve smoothness  
        # higher the value, smoother the curve
        self.beziercurve_smoothness = 1000

        # text offset (y px)
        self.text_offset = 15

        self.control_points = None
        self.draggable = False

        # initialize pygame instance and draw window
        pygame.init()
        self.surface = pygame.display.set_mode((self.width, self.height))
        self.surface.fill(self.background_color)
    
    # pygame main loop
    def main(self):
        # Obtain number of control points from user terminal input -- degree
        self.control_points = BezierTools.gen_controlpoints(self)
        self.degree = self.control_points.shape[0]

        while True:
            self.draw_control_segs(self.control_points)
            self.bboxes = self.draw_boundingboxes(self.control_points)
            self.draw_beziercurve(self.control_points, self.degree)
            self.text_on_bboxes(self.control_points)
            pygame.display.update()

            for event in pygame.event.get():
                # Exit sequence
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                # Upon mouse pressed, do this
                # event.button == 1 is left mouse click
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        for idx, _ in enumerate(self.control_points):
                            if self.bboxes[idx].collidepoint(mouse_pos):
                                self.draggable = True
                                mouse_x, mouse_y = mouse_pos
                                offset_x = self.bboxes[idx].x - mouse_x
                                offset_y = self.bboxes[idx].y - mouse_y
                                break

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.draggable = False

                elif event.type == pygame.MOUSEMOTION:
                    if self.draggable:
                        mouse_x, mouse_y = event.pos
                        self.control_points[idx][0] = mouse_x + offset_x
                        self.control_points[idx][1] = mouse_y + offset_y

            self.surface.fill(self.background_color)

    # Plot bezier control points and lines on screen
    def draw_control_segs(self, points) -> None:
        for i, ctrl_pt in enumerate(points):
            # plot control points
            pygame.draw.circle(self.surface, self.ctrl_point_color, ctrl_pt, self.ctrl_point_radius)

            # draw lines between control points
            if i < len(points)-1:
                pygame.draw.line(self.surface, self.ctrl_line_color, ctrl_pt, points[i+1], self.ctrl_line_thickness)

    # Plot the bezier curve itself
    def draw_beziercurve(self, points, n) -> None:
        bezier_coords = []
        # 0 <= t <= 1
        sample_points = np.linspace(0, 1, self.beziercurve_smoothness)
        for idx, t in enumerate(sample_points):
            bezier_coords.append(BezierTools.bezier(self, points, t))
        pygame.draw.lines(self.surface, self.beziercurve_color, False, bezier_coords, self.beziercurve_thickness)

    # Draw bounding boxes on the control points
    def draw_boundingboxes(self, points: npt.ArrayLike) -> list:
        boxes = []
        for i, point in enumerate(points):
            left, top = point - self.boundingbox_size
            rect = pygame.Rect(left, top, self.boundingbox_size*2, self.boundingbox_size*2)
            boxes.append(rect)
            pygame.draw.rect(self.surface, self.boundingbox_color, boxes[i], self.boundingbox_thickness)
        return boxes

    # Draw text on bounding boxes showing the x,y coords of control point
    def text_on_bboxes(self, points: npt.ArrayLike) -> None:
        text = []
        text_rect = []
        font = pygame.font.Font('freesansbold.ttf', 16)
        for idx, point in enumerate(points):
            coord_text = f"({point})"
            text_render = font.render(coord_text, True, self.ctrl_point_color)
            text.append(text_render)
            text_rect.append(text_render.get_rect())
            text_rect[idx].center = (point[0], point[1]-self.text_offset)
            self.surface.blit(text[idx], text_rect[idx])

if __name__ == "__main__":
    window = MainWindow()
    window.main()