import csv
import requests
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk


#dynamically obtain csv file about global confirmed cases from john hopkin's github
url_confirmed = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
req_confirmed = requests.get(url_confirmed)
covid_content_confirmed = req_confirmed.content
csvfile = open('covid_global_confirmed.csv', 'wb')

csvfile.write(covid_content_confirmed)
csvfile.close()

df_confirmed = pd.read_csv('covid_global_confirmed.csv')
#merge rows based on countries, eliminate need to handle province and states
df_confirmed = df_confirmed.groupby(['Country/Region']).sum()
df_confirmed = df_confirmed.drop(['Lat','Long'], axis = 1).reset_index()
#df_confirmed = df_confirmed.rename(index = {'Taiwan*':'Taiwan'})

#dynamically obtain csv file about number of deaths from john hopkins github
url_deaths = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
req_deaths = requests.get(url_deaths)
covid_content_deaths = req_deaths.content
csvfile = open('covid_global_deaths.csv','wb')

csvfile.write(covid_content_deaths)
csvfile.close()

df_deaths = pd.read_csv('covid_global_deaths.csv')
df_deaths = df_deaths.groupby(['Country/Region']).sum()
df_deaths = df_deaths.drop(['Lat','Long'],axis = 1).reset_index()
#print(df_deaths)

#dynamically obtain csv file about number of deaths from john hopkins github
url_recovery = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"
req_recovery = requests.get(url_recovery)
covid_content_recovery = req_recovery.content
csvfile = open('covid_global_recovery.csv','wb')

csvfile.write(covid_content_recovery)
csvfile.close()

df_recovery = pd.read_csv('covid_global_recovery.csv')
df_recovery = df_recovery.groupby(['Country/Region']).sum()
df_recovery = df_recovery.drop(['Lat','Long'],axis = 1).reset_index()
#print(df_recovery)





def date_index(inputdate):
    ref_date = datetime.datetime(2020,1,22) #record of all covid cases start from 22.1.2020
    #remove / from inputdate
    x = inputdate.split('/')
    for i in range(len(x)):
        x[i]  = int(x[i])
    outputdate = datetime.datetime(2020,x[0],x[1])
    return (outputdate-ref_date).days

#list of all dates from 22nd JAN 2020
date_list = df_confirmed.columns[1:]


