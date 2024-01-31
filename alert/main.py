from typing import List  #, Union

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from telegram import Bot
from pydantic import BaseModel

import os
import base64
import io
import requests
#import json

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')


app = FastAPI(
  title="Alerts",
  version="1.0",
)

app.add_middleware(
  CORSMiddleware,
  allow_origins=['*'],
  allow_credentials=True,
  allow_methods=['*'],
  allow_headers=['*'],
)

# Default root endpoint
@app.get("/")
async def root():
  return {"message": "Handle alerts"}


class emailPayload(BaseModel):
  headers: dict
  envelope: dict
  plain: str
  attachments: List

# these set of endpoints are for Connect Security Proof of solution
  
@app.post("/cloudmailin_alert", status_code=200, tags=["Endpoints"])
async def sent_tg_alert(
    request: Request,
    payload: emailPayload,
):


    if "<" in payload.headers['from']:
        from_email = payload.headers['from'].split("<")[1].split(">")[0]
    else:
        from_email = payload.headers['from']  #take from headers instead

    lookup = {
        "sssecurity@alarmlink.co": "-1002122690730",
        "nms_takanini@alarmlink.co": "-1001524700237",
        "limhss@gmail.com": "-1001524700237",
        "acannon.za@gmail.com": "-1001524700237"
    }

    try:
        unit_name = "" # avoid any exceptions
        alert_time = ""

        lines = payload.plain.split("\n")

        unit_ln = next((ln for ln in lines if "Unit name:" in ln), None)
        time_ln = next((ln for ln in lines if "Local Unit time:" in ln), None)

        if unit_ln != None:
            unit_name = unit_ln.split("Unit name:", 1)[1].strip()
        if time_ln != None:
            alert_time = time_ln.split("Local Unit time:", 1)[1]
        else:
            return JSONResponse(content={"result": "Unit name cannot be found"})

        print(from_email)
        
        if from_email in lookup.keys():
            channel_tme_id = str(lookup[from_email])
        else:
            return JSONResponse(content={"result": "Invalid Sender Email"})

        attachments = payload.attachments

        if len(attachments) == 0:
            return JSONResponse(content={"result": "No attachments found"})

        print(f"Up Next unit {unit_name} at {alert_time}")
        for attach in attachments:
            print("inside")
            char_list = []
            text = f"An alert has been detected, please standby to receive the image captured for unit {unit_name} at {alert_time}"

            for char in text:
                if char in [
                    '_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=',
                    '|', '{', '}', '.', '!'
                ]:
                    char_list.append(f"\{char}")
                else:
                    char_list.append(char)
            
            formatted_text = "".join(char_list)

            print("about to")
            if TELEGRAM_BOT_TOKEN == None:
                    print("TOKEN is None")
                    return JSONResponse(content={"message" : "Telegram Token on set"})
                
            bot = Bot(TELEGRAM_BOT_TOKEN)
            print(f"posting message to {channel_tme_id}")
            await bot.sendMessage(chat_id=channel_tme_id,
                                          text=formatted_text,
                                          parse_mode='MarkdownV2')
            print(f"posting message to {channel_tme_id} SUCCESSFUL")


            print(f"posting image to {channel_tme_id}")
            await bot.sendPhoto(chat_id=channel_tme_id,
                                    photo=io.BytesIO(base64.b64decode(
                                        attach['content'])),
                                        caption=f"{unit_name} at {alert_time}")
            print(f"posting image to {channel_tme_id} SUCCESSFUL")
            
            break  # assumes 1 image per email

    except:
        
        print("Error - See the last print message")
        return JSONResponse(
            content={'result': 'Error - See the last print message'},
            status_code=500)

    return JSONResponse(content={'result': 'OK'})

@app.post("/tradingview_alert", status_code=200, tags=["Endpoints"])
async def sent_tradingview_alert(
    request: Request
):
    if TELEGRAM_BOT_TOKEN == None:
        print("TOKEN is None")
        return JSONResponse(content={"message" : "Telegram Token on set"})
    
    data = await request.json()
    print(f"data is {data}")
    channel_tme_id = "-1001524700237"
    bot = Bot(TELEGRAM_BOT_TOKEN)
    char_list = []
    """for char in text:
        if char in [
            '_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=',
            '|', '{', '}', '.', '!'
        ]:
            char_list.append(f"\{char}")
        else:
            char_list.append(char)
            
        formatted_text = "".join(char_list)"""

    print(f"posting message to {channel_tme_id}")
    await bot.sendMessage(chat_id=channel_tme_id,
                          text="To be determined",
                          parse_mode='MarkdownV2')
    print(f"posting message to {channel_tme_id} SUCCESSFUL")
    return JSONResponse(content={'result': 'OK'})