#import modules
from bs4 import BeautifulSoup
import requests
import tkinter
import time
from tkinter import W,END
#define main window
root = tkinter.Tk()
root.title('Scraping App')
root.geometry('500x500')
root.config(bg = '#a669d7')
#define labels
label_1 = tkinter.Label(root, text = '', bg = '#a669d7')
label_1.grid(row = 0, column = 0 )
label_1 = tkinter.Label(root, text = '', bg = '#a669d7')
label_1.grid(row = 0, column = 1 )
label_2 = tkinter.Label(root, text = 'Scrape upto page: ', width = 15)
label_2.grid(row = 1, column = 1, padx = 5 ,ipady = 2, sticky = W)
label_3 = tkinter.Label(root, text = 'Min Vote: ' )
label_3.grid(row = 1,column = 3, padx = 5,ipady = 2 )
label_4 = tkinter.Label(root, text = 'Min Vote: ')
label_4.grid(row =2,column =3)
label_5 = tkinter.Label(root, text = 'Scrape page number: ')
label_5.grid(row = 2, column = 1, padx = 5 ,ipady = 2)
#define textboxes
text_box_1 = tkinter.Entry(root,width = 20)
text_box_1.grid(row = 1, column = 2, padx = 5,ipady = 2)
minimum_votes_1 = tkinter.Entry(root,width = 10)
minimum_votes_1.grid(row = 1,column = 4,padx = 5,ipady = 2)
minimum_votes_2 = tkinter.Entry(root,width = 10)
minimum_votes_2.grid(row=2,column = 4)
text_box_2 = tkinter.Entry(root,width = 20)
text_box_2.grid(row = 2, column = 2, padx = 5,ipady = 2)
#scrape first page
def scrape_a_particular_page():
    page = int(text_box_2.get())
    res = requests.get(f"https://news.ycombinator.com/news?p={page}")
    soup_1 = BeautifulSoup(res.content, 'html.parser')
    titles_1 = soup_1.select('.storylink')
    links_1 = soup_1.find_all(class_='storylink', href=True)
    votes_1 = soup_1.select('.score')
    result = zip(titles_1,links_1,votes_1)
    idx = 1
    with open('data_1','w',encoding="utf-8") as file_1:
        for i in result:
            if int((i[2].text).replace('points', '')) > int(minimum_votes_2.get()):
                file_1.write(f"{idx}.{i[0].text}\n {i[1]['href']}\n{i[2].text}\n")
                idx+=1
        time.sleep(2)
    text_box_2.delete(0,END)
    minimum_votes_2.delete(0,END)
#scrape upto a certain page
def scrape_data_upto():
    idx = 1
    titles = []
    links = []
    votes = []
    for i in range(int(text_box_1.get())):
        r = requests.get("https://news.ycombinator.com/news?p="+str(i+1))
        soup = BeautifulSoup(r.content, 'html.parser')
        for title in soup.select('.storylink'):
            titles.append(title)
        for link in soup.find_all(class_='storylink', href=True):
            links.append(link)
        for vote in soup.select('.score'):
            votes.append(vote)
    with open('data_1','w',encoding="utf-8") as file:
        for z in zip(titles,links,votes):
            if int((z[2].text).replace('points','')) > int(minimum_votes_1.get()):
                #print(f"{idx}.{z[0].text}\n {z[1].text}")
                file.write(f"{idx}.{z[0].text}\n{z[1]['href']}\n {z[2].text}\n")
                idx += 1
        time.sleep(2)
    text_box_1.delete(0,END)
    minimum_votes_1.delete(0,END)
#define scraping buttons
scrape = tkinter.Button(root,width = 10, text = 'Scrape',command = scrape_data_upto)
scrape.grid(row = 1, column = 5,padx = 2)
scrape_button = tkinter.Button(root,width =10, text ='Scrape',command = scrape_a_particular_page)
scrape_button.grid(row =2,column=5)
root.mainloop()