# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 20:40:07 2020

@author: Volkan
"""

import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.graphics import Color, Line
from kivy.uix.scatter import Scatter
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, BooleanProperty


class FullView(Widget):
    active_vid_name = StringProperty()
    menu_visible = BooleanProperty(True)

    tkn_err_content = BoxLayout(orientation='vertical')
    tkn_err_content.add_widget(Label(text="Please use PNG, JPG or JPEG files for tokens", size_hint=(1, 0.8)))
    tkn_err_button = Button(text='Close', size_hint=(1, 0.2))
    tkn_err_content.add_widget(tkn_err_button)
    tkn_err_popup = Popup(title="Token filetype error",
                          content=tkn_err_content,
                          size_hint=(None, None),
                          size=(400, 400),
                          auto_dismiss=False)
    tkn_err_button.bind(on_press=tkn_err_popup.dismiss)

    def menubtn(self):
        self.menu_visible = not self.menu_visible
        Clock.schedule_once(self.gridcb)

    def playbtn(self):
        if self.ids.v1_1.state == "stop":
            self.ids.v1_1.state = "play"
        elif self.ids.v1_1.state == "play":
            self.ids.v1_1.state = "stop"

    def tokenbtn(self):
        tmp_str = "".join(self.ids.file_list.selection)
        if tmp_str.lower().endswith(('.png', '.jpg', '.jpeg')):
            tmp_img = Image(source=tmp_str)
            tmp_token = Scatter(size_hint=(None, None),
                                size=tmp_img.size,
                                center=self.ids.token_area.center)
            tmp_token.add_widget(tmp_img)
            self.ids.token_area.add_widget(tmp_token)
        else:
            self.tkn_err_popup.open()

    def clearbtn(self):
        self.ids.token_area.clear_widgets()

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

    def gridcb(self, dt):
        self.drawgrid()


class BattlemApp(App):
    def build(self):
        return FullView()


if __name__ == "__main__":
    BattlemApp().run()
