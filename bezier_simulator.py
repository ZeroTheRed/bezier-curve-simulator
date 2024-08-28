import dearpygui.dearpygui as dpg
import bezier as bz


dpg.create_context()


def draw_bezier():
    num_ctrl_points = dpg.get_value("ctrl_pts")
    smoothness = dpg.get_value("smooth")


    bezier_coords, ctrl_points = bz.bezier_curve_points(num_ctrl_points, smoothness)

    bezier_coords_x = [coords[0] for coords in bezier_coords]
    bezier_coords_y = [coords[1] for coords in bezier_coords]

    ctrl_points_x = [coords[0] for coords in ctrl_points]
    ctrl_points_y = [coords[1] for coords in ctrl_points]

    # Colour theme for the curve
    with dpg.theme() as bezier_theme:
        with dpg.theme_component(dpg.mvLineSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line,
                                (255, 115, 0),
                                category=dpg.mvThemeCat_Plots)

        with dpg.theme_component(dpg.mvScatterSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line,
                                (238, 89, 255, 255),
                                category=dpg.mvThemeCat_Plots)
            dpg.add_theme_style(dpg.mvPlotStyleVar_Marker,
                                dpg.mvPlotMarker_Circle,
                                category=dpg.mvThemeCat_Plots)
            dpg.add_theme_style(dpg.mvPlotStyleVar_MarkerSize,
                                4,
                                category=dpg.mvThemeCat_Plots)

    dpg.delete_item("bezier_plot")
    with dpg.plot(label="Bezier Curve", parent="Primary Window", tag="bezier_plot", width=600, height=400):
        dpg.add_plot_axis(dpg.mvXAxis, label="X", tag="bezier_x")
        dpg.add_plot_axis(dpg.mvYAxis, label="Y", tag="bezier_y")
        dpg.set_axis_limits("bezier_x", 0, 500)
        dpg.set_axis_limits("bezier_y", 0, 500)

        dpg.add_line_series(bezier_coords_x, bezier_coords_y, parent="bezier_y", label="Bezier", tag="bezier_curve")
        dpg.add_scatter_series(ctrl_points_x, ctrl_points_y, parent="bezier_y", label="Bezier Control Points", tag="bezier points")
        dpg.add_line_series(ctrl_points_x, ctrl_points_y, parent="bezier_y", tag="bezier polygon")

        # dpg.bind_item_theme("bezier_curve", bezier_theme)
        dpg.bind_item_theme("bezier points", bezier_theme)

        # Create a theme for annotations
        with dpg.theme() as annotation_theme:
            with dpg.theme_component(dpg.mvAnnotation):
                dpg.add_theme_color(dpg.mvPlotCol_Query, (0, 255, 0, 255), category=dpg.mvThemeCat_Plots)
                dpg.add_theme_color(dpg.mvPlotCol_FrameBg, (0, 0, 0, 0), category=dpg.mvThemeCat_Plots)

        # Add annotations for control points
        for i, (x, y) in enumerate(ctrl_points):
            annotation = dpg.add_plot_annotation(
                label=f"P{i}: ({x:.1f}, {y:.1f})",
                default_value=(x, y),
                offset=(10, 10),
                tag=f"annotation_{i}",
                parent="bezier_plot",
                clamped=False
            )
            dpg.bind_item_theme(annotation, annotation_theme)


# Main Window
with dpg.window(tag="Primary Window"):
    dpg.add_input_int(label="Control points", width=100, tag="ctrl_pts")
    dpg.add_input_int(label="Smoothness", width=100, tag="smooth")

    dpg.add_button(label="Generate Curve", callback=draw_bezier)


if __name__ == "__main__":
    dpg.create_viewport(title="Bezier Curve Generator", width=450, height=500)

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("Primary Window", True)
    dpg.start_dearpygui()
    dpg.destroy_context()