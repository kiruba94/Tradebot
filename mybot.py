import gsheetsapi
from telegram import Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import filters, ApplicationBuilder, MessageHandler, ContextTypes, CommandHandler, ConversationHandler, Application, CallbackQueryHandler

async def start(update:Update, context: ContextTypes.DEFAULT_TYPE):
    message="""
Basic Commands Avaiable:
/stocks - lists all the stocks given as tips
/stock <stockname> - type the nse scrip name after the /stock command to get complete details of the stock tip provided
ex: /stock ITC
"""
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

# Stages
START_ROUTES, END_ROUTES = range(2)



async def echo(update:Update, context:ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,text=update.message.text)

async def stocks(update:Update, context:ContextTypes.DEFAULT_TYPE):
    allstocks = gsheetsapi.get_all_stocks()
    keyboard=[]
    i=0
    currentRow=[]
    for stock in allstocks:
        if i<3:
            currentRow.append(InlineKeyboardButton(stock, callback_data=stock))
            i+=1
        elif i==3:
            keyboard.append(currentRow)
            currentRow=[]
            currentRow.append(InlineKeyboardButton(stock, callback_data=stock))
            i=1
    keyboard.append(currentRow)
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Select a stock to view details:", reply_markup=reply_markup)
    return START_ROUTES

async def stockdetails(update:Update, context:ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    try:
        stocksymbol = query.data
        stockdetails = gsheetsapi.get_stock_details(str(stocksymbol))
        message=""
        if stockdetails==None:
            message = "Stock {} found, try the /stocks command to get the list of scrips available!".format(str(stocksymbol))
        message = """
SYMBOL:         {}
DATE OF TIP:    {}
ALLOCATION%:    {}
BUY PRICE:      {}
TARGETS:        {}/{}/{}
STOPLOSS:       {}
LTP:            {}
P/L(%):         {}""".format(stockdetails[0],stockdetails[1],stockdetails[2],stockdetails[3],stockdetails[5],stockdetails[6],stockdetails[7],stockdetails[4],stockdetails[8],stockdetails[9])
        await query.edit_message_text(text=message)
    except:
        message = "No Stock Name given or invalid stock, try the /stocks command to get the list of scrips available!"
        await query.edit_message_text(text=message)
    return ConversationHandler.END


if __name__=='__main__':
    application = ApplicationBuilder().token('6570419673:AAGuLBLh_pEYj1yKuB4BAaYJXsPL81QWftg').build()
    start_handler=CommandHandler('start',start)
    echo_handler=MessageHandler(filters.TEXT & (~filters.COMMAND),echo)
    stockdetails_handler=CommandHandler('stock',stockdetails)

    stock_selection_handler = ConversationHandler(
        entry_points=[CommandHandler('stocks', stocks)],
        states={
            START_ROUTES:[
                CallbackQueryHandler(stockdetails,pattern="^[a-zA-Z0-9]*$")
            ]
        },
        fallbacks=[CommandHandler("start", start)],

    )

    application.add_handler(stock_selection_handler)
    application.add_handler(echo_handler)
    application.add_handler(stockdetails_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)
