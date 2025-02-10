#Google BC
import requests
from tkinter import *
import webbrowser as wb

def search(query, pageNum, RPP):
    num = 0
    searchResults = []
    
    URL = "https://web-search30.p.rapidapi.com/"
    HEADERS = {
        'x-rapidapi-host': "web-search30.p.rapidapi.com",
        'x-rapidapi-key': "1a4a00acfamshaa568dd02d6fc4dp14bd0cjsnfb1b83f87741"
    }

    query = query
    page_number = pageNum
    page_size = RPP
    auto_correct = False
    safe_search = True

    querystring = {"q": query, "limit":"1000"}
    response = requests.get(URL, headers=HEADERS, params=querystring).json()

    print(response)

    total_count = len(response["results"])

    for web_page in response["results"]:
        if num == 0:
            resultsPage = []
        elif num % page_size == 0:
            searchResults.append(resultsPage)
            resultsPage = []
            
        num += 1

        url = web_page["url"]
        title = web_page["title"]
        description = web_page["description"]

        text = f"{str(num)}. Url: {url}, Title: {title} \n"
        resultsPage.append(text)

    return searchResults, total_count

class Window(Toplevel):
    def __init__(self, parent, query, pageNum, RPP, searchResults, total):
        super().__init__(parent)

        self.results = searchResults

        self.geometry('750x500')
        self.title('Google BC (search engine)')
        self.configure(bg="Red")

        label1 = Label(self, text="The search results are displayed below:", bg="Red")
        label1.config(font=('Helvetica bold',20))
        label1.grid(row=0,columnspan=2)

        Label(self, text="© Hasan Akhtar 2023", bg="Red").grid(row=1, columnspan=2)

        startNum = (pageNum*RPP)-(RPP-1)
        endNum = (pageNum*RPP)

        self.b = IntVar()
        self.b.set(startNum)

        self.num = startNum

        resultsBox = Text(self, bg="Red")
        resultsBox.grid(row=2, columnspan=2)

        for result in searchResults:
            resultsBox.insert(END, result)

        Label(self, text=f"Showing results {startNum} to {endNum} of {total}", bg="Red").grid(row=3, columnspan=2)
        
        Button(self,text="Next Page",bg="Red",command=self.next_page(query, total, RPP)).grid(row=4, column=0)
        Spinbox(self, bg="Red", textvariable=self.b, from_=startNum, to = endNum).grid(row=4, column=1)
        Button(self,text="Open Link",bg="Red",command=self.open_link).grid(row=4, column=2)
        Button(self,text='Close',bg="Red",command=self.destroy).grid(row=4, column=3)

    def next_page(self, query, total, RPP):
        global pageNum
        pageNum += 1
        print(pageNum)
        allSearchResults, total = search(query, pageNum, RPP)
        searchResults = allSearchResults[pageNum - 1]
        window = Window(self, query, pageNum, RPP, searchResults, total)
        window.grab_set()

    def open_link(self):
        resultNum = self.b.get()
        result = self.results[resultNum - self.num]
        startLink = result.find("Url") + 5
        endLink = result.find(",")
        link = result[startLink:endLink]
        print(link)
        #wb.open(link)
        
class App(Tk):
    def __init__(self, pageNum):
        super().__init__()
        self.geometry('300x200')
        self.title('Google BC (search engine)')
        self.configure(bg="Red")

        label1 = Label(self, text="Search", bg="Red")
        label1.config(font=('Helvetica bold',40))
        label1.grid(row=0,columnspan=2)

        self.a = IntVar()
        self.a.set(10)

        Label(self, text="© Hasan Akhtar 2023", bg="Red").grid(row=1, columnspan=2)
        Label(self, text="Enter search query:", bg="Red").grid(row=2, column=0)
        Label(self, text="Results per page:", bg="Red").grid(row=3, column=0)

        self.queryBox = Entry(self,bg="Red")
        self.queryBox.grid(row=2, column=1, sticky= E)

        self.spin = Spinbox(self, bg="Red", textvariable=self.a, from_=1, to = 50)
        self.spin.grid(row=3, column=1)
        
        Button(self,text='Submit',bg="Red",command=lambda: self.open_search(pageNum)).grid(row=4, column=0)
        Button(self,text='Exit',bg="Red",command=self.destroy).grid(row=4, column=1)

    def open_search(self, pageNum):
        RPP = self.a.get()
        query = self.queryBox.get()
        allSearchResults, total = search(query, pageNum, RPP)
        searchResults = allSearchResults[pageNum - 1]
        window = Window(self, query, pageNum, RPP, searchResults, total)
        window.grab_set()

if __name__ == "__main__":
    pageNum = 1
    app = App(pageNum)
    app.mainloop()
    
