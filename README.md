# Morpheus :sunglasses:

Morpheus is a telegram bot that helps to simplify the process of making custom telegram stickers.

As you may know, Telegram's official [Stickers bot](https://telegram.me/stickers) has strict requirements for a file to be made as a sticker. Morepheus helps to avoid this hassle.

Simply send a file <b>(image for regular stickers and video for animated stickers)</b> and morpheus will return the suitable file (that fulfills the requirements of the telegram overlords :grinning:), which you can forward to the sticker bot.

Try out the bot: [@morpheus_stickerbot](https://telegram.me/morpheus_stickerbot)

## Demo

![Demo gif](./images/demo.gif)

## Prerequisites

Requires [ffmpeg](https://ffmpeg.org) installed in the device

## Installation

Download the source code or clone it using <br>

```
https://github.com/Abhijith-K-S/Morpheus.git
```

Change to Morpheus directory<br>
`cd Morpheus`

Install the required libraries<br>

`pip install -r requirements.txt`

<br>

To make your own bot, you need to obtain an api token from [@BotFather](https://telegram.me/BotFather). Follow the instructions [here](https://core.telegram.org/bots#6-botfather) and obtain the same.

Create a file called `key.py` and write in it as follows: <br>

```
API_TOKEN = "<Your api token here>"
```

<br>
Now you are all set to run your bot. Enter the following commands in the terminal

<br>

`python bot.py`

Your bot is now all set to receive instructions.
