from math import sqrt
from difflib import SequenceMatcher

import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Ellipse, Line
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.popup import Popup

WIDTH, HEIGHT = Window.size

d = 0
l_s = 299792458
t = 3600*24
F = 0
AU = 149.6e6*1000
G = 6.67428e-11
K = 100/AU

colors = {
        'red': ('червоний', (100, 0, 0)),
        'pink': ('рожевий', (255, 192, 203)),
        'pink': ('світло-червоний', (255, 192, 203)),
        'dark red': ('темно-червоний', (139, 0, 0)),
        'dark red': ('бордовий', (139, 0, 0)),
        'orange': ('оранжевий', (255, 165, 0)),
        'orange': ('помаранчевий', (255, 165, 0)),
        'dark orange': ('темно-оранжевий', (255, 140, 0)),
        'yellow': ('жовтий', (255, 255, 0)),
        'light yellow': ('світло-жовтий', (255, 250, 205)),
        'gold': ('золотий', (255, 215, 0)),
        'green': ('зелений', (0, 128, 0)),
        'light green': ('світло-зелений', (0, 255, 0)),
        'light green': ('салатовий', (0, 255, 0)),
        'dark green': ('темно-зелений', (0, 100, 0)),
        'blue': ('синій', (0, 0, 255)),
        'light blue': ('блакитний', (0, 255, 255)),
        'dark blue': ('темно-синій', (0, 0, 128)),
        'purple': ('фіолетовий', (128, 0, 128)),
        'light purple': ('світло-фіолетовий', (255, 0, 255)),
        'dark purple': ('темно-фіолетовий', (75, 0, 130)),
        'white': ('білий', (255, 255, 255)),
        'gray': ('сірий', (128, 128, 128)),
        'silver': ('срібний', (192, 192, 192)),
        'black': ('чорний', (0, 0, 0))
    }

number_planets = 0
planets = []

draw_orbits = False
draw_names = False

