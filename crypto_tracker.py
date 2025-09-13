from tkinter import *
import requests
import datetime
from PIL import Image,ImageTk
import io

price_base_url = "https://api.binance.com/api/v3/ticker/price?symbol="
crypto_image_base_url = "https://min-api.cryptocompare.com/data/all/coinlist"

response_image = requests.get(crypto_image_base_url,timeout=10).json()
coinlist = response_image.get("Data")

after_id = None
def get_price():
    global url,symbol,currency,content,after_id
    content = textbox.get(1.0,"end-1c").strip().upper()
    symbol,currency = content.split("-",1)
    url = f"{price_base_url}{symbol}{currency}"

    if after_id is not None:
        root.after_cancel(after_id)

    tracking()

def tracking():
    global base_url, cyrpto_image_base_url,coinlist,url,symbol,currency,content, after_id

    respons_price = requests.get(url,timeout=10)
    if respons_price.status_code == 200:
        response_price = respons_price.json()
        price = float(response_price["price"])
        label_price.config(text=f"Price: {price:.2f} $")        
        label_symbol.config(text=f"{content}")

        base_image_url = "https://www.cryptocompare.com"
        image_url = f"{base_image_url}{coinlist[symbol]['ImageUrl']}"

        respons_image = requests.get(image_url,timeout=10)
        if respons_image.status_code == 200:
            photo = ImageTk.PhotoImage(Image.open(io.BytesIO(respons_image.content)))
            label_image.config(image=photo)
            label_image.image = photo

    after_id = root.after(2500,tracking)


root = Tk()
root.geometry("400x600")
root.title("Crypto Price Tracker")


textbox = Text(root,height=2,font=("Arial",24))
textbox.pack(fill="x",side="top")

label_symbol = Label(root,pady=20,text="Crypto:",font=("Arial",24))
label_symbol.pack()

defauld_image = PhotoImage(file=r"default_image.png")
label_image = Label(root,pady=20,image=defauld_image,font=("Arial",24))
label_image.pack()

label_price = Label(root,pady=20,text="Price:",font=("Arial",18))
label_price.pack()


frame = Frame(root,pady=20)
frame.pack(side="top")

search_button = Button(frame,text="Search",padx=10,command=get_price)
search_button.pack(side="left")

exit_button = Button(frame,text="Exit",padx=10,command=root.destroy)
exit_button.pack(side="right")

root.mainloop()