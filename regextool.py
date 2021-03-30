import re
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from os import system #For printing debugging.

Builder.load_string("""

<RegexApp>:
    PatternInput:
        id:pattern
        pos_hint: {'x':0,'top':1}
        size_hint:0.3,0.05


    RegexLabel:
        canvas.before:
            Color:
                rgba:1,0,0,1
            Line:
                width: 3
                rectangle: self.x, self.y, self.width, self.height
        markup:True
        pos_hint: {'x':0.3,'top':0.95}
        size_hint: 0.68,None
        text_size:self.width,None
        height: self.texture_size[1]

""")



class RegexApp(FloatLayout):
    pass


class PatternInput(TextInput):
    def __init__(self, **kwargs):
        super(PatternInput, self).__init__(**kwargs)

        self.bind(text=self.update_regex)

    def update_regex(self,instance,pattern):
        regexlabel=self.parent.children[0]
        try:
            if pattern=='':
                regexlabel.output=regexlabel.source_text
                regexlabel.refresh_display(regexlabel.source_text)

            elif pattern != '' and pattern[-1]!='\\' and pattern not in [r'\b']:
                output=regexlabel.highlight_matches(pattern,regexlabel.source_text)
                regexlabel.refresh_display(output)

            elif pattern[-1]=='\\' or pattern in [r'\b']:
                pass
        except:
            pass




class RegexLabel(Label):
    def __init__(self, **kwargs):
        super(RegexLabel, self).__init__(**kwargs)
        #Original text split into lines. This is so only lines shown are loaded
        #into the label text instead of the full document.
        self.source_text=''

        #Load text from file.
        self.load_text()

        #Set range of lines to be displayed.
        self.first=0
        self.last=50


        self.refresh_display(self.source_text)
        self.output=self.source_text


    #Calls Scrolls on scroll up or down.
    def on_touch_down(self, touch):
        if touch.button in ['scrollup','scrolldown']:
            self.scroll(touch.button)

    #Changes the range depending on the scroll and refreshes display.
    def scroll(self,direction):

        max=len(self.text)


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

        self.refresh_display(self.output)


    #Load text from file.
    def load_text(self,filepath='testfile.txt'):
        with open(filepath,'r') as f:
            self.source_text=f.read()


    #Loads the display.
    def refresh_display(self,text):
        text=text.splitlines()
        self.text='\n'.join(text[self.first:self.last])
        # system('cls')
        # print('\n'.join(self.text.splitlines()[self.first:self.last]))



    #Upgraded re.findall function that will be used on highlight_matches function.
    def find_all(self,pattern,text):
        '''This function acts like re.findall, but returns the spans in addition to the matched strings.'''

        #Variable where the matches and spans are stored.
        matches=[]

        #Variable to resume re.search after first match.
        span_start=0

        #While the position is located before the end of the string.
        while span_start<len(text)-1:

            match=re.search(pattern,text[span_start:])

            #If there are no more matches in the current text, then stop seaerching.
            if match==None:
                break

            #Add match with its span to the result.
            matches+=[[match.group(),match.span()[0]+span_start,match.span()[1]+span_start]]
            span_start=match.span()[1]+span_start

        return matches

    #Requires a whole string. Not lines list.
    def highlight_matches(self,pattern,text):

        #The way the function is made now, it requires for all the text to be joined in one large string.
        matches=self.find_all(pattern,text)

        output=list(text)

        #When a item is inserted in the list, the spans coordinates get shifted. Count variable accounts for this.
        count=0

        for match in matches:
            output.insert(match[1]+count,'[color=ff6600]')
            count+=1
            output.insert(match[2]+count,'[/color]')
            count+=1

        output=''.join(output)

        self.output=output
        return output





if __name__ == '__main__':
    from kivy.app import App

    class test(App):
        def build(self):
            return RegexApp()

    test().run()