def graph_plot(start_date,end_date,country1,country2):

    start_date_index = date_index(start_date)
    end_date_index = date_index(end_date)
    countries_to_plot = [country1,country2]

    x_axis = date_list[start_date_index:end_date_index+1] #start and end index inclusive

    for country in countries_to_plot: #countries_to_plot:
        #create new data frame with corresponding countries and respective values
        # python pandas to filter data, select rows of corresponding countries
        country_df = df_confirmed[df_confirmed['Country/Region'] == country] #data frame with countries to plot
        y_axis = [int(country_df[c]) for c in x_axis]
        #print(y_axis)
        plt.plot(x_axis, y_axis, label = country)

    df_confirmed1 = df_confirmed.set_index("Country/Region")
    output1 = 'Country: %s\nDate: %s\nConfirmed Cases: %s' % (country1,end_date,df_confirmed1.loc[country1,end_date])
    outputlabel1['text'] = output1
    output2 = 'Country: %s\nDate: %s\nConfirmed Cases: %s' % (country2,end_date,df_confirmed1.loc[country2,end_date])
    outputlabel2['text'] = output2


    plt.title('Confirmed Cases Over Time')
    skip = max(len(x_axis) // 5, 1)  # Helps ensure we don't add too many date tick marks
    plt.xticks(x_axis[::skip]) #ticks once on x axis every skip-number of days)
    plt.xlabel("Date (MM/DD/YY)")
    plt.ylabel("Confirmed Cases")
    plt.legend()
    plt.show()


def graph_deaths(start_date,end_date,country1,country2):
    start_date_index = date_index(start_date)
    end_date_index = date_index(end_date)
    countries_to_plot = [country1, country2]
    x_axis = date_list[start_date_index:end_date_index + 1]

    for country in countries_to_plot:  # countries_to_plot:
        country_df = df_deaths[df_deaths['Country/Region'] == country]  # data frame with countries to plot
        y_axis = [int(country_df[c]) for c in x_axis]
        # print(y_axis)
        plt.plot(x_axis, y_axis, label=country)

    df_deaths1 = df_deaths.set_index("Country/Region")
    output1 = 'Country: %s\nDate: %s\nNumber of Deaths: %s' % (country1, end_date, df_deaths1.loc[country1, end_date])
    outputlabel1['text'] = output1
    output2 = 'Country: %s\nDate: %s\nNumber of Deaths: %s' % (country2, end_date, df_deaths1.loc[country2, end_date])
    outputlabel2['text'] = output2

    plt.title('Number of Deaths Over Time')
    skip = max(len(x_axis) // 5, 1)  # Helps ensure we don't add too many date tick marks
    plt.xticks(x_axis[::skip])  # ticks once on x axis every skip-number of days)
    plt.xlabel("Date (MM/DD/YY)")
    plt.ylabel("Number of Deaths")
    plt.legend()
    plt.show()


def graph_recovered(start_date,end_date,country1,country2):
    start_date_index = date_index(start_date)
    end_date_index = date_index(end_date)
    countries_to_plot = [country1, country2]
    x_axis = date_list[start_date_index:end_date_index + 1]

    for country in countries_to_plot:  # countries_to_plot:
        country_df = df_recovery[df_recovery['Country/Region'] == country]  # data frame with countries to plot
        y_axis = [int(country_df[c]) for c in x_axis]
        plt.plot(x_axis, y_axis, label=country)
    df_recovery1 = df_recovery.set_index("Country/Region")
    output1 = 'Country: %s\nDate: %s\nNumber of Recoveries: %s' % (country1, end_date, df_recovery1.loc[country1, end_date])
    outputlabel1['text'] = output1
    output2 = 'Country: %s\nDate: %s\nNumber of Recoveries: %s' % (country2, end_date, df_recovery1.loc[country2, end_date])
    outputlabel2['text'] = output2

    plt.title('Number of Recoveries Over Time')
    skip = max(len(x_axis) // 5, 1)  # Helps ensure we don't add too many date tick marks
    plt.xticks(x_axis[::skip])  # ticks once on x axis every skip-number of days)
    plt.xlabel("Date (MM/DD/YY)")
    plt.ylabel("Recovered")
    plt.legend()
    plt.show()
    return True



Height = 400
Width = 700
country_list = df_confirmed['Country/Region']

parent = tk.Tk()
canvas = tk.Canvas(parent, height = Height, width = Width)
canvas.pack()

background = tk.PhotoImage(file = 'coronavirus-750x400.png')
background_label = tk.Label(parent, image = background)
background_label.place(x = 0, y = 0,relheight = 1, relwidth =1, anchor = 'nw' )

#topframe
frame = tk.Frame(parent, bg = "#CBD7D5")
frame.place(relx = 0.5, rely = 0.1, relheight = 0.3, relwidth = 0.75, anchor = 'n')

entry1 = StringVar(parent)
entry1.set(date_list[0])#default value

opt1 = OptionMenu(frame,entry1,*date_list)
opt1.place(relx = 0.2, rely = 0.1, relwidth = 0.3, relheight = 0.2)

labelopt1 = tk.Label(frame,text = 'start date:')
labelopt1.place(relx = 0, rely = 0.1, relwidth = 0.2, relheight = 0.2)
#button_opt1 = tk.Button(frame, text = "Submit Initial Date", bg = 'gray')
#button_opt1.place(relx = 0.5, rely = 0, relwidth = 0.3, relheight= 0.14)
labelopt2 = tk.Label(frame,text = 'end date:')
labelopt2.place(relx = 0.5, rely = 0.1, relwidth = 0.2, relheight = 0.2)
entry2 = StringVar(parent)
entry2.set(date_list[1])

opt2 = OptionMenu(frame, entry2, *date_list[1:])
opt2.place(relx = 0.7, rely = 0.1, relwidth = 0.3, relheight = 0.2)

labelc1 = tk.Label(frame,text = "Countries:")
labelc1.place(relx = 0, rely = 0.4, relwidth = 0.15, relheight = 0.2)

cslec1 = StringVar(parent)
cslec1.set(country_list[0])
opt3 = OptionMenu(frame,cslec1,*country_list)
opt3.place(relx = 0.2, rely = 0.4, relwidth = 0.3, relheight = 0.2)

cslec2 = StringVar(parent)
cslec2.set(country_list[0])
opt4 = OptionMenu(frame,cslec2,*country_list)
opt4.place(relx = 0.6, rely = 0.4, relwidth = 0.3, relheight = 0.2)


button_confirmed = tk.Button(frame, text = 'Confirmed Cases', bg = 'gray',\
                             command =lambda : graph_plot(entry1.get(),entry2.get(),cslec1.get(),cslec2.get()))
button_confirmed.place(relx = 0.05, rely = 0.7, relwidth = 0.2, relheight = 0.2)

#Output frame
frame2 = tk.Frame(parent,bg = "#CBD7D5", bd = 5)
frame2.place(relx = 0.5, rely = 0.45, relwidth = 0.75, relheight = 0.5, anchor = 'n')

outputlabel1 = tk.Label(frame2, font = 8,anchor = "w", justify = 'left')
outputlabel1.place(relwidth = 0.5, relheight = 1)

outputlabel2 = tk.Label(frame2, font = 8,anchor = "e", justify = 'left')
outputlabel2.place(relx = 0.5,rely = 0,relwidth = 0.5, relheight = 1)

button_death = tk.Button(frame, text = 'Number of Deaths', bg = 'gray',\
                             command =lambda :graph_deaths(entry1.get(),entry2.get(),cslec1.get(),cslec2.get()))
button_death.place(relx = 0.4, rely = 0.7, relwidth = 0.2, relheight = 0.2)

button_recovered = tk.Button(frame, text = 'Recoveries', bg = 'gray',\
                             command =lambda : graph_recovered(entry1.get(),entry2.get(),cslec1.get(),cslec2.get()))
button_recovered.place(relx = 0.75, rely = 0.7, relwidth = 0.2, relheight = 0.2)

parent.mainloop()