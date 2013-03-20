import cherrypy
import datetime
import sqlite3

conn = sqlite3.connect('test.db')
c = conn.cursor()

c.execute('SELECT names FROM Employee')

employees = c.fetchall

class Page:
    title = 'Untitled Page'
    
    def header(self):
        return '''
            <html>
            <head>
                <title>%s</title>
            <head>
            <body>
            <h2>%s</h2>
        ''' % (self.title, self.title)
        
    def footer(self):
        return '''
            </body>
            </html>
        '''

class StartPage(Page):
    title = 'Theo Production Tracking'
    
    def __init__(self):
        self.destone = Destone()
        self.roast = Roast()
        self.winnow = Winnow()
        self.mill = Mill()
        self.refine = Refine()
    
    def index(self):
        return self.header() + '''
            <p> Select a production step to input data: </p>
            <ul>
                <li><a href="./destone/">Destone</a></li>
                <li><a href="./roast/">Roast</a></li>
                <li><a href="./winnow/">Winnow</a></li>
                <li><a href="./mill/">Mill</a></li>
                <li><a href="./refine/">Refine</a></li>
            </ul>
        ''' + self.footer()
    index.exposed = True
    
class Destone(Page):
    title = 'Destoning Data'

    def index(self):
        return self.header() + '''
            <p> Input destoning data: </p>
            <form action="submitDestone" method="GET">
                Employee name: 
                <input type="text" name="employee" required />
                <br>
                Date: 
                <input type="text" name="date" value="%s" required />
                <br>
                Labor in minutes: 
                <input type="number" name="labor" min="5" max="1000" required />
                <br>
                Origin: 
                <input type="text" name="origin" required />
                <br>
                Total pounds in:
                <input type="number" name="lbsIn" min="100" required />
                <br>
                Total pounds out:
                <input type="number" name="lbsOut" min="100" required />
                <br>
                <input type="submit" />
        ''' % str(datetime.datetime.now()).split()[0] + self.footer()
    index.exposed = True
    
    def submitDestone(self, employee = None, date = None, labor = None, origin = None,
                     lbsIn = None, lbsOut = None):
#         c.execute('''
#             INSERT INTO Destone(
#                 ''')
        return self.header() + '''
            <p> The following was submitted </p>
            <p> Employee: %s </p>
            <p> Date: %s </p>
            <p> Labor (in minutes): %s </p>
            <p> Origin: %s </p>
            <p> Lbs In: %s </p>
            <p> Lbs Out: %s </p>
            <br>
            <p><a href="./"> Return to the main page </a></p>
        ''' % (employee, date, labor, origin, lbsIn, lbsOut) + self.footer()
    submitDestone.exposed = True
    
class Roast(Page):
    title = 'Roasting Data'
    
    def index(self):
        return self.header() + '''
            <p> roasting fields here </p>
        ''' + self.footer()
    index.exposed = True

class Winnow(Page):
    title = 'Winnowing Data'
    
    def index(self):
        return self.header() + '''
            <p> winnowing fields here </p>
        ''' + self.footer()
    index.exposed = True

class Mill(Page):
    title = 'Milling Data'
    
    def index(self):
        return self.header() + '''
            <p> milling fields here </p>
        ''' + self.footer()
    index.exposed = True

class Refine(Page):
    title = 'Refining Data'
    
    def index(self):
        return self.header() + '''
            <p> refining fields here </p>
        ''' + self.footer()
    index.exposed = True

root = StartPage()

import os.path
pageconfig = os.path.join(os.path.dirname(__file__), 'ts.conf')

if __name__ == '__main__':
    cherrypy.quickstart(root, config=pageconfig)