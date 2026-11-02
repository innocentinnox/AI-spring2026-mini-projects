from typing import List, Tuple

from map_util import (
    CityMap,
    compute_distance,
    create_stanford_map,
    location_from_tag,
    make_tag,
)
from util import Heuristic, SearchProblem, State, UniformCostSearch


# *IMPORTANT* :: A key part of this assignment is figuring out how to model states
# effectively. We've defined a class `State` to help you think through this, with a
# field called `memory`.
#
# As you implement the different types of search problems below, think about what
# `memory` should contain to enable efficient search!
#   > Please read the docstring for `State` in `util.py` for more details and code.
#   > Please read the docstrings for in `map_util.py`, especially for the CityMap class

########################################################################################
# Problem 2a: Modeling the Shortest Path Problem.


class ShortestPathProblem(SearchProblem):
    """
    Defines a search problem that corresponds to finding the shortest path
    from `start_location` to any location with the specified `end_tag`.
    """

    def __init__(self, start_location: str, end_tag: str, city_map: CityMap):
        self.start_location = start_location
        self.end_tag = end_tag
        self.city_map = city_map

    def start_state(self) -> State:
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        # No waypoints to remember here, so the state is just where we are.
        return State(location=self.start_location)
        # END_YOUR_CODE

    def is_end(self, state: State) -> bool:
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        # Any location carrying the end tag is an acceptable destination.
        return self.end_tag in self.city_map.tags[state.location]
        # END_YOUR_CODE

    def action_successors_and_costs(self, state: State) -> List[Tuple[str, State, float]]:
        """
        Note we want to return a list of *3-tuples* of the form:
            (actionToReachSuccessor: str, successorState: State, cost: float)
        Our action space is the set of all named locations, where a named location
        string represents a transition from the current location to that new location.
        """
        # BEGIN_YOUR_CODE (our solution is 7 lines of code, but don't worry if you deviate from this)
        # city_map.distances[loc] maps each neighbouring location to the length of
        # the connection in metres; the action is simply the neighbour's label.
        return [
            (neighbor, State(location=neighbor), distance)
            for neighbor, distance in self.city_map.distances[state.location].items()
        ]
        # END_YOUR_CODE


########################################################################################
# Problem 2b: Custom -- Plan a Route through Stanford


def get_stanford_shortest_path_problem() -> ShortestPathProblem:
    """
    Create your own search problem using the map of Stanford, specifying your own
    `start_location`/`end_tag`. 

    Run `python map_util.py > readableStanfordMap.txt` to dump a file with a list of
    locations and associated tags; you might find it useful to search for the following
    tag keys (amongst others):
        - `landmark=` - Hand-defined landmarks (from `data/stanford-landmarks.json`)
        - `amenity=`  - Various amenity types (e.g., "parking_entrance", "food")
        - `parking=`  - Assorted parking options (e.g., "underground")
    """
    city_map = create_stanford_map()

    # BEGIN_YOUR_CODE (our solution is 2 lines of code, but don't worry if you deviate from this)
    # "I am at the Gates building and hungry: where is the nearest place with food?"
    # Several landmarks carry amenity=food, so the search picks the closest one.
    start_location = location_from_tag(make_tag("landmark", "gates"), city_map)
    end_tag = make_tag("amenity", "food")
    # END_YOUR_CODE
    return ShortestPathProblem(start_location, end_tag, city_map)


########################################################################################
# Problem 3a: Modeling the Waypoints Shortest Path Problem.


