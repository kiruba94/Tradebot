import logging
import gsheetsapi
from telegram import Update
from telegram.ext import filters, ApplicationBuilder, MessageHandler, ContextTypes, CommandHandler


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

async def start(update:Update, context: ContextTypes.DEFAULT_TYPE):
    message="""
Basic Commands Avaiable:
/stocks - lists all the stocks given as tips
/stock <stockname> - type the nse scrip name after the /stock command to get complete details of the stock tip provided
ex: /stock ITC
"""
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)


async def echo(update:Update, context:ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,text=update.message.text)

async def stocks(update:Update, context:ContextTypes.DEFAULT_TYPE):
    allstocks = gsheetsapi.get_all_stocks()
    message=""
    index=1
    for stock in allstocks:
        message=message+'\n'+str(index)+'. '+stock
        index+=1
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

async def stockdetails(update:Update, context:ContextTypes.DEFAULT_TYPE):
    try:
        stocksymbol = context.args[0]
        stockdetails = gsheetsapi.get_stock_details(str(stocksymbol))
        message=""
        if stockdetails==None:
            message = "Stock {} found, try the /stocks command to get the list of scrips available!".format(str(stocksymbol))
        message = """
SYMBOL:         {}
DATE OF TIP:    {}
BUY PRICE:      {}
TARGETS:        {}/{}/{}
STOPLOSS:       {}
LTP:            {}
P/L(%):         {}""".format(stockdetails[0],stockdetails[1],stockdetails[3],stockdetails[5],stockdetails[6],stockdetails[7],stockdetails[4],stockdetails[8],stockdetails[9])
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    except:
        message = "No Stock Name given or invalid stock, try the /stocks command to get the list of scrips available!"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message)


if __name__=='__main__':
    application = ApplicationBuilder().token('6570419673:AAGuLBLh_pEYj1yKuB4BAaYJXsPL81QWftg').build()

    start_handler=CommandHandler('start',start)
    echo_handler=MessageHandler(filters.TEXT & (~filters.COMMAND),echo)
    stocks_handler=CommandHandler('stocks', stocks)
    stockdetails_handler=CommandHandler('stock',stockdetails)
    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(stocks_handler)
    application.add_handler(stockdetails_handler)
    application.run_polling()