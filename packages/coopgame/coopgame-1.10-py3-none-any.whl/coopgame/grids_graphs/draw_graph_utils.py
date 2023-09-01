from coopgame.colors import Color
import pygame
from coopgraph.graphs import Graph, Edge
from coopstructs.geometry.vectors.vectorN import Vector2
from coopstructs.geometry import Rectangle
import coopgame.pygamehelpers as help
from typing import Callable, Tuple, Dict, Iterable
from coopstructs.geometry.curves.curves import LineCurve, Curve
from cooptools.coopEnum import Directionality
from dataclasses import dataclass, asdict
import numpy as np
from coopgame.pointdrawing import point_draw_utils as putils
from coopgame.label_drawing import label_drawing_utils as lutils
from coopgame.linedrawing import line_draw_utils as nutils
from coopstructs.geometry.lines import Line
import cooptools.matrixManipulation as mm
import cooptools.geometry_utils.vector_utils as vec

@dataclass(frozen=True)
class GraphDrawArgs:
    coordinate_converter: Callable[[Vector2], Vector2] = None,
    node_draw_args: putils.DrawPointArgs = None
    enabled_edge_args: nutils.DrawLineArgs = None
    disabled_edge_args: nutils.DrawLineArgs = None
    node_label_args: lutils.DrawLabelArgs = None
    articulation_points_args: putils.DrawPointArgs = None
    source_node_args: putils.DrawPointArgs = None
    sink_node_args: putils.DrawPointArgs = None
    orphan_node_args: putils.DrawPointArgs = None

    def with_(self, **kwargs):
        definition = self.__dict__
        for kwarg, val in kwargs.items():
            definition[kwarg] = val

        return type(self)(**definition)

    def converted_coordinate(self, coord: Tuple[float, float]):
        if self.coordinate_converter is None:
            return coord

        else:
            return self.coordinate_converter(Vector2.from_tuple(coord)).as_tuple()

    @classmethod
    def from_(cls, args, **kwargs):
        kw = asdict(args)
        kw.update(kwargs)
        return GraphDrawArgs(**kw)

    @property
    def EdgesBaseArgs(self):
        return GraphDrawArgs(
            coordinate_converter=self.coordinate_converter,
            enabled_edge_args=self.enabled_edge_args.BaseArgs,
            disabled_edge_args=self.disabled_edge_args.BaseArgs
        )

    @property
    def EdgesLabelArgs(self):
        return GraphDrawArgs(
            coordinate_converter=self.coordinate_converter,
            enabled_edge_args=self.enabled_edge_args.LabelArgs,
            disabled_edge_args=self.disabled_edge_args.LabelArgs
        )

    @property
    def NodesBaseArgs(self):
        return GraphDrawArgs(
            coordinate_converter=self.coordinate_converter,
            node_draw_args=self.node_draw_args
        )

    @property
    def NodesLabelArgs(self):
        return GraphDrawArgs(
            coordinate_converter=self.coordinate_converter,
            node_label_args=self.node_label_args
        )

    @property
    def OverlayArgs(self):
        return GraphDrawArgs(
            coordinate_converter=self.coordinate_converter,
            articulation_points_args=self.articulation_points_args,
            source_node_args=self.source_node_args,
            sink_node_args=self.sink_node_args,
            orphan_node_args=self.orphan_node_args
        )

def draw_to_surface(surface: pygame.Surface ,
                    graph: Graph,
                    args: GraphDrawArgs,
                    vec_transformer: vec.VecTransformer = None):
    if graph is None:
        return

    if args.enabled_edge_args or args.disabled_edge_args:
        _draw_edges(
            surface=surface,
            edge_draw_args={
                e: args.enabled_edge_args if e.enabled() else args.disabled_edge_args for e in graph.edges
            },
            vec_transformer=vec_transformer
        )

    if args.node_draw_args or args.node_label_args:
        draw_graph_nodes(surface,
                         graph=graph,
                         node_draw_args=args.node_draw_args,
                         coordinate_converter=args.coordinate_converter,
                         vec_transformer=vec_transformer,
                         draw_label_args=args.node_label_args)

    if args.articulation_points_args:
        putils.draw_points(
            points={args.converted_coordinate(x.pos): args.articulation_points_args for x in graph.AP()},
            surface=surface,
            vec_transformer_getter=vec_transformer
        )

    if args.source_node_args:
        putils.draw_points(
            points={args.converted_coordinate(x.pos): args.source_node_args for x in graph.Sources},
            surface=surface,
            vec_transformer_getter=vec_transformer
        )

    if args.sink_node_args:
        putils.draw_points(
            points={args.converted_coordinate(x.pos): args.sink_node_args for x in graph.Sinks},
            surface=surface,
            vec_transformer_getter=vec_transformer
        )

    if args.orphan_node_args:
        putils.draw_points(
            points={args.converted_coordinate(x.pos): args.orphan_node_args for x in graph.Orphans},
            surface=surface,
            vec_transformer_getter=vec_transformer
        )
