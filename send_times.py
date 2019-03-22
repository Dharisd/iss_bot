import telegram 
from iss import get_passes
from datetime import date


'''
replace token and coords with your values
change chatid to your channel/chatid

'''


bot = telegram.Bot(token='')




def send(bot, pass_data):
    
    message_string = ""
    if len(pass_data) > 0:
        dt = date.today().strftime("%Y-%m-%d")
        message_string = "{0} passes for today {1} \n \n".format((len(pass_data) + 1),dt)
        for i in pass_data:
            message_string += i[0] + "\n"
            message_string += i[1]
            message_string += "\n \n"
            
        bot.sendMessage(chat_id="",text=message_string)

        for image in pass_data:
            bot.sendPhoto(chat_id="",photo=open(image[2],"rb"))






def allpasses(bot):
    """send the visible passes for today"""

    cords =[['6.5490 N','72.9534 E','vaikaradhoo'],['6.1497 N','73.2905 E','Funadhoo']]

    all_passes = []

    passes_morning = (get_passes(240,420,cords[1],date(.today())))
    passes_evening = (get_passes(1050,1170,cords[1],date.today()))

    all_passes = passes_morning + passes_evening

    if len(all_passes) > 0:
        send(bot, all_passes)



allpasses(bot)
