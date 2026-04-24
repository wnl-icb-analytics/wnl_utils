# Expected tests for coordinate plotting helper
#
# - test_plot_static_coordinates_runs_with_default_style:
#   Verify function runs with default pointstyle and returns axes.
#
# - test_plot_static_coordinates_all_supported_styles_run:
#   Parametrize styles (white, black, red, triangle, diamond, plus) and assert no error.
#
# - test_plot_static_coordinates_with_labels_requires_label_column:
#   Assert ValueError when labels=True and label_column is not provided.
#
# - test_plot_static_coordinates_with_labels_runs_when_column_present:
#   Provide label column and verify annotation mode executes.
#
# - test_plot_static_coordinates_uses_current_canvas_when_ax_missing:
#   Ensure function uses internal current canvas if ax is omitted.