def _draw_edges(
    surface: pygame.Surface,
    edge_draw_args: Dict[Edge, nutils.DrawLineArgs],
    vec_transformer: vec.VecTransformer = None
):
    line_args = {Line(Vector2.from_tuple(k.start.pos),
                      Vector2.from_tuple(k.end.pos)): v.with_(label_text=str(k))
                 for k, v in edge_draw_args.items() if k.start.pos != k.end.pos}

    nutils.draw_lines(lines=line_args,
                      surface=surface,
                      vec_transformer_getter=vec_transformer
                      )

def draw_graph_nodes(surface: pygame.Surface,
                     graph: Graph,
                     coordinate_converter: Callable[[Vector2], Vector2] = None,
                     node_draw_args: putils.DrawPointArgs = None,
                     draw_label_args: lutils.DrawLabelArgs = None,
                     vec_transformer: vec.VecTransformer = None):
    if not coordinate_converter:
        coordinate_converter = lambda x: x

    txt_dict = {}
    for node in graph.nodes:
        converted_point = coordinate_converter(Vector2.from_tuple(node.pos)).as_tuple()
        if node_draw_args:
            putils.draw_points({converted_point: node_draw_args},
                               surface=surface,
                               vec_transformer_getter=vec_transformer)


        if vec_transformer is None:
            scaled = converted_point
        else:
            scaled = vec_transformer([converted_point])[0]

        txt_dict.setdefault(scaled, []).append(node.name)


    if draw_label_args:
        for pos, labels in txt_dict.items():
            lutils.draw_label(
                hud=surface,
                text=",".join(labels),
                args=draw_label_args,
                pos=pos
            )


def draw_articulation_points(surface: pygame.Surface,
                             graph: Graph,
                             color: Color = None,
                             vec_transformer: vec.VecTransformer = None
                             ):
    if graph is None:
        return

    articulation_points = graph.AP()

    if color is None:
        color = Color.ORANGE

    scaled_pos = vec_transformer([node.pos for node in articulation_points.keys()])

    for point in scaled_pos:
        pygame.draw.circle(surface, color.value, (int(point[0]), int(point[1])), 10, 1)

def draw_directionality_indicators(curves: Dict[Curve, Directionality],
                                    surface: pygame.Surface,
                                    indicator_color: Color,
                                    num_arrows: int = 5,
                                    size: float = 1,
                                    indicator_points_color: Color | Tuple[Color, ...]=None,
                                   vec_transformer: vec.VecTransformer = None):
    arrow_ts = [1.0 / (num_arrows - 1) * x for x in range(0, num_arrows)] if num_arrows > 1 else [0.5]


    for curve, direction in curves.items():
        for t in arrow_ts:
            centre = curve.point_at_t(t)

            try:
                # get derivative of curve for drawing
                derivative = curve.derivative_at_t(t)
                d_unit = derivative.unit()
            except:
                # most likely a vertical curve (no derivative), handle by pointing up or down.
                d_unit = (curve.EndPoint - curve.origin).unit()

            if d_unit is None or d_unit.y == 0:
                continue

            d_foreward = d_unit.scaled_to_length(size)
            d_ort_1 = Vector2(1, - d_unit.x / d_unit.y).scaled_to_length(size / 2)
            # d_ort_2 = d_ort_1 * -1

            a = b = c = d = e = f = None
            if direction in [Directionality.FOREWARD, Directionality.BIDIRECTIONAL]:
                a = centre
                b = centre - d_foreward + d_ort_1
                c = centre - d_foreward - d_ort_1

                scaled_polygon_points = [a.as_tuple(), b.as_tuple(), c.as_tuple()]
                if vec_transformer is not None:
                    scaled_polygon_points = vec_transformer(scaled_polygon_points)

                help.draw_polygon(surface, scaled_polygon_points, color=indicator_color)

            if direction in [Directionality.BACKWARD, Directionality.BIDIRECTIONAL]:
                d = centre
                e = centre + d_foreward + d_ort_1
                f = centre + d_foreward - d_ort_1

                scaled_polygon_points = [d.as_tuple(), e.as_tuple(), f.as_tuple()]
                if vec_transformer is not None:
                    scaled_polygon_points = vec_transformer(scaled_polygon_points)

                help.draw_polygon(surface, scaled_polygon_points, color=indicator_color)

            ip_color_getter = lambda ii: indicator_points_color[ii % len(indicator_points_color)] \
                if type(indicator_points_color) == tuple \
                else indicator_points_color

            if indicator_points_color:
                points = [a, b, c, d, e, f]
                putils.draw_points(
                    points={
                        x.as_tuple(): putils.DrawPointArgs(
                            color=ip_color_getter,
                            outline_color=None,
                            radius=2
                        ) for ii, x in enumerate(points)
                    },
                    surface=surface,
                    vec_transformer_getter=vec_transformer
                )