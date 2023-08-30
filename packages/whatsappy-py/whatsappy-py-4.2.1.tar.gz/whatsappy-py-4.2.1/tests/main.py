from whatsappy import Whatsapp

whatsapp = Whatsapp(data_path="C:\\Whatsappy", visible=True)

@whatsapp.event
def on_ready() -> None:
    print("WhatsApp Web está pronto!")

whatsapp.run()

chat = whatsapp.open("Esquizofrenia")
chat.send("https://www.youtube.com/")

whatsapp.close()