import threading

import wikipedia
import webbrowser
from kivy.core.clipboard import Clipboard

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.stacklayout import MDStackLayout
from kivy.core.window import Window
from kivymd.uix.list import OneLineListItem
from kivy.properties import ListProperty, StringProperty, ObjectProperty
import requests
from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineIconListItem, MDList
from kivymd.theming import ThemableBehavior

Window.keyboard_anim_args = {'d': .2, 't': 'in_out_expo'}
Window.softinput_mode = "below_target"

#Abre el Navegador predeterminado con la pagina Google.
class func():
    def open():
        webbrowser.open('google.com')

class UI(ScreenManager):
    pass

# Para añadir elementos de arriba a abajo.
class ContentNavigationDrawer(MDStackLayout):
    pass

class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()
    text_color = ListProperty((0,0,0,1))

class DrawerList(ThemableBehavior, MDList):
    def set_color_item(self, instance_item):
        '''Called when tap on a menu item.'''

        # Set the color of the icon and text for the menu item.
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color

class MainApp(MDApp):
    #Iconos y demases
    def on_start(self):
        icons_item = {
            "folder": "Mis Datos",
            "account-multiple": "Telecomunicaciones",
            "star": "Marcadores",
            "history": "Reciente",
            "checkbox-marked": "Informacion",
            "upload": "Subir",
        }
        for icon_name in icons_item.keys():
            self.root.ids.content_drawer.ids.md_list.add_widget(
                ItemDrawer(icon=icon_name, text=icons_item[icon_name])
            ) 
            
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Pink" 
        Builder.load_file('./KVStyle/estilo.kv')
        
        return UI()
    
    #Attempt at a repository part.
    url = ""
        
    def search(self, text):
        t1 = threading.Thread(target=self.get_wiki, args=(text,))
        t1.start()

    def get_wiki(self, text):
        self.root.ids.rc_spin.active = True
        self.root.ids.summary.text = ""
        self.root.ids.title.text = ""
        self.root.ids.error.text = ""

        wikipedia.set_lang("es")
        try:
            summary = wikipedia.page(text.strip())
            self.root.ids.title.text = summary.title
            self.root.ids.summary.text = f"\n{summary.summary}"
        except Exception as e:
            print(e)
            self.root.ids.summary.text = (
                "Disculpa, no se pudo encontrar " + self.root.ids.fld.text + " en la Wiki, prueba algo más específico"
            )
        self.root.ids.rc_spin.active = False
        
    #End of Attempt
    
    
        
if __name__=="__main__":
    MainApp().run()