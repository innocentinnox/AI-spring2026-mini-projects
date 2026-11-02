"""Export static PNG maps of our Route Planning solutions for the report (Assignment 3, 2b and 3c).

The starter's `visualization.plot_map` draws the Stanford map with Plotly and ends with `fig.show()`
(opens a browser tab). We reuse it unchanged and simply intercept `show()` to grab the figure, then
write it with kaleido to report/figures/03_route/<name>.png.

Run from anywhere:   python scripts/route_figures.py
Requires the cs221 environment (osmium, plotly, kaleido).
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ROUTE_DIR = REPO_ROOT / "assignments" / "03_route"
FIG_DIR = REPO_ROOT / "report" / "figures" / "03_route"

os.chdir(ROUTE_DIR)                 # the starter code opens data/stanford.pbf relatively
sys.path.insert(0, str(ROUTE_DIR))

import plotly.graph_objects as go   # noqa: E402

import submission                   # noqa: E402
import util                         # noqa: E402
from map_util import create_stanford_map, get_total_cost, location_from_tag, make_tag  # noqa: E402
from visualization import plot_map  # noqa: E402

# --- capture instead of opening a browser -------------------------------------------------
_captured: list[go.Figure] = []
go.Figure.show = lambda self, *args, **kwargs: _captured.append(self)  # type: ignore[assignment]


def solve_and_plot(name: str, problem, waypoint_tags, city_map, title: str) -> list[str]:
    """Run UCS on `problem`, print the result and save the map as FIG_DIR/<name>.png."""
    ucs = util.UniformCostSearch(verbose=0)
    ucs.solve(problem)
    path = [problem.start_location] + ucs.actions
    landmarks = [t for loc in path for t in city_map.tags[loc] if t.startswith(("landmark=", "amenity="))]
    print(f"\n[{name}] {title}")
    print(f"  {len(path)} locations, {get_total_cost(path, city_map):.1f} m, "
          f"{ucs.num_states_explored} states explored")
    print(f"  tagged locations on the path: {landmarks}")

    _captured.clear()
    plot_map(city_map, path, list(waypoint_tags), title)
    fig = _captured[-1]
    # plot_map centres the view on the whole map; frame it on the path instead (15 % margin).
    lats = [city_map.geo_locations[loc].latitude for loc in path]
    lons = [city_map.geo_locations[loc].longitude for loc in path]
    pad_lat = max(0.15 * (max(lats) - min(lats)), 0.0015)
    pad_lon = max(0.15 * (max(lons) - min(lons)), 0.0015)
    fig.update_geos(projection_scale=None, center=None,
                    lataxis_range=[min(lats) - pad_lat, max(lats) + pad_lat],
                    lonaxis_range=[min(lons) - pad_lon, max(lons) + pad_lon])
    fig.update_layout(width=1100, height=800, showlegend=False, margin=dict(l=20, r=20, t=60, b=20))
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    out = FIG_DIR / f"{name}.png"
    fig.write_image(str(out), scale=2)
    print(f"  -> {out.relative_to(REPO_ROOT)}")
    return path


def main() -> None:
    city_map = create_stanford_map()

    # 2b (i): our custom problem from submission.py (Gates -> nearest food).
    p = submission.get_stanford_shortest_path_problem()
    solve_and_plot("2b_insight", p, [], city_map, f"2b: {p.start_location} -> {p.end_tag}")

    # 2b (ii): a query whose "shortest" path is not what a person would want.
    # From Hoover Tower to the nearest food (Coupa Cafe at Green Library): the cafe is ~137 m
    # away as the crow flies, but the map's footpaths force a ~447 m walk around the buildings.
    start = location_from_tag(make_tag("landmark", "hoover_tower"), city_map)
    p2 = submission.ShortestPathProblem(start, make_tag("amenity", "food"), city_map)
    solve_and_plot("2b_undesirable", p2, [], city_map, "2b: hoover_tower -> amenity=food")

    # 3c: our custom waypoints problem from submission.py.
    w = submission.get_stanford_waypoints_shortest_path_problem()
    solve_and_plot("3c_waypoints", w, w.waypoint_tags, city_map,
                   f"3c: {w.start_location} via {list(w.waypoint_tags)} -> {w.end_tag}")


if __name__ == "__main__":
    main()
