import cherrypy
import datetime
import sqlite3
import os.path

DATABASE_FILENAME = 'test.db'

# sitewide template page
class Page:
    title = 'tbd page'
    action = 'tbd action'
    
    def datetoday(self):
      return str(datetime.datetime.now()).split()[0]
    
    # html header, for convenience
    def header(self):
        return '''
            <html>
            <head>
                <title>%s</title>
            <head>
            <body>
            <h2>%s</h2>
        ''' % (self.title, self.title)
    
    # html footer, for convenience
    def footer(self):
        return '''
            </body>
            </html>
        '''
    
    # data entry form, presents differently based on process step
    # but tuples constructed and sent to the DB are all of the same format
    # milling does not get assigned a batch
    def primaryForm(self, action):
      
      # assign throughput info based on process step
      if action == "submitRoast":
        lbsInfo = '''
          Total pounds in:
          <input type="number" name="lbsIn" min="0" value="0" />
          <br> '''
      elif action == "submitWinnow":
        lbsInfo = '''
          Total pounds out:
          <input type="number" name="lbsOut" min="0" value="0" />
          <br> '''
      else:
        lbsInfo = '''
          Total pounds in:
          <input type="number" name="lbsIn" min="0" value="0" />
          <br>
          Total pounds out:
          <input type="number" name="lbsOut" min="0" value="0" />
          <br> '''     
      
      # milling isn't associated with a batch
      if action == "submitMill":
        batchString = ''
      else:
        batchString = '''
          Batch number:
          <input type="number" name="batch" required />
          <br> '''
      
      # construct and return the form
      return ('''
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
          <br> ''' + \
          # add relevant throughput and batch fields
          lbsInfo + batchString + '''
          comment:
          <input type="text" name="comment" value="no comment" required />
          <input type="submit" />
          </form>
        ''') % ( action, self.datetoday() )
    
    # adds form info to the database file
    def databaseSubmission(self, tuple):
        conn = sqlite3.connect(DATABASE_FILENAME)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Production VALUES
            (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', tuple)
        conn.commit()
        conn.close()
    
    # displays for the user their input after form submission
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
        <p> %s </p>
        <p><a href="/"> Return to the main page </a></p> 
      ''' % tuple

# homepage with links to data submitting and report generating pages
class StartPage(Page):
    title = 'Theo Production Tracking'
    
    # initialize mapping StartPage methods to their respective page classes
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

# data submission for destoning
class Destone(Page):
    title = 'Destoning Data'

    def index(self):
        return self.header() + self.primaryForm('submitDestone') + self.footer()
    index.exposed = True
    
    def submitDestone(self, employee = None, date = None, labor = None, origin = None,
                     lbsIn = None, lbsOut = None, batch=None, comment=None):
        
        infoTuple = ('Destone', date, origin, employee, labor, lbsIn, lbsOut, batch, comment)
        # add info to database
        self.databaseSubmission( infoTuple )

        # display info for user
        return self.header() + self.displayInput( infoTuple ) + self.footer()
    submitDestone.exposed = True
    
# data submission for roasting
class Roast(Page):
    title = 'Roasting Data'
    
    def index(self):
        return self.header() + self.primaryForm('submitRoast') + self.footer()
    index.exposed = True
    
    def submitRoast(self, employee = None, date = None, labor = None, origin = None,
                     lbsIn = None, lbsOut = "N/A", batch=None, comment=None):
        
        infoTuple = ('Roast', date, origin, employee, labor, lbsIn, lbsOut, batch, comment)
        # add info to database
        self.databaseSubmission( infoTuple )

        # display info for user
        return self.header() + self.displayInput( infoTuple ) + self.footer()
    submitRoast.exposed = True

# data submission for winnowing
class Winnow(Page):
    title = 'Winnowing Data'
    
    def index(self):
        return self.header() + self.primaryForm('submitWinnow') + self.footer()
    index.exposed = True
    
    def submitWinnow(self, employee = None, date = None, labor = None, origin = None,
                     lbsIn = "N/A", lbsOut = None, batch=None, comment=None):
        
        infoTuple = ('Winnow', date, origin, employee, labor, lbsIn, lbsOut, batch, comment)
        # add info to database
        self.databaseSubmission( infoTuple )

        # display info for user
        return self.header() + self.displayInput( infoTuple ) + self.footer()
    submitWinnow.exposed = True

# data submission for milling
class Mill(Page):
    title = 'Milling Data'
    
    def index(self):
        return self.header() + self.primaryForm('submitMill') + self.footer()
    index.exposed = True
    
    def submitMill(self, employee = None, date = None, labor = None, origin = None,
                     lbsIn = None, lbsOut = None, batch="N/A", comment=None):
        
        infoTuple = ('Mill', date, origin, employee, labor, lbsIn, lbsOut, batch, comment)
        # add info to database
        self.databaseSubmission( infoTuple )

        # display info for user
        return self.header() + self.displayInput( infoTuple ) + self.footer()
    submitMill.exposed = True
  
# report generating page, reports can be generated by date or batch number
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
        <p> or </p>
        <form action="displayDateReport" method="GET">
          Date:
          <input type="text" name="date" value="%s" />
          <input type="submit" />
        </form>
        ''' % self.datetoday() + self.footer()
    index.exposed = True
    
    def displayBatchReport(self, batch = None):
      conn = sqlite3.connect(DATABASE_FILENAME)
      cursor = conn.cursor()
      cursor.execute('''
        SELECT * FROM Production WHERE batch=?
        ''', [batch])
      displayString = ''
      
      items = cursor.fetchall()
      for item in items:
        line = '<p>%s: %s IN/OUT: %s / %s LABOR: %s %s    %s   %s</p>' \
          % (item[0], item[2], item[5], item[6], item[4], item[3], item[1], item[8])
        displayString = displayString + line
      conn.close()
      return self.header() + '''
        <p>Here lies batch number %s:</p>
        ''' % batch + displayString + self.footer()
    displayBatchReport.exposed = True
    
    def displayDateReport(self, date = None):
      conn = sqlite3.connect(DATABASE_FILENAME)
      cursor = conn.cursor()
      cursor.execute('''
        SELECT * FROM Production WHERE date=?
        ''', [date])
      displayString = ''
      "blah blah blah blah blah"
      items = cursor.fetchall()
      for item in items:
        line = '<p>%s: %s BATCH: %s IN/OUT: %s / %s LABOR: %s %s    %s   %s</p>' \
          % (item[0], item[2], item[7], item[5], item[6], item[4], item[3], item[1], item[8])
        displayString = displayString + line
      conn.close()
      return self.header() + '''
        <p>Here's everything done on %s:</p>
        ''' % date + displayString + self.footer()
    displayDateReport.exposed = True

pageconfig = os.path.join(os.path.dirname(__file__), 'DataEntry.conf')

# set root page for cherrypy
root = StartPage()

# launch cherrpy with 'root' and 'pageconfig' 
if __name__ == '__main__':
    cherrypy.quickstart(root, config=pageconfig)