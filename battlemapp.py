# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 20:40:07 2020

@author: Volkan
"""

import kivy
from kivy.app import App
from kivy.uix.image import Image
from kivy.graphics import Color, Line
from kivy.uix.behaviors import DragBehavior
from kivy.uix.widget import Widget
from kivy.properties import StringProperty


class DraggableImage(DragBehavior, Image):
    pass


class FullView(Widget):
    active_vid_name = StringProperty()

    def playbtn(self):
        if self.ids.v1_1.state == "stop":
            self.ids.v1_1.state = "play"
        elif self.ids.v1_1.state == "play":
            self.ids.v1_1.state = "stop"

    def tokenbtn(self):
        tmp_str = "".join(self.ids.file_list.selection)
        tmp_x = self.ids.map_tokens_layout.x
        tmp_y = self.ids.map_tokens_layout.y
        tmp_w = self.ids.map_tokens_layout.width
        tmp_h = self.ids.map_tokens_layout.height
        tmp_token = DraggableImage(source=tmp_str,
                                   keep_ratio=True,
                                   drag_rectangle=(tmp_x, tmp_y, tmp_w, tmp_h),
                                   drag_timeout=100000000000,
                                   drag_distance=0)
        self.ids.token_area.add_widget(tmp_token)

    def mapbtn(self):
        if self.ids.v1_1.state == "play":
            self.ids.v1_1.state = "stop"
            self.ids.v1_1.unload()
        self.active_vid_name = "".join(self.ids.file_list.selection)

    def drawgrid(self):
        self.ids.grid_overlay.canvas.clear()
        self.ids.grid_overlay.canvas.add(Color(1.0, 1.0, 1.0))
        h = 0
        w = 0
        grid_dist = self.ids.grid_size_slider.value
        map_area = self.ids.map_area
        while h+grid_dist < map_area.height:
            h = h+grid_dist
            tmp_line = Line(points=[map_area.x, map_area.y+h, map_area.x + map_area.width, map_area.y+h])
            self.ids.grid_overlay.canvas.add(tmp_line)
        while w+grid_dist < map_area.width:
            w = w+grid_dist
            tmp_line = Line(points=[map_area.x+w, map_area.y, map_area.x+w, map_area.y+map_area.height])
            self.ids.grid_overlay.canvas.add(tmp_line)

class MyApp(App):
    def build(self):
        self.layout = FullView()
        return self.layout


if __name__ == "__main__":
    MyApp().run()
