import dearpygui.dearpygui as dpg
from collections.abc import Iterable
import bezier as bz

class BezierSimulator:
    def __init__(self) -> None:
        self.showcoords_flag = True
        self.show()

    def show(self):
        dpg.create_context()
        dpg.create_viewport(title="Bezier Curve Generator", width=600, height=600)

        with dpg.window(tag="Primary Window"):
            with dpg.group(horizontal=True):
                dpg.add_input_int(
                    label="Control points", width=100, tag="ctrl_pts", default_value=4
                )
                dpg.add_input_int(
                    label="Smoothness", width=100, tag="smooth", default_value=1000
                )

            dpg.add_checkbox(
                label="Show coordinates",
                default_value=True,
                callback=self.toggle_coords,
                tag="show_coords",
            )
            dpg.add_button(label="Generate Curve", callback=self.draw_bezier)

        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("Primary Window", True)
        dpg.start_dearpygui()
        dpg.destroy_context()

    def detect_bezier_type(self, deg: int) -> str:
        """
        Displays the type of the Bezier curve based on its degree.
        It's helpful to ascribe a name to it. This does not affect
        the curve itself, it's merely a QoL annotation.

        :param deg: The number of control points i.e. the degree
        :returns: An f-string denoting the type of the curve
        """
        curve_types = {1: "Linear", 2: "Quadratic", 3: "Cubic", 4: "Quartic"}
        if deg in curve_types.keys():
            return curve_types[deg] + " Bezier curve"
        else:
            return f"{deg}-degree Bezier curve"

    def generate_bezier(self, n_ctrl: int, smoothness: int) -> Iterable:
        """
        Generates the points comprising the Bezier curve as two arrays
        -- The Bezier curve data itself and the control points. Pass them
        to plotting functions to graph the curve

        :param n_ctrl: No. of control points/degree
        :param smoothness: The higher this number, the smoother the curve
        :returns bezier_coords: The Bezier curve data
        :returns ctrl_points: The control points themselves
        """
        self.bezier_coords, self.ctrl_points = bz.bezier_curve_points(n_ctrl, smoothness)
        return self.bezier_coords, self.ctrl_points

    def annotate_plot(self, ctrl_points: Iterable):
        """
        Annotates the curve plot

        :param ctrl_points: The control points, as an array
        """
        if dpg.does_alias_exist("curvetype"): dpg.remove_alias("curvetype")
        if self.showcoords_flag:
            for i, (x, y) in enumerate(ctrl_points):
                dpg.add_plot_annotation(
                    label=f"P{i}: ({x:.1f}, {y:.1f})",
                    default_value=(x, y),
                    offset=(10, 10),
                    tag=f"annotation_{i}",
                    parent="bezier_plot",
                    clamped=False,
                )
            dpg.bind_item_theme(f"annotation_{i}", "annotation_theme")

        dpg.add_plot_annotation(
            label=self.detect_bezier_type(len(ctrl_points)),
            default_value=(250, 480),
            tag="curvetype",
            parent="bezier_plot",
            clamped=False,
            color=(0, 0, 255, 255),
        )
        dpg.bind_item_theme("curvetype", "curve_label_theme")

    def draw_bezier(self) -> None:
        """
        The callback function that plots the Bezier curve
        """
        if dpg.does_alias_exist("bezier_theme"):
            dpg.remove_alias("bezier_theme")
        if dpg.does_alias_exist("annotation_theme"):
            dpg.remove_alias("annotation_theme")
        if dpg.does_alias_exist("curve_label_theme"):
            dpg.remove_alias("curve_label_theme")
        if dpg.does_alias_exist("bezier_plot"):
            dpg.delete_item("bezier_plot")

        # Colour theme for the curve
        with dpg.theme(tag="bezier_theme"):
            with dpg.theme_component(dpg.mvLineSeries):
                dpg.add_theme_color(
                    dpg.mvPlotCol_Line, (255, 115, 0), category=dpg.mvThemeCat_Plots
                )

            with dpg.theme_component(dpg.mvScatterSeries):
                dpg.add_theme_color(
                    dpg.mvPlotCol_Line, (238, 89, 255, 255), category=dpg.mvThemeCat_Plots
                )
                dpg.add_theme_style(
                    dpg.mvPlotStyleVar_Marker,
                    dpg.mvPlotMarker_Circle,
                    category=dpg.mvThemeCat_Plots,
                )
                dpg.add_theme_style(
                    dpg.mvPlotStyleVar_MarkerSize, 4, category=dpg.mvThemeCat_Plots
                )

        # Create a theme for annotations
        with dpg.theme(tag="annotation_theme"):
            with dpg.theme_component(dpg.mvAnnotation):
                dpg.add_theme_color(
                    dpg.mvPlotCol_FrameBg, (0, 0, 0, 0), category=dpg.mvThemeCat_Plots
                )

        # Theme for curve label
        with dpg.theme(tag="curve_label_theme"):
            with dpg.theme_component(dpg.mvAnnotation):
                dpg.add_theme_color(
                    dpg.mvPlotCol_FrameBg,
                    (0, 0, 255, 255),
                    category=dpg.mvThemeCat_Plots,
                )

        self.n_ctrl_points = dpg.get_value("ctrl_pts")
        self.smoothness = dpg.get_value("smooth")

        self.bezier_coords, self.ctrl_points = self.generate_bezier(self.n_ctrl_points, self.smoothness)

        bezier_coords_x, bezier_coords_y = zip(*self.bezier_coords)
        ctrl_points_x, ctrl_points_y = zip(*self.ctrl_points)

        with dpg.plot(
            label="Bezier Curve",
            parent="Primary Window",
            tag="bezier_plot",
            width=600,
            height=400,
        ):
            dpg.add_plot_axis(dpg.mvXAxis, label="X", tag="bezier_x")
            dpg.add_plot_axis(dpg.mvYAxis, label="Y", tag="bezier_y")
            dpg.set_axis_limits("bezier_x", 0, 500)
            dpg.set_axis_limits("bezier_y", 0, 500)

            dpg.add_line_series(
                bezier_coords_x,
                bezier_coords_y,
                parent="bezier_y",
                label="Bezier",
                tag="bezier_curve",
            )
            dpg.add_scatter_series(
                ctrl_points_x,
                ctrl_points_y,
                parent="bezier_y",
                label="Bezier Control Points",
                tag="bezier points",
            )
            dpg.add_line_series(
                ctrl_points_x, ctrl_points_y, parent="bezier_y", tag="bezier polygon"
            )

            dpg.bind_item_theme("bezier_curve", "bezier_theme")
            dpg.bind_item_theme("bezier points", "bezier_theme")

        self.annotate_plot(self.ctrl_points)

    def toggle_coords(self, sender, app_data):
        self.showcoords_flag = app_data
        # If "Show Coordinates" is unchecked, hide the annotations
        if app_data is False:
            if dpg.does_alias_exist("annotation_0"):
                for i in range(self.n_ctrl_points):
                    dpg.hide_item(f"annotation_{i}")
        else:
            if dpg.does_alias_exist("annotation_0"):
                for i in range(self.n_ctrl_points):
                    dpg.show_item(f"annotation_{i}")
            else:
                self.annotate_plot(self.ctrl_points)

