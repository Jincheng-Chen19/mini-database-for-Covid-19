# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 16:31:17 2020

@author: lenovo
"""
# import the psycopg2 database adapter for PostgreSQL
import psycopg2 as psy
from psycopg2 import connect, sql
# for the sys.exit() method call
import sys
# import the Pygame libraries
import pygame
from pygame.locals import *
#import matplotlib
import matplotlib.pyplot as plt
# import pandas
import pandas as pd

# set the DB name, table, and table data to 'None'
db_name = "Covid_19" #need to modify based on the name of your database
Date = None
Country = None
Province = None
Rank = None
# initialize the output with None
result_return = None
op = True

# setting for postgreSQL
#change these globals (user name and user password) to match your settings
user_name = "postgres" #the username for accessing your postgreSQL
user_pass = "SqL75944153" #the password for accessing your postgreSQL

# create a class for the buttons and labels
class Button():

    # empty list for button registry
    registry = []

    # selected button (will have outline rect)
    selected = None

    # pygame RGBA colors
    white = (255, 255, 255, 255)
    black = (0, 0, 0, 255)
    red = (255, 0, 0, 255)
    green = (50, 205, 50, 255)
    light_blue = (173, 216, 230, 255)
    NavajoWhite = (255,222,173,255)
    DimGrey = (105,105,105,255)
    
    # default font color for buttons/labels is white
    def __init__(self, name, loc, color=white):

        # add button to registry
        self.registry.append(self)

        # paramater attributes
        self.name = name
        self.loc = loc
        self.color = color
        
        # text attr for button
        self.text = ""

        # size of button changes depending on length of text
        self.size = (int(len(self.text)*200), 200)

        # font.render(text, antialias, color, background=None) -> Surface
        self.font = font.render (
            self.name + " " + self.text, # display text
            True, # antialias on
            self.color, # font color
        )
        
        # rect for button
        self.rect = self.font.get_rect()
        self.rect.x = loc[0]
        self.rect.y = loc[1]
        
# function that connects to Postgres
def connect_postgres(db):

    # connect to PostgreSQL
    print ("\nconnecting to PostgreSQL")
    try:
        conn = connect (
            dbname = db,
            user = user_name,
            host = "localhost",
            password = user_pass
        )
    except Exception as err:
        print ("PostgreSQL Connect() ERROR:", err)
        conn = None

    # return the connection object
    return conn

def result_R(conn,op):
    op =True
    # get data and return for the function1
    if x == 1:
        if Country == "no" and Province == "no" :
            SQLquery = 'SELECT date, confirmed,recovered,deaths FROM date_worldwide;'
            print(SQLquery)
            
        if Country != "no" and Province == "no" :
            SQLquery = 'SELECT date, confirmed,recovered,deaths FROM date_country Where country = \'' + str(Country) + '\';'
            print(SQLquery)
    
        if Country != "no" and Province != "no":
            SQLquery = 'SELECT date ,confirmed,recovered,deaths FROM date_Province Where country = \'' + str(Country) + '\' and Province = \'' + str(Province) + '\';'
            print(SQLquery)
        
        # instantiate a new cursor object
        cursor = conn.cursor()

        # (use sql.SQL() to prevent SQL injection attack)
        sql_object = sql.SQL(
        
        # pass SQL statement to sql.SQL() method
            SQLquery
        )
        try:
            # use the execute() method to put table data into cursor obj
            cursor.execute( sql_object )

            # use the fetchall() method to return a list of all the data
            result_return = cursor.fetchall()
        
            # close cursor objects to avoid memory leaks
            cursor.close()
        
            # remove the plot before
            plt.clf()
        
            # make the dataframe
            df2 = pd.DataFrame(result_return)
            date = df2.loc[:,0]
            confirmed = df2.loc[:,1]
            recovered = df2.loc[:,2]
            deaths = df2.loc[:,3]
        
            # make plot for the data with matplotlib
            plt.plot(date, confirmed, 'b',label = 'Confirmed')
            plt.plot(date, recovered,'g', label = 'Recovered')
            plt.plot(date, deaths,'r', label = 'Deaths')
            plt.xlabel('Date')
            plt.ylabel('Aggregate Number of Cases')
            plt.legend(loc=0,ncol=1)
            plt.title('Trend Plot of Covid-19')
            plt.savefig('image.png', dpi=75)
            pic = pygame.image.load('image.png')
        except Exception as err:

            # print psycopg2 error and set table data to None
            print ("PostgreSQL psycopg2 cursor.execute() ERROR:", err)
            pic = "Some of the buttons have not typed in or the input is not in the table."
            op = False
        return pic,op           
    
    #get the data and return for function2
    if x == 2:    
        if Country == "no" and Date != None and Province == "no":
            SQLquery = 'SELECT confirmed,recovered,deaths FROM date_worldwide Where date = \'' + str(Date) + '\';'
            print(SQLquery)
        
        if Country != "no" and Province == "no" and  x == 2:
            SQLquery = 'SELECT confirmed,recovered,deaths FROM date_country Where date = \'' + str(Date) + '\' and country = \'' + str(Country) + '\';'
            print(SQLquery)
        
        if Country != "no" and Province != "no" and x == 2:
            SQLquery = 'SELECT confirmed,recovered,deaths FROM date_province Where date = \'' + str(Date) + '\' and country = \'' + str(Country) + '\' and Province = \'' + str(Province) +'\';'
            print(SQLquery)
        
        # instantiate a new cursor object
        cursor = conn.cursor()

        # (use sql.SQL() to prevent SQL injection attack)
        sql_object = sql.SQL(
        
        # pass SQL statement to sql.SQL() method
            SQLquery
        )
        
        try:
            # use the execute() method to put table data into cursor obj
            cursor.execute( sql_object )

            # use the fetchall() method to return a list of all the data
            result_return = cursor.fetchall()
            
            # close cursor objects to avoid memory leaks
            cursor.close()
        except Exception as err:

            # print psycopg2 error and set table data to None
            print ("PostgreSQL psycopg2 cursor.execute() ERROR:", err)
            result_return = "Some of the buttons have not typed in or the input is not in the table."
            op = False
        return result_return,op
    
    #get the data and return for function3
    if x == 3:
        SQLquery = 'SELECT Country,confirmed FROM date_country Where date = \'' + str(Date) + '\' ORDER BY Confirmed DESC LIMIT ' + str(Rank) + ';'
        print(SQLquery)
        
         # instantiate a new cursor object
        cursor = conn.cursor()

        # (use sql.SQL() to prevent SQL injection attack)
        sql_object = sql.SQL(
        
        # pass SQL statement to sql.SQL() method
            SQLquery
        )
        try:
            
            # use the execute() method to put table data into cursor obj
            cursor.execute( sql_object )
            
            # use the fetchall() method to return a list of all the data
            result_return = cursor.fetchall()
            
            # close cursor objects to avoid memory leaks
            cursor.close()
        except Exception as err:

            # print psycopg2 error and set table data to None
            print ("PostgreSQL psycopg2 cursor.execute() ERROR:", err)
            result_return = "Some of the buttons have not typed in or the input is not in the table."
            op = False
        return result_return,op
    
# initialize the pygame
pygame.init()

# change the caption/title for the Pygame app
pygame.display.set_caption("2020 DST2 Final Project 9068")

# create a pygame resizable screen
screen = pygame.display.set_mode(
    (900,700),
    HWSURFACE | DOUBLEBUF| RESIZABLE
)

# set the font
try:
    font = pygame.font.SysFont('Calibri', 20)
except Exception as err:
    print ("pygame.font ERROR:", err)
    font = pygame.font.SysFont('Arial', 20)

# load the start background picture
background = pygame.image.load('COVID-19-Banner-Large-EN.jpg')

# begin the pygame loop
app_running = True
x = 0
r = None
while app_running == True:
    
    # reset the screen
    # give the user some function to choose and set the start background
    if x == 0:
        screen.blit(background, (-190,0))
        function1 = Button("1. Trend Chart", (10,20))
        function2 = Button("2. Aggregate Cases", (10, 80))
        function3 = Button("3. Rank the Aggregate Confirmed cases of Countries", (10, 130))
        Ref_text = 'https://capacoa.ca/en/covid-19-information/'
        ref_font =font.render(Ref_text, True, Button.light_blue)
        screen.blit(ref_font, (540,670))
        # give the users some hint to choose and use the function
        hint_text = "hint: Press the button to choose the function you want"
        hint = font.render(hint_text, True, Button.light_blue)
        screen.blit(hint, (10, 160))
    
    # set the screen for the function
    else:
        pygame.draw.rect(screen, Button.DimGrey, [0,0,900,285])
        pygame.draw.rect(screen, Button.NavajoWhite, [0,285,900,115])
        pygame.draw.rect(screen, Button.white,[0,400,900,300])        
        restart = Button("<-Restart", (10,250))
        result = Button("->Get Result", (790,250))
        
        # give hints to use the actual function
        hint_text1 = 'hint: type in all the button, press "return" after each typing in.'
        hint_text2 = 'Type in "no" in country and province if you want the data for worldwide.'
        hint_text3 = 'Type in "no" in Province if you want the data for a certain country.'

        # set button for function1
        if x == 1:
            CR = Button('Country/Region:',(10,70))
            PS = Button('Province/State:',(10,170))
    
        # set button for function2
        if x == 2:
            D = Button('Date:',(10,20))
            CR = Button('Country/Region:',(10,100))
            PS = Button('Province/State:',(10,170))
    
        # set button for function3
        if x == 3:
            D = Button('Date:',(10,70))
            R = Button('Rank',(10,170))
            hint_text2 = 'Type in the ranking of the country you want'
            hint_text3 = ''
        
        hint1 = font.render(hint_text1, True, Button.green)
        hint2 = font.render(hint_text2, True, Button.green)
        hint3 = font.render(hint_text3, True, Button.green)
        screen.blit(hint1, (10, 300))
        screen.blit(hint2,(10,333))
        screen.blit(hint3, (10,367))
        
        
    # set the clock FPS for app
    clock = pygame.time.Clock()
    
    # iterate over the pygame events
    for event in pygame.event.get():

        # user clicks the quit button on app window
        if event.type == QUIT:
            app_running = False
            pygame.display.quit()
            pygame.quit()
            sys.exit()
            quit()

        # user presses a key on keyboard
        if event.type == KEYDOWN:
            if Button.selected != None:
                
                # get the selected button
                b = Button.selected
                
                # user presses the return key
                if event.key == K_RETURN:
                    
                    # check if the selected button is the date
                    if "Date" in b.name:
                        Date = b.text
                        
                    # check if the selected button is the Country/Region
                    if "Country" in b.name:
                        Country = b.text
                        
                    # check if the selected button is the Province/State
                    if "Province" in b.name:
                        Province = b.text
                    
                    # check if the selected button is the Rank
                    if "Rank" in b.name:
                        Rank = b.text
                        
                    # reset the button selected
                    Button.selected = None
                    
                else:
                    
                    # get the key pressed
                    key_press = pygame.key.get_pressed()

                    # iterate over the keypresses
                    for keys in range(255):
                        if key_press[keys]:
                            if keys == 8: # backspace
                                b.text = b.text[:-1]
                            else:
                                
                                # convert key to unicode string
                                b.text += event.unicode
                                print ("KEYPRESS:", event.unicode)
                        b.font = font.render(b.name + " " + b.text, True, Button.white)
        
        # check for mouse button down events
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            print ("\nMOUSE CLICK:", event)

            # iterate over the button registry list
            for b in Button.registry:

                # check if the mouse click collided with button
                if b.rect.collidepoint(event.pos) == 1:
                    
                    # store button object under selected attr
                    Button.selected = b
       
        
        # set the Button for the function screen            
        if x == 0:
            if Button.selected == function1:
                x = 1
                Button.selected = None
                Button.registry.clear()
            if Button.selected == function2:
                x = 2
                text=["Confirmed Cases: ","Recovered Cases: ","Deaths: "]
                Button.selected = None
                Button.registry.clear()
            if Button.selected == function3:
                x = 3
                Button.selected = None
                Button.registry.clear()
        else:
            
            # restart the app
            if Button.selected == restart:
                x = 0
                Button.selected = None
                Button.registry.clear()
                Date = None
                Rank = None
                Population = None
                Country = None
                Province = None
                # initialize the output with None
                result_return = None
            
            # get the data from SQL
            if Button.selected == result:
                connection = connect_postgres(db_name)
                result_return = result_R(connection,op)[0]
                op = result_R(connection, op)[1]
                if x ==3:
                    if op == True:
                        text = ['Rank ' + str(Rank) + ' of the country for that date is: ', 'Aggregate confirmed cases: ']
                        r = int(Rank)
                Date = None
                Population = None
                Country = None
                Province = None
                Rank =None
                Button.selected = None
                Button.registry.clear()
                
                
    # iterate over the button registry list
    for b in Button.registry:

        # blit the button's font to screen
        screen.blit(b.font, b.rect)

        # check if the button has been clicked by user
        if Button.selected == b:

            # blit an outline around button if selected
            rect_pos = (b.rect.x-10, b.rect.y-10, b.rect.width+20, b.rect.height+20)
            pygame.draw.rect(screen, Button.white, rect_pos, 3) # width 3 pixels
    
    # output the result
    if result_return != None:
        if op == True:
            # the result of the function1
            if x == 1:

                screen.blit(result_return, (250,400))
            
            # the result of the function2
            if x == 2:
                result_text = "For the aggregate number, "
                result_font = font.render(result_text, True, Button.black)
                screen.blit(result_font,(10,400))
                y = len(result_return[0])
                for i in range(0,y):
                    blit_text = str(result_return[0][i])
                    table_font = font.render(text[i] + blit_text,True, Button.black)
                    screen.blit(table_font, (10, 450 + int(i * 50)))
    
            if x == 3:
                result_text = "For the aggregate number, "
                result_font = font.render(result_text, True, Button.black)
                screen.blit(result_font,(10,400))
                y = len(result_return[r-1])
                for i in range(0,y):
                    blit_text = str(result_return[r-1][i])
                    table_font = font.render(text[i] + blit_text,True, Button.black)
                    screen.blit(table_font, (10, 450 + int(i * 50)))
        else:
            False_font = font.render(result_return, True, Button.black)
            screen.blit(False_font, (10,400))
        
    # set the clock FPS for application
    clock.tick(30)
    
    # use the flip() method to display text on surface
    pygame.display.flip()
    pygame.display.update()
    
    
    
    
