# Expected tests for choropleth plotting helpers
#
# - test_plot_static_continuous_choropleth_runs_with_defaults:
#   Verify function runs on a tiny GeoDataFrame and returns axes.
#
# - test_plot_static_continuous_choropleth_respects_vmin_vmax:
#   Pass explicit vmin/vmax and verify function accepts them without error.
#
# - test_plot_static_continuous_choropleth_reverse_mode_runs:
#   Verify reverse=True path executes successfully.
#
# - test_plot_static_categorical_choropleth_runs_with_categories:
#   Verify categorical plotting executes with supplied category order.
#
# - test_plot_static_categorical_choropleth_reverse_mode_runs:
#   Verify reverse=True path executes successfully for categorical mode.
#
# - test_choropleth_functions_use_current_canvas_when_fig_ax_missing:
#   Ensure both functions use internal current canvas by default.