class Planet(Widget):
    def __init__(self, **kwargs):
        super(Planet, self).__init__(**kwargs)
        self.plnts = []
        self.orbits = []
        with self.canvas:
            for i in range(number_planets):
                self.Color_change_planet(i)
                r = planets[i][2]
                x = planets[i][3][0]
                x = x*K + WIDTH/2 - r
                y = planets[i][3][1]
                y = y*K + HEIGHT/2 - r

                self.line = Line(points = (), width = 2)
                self.orbits.append(self.line)
                
                self.circle = Ellipse(pos = (x, y), size = (r*2, r*2))
                self.plnts.append(self.circle)

        Clock.schedule_interval(self.update, 1. / 30.)

    def Color_change_planet(self, i):
        with self.canvas:
            RC = {'Col': '', 'percent': 0}
            col = planets[i][6]
            for I1,I2 in colors.items():
                color = I2[0]
                m = SequenceMatcher(None, col, color)
                vrt = m.ratio()
                if vrt > RC['percent']:
                    RC['Col'] = I2[1]
                    RC['percent'] = vrt
                if vrt == 0:
                    RC['Col'] = (255, 255, 255)
                    RC['percent'] = vrt
            Col = RC['Col']
            Color(rgba = (Col[0]/255, Col[1]/255, Col[2]/255, 1))

    def Color_change_orbit(self, i):
        with self.canvas:
            RC = {'Col': '', 'percent': 0}
            col = planets[i][6]
            for I1,I2 in colors.items():
                color = I2[0]
                m = SequenceMatcher(None, col, color)
                vrt = m.ratio()
                if vrt > RC['percent']:
                    RC['Col'] = I2[1]
                    RC['percent'] = vrt
                if vrt == 0:
                    RC['Col'] = (255, 255, 255)
                    RC['percent'] = vrt
            Col = RC['Col']
            Color(rgba = (Col[0]/255, Col[1]/255, Col[2]/255, .5))
            
    def update(self, *args):
        global d
        d += 1
        global planets
        for i in range(number_planets):
            x, y = self.simulation(i)
            self.plnts[i].pos = x, y
            if draw_orbits == True:
                if self.orbits[i] in self.canvas.children:
                    with self.canvas:
                        self.Color_change_orbit(i)
                        self.orbits[i].points += [x+planets[i][2], y+planets[i][2]]
                else:
                    with self.canvas:
                        self.Color_change_orbit(i)
                        self.line = Line(points = (), width = 2)
                        self.orbits[i] = self.line
            else:
                try:
                    self.canvas.children.remove(self.orbits[i])
                except:
                    with self.canvas:
                        self.Color_change_orbit(i)
                        self.line = Line(points = (), width = 2)
                        self.orbits[i] = self.line

    def simulation(self, i):
        global planets
        r = planets[i][2]
            
        x = planets[i][3][0]
        y = planets[i][3][1]

        vx = planets[i][4]
        vy = planets[i][5]

        m = planets[i][1]

        Fx = 0
        Fy = 0
            
        if number_planets != 1:
            for N in range(number_planets):
                if N != i:
                    x2 = planets[N][3][0]
                    y2 = planets[N][3][1]

                    s2 = sqrt((x2-x)**2 + (y2-y)**2)

                    F2 = (G*m*planets[N][1])/(s2**2)

                    cos_a = abs(x2-x) / sqrt((x2-x)**2 + (y2-y)**2)
                    sin_a = abs(y2-y) / sqrt((x2-x)**2 + (y2-y)**2)

                    if x2 > x:
                        Fx += F2*cos_a
                    elif x2 < x:
                        Fx -= F2*cos_a

                    if y2 > y:
                        Fy += F2*sin_a
                    elif y2 < y:
                        Fy -= F2*sin_a
        try:            
            ax = Fx/m
            ay = Fy/m

            vx += ax*t
            sx = vx*t

            vy += ay*t
            sy = vy*t
                
            x += sx
            cur_x = x*K + WIDTH/2 - r
            y += sy
            cur_y = y*K + HEIGHT/2 - r

            x = (cur_x + r - WIDTH/2)/K
            y = (cur_y + r - HEIGHT/2)/K
                
            coor = []
            coor.append(x)
            coor.append(y)
            planets[i][3] = coor

            try:
                current_coor = []
                current_coor.append(cur_x)
                current_coor.append(cur_y)
                planets[i][7] = current_coor
            except:
                current_coor = []
                current_coor.append(cur_x)
                current_coor.append(cur_y)
                planets[i].append(current_coor)

            planets[i][4] = vx
            planets[i][5] = vy
            
        except:
            vx += l_s
            sx = vx*t

            vy += l_s
            sy = vy*t
                
            x += sx
            cur_x = x*K + WIDTH/2 - r
            y += sy
            cur_y = y*K + HEIGHT/2 - r

            x = (cur_x + r - WIDTH/2)/K
            y = (cur_y + r - HEIGHT/2)/K
                
            coor = []
            coor.append(x)
            coor.append(y)
            planets[i][3] = coor

            try:
                current_coor = []
                current_coor.append(cur_x)
                current_coor.append(cur_y)
                planets[i][7] = current_coor
            except:
                current_coor = []
                current_coor.append(cur_x)
                current_coor.append(cur_y)
                planets[i].append(current_coor)

        return cur_x, cur_y

