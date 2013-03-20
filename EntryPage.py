import cherrypy
import datetime
import sqlite3

class Page:
    title = 'tbd page'
    action = 'tbd action'
    
    def datetoday(self):
      return str(datetime.datetime.now()).split()[0]
    
    def header(self):
        return '''
            <html>
            <head>
                <title>%s</title>
            <head>
            <body>
            <h2>%s</h2>
        ''' % (self.title, self.title)
        
    def primaryForm(self, action):
      conn = sqlite3.connect('test.db')
      cursor = conn.cursor()
      cursor.execute('SELECT max(batch) FROM Production')
      currentBatch = cursor.fetchone()
      conn.close()
      return '''
        <form action="%s" method="GET">
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
          <input type="number" name="lbsIn" min="0" value="0" />
          <br>
          Total pounds out:
          <input type="number" name="lbsOut" min="0" value="0" />
          <br>
          Batch number:
          <input type="number" name="batch" value="%s" required />
          <br> 
          <input type="submit" />
          </form>
        ''' % ( action, self.datetoday(), currentBatch[0] )
    
    def databaseSubmission(self, tuple):
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Production VALUES
            (?, ?, ?, ?, ?, ?, ?, ?)
                ''', tuple)
        conn.commit()
        conn.close()
        
    def displayInput(self, tuple):
      return '''
        <p> The following was submitted for %s: </p>
        <p> Date: %s </p>
        <p> Origin: %s </p>
        <p> Employee: %s </p>
        <p> Labor (in minutes): %s </p>
        <p> Lbs In: %s </p>
        <p> Lbs Out: %s </p>
        <p> Batch number: %s </p>
        <p><a href="/"> Return to the main page </a></p> 
      ''' % tuple
    
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
        self.report = Report()
    
    def index(self):
        return self.header() + '''
            <p> Select a production step to input data: </p>
            <ul>
                <li><a href="./destone/">Destone</a></li>
                <li><a href="./roast/">Roast</a></li>
                <li><a href="./winnow/">Winnow</a></li>
                <li><a href="./mill/">Mill</a></li>
            </ul>
            <p><a href="./report/">Or generate a production report</a></p>

        ''' + self.footer()
    index.exposed = True
    
class Destone(Page):
    title = 'Destoning Data'

    def index(self):
        return self.header() + self.primaryForm('submitDestone') + self.footer()
    index.exposed = True
    
    def submitDestone(self, employee = None, date = None, labor = None, origin = None,
                     lbsIn = None, lbsOut = None, batch=None):
        
        infoTuple = ('Destone', date, origin, employee, labor, lbsIn, lbsOut, batch)
        # add info to database
        self.databaseSubmission( infoTuple )

        # display info for user
        return self.header() + self.displayInput( infoTuple ) + self.footer()
    submitDestone.exposed = True
    
class Roast(Page):
    title = 'Roasting Data'
    
    def index(self):
        return self.header() + self.primaryForm('submitRoast') + self.footer()
    index.exposed = True
    
    def submitRoast(self, employee = None, date = None, labor = None, origin = None,
                     lbsIn = None, lbsOut = None, batch=None):
        
        infoTuple = ('Roast', date, origin, employee, labor, lbsIn, lbsOut, batch)
        # add info to database
        self.databaseSubmission( infoTuple )

        # display info for user
        return self.header() + self.displayInput( infoTuple ) + self.footer()
    submitRoast.exposed = True

class Winnow(Page):
    title = 'Winnowing Data'
    
    def index(self):
        return self.header() + self.primaryForm('submitWinnow') + self.footer()
    index.exposed = True
    
    def submitWinnow(self, employee = None, date = None, labor = None, origin = None,
                     lbsIn = None, lbsOut = None, batch=None):
        
        infoTuple = ('Winnow', date, origin, employee, labor, lbsIn, lbsOut, batch)
        # add info to database
        self.databaseSubmission( infoTuple )

        # display info for user
        return self.header() + self.displayInput( infoTuple ) + self.footer()
    submitWinnow.exposed = True

class Mill(Page):
    title = 'Milling Data'
    
    def index(self):
        return self.header() + self.primaryForm('submitMill') + self.footer()
    index.exposed = True
    
    def submitMill(self, employee = None, date = None, labor = None, origin = None,
                     lbsIn = None, lbsOut = None, batch=None):
        
        infoTuple = ('Mill', date, origin, employee, labor, lbsIn, lbsOut, batch)
        # add info to database
        self.databaseSubmission( infoTuple )

        # display info for user
        return self.header() + self.displayInput( infoTuple ) + self.footer()
    submitMill.exposed = True
    
class Report(Page):
    title = 'Production report generator'
    
    def index(self):
      return self.header() + '''
        <p>Generate a report by:</p>
        <form action="displayBatchReport" method="GET">
          Batch number:
          <input type="number" name="batch" />
          <input type="submit" />
        </form>
        <form action="displayDateReport" method="GET">
          Date:
          <input type="text" name="date" value="%s" />
          <input type="submit" />
        </form>
        ''' % self.datetoday() + self.footer()
    index.exposed = True
    
    def displayBatchReport(self, batch = None):
      conn = sqlite3.connect('test.db')
      cursor = conn.cursor()
      cursor.execute('''
        SELECT * FROM Production WHERE batch=?
        ''', [batch])
      displayString = ''
      
      items = cursor.fetchall()
      for item in items:
        line = '<p>%s: %s IN/OUT: %s / %s LABOR: %s %s    %s</p>' \
          % (item[0], item[2], item[5], item[6], item[4], item[3], item[1])
        displayString = displayString + line
      conn.close()
      return self.header() + '''
        <p>Here lies batch number %s:</p>
        ''' % batch + displayString + self.footer()
    displayBatchReport.exposed = True
    
    def displayDateReport(self, date = None):
      conn = sqlite3.connect('test.db')
      cursor = conn.cursor()
      cursor.execute('''
        SELECT * FROM Production WHERE date=?
        ''', [date])
      displayString = ''
      
      items = cursor.fetchall()
      for item in items:
        line = '<p>%s: %s IN/OUT: %s / %s LABOR: %s %s    %s</p>' \
          % (item[0], item[2], item[5], item[6], item[4], item[3], item[1])
        displayString = displayString + line
      conn.close()
      return self.header() + '''
        <p>Here's everything done on %s:</p>
        ''' % date + displayString + self.footer()
    displayDateReport.exposed = True
    
    
root = StartPage()

import os.path
pageconfig = os.path.join(os.path.dirname(__file__), 'DataEntry.conf')

if __name__ == '__main__':
    cherrypy.quickstart(root, config=pageconfig)