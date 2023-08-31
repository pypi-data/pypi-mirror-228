from typing import Tuple, Union

import numpy as np
from shapely.geometry import Point
from shapely.affinity import affine_transform
import pygame
from pygame.colordict import THECOLORS

from .sensor_base import SensorBase
from tactics2d.map.element import Map
from tactics2d.participant.element import Vehicle, Cyclist, Pedestrian


LANE_COLOR = {
    "default": THECOLORS["darkgray"],
    "road": THECOLORS["darkgray"],
    "highway": THECOLORS["dimgray"],
    "play_street": THECOLORS["slategray"],
    "emergency_lane": THECOLORS["red4"],
    "bus_lane": THECOLORS["dodgerblue4"],
    "bicycle_lane": THECOLORS["darkgreen"],
    "exit": THECOLORS["palegreen4"],
    "walkway": THECOLORS["azure3"],
    "shared_walkway": THECOLORS["darkgray"],
    "crosswalk": THECOLORS["silver"],
    "stairs": THECOLORS["lightslategray"],
}


AREA_COLOR = {
    "default": THECOLORS["slategray"],
    "hole": THECOLORS["white"],
    "parking": THECOLORS["darkgray"],
    "freespace": THECOLORS["slategray"],
    "vegetation": THECOLORS["forestgreen"],
    "keepout": THECOLORS["red2"],
    "building": THECOLORS["steelblue1"],
    "traffic_island": THECOLORS["silver"],
    "obstacle": THECOLORS["gray"],
}


ROADLINE_COLOR = {"default": THECOLORS["white"]}


VEHICLE_COLOR = {"default": THECOLORS["turquoise1"]}


CYCLIST_COLOR = {"default": THECOLORS["cyan1"]}


PEDESTRIAN_COLOR = {"default": THECOLORS["lightpink1"]}