class WaypointsShortestPathProblem(SearchProblem):
    """
    Defines a search problem that corresponds to finding the shortest path from
    `start_location` to any location with the specified `end_tag` such that the path also
    traverses locations that cover the set of tags in `waypoint_tags`. Note that tags 
    from the `start_location` count towards covering the set of tags.

    Hint: naively, your `memory` representation could be a list of all locations visited.
    However, that would be too large of a state space to search over! Think 
    carefully about what `memory` should represent.
    """
    def __init__(
        self, start_location: str, waypoint_tags: List[str], end_tag: str, city_map: CityMap
    ):
        self.start_location = start_location
        self.end_tag = end_tag
        self.city_map = city_map

        # We want waypoint_tags to be consistent/canonical (sorted) and hashable (tuple)
        self.waypoint_tags = tuple(sorted(waypoint_tags))

    # State design: `memory` is the sorted tuple of waypoint tags covered so far.
    # Which locations were visited, and in which order, is irrelevant to the
    # future, so the state space is only (#locations) x 2^(#waypoints) instead of
    # growing with the length of the path.

    def _waypoints_at(self, location: str) -> frozenset:
        """The subset of the waypoint tags that `location` carries."""
        return frozenset(self.waypoint_tags).intersection(self.city_map.tags[location])

    def start_state(self) -> State:
        # BEGIN_YOUR_CODE (our solution is 6 lines of code, but don't worry if you deviate from this)
        # Tags at the start location already count as covered.
        covered = tuple(sorted(self._waypoints_at(self.start_location)))
        return State(location=self.start_location, memory=covered)
        # END_YOUR_CODE

    def is_end(self, state: State) -> bool:
        # BEGIN_YOUR_CODE (our solution is 5 lines of code, but don't worry if you deviate from this)
        # Done when we stand on an end-tag location AND every waypoint is covered
        # (both tuples are sorted, so equality is a set comparison).
        return (self.end_tag in self.city_map.tags[state.location]
                and state.memory == self.waypoint_tags)
        # END_YOUR_CODE

    def action_successors_and_costs(self, state: State) -> List[Tuple[str, State, float]]:
        # BEGIN_YOUR_CODE (our solution is 17 lines of code, but don't worry if you deviate from this)
        covered = set(state.memory)
        successors = []
        for neighbor, distance in self.city_map.distances[state.location].items():
            # Moving to `neighbor` additionally covers whatever waypoint tags it has.
            new_covered = tuple(sorted(covered | self._waypoints_at(neighbor)))
            successors.append((neighbor, State(location=neighbor, memory=new_covered), distance))
        return successors
        # END_YOUR_CODE


########################################################################################
# Problem 3c: Custom -- Plan a Route with Unordered Waypoints through Stanford


def get_stanford_waypoints_shortest_path_problem() -> WaypointsShortestPathProblem:
    """
    Create your own search problem with waypoints using the map of Stanford, 
    specifying your own `start_location`/`waypoint_tags`/`end_tag`.

    Similar to Problem 2b, use `readableStanfordMap.txt` to identify potential
    locations and tags.
    """
    city_map = create_stanford_map()
    # BEGIN_YOUR_CODE (our solution is 4 lines of code, but don't worry if you deviate from this)
    # An end-of-day errand run: leave the Rains dorm, grab food somewhere, buy
    # notebooks at the bookstore and return a book to Green Library (in any
    # order), then end the day at the Gates building.
    start_location = location_from_tag(make_tag("landmark", "rains"), city_map)
    waypoint_tags = [
        make_tag("amenity", "food"),
        make_tag("landmark", "bookstore"),
        make_tag("landmark", "green_library"),
    ]
    end_tag = make_tag("landmark", "gates")
    # END_YOUR_CODE
    return WaypointsShortestPathProblem(start_location, waypoint_tags, end_tag, city_map)


########################################################################################
# Problem 4a: A* to UCS reduction

# Turn an existing SearchProblem (`problem`) you are trying to solve with a
# Heuristic (`heuristic`) into a new SearchProblem (`newSearchProblem`), such
# that running uniform cost search on `newSearchProblem` is equivalent to
# running A* on `problem` subject to `heuristic`.
#
# This process of translating a model of a problem + extra constraints into a
# new instance of the same problem is called a reduction; it's a powerful tool
# for writing down "new" models in a language we're already familiar with.
# See util.py for the class definitions and methods of Heuristic and SearchProblem.


def a_star_reduction(problem: SearchProblem, heuristic: Heuristic) -> SearchProblem:
    class NewSearchProblem(SearchProblem):
        # A* = UCS on the same graph with the reduced cost
        #     cost'(s, a) = cost(s, a) + h(Succ(s, a)) - h(s).
        # Along any path the h terms telescope to h(end) - h(start), a constant,
        # so the cheapest path is unchanged while UCS is steered towards states
        # with small h. States and goals are exactly those of the original problem.

        def start_state(self) -> State:
            # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
            return problem.start_state()
            # END_YOUR_CODE

        def is_end(self, state: State) -> bool:
            # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
            return problem.is_end(state)
            # END_YOUR_CODE

        def action_successors_and_costs(self, state: State) -> List[Tuple[str, State, float]]:
            # BEGIN_YOUR_CODE (our solution is 8 lines of code, but don't worry if you deviate from this)
            h_here = heuristic.evaluate(state)
            return [
                (action, successor, cost + heuristic.evaluate(successor) - h_here)
                for action, successor, cost in problem.action_successors_and_costs(state)
            ]
            # END_YOUR_CODE

    return NewSearchProblem()


