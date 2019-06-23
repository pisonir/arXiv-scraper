import urllib.request
from bs4 import BeautifulSoup
from tkinter import *
import webbrowser



class Scraper:
    def __init__(self, site):
        self.site = site

    def weblink(self, *args):
        '''
        Open the .pdf document corresponding to the link that has been selected by the user.
        :param args: event of selecting an item in the listbox
        :return: None
        '''
        index = self.titles_list.curselection()[0]
        item = self.titles_list.get(index)
        if 'https://' in item:
            webbrowser.open_new(item)

    def open_and_parse(self):
        '''
        Open and parse the website we are interested in, in this example is arXiv.
        :return: None
        '''
        r = urllib.request.urlopen(self.site)  # to access the website (in this example is arXiv)
        html = r.read()  # all of the HTML from the website is in the variable html
        parser = "html.parser"
        self.sp = BeautifulSoup(html, parser)  # The BeautifulSoup object does all the hard work and parses the HTML

    def scrape(self, keyword):
        '''
        Scrape the latest arXiv publications and select all the titles that include keyword.
        :param keyword: str
        :return:
        '''
        self.open_and_parse()
        # CREATE a LIST of items that contain the KEYWORD and present them on the root window using the Listbox class
        self.titles_list = Listbox(root, yscrollcommand = scrollbar.set, bg = 'white', font=('times',13))
        self.titles_list.bind('<<ListboxSelect>>', self.weblink)
        for tag in self.sp.find_all("span", class_="descriptor", text="Title:"):
            title = tag.next_sibling.string
            if keyword in title.lower():
                self.titles_list.insert(END, title)
                # the next line of code is really ugly but I haven't found a better solution yet
                link_1 = tag.previous_element.previous_element.previous_element.previous_element.previous_element.previous_element.previous_element.previous_element.previous_element.previous_element.previous_element.previous_element.previous_element
                link_2 = link_1.previous_element.previous_element
                link_3 = link_2.previous_element.previous_element.previous_element
                if 'arXiv' in link_1.string:
                    url = 'https://arxiv.org/pdf/'+link_1.string[-10:]
                    self.titles_list.insert(END, url)
                    self.titles_list.insert(END, '')
                elif 'arXiv' in link_2.string:
                    url = 'https://arxiv.org/pdf/'+link_2.string[-10:]
                    self.titles_list.insert(END, url)
                    self.titles_list.insert(END, '')
                else:
                    # The following happens if there are replacements
                    url = 'https://arxiv.org/pdf/' + link_3.string[-10:]
                    self.titles_list.insert(END, url)
                    self.titles_list.insert(END, '')
        self.titles_list.pack(side = LEFT, fill = BOTH, expand = YES)
        # ADD the SCROLLBAR
        scrollbar.pack(side=RIGHT, fill=Y)
        scrollbar.config(command=self.titles_list.yview)
        for i in range(self.titles_list.size()):
            # to highlight the url items
            if 'https://' in self.titles_list.get(i):
                self.titles_list.itemconfig(i, bg='lightyellow')


if __name__ == "__main__":
    news = "https://arxiv.org/list/cond-mat.mes-hall/new/"
    root = Tk()  # root is an instance of the class Tk. Main window of the application
    keyword = input('Please enter a keyword \n')
    scrollbar = Scrollbar(root) # to add a scrollbar on the root window
    Scraper(news).scrape(keyword) # To scrape all the titles on news that include the word 'graphene'
    root.title('Today arXiv publications')
    root.mainloop()  # mainloop() is an ininite loop used to run the application...until an event occurs such as closing
    # the window