class TopDownCamera(SensorBase):
    """This class implements a pseudo camera with top-down view RGB semantic segmentation image.

    Attributes:
        id_ (int): The unique identifier of the sensor.
        map_ (Map): The map that the sensor is attached to.
        perception_range (Union[float, tuple]): The distance from the sensor to its maximum detection range in
            (left, right, front, back). When this value is undefined, the camera is assumed to
            detect the whole map. Defaults to None.
        window_size (Tuple[int, int]): The size of the rendering window. Defaults to (200, 200).
        off_screen (bool): Whether to render the sensor off screen. Defaults to True.
    """

    def __init__(
        self,
        id_: int,
        map_: Map,
        perception_range: Union[float, Tuple[float]] = None,
        window_size: Tuple[int, int] = (200, 200),
        off_screen: bool = True,
    ):
        super().__init__(id_, map_, perception_range, window_size, off_screen)

        self.position = None
        self.heading = None

    def _update_transform_matrix(self):
        if None in [self.position, self.heading]:
            if not hasattr(self, "transform_matrix"):
                x_center = 0.5 * (self.map_.boundary[0] + self.map_.boundary[1])
                y_center = 0.5 * (self.map_.boundary[2] + self.map_.boundary[3])

                self.transform_matrix = np.array(
                    [
                        self.scale,
                        0,
                        0,
                        -self.scale,
                        0.5 * self.window_size[0] - self.scale * x_center,
                        0.5 * self.window_size[1] + self.scale * y_center,
                    ]
                )
        else:
            theta = self.heading - np.pi / 2

            self.transform_matrix = self.scale * np.array(
                [
                    np.cos(theta),
                    np.sin(theta),
                    np.sin(theta),
                    -np.cos(theta),
                    self.perception_range[0]
                    - self.position.x * np.cos(theta)
                    - self.position.y * np.sin(theta),
                    self.perception_range[2]
                    - self.position.x * np.sin(theta)
                    + self.position.y * np.cos(theta),
                ]
            )

    def _in_perception_range(self, geometry) -> bool:
        return geometry.distance(self.position) > self.max_perception_distance * 2

    def _render_areas(self):
        for area in self.map_.areas.values():
            if self.position is not None:
                if self._in_perception_range(area.geometry):
                    continue

            color = (
                AREA_COLOR[area.subtype]
                if area.subtype in AREA_COLOR
                else AREA_COLOR["default"]
            )
            color = color if area.color is None else area.color
            polygon = affine_transform(area.geometry, self.transform_matrix)
            outer_points = list(polygon.exterior.coords)
            inner_list = list(polygon.interiors)

            pygame.draw.polygon(self.surface, color, outer_points)
            for inner_points in inner_list:
                pygame.draw.polygon(self.surface, AREA_COLOR["hole"], inner_points)

    def _render_lanes(self):
        for lane in self.map_.lanes.values():
            if self.position is not None:
                if self._in_perception_range(lane.geometry):
                    continue

            color = (
                LANE_COLOR[lane.subtype]
                if lane.subtype in LANE_COLOR
                else LANE_COLOR["default"]
            )
            color = color if lane.color is None else lane.color
            points = list(affine_transform(lane.geometry, self.transform_matrix).coords)

            pygame.draw.polygon(self.surface, color, points)

    def _render_roadlines(self):
        for roadline in self.map_.roadlines.values():
            if self.position is not None:
                if self._in_perception_range(roadline.linestring):
                    continue

            color = (
                ROADLINE_COLOR[roadline.color]
                if roadline.subtype in ROADLINE_COLOR
                else ROADLINE_COLOR["default"]
            )
            color = color if roadline.color is None else roadline.color
            points = list(
                affine_transform(roadline.linestring, self.transform_matrix).coords
            )

            if roadline.type_ == "line_thick":
                width = max(2, 0.2 * self.scale)
            else:
                width = max(1, 0.1 * self.scale)

            pygame.draw.aalines(self.surface, color, False, points, width)

    def _render_vehicle(self, vehicle: Vehicle, frame: int = None):
        color = VEHICLE_COLOR["default"] if vehicle.color is None else vehicle.color
        points = np.array(
            affine_transform(vehicle.get_pose(frame), self.transform_matrix).coords
        )
        triangle = [
            (points[0] + points[1]) / 2,
            (points[1] + points[2]) / 2,
            (points[3] + points[0]) / 2,
        ]

        pygame.draw.polygon(self.surface, color, points)
        pygame.draw.polygon(self.surface, (0, 0, 0), triangle, width=1)

    def _render_cyclist(self, cyclist: Cyclist, frame: int = None):
        color = CYCLIST_COLOR["default"] if cyclist.color is None else cyclist.color
        points = list(
            affine_transform(cyclist.get_pose(frame), self.transform_matrix).coords
        )

        pygame.draw.polygon(self.surface, color, points)

    def _render_pedestrian(self, pedestrian: Pedestrian, frame: int = None):
        color = (
            PEDESTRIAN_COLOR["default"] if pedestrian.color is None else pedestrian.color
        )
        point = affine_transform(
            Point(pedestrian.trajectory.get_state(frame).location), self.transform_matrix
        )
        radius = max(1, 0.5 * self.scale)

        pygame.draw.circle(self.surface, color, point, radius)

    def _render_participants(
        self, participants: dict, participant_ids: list, frame: int = None
    ):
        for participant_id in participant_ids:
            participant = participants[participant_id]

            state = participant.trajectory.get_state(frame)
            if self.position is not None:
                if self._in_perception_range(Point(state.location)):
                    continue

            if isinstance(participant, Vehicle):
                self._render_vehicle(participant, frame)
            elif isinstance(participant, Pedestrian):
                self._render_pedestrian(participant, frame)
            elif isinstance(participant, Cyclist):
                self._render_cyclist(participant, frame)

    def update(
        self,
        participants,
        participant_ids: list,
        frame: int = None,
        position: Point = None,
        heading: float = None,
    ):
        """_summary_

        Args:
            participants (_type_): _description_
            participant_ids (list): _description_
            frame (int, optional): _description_. Defaults to None.
            position (Point, optional): _description_. Defaults to None.
            heading (float, optional): _description_. Defaults to None.
        """
        self.position = position
        self.heading = heading
        self._update_transform_matrix()

        self.surface.fill(THECOLORS["white"])
        self._render_areas()
        self._render_lanes()
        self._render_roadlines()
        self._render_participants(participants, participant_ids, frame)

    def get_observation(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return pygame.surfarray.array3d(self.surface)
