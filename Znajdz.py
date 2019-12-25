import requests as req
import webbrowser
from tkinter import *
from tkinter import messagebox

window = Tk()
window.title("Filmoszukajka")
window.geometry("400x50")
window.resizable(width=False,height=False)

def replace(data):
    data = data.replace("ą", "a", 100)
    data = data.replace("ż", "z", 100)
    data = data.replace("ó", "o", 100)
    data = data.replace("ę", "e", 100)
    data = data.replace("ś", "s", 100)
    return data

def get(dd):
    dd = dd.replace(" ","+",100)
    dd = replace(dd)

    print("Prosze czekac..")

    vid = req.get(f"https://fdb.pl/szukaj?query={dd}")

    find = re.findall(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", vid.text)

    dd = dd.replace("+","-",100)
    dd = dd.lower()

    data = re.search(f"https://fdb.pl/film/([0-9])+-{dd}",str(find))

    if data == None:
        data = {"text":"Nie znaleziono filmu.","status": "err"}
    else:
        data = {"text":f"Znaleziono film: \n{data.group()}","status": "ok","link":data.group()}
    return data

def message(msg):
    if msg["status"] == "ok":
        msgbox = messagebox.askokcancel("",msg["text"] + "\n\nClick cancel to open link in webbrowser")
        if msgbox == False:
            webbrowser.open_new_tab(msg["link"])
    else:
        messagebox.showinfo("",msg["text"])

Textbox = Entry(window)
btn = Button(window, text="Szukaj!", command=lambda: message(get(Textbox.get())))

Textbox.grid(row = 0, column = 5)
btn.grid(row = 0, column = 6)


window.mainloop()