class MainApp(App):
    def build(self):
        self.title = "Симулятор планет"
        self.f = FloatLayout(size_hint = (1, 1))

        self.label = Label(text = 'Симулятор планет',
                      font_size = 50,
                      color = [0, 191/255, 1],
                      pos = (0,100))
        self.f.add_widget(self.label)
        
        self.entry = TextInput(hint_text = 'Введіть кількість планет',
                          size_hint = (.5, .12),
                          pos = (WIDTH/2 - WIDTH/2/2, HEIGHT/2 - HEIGHT*0.15+15))
        self.f.add_widget(self.entry)
        
        self.button = Button(text = 'Ввести',
                        on_press = self.get_text,
                        background_color = [1,1,1,1],
                        font_size = 30,
                        size_hint = (.25, .1),
                        pos = (WIDTH/2, HEIGHT/2 - HEIGHT*0.15-100))
        self.f.add_widget(self.button)
        
        self.ex_button = Button(text = 'Вийти',
                        on_press = self.EXIT,
                        background_color = [1,1,1,1],
                        font_size = 30,
                        size_hint = (.25, .1),
                        pos = (WIDTH/2 - WIDTH*0.25, HEIGHT/2 - HEIGHT*0.15-100))
        self.f.add_widget(self.ex_button)

        self.s_v = ScrollView(size_hint = (1, None), size = (WIDTH, HEIGHT))
        self.s_v.add_widget(self.f)

        return self.s_v
        
    def get_text(self, t):
        global number_planets
        try:
            number_planets += int(self.entry.text)
            self.s_v.remove_widget(self.f)
            self.SecondApp()
        except:
            popup = Popup(title="Увага!", content = Label(text='Ви не вказали кількість планет!'), size_hint=(.5, .5))
            popup.open()

        
    def SecondApp(self):
        self.ENTRYLIST = []
        g_main = GridLayout(cols = 1, spacing = 10, size_hint_y = None)
        g_main.bind(minimum_height = g_main.setter('height'))
        global number_planets
        for i in range(number_planets):
            entries = []
            
            number_planet = i + 1

            f = FloatLayout(size_hint = (1, None), height = HEIGHT)
            g = GridLayout(cols = 2, rows = 4, padding = [15, HEIGHT/2-50, 15, 20],pos = (0, 200 + HEIGHT*(number_planets-number_planet)))

            self.label = Label(text = f'Планета № {number_planet}',
                          font_size = 50,
                          color = [0, 191/255, 1],
                          pos = (0, 300 + HEIGHT*(number_planets-number_planet)))
            f.add_widget(self.label)
            
            self.entry1 = TextInput(hint_text = f"Назва планети № {number_planet}",
                              font_size = 25,
                              size_hint = (.5, .15),
                              pos = (WIDTH/2 - WIDTH/2/2 - WIDTH/2/2/2, HEIGHT/2 + HEIGHT*(number_planets-number_planet)))
            g.add_widget(self.entry1)
            entries.append(self.entry1)

            self.entry2 = TextInput(hint_text = f"Маса пленети в кг",
                              font_size = 25,
                              size_hint = (.5, .15),
                              pos = (WIDTH/2 - WIDTH/2/2 - WIDTH/2/2/2, HEIGHT/2 - HEIGHT*0.15 + HEIGHT*(number_planets-number_planet)))
            g.add_widget(self.entry2)
            entries.append(self.entry2)

            self.entry3 = TextInput(hint_text = f"Радіус пленети (найкращий для відображення діапазон: 5-70)",
                              font_size = 25,
                              size_hint = (.5, .15),
                              pos = (WIDTH/2 - WIDTH/2/2 - WIDTH/2/2/2, HEIGHT/2 - HEIGHT*0.3 + HEIGHT*(number_planets-number_planet)))
            g.add_widget(self.entry3)
            entries.append(self.entry3)

            self.entry4 = TextInput(hint_text = f"Колір планети",
                              font_size = 25,
                              size_hint = (.5, .15),
                              pos = (WIDTH/2 - WIDTH/2/2 - WIDTH/2/2/2, HEIGHT/2 - HEIGHT*0.45 + HEIGHT*(number_planets-number_planet)))
            g.add_widget(self.entry4)
            entries.append(self.entry4)

            self.entry5 = TextInput(hint_text = f"Початкова координата x (за одиницю відстані взято 1 а.о. ≈ 149,6 млн. км)",
                              font_size = 25,
                              size_hint = (.5, .15),
                              pos = (WIDTH/2 - WIDTH/2/2 + WIDTH/2/2/2, HEIGHT/2 + HEIGHT*(number_planets-number_planet)))
            g.add_widget(self.entry5)
            entries.append(self.entry5)

            self.entry6 = TextInput(hint_text = f"Початкова координата y (за одиницю відстані взято 1 а.о. ≈ 149,6 млн. км)",
                              font_size = 25,
                              size_hint = (.5, .15),
                              pos = (WIDTH/2 - WIDTH/2/2 + WIDTH/2/2/2, HEIGHT/2 - HEIGHT*0.15 + HEIGHT*(number_planets-number_planet)))
            g.add_widget(self.entry6)
            entries.append(self.entry6)

            self.entry7 = TextInput(hint_text = f"Початкова швидкість по осі x планети в м\с",
                              font_size = 25,
                              size_hint = (.5, .15),
                              pos = (WIDTH/2 - WIDTH/2/2 + WIDTH/2/2/2, HEIGHT/2 - HEIGHT*0.3 + HEIGHT*(number_planets-number_planet)))
            g.add_widget(self.entry7)
            entries.append(self.entry7)

            self.entry8 = TextInput(hint_text = f"Початкова швидкість по осі y планети в м\с",
                              font_size = 25,
                              size_hint = (.5, .15),
                              pos = (WIDTH/2 - WIDTH/2/2 + WIDTH/2/2/2, HEIGHT/2 - HEIGHT*0.45 + HEIGHT*(number_planets-number_planet)))
            g.add_widget(self.entry8)
            entries.append(self.entry8)

            f.add_widget(g)
            g_main.add_widget(f)
            self.ENTRYLIST.append(entries)

        
        self.button = Button(text = 'Ввести',
                        on_press = self.get_text2,
                        background_color = [1,1,1,1],
                        font_size = 30,
                        size_hint = (.25, .1),
                        pos = (WIDTH/2, HEIGHT/2 - HEIGHT*0.15-250))
        
        self.re_button = Button(text = 'Вийти',
                        on_press = self.EXIT,
                        background_color = [1,1,1,1],
                        font_size = 30,
                        size_hint = (.25, .1),
                        pos = (WIDTH/2 - WIDTH*0.25, HEIGHT/2 - HEIGHT*0.15-250))
        
        f.add_widget(self.button)
        f.add_widget(self.re_button)
        self.s_v.add_widget(g_main)

    
    def get_text2(self, t):
        for entr in self.ENTRYLIST:
            try:
                planet = entr[0].text
                col = entr[3].text
                mas = float(entr[1].text)
                r = int(entr[2].text)
                x = float(entr[4].text)*AU
                y = float(entr[5].text)*AU
                v0x = float(entr[6].text)
                v0y = float(entr[7].text)
                m = []
                coor = []
                m.append(planet)
                m.append(mas)
                m.append(r)
                coor.append(x)
                coor.append(y)
                m.append(coor)
                m.append(v0x)
                m.append(v0y)
                m.append(col)
                planets.append(m)

                if self.ENTRYLIST.index(entr) == len(self.ENTRYLIST)-1:
                    self.s_v.clear_widgets()
                    self.PlanetSimulationApp()
            except:
                popup = Popup(title="Увага!", content = Label(text='Усі характеристики планети, крім назви\nта кольору, повинні бути цифровими\n(радіус повинен бути цілим числом,\nмаса не може дорівнювати нулю)!'), size_hint=(.5, .5))
                popup.open()
        
    def PlanetSimulationApp(self):
        self.COLORS = []
        self.labels = []

        self.f = FloatLayout(size_hint = (1, 1))
        g = GridLayout(cols = 2, rows = 2, size_hint = [.2, .2])
        anch1 = AnchorLayout(anchor_x = 'right', anchor_y = 'top')
        anch2 = AnchorLayout(anchor_x = 'left', anchor_y = 'top')
        anch3 = AnchorLayout(anchor_x = 'right', anchor_y = 'bottom')
        
        self.re_button = Button(text = 'Вийти',
                        on_press = self.EXIT,
                        background_color = [1,1,1,1],
                        font_size = 30,
                        size_hint = (.15, .1))

        self.time_label = Label(text = 'Час:',
                            font_size = 30,
                            color = [0, 191/255, 1],
                            size_hint = [.15, .15])
        self.time_label.pos[0] =+ 20

        global planets
        for i in planets:
            text = i[0]
            col = self.Change_color(planets.index(i))
            self.label = Label(text = i[0],
                            font_size = 20,
                            color = [col[0]/255, col[1]/255, col[2]/255, 1],
                            pos = (planets[planets.index(i)][3][0]*K-WIDTH/2+7, planets[planets.index(i)][3][1]*K-HEIGHT/2))
            self.labels.append(self.label)

            self.f.add_widget(self.label)

        self.label1 = Label(text = 'Орбіти планет',
                        font_size = 16,
                        color = [0, 191/255, 1])
        
        self.label2 = Label(text = 'Назви планет',
                        font_size = 16,
                        color = [0, 191/255, 1])

        check1 = CheckBox(color = [0, 191/255, 1])
        check1.bind(active = self.on_checkbox_active1)
        
        check2 = CheckBox(color = [0, 191/255, 1])
        check2.bind(active = self.on_checkbox_active2)
        
        g.add_widget(check1)
        g.add_widget(self.label1)
        g.add_widget(check2)
        g.add_widget(self.label2)
        anch1.add_widget(g)
        anch2.add_widget(self.time_label)
        anch3.add_widget(self.re_button)
        self.f.add_widget(anch1)
        self.f.add_widget(anch2)
        self.f.add_widget(anch3)
        self.f.add_widget(Planet())

        self.s_v.add_widget(self.f)

        Clock.schedule_interval(self.Show_names_and_time, 1. / 30.)
    
    def Show_names_and_time(self, a):
        global planets
        if draw_names == True:
            for l in self.labels:
                l.pos = (planets[self.labels.index(l)][7][0]-WIDTH/2+planets[self.labels.index(l)][2]*2+7, planets[self.labels.index(l)][7][1]-HEIGHT/2+planets[self.labels.index(l)][2]*2)
                self.hide_widget(l, False)
        else:
            for l in self.labels:
                self.hide_widget(l, True)

        global d
        self.time_label.text = 'Час: ' + str(d) + ' день'
        
        if d == 1000:
            self.time_label.pos[0] += 15
            
    def on_checkbox_active1(self, check1, value1):
        global draw_orbits
        if value1:
            draw_orbits = True
        else:
            draw_orbits = False

    def on_checkbox_active2(self, check2, value2):
        global draw_names
        if value2:
            draw_names = True
        else:
            draw_names = False

    def Change_color(self, i):
        RC = {'Col': '', 'percent': 0}
        col = planets[i][6]
        for I1,I2 in colors.items():
            color = I2[0]
            m = SequenceMatcher(None, col, color)
            vrt = m.ratio()
            if vrt > RC['percent']:
                RC['Col'] = I2[1]
                RC['percent'] = vrt
            if vrt == 0:
                RC['Col'] = (255, 255, 255)
                RC['percent'] = vrt

        c = RC['Col']
        return c
            
    def hide_widget(self, wid, dohide):
        if hasattr(wid, 'saved_attrs'):
            if not dohide:
                wid.height, wid.size_hint_y, wid.opacity, wid.disabled = wid.saved_attrs
                del wid.saved_attrs
        elif dohide:
            wid.saved_attrs = wid.height, wid.size_hint_y, wid.opacity, wid.disabled
            wid.height, wid.size_hint_y, wid.opacity, wid.disabled = 0, None, 0, True

    def empty_entry(self, t):
        t.text = ''

    def EXIT(self, b):
        App.get_running_app().stop()
        Window.close()

    def RESTART(self, b):
        self.s_v.clear_widgets()
        self.stop()
        
        global number_planets
        number_planets = 0
        global planets
        planets = []
        global draw_orbits
        draw_orbits = False
        global draw_names
        draw_names = False

        return MainApp().run()   
        
MainApp().run()