########################################################################################
# Problem 4b: "straight-line" heuristic for A*


class StraightLineHeuristic(Heuristic):
    """
    Estimate the cost between locations as the straight-line distance.
        > Hint: you might consider using `compute_distance` defined in `map_util.py`
    """
    def __init__(self, end_tag: str, city_map: CityMap):
        self.end_tag = end_tag
        self.city_map = city_map

        # Precompute
        # BEGIN_YOUR_CODE (our solution is 5 lines of code, but don't worry if you deviate from this)
        # Collect the coordinates of every possible destination once, so that
        # evaluating the heuristic is just a min over a short list.
        self.end_geo_locations = [
            city_map.geo_locations[location]
            for location, tags in city_map.tags.items()
            if end_tag in tags
        ]
        # END_YOUR_CODE

    def evaluate(self, state: State) -> float:
        # BEGIN_YOUR_CODE (our solution is 6 lines of code, but don't worry if you deviate from this)
        # Straight-line (great-circle) distance to the nearest end location. It
        # never exceeds the walking distance, so the heuristic is admissible, and
        # it is consistent because straight-line distance obeys the triangle
        # inequality.
        current = self.city_map.geo_locations[state.location]
        if not self.end_geo_locations:
            return 0.0
        return min(compute_distance(current, end) for end in self.end_geo_locations)
        # END_YOUR_CODE


########################################################################################
# Problem 4c: "no waypoints" heuristic for A*


class NoWaypointsHeuristic(Heuristic):
    """
    Returns the minimum distance from `start_location` to any location with `end_tag`,
    ignoring all waypoints.
    """
    def __init__(self, end_tag: str, city_map: CityMap):
        """
        Precompute cost of shortest path from each location to a location with the desired end_tag
        """
        # Define a reversed shortest path problem from a special END state
        # (which connects via 0 cost to all end locations) to `start_location`.
        # Solving this reversed shortest path problem will give us our heuristic,
        # as it estimates the minimal cost of reaching an end state from each state
        class ReverseShortestPathProblem(SearchProblem):
            def start_state(self) -> State:
                """
                Return special "END" state
                """
                # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
                return State(location=END)
                # END_YOUR_CODE

            def is_end(self, state: State) -> bool:
                """
                Return False for each state.
                Because there is *not* a valid end state (`is_end` always returns False),
                UCS will exhaustively compute costs to *all* other states.
                """
                # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
                return False
                # END_YOUR_CODE

            def action_successors_and_costs(
                self, state: State
            ) -> List[Tuple[str, State, float]]:
                # If current location is the special "END" state,
                # return all the locations with the desired end_tag and cost 0
                # (i.e, we connect the special location "END" with cost 0 to all locations with end_tag)
                # Else, return all the successors of current location and their corresponding distances according to the city_map
                # BEGIN_YOUR_CODE (our solution is 14 lines of code, but don't worry if you deviate from this)
                if state.location == END:
                    return [
                        (location, State(location=location), 0.0)
                        for location, tags in city_map.tags.items()
                        if end_tag in tags
                    ]
                return [
                    (neighbor, State(location=neighbor), distance)
                    for neighbor, distance in city_map.distances[state.location].items()
                ]
                # END_YOUR_CODE

        # Call UCS.solve on our `ReverseShortestPathProblem` instance. Because there is
        # *not* a valid end state (`is_end` always returns False), will exhaustively
        # compute costs to *all* other states.

        # BEGIN_YOUR_CODE (our solution is 2 lines of code, but don't worry if you deviate from this)
        # A label that cannot clash with a real location (real labels are OSM ids
        # or "x,y" grid labels).
        END = "__END__"
        ucs = UniformCostSearch(verbose=0)
        ucs.solve(ReverseShortestPathProblem())
        # END_YOUR_CODE

        # Now that we've exhaustively computed costs from any valid "end" location
        # (any location with `end_tag`), we can retrieve `ucs.past_costs`; this stores
        # the minimum cost path to each state in our state space.
        #   > Note that we're making a critical assumption here: costs are symmetric!

        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        # past_costs[location] = exact shortest walking distance from `location`
        # to the nearest end-tag location (distances are symmetric).
        self.past_costs = ucs.past_costs
        # END_YOUR_CODE

    def evaluate(self, state: State) -> float:
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        # Waypoints are ignored, so this is a lower bound on the remaining cost;
        # a location that cannot reach any end location gets an infinite estimate.
        return self.past_costs.get(state.location, float("inf"))
        # END_YOUR_CODE
