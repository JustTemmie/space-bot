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

<a href="https://discord.com/oauth2/authorize?client_id=765222621779853312&permissions=1541842332758&scope=bot%20applications.commands">
  Invite the bot!
</a>
<br/>
Take a look at the <a href="https://top.gg/bot/765222621779853312">top.gg page</a>.

##  Setup
`NOTE: This is only for self hosting`

you can skip the top.gg steps but it will likely throw an error :p

First, install the requirements.txt file with pip.

`pip3 install -r requirements.txt`

Read through setup.txt and do everything in there.

Run build.py in order to get a library.

`NOTE: build.py requries rust to be installed https://rustup.rs/`

lastly fill in the these entries in a file named keys.env

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

discord key from https://discord.com/developers/applications

deep ai from https://deepai.org/dashboard/profile

imgur from https://api.imgur.com/oauth2/addclient?

tenor key from https://tenor.com/developer/keyregistration

open weather from https://home.openweathermap.org/api_keys

top.gg from https://top.gg/bot/YOURBOTIDHERE/webhooks
