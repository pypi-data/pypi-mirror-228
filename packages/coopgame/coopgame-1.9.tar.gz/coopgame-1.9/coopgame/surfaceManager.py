import pygame
from typing import Callable, Tuple, Dict
from cooptools.toggles import BooleanToggleable
from typing import List, Any, Callable
from dataclasses import dataclass, field
from cooptools.register import Register
import logging

logger = logging.getLogger(f"coopgame.surfacemanager")

DrawCallback = Callable[[], pygame.Surface]

@dataclass(frozen=True)
class SurfaceRegistryArgs:
    id: str
    callback: DrawCallback
    frame_update: bool = False

@dataclass
class SurfaceRegister:
    registry_args: SurfaceRegistryArgs
    visibility_toggle: BooleanToggleable = field(init=False, default_factory=lambda: BooleanToggleable(default=True))

class SurfaceManager:
    def __init__(self,
                 surface_draw_callbacks: List[SurfaceRegistryArgs] = None):
        self.surface_register: Register = Register[SurfaceRegister]()

        if surface_draw_callbacks:
            self.register_surface_ids(surface_draw_callbacks)

        self.surfaces: Dict[str, pygame.Surface] = {}

    @property
    def RegisteredSurfaceIds(self) -> List[str]:
        return list(self.surface_register.Registry.keys())

    @property
    def FrameUpdateSurfaceIds(self) -> List[str]:
        return [surf.registry_args.id for id, surf in self.surface_register.Registry.items() if surf.registry_args.frame_update]

    def register_surface_ids(self,
                             surface_draw_callbacks: List[SurfaceRegistryArgs]):
        self.surface_register.register(
            to_register=[SurfaceRegister(x) for x in surface_draw_callbacks],
            ids=[x.id for x in surface_draw_callbacks]
        )

    def invalidate(self, ids: List[str] = None):
        self.redraw(ids=ids)

    def redraw(self,
               ids: List[str] = None):
        if ids is None:
            ids = list(self.surface_register.Registry.keys())

        for id in ids:
            logger.debug(f"Drawing surface {id}...")
            self.surfaces[id] = self.surface_register.Registry[id].registry_args.callback()
            logger.debug(f"Surface {id} drawn")

    def update(self):
        self.update_if_visible(self.FrameUpdateSurfaceIds)

    def render(self,
               surface: pygame.Surface,
               at_pos: Tuple[int, int] = None,
               frame_update: bool = False):
        if frame_update:
            self.update()

        if at_pos is None:
            at_pos = (0, 0)

        for id, sr in self.surface_register.Registry.items():
            if sr.visibility_toggle.value:
                surface.blit(self.get_surfaces(ids=[id], dims=surface.get_size())[id], dest=at_pos)

    def get_surfaces(self,
                     ids: List[str],
                     dims: Tuple[int, int],
                     force_update: bool = False) -> Dict[str, pygame.Surface]:
        # update surfaces that dont exist or that dont match dims
        for id in ids:
            if id not in self.surfaces.keys() or \
                self.surfaces[id].get_size() != dims or \
                force_update:
                self.redraw([id])

        # return the surfaces
        return {id: self.surfaces[id] for id in ids}

    def get_toggled_state(self, ids: List[str]) -> Dict[str, bool]:
        return {
            x: self.surface_register.Registry[x].visibility_toggle.value for x in ids
        }

    def toggle_visible(self, ids: List[str]) -> Dict[str, bool]:
        # toggle
        [self.surface_register.Registry[x].visibility_toggle.toggle() for x in ids]

        return self.get_toggled_state(ids)

    def set_visiblility(self, ids: List[str], visible: bool):
        # toggle
        [self.surface_register.Registry[x].visibility_toggle.set_value(visible) for x in ids]
        return self.get_toggled_state(ids)

    def hide_all(self) -> Dict[str, bool]:
        self.set_visiblility(ids=self.RegisteredSurfaceIds, visible=False)
        return self.get_toggled_state(self.RegisteredSurfaceIds)

    def show_all(self) -> Dict[str, bool]:
        self.set_visiblility(ids=self.RegisteredSurfaceIds, visible=True)
        return self.get_toggled_state(self.RegisteredSurfaceIds)

    def update_if_visible(self, ids: List[str]):
        self.redraw([id for id, visible in self.get_toggled_state(ids).items() if visible])

