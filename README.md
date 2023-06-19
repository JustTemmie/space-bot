# Andromeda

<a href="https://github.com/JustTemmie/space-bot/blob/main/LICENSE"><img src="https://img.shields.io:/github/license/JustTemmie/space-bot?color=informational"></img></a>
<a href="https://github.com/JustTemmie/space-bot/issues"><img src="https://img.shields.io:/github/issues/JustTemmie/space-bot?color=important"></img></a>
<a href="https://twitter.com/intent/tweet?text=Wow:&url=https%3A%2F%2Fgithub.com%2FJustTemmie%2Fspace-bot"><img src="https://img.shields.io:/twitter/url?style=social&url=https%3A%2F%2Fgithub.com%2FJustTemmie%2Fspace-bot"></img></a>

## Useful links
- [Invite](#invite)
- [Terms of Service](service.md)
- [Privacy Policy](privacy-policy.md)
- [Setup](#setup)


## Invite

<a href="https://discord.com/oauth2/authorize?client_id=870019731527204875&permissions=1541842332758&scope=bot%20applications.commands">
  Invite the bot!
</a>
<br/>

##  Setup
`NOTE: This is only for self hosting`

you can skip the top.gg steps if disired

fill in the these entries in a file named keys.env

```
DISCORD=
DEEP_AI=
IMGUR_CLIENT_ID=
IMGUR_CLIENT_SECRET=
TENOR=
OPENWEATHER=
TOP_GG_TOKEN=
TOP_GG_PORT= you need to port forward your sever with a port i don't remember the exact ports but keep it between 5000 and 45000 and you should be good
TOP_GG_ENCRYPTION_KEY= the "Authorization" field
```
then on top.gg add "http://yourIPAddress:port/dblwebhook" to the wekbook field.

## the keys can be obtained from:

discord key from https://discord.com/developers/applications

deep ai from https://deepai.org/dashboard/profile

imgur from https://api.imgur.com/oauth2/addclient?

tenor key from https://tenor.com/developer/keyregistration

open weather from https://home.openweathermap.org/api_keys

top.gg from https://top.gg/bot/YOURBOTIDHERE/webhooks



and lastly, just build the docker container using

`sudo docker-compose build`


now, whenever you want to start the bot just run

`sudo docker-compose up`

and it should theoretically work