import re
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

Builder.load_string("""

<RegexApp>:
    TextInput:
        id:pattern
        pos_hint: {'x':0,'top':1}
        size_hint:0.3,0.05

    ScrollView:
        pos_hint: {'x':0.3,'top':1}
        size_hint:0.7,1
        canvas.before:
            Color:
                rgba:1,0,0,1
            Line:
                width: 3
                rectangle: self.x, self.y, self.width, self.height
        Label:
            id: target
            markup:True
            pos_hint: {'x':0.20,'top':0.95}
            size_hint: 1,None
            text_size:self.width,None
            height: self.texture_size[1]

""")


class RegexApp(FloatLayout):


    def __init__(self, **kwargs):
        super(RegexApp, self).__init__(**kwargs)
        #The text, split in lines.
        self.textlist=''

        #Load text from file.
        self.load_text()

        #Set range of lines to be displayed.
        self.first=0
        self.last=50

        #Display the rows in the range.
        self.refresh_display()


        self.highlight_matches(r'\b2\d{3}\b')

    #Calls Scrolls on scroll up or down.
    def on_touch_down(self, touch):
        if touch.button in ['scrollup','scrolldown']:
            self.scroll(touch.button)

    #Changes the range depending on the scroll and refreshes display.
    def scroll(self,direction):

        max=len(self.textlist)


        if direction=='scrolldown':

            if self.first>0:
                self.first-=10
                self.last-=10
                #print(self.first,self.last)

        if direction=='scrollup':

            if self.last<max+25:
                self.first+=10
                self.last+=10
                #print(self.first,self.last)

        self.refresh_display()


    #Load text from file.
    def load_text(self,filepath='testfile.txt'):
        with open(filepath,'r') as f:
            #self.ids.target.text=f.read()
            self.textlist=f.readlines()
            print(len(self.textlist))


    #Loads the display.
    def refresh_display(self):
        self.ids.target.text=''.join(self.textlist[self.first:self.last+1])


    def highlight_matches(self,regex_pattern):
        text=''.join(self.textlist)
        matches=re.findall(regex_pattern,text)
        print(matches)

        for number,line in enumerate(self.textlist):
            for match in matches:
                if match in line:
                    self.textlist[number].replace(match,f'[color=ff6600]{match}[/color=ff6600]')
                    print('match highlighted')


        self.refresh_display()





if __name__ == '__main__':
    from kivy.app import App

    class test(App):
        def build(self):
            return RegexApp()

    test().run()
