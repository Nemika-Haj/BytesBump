# BytesBump
 A bump bot written in Discord.py!

## Features
- Easy to configure bot
- Direct support from the devs
- Webhook bumps
- Server List Extension

# Setting up
### Configuring the bot
- Rename `config-example.yml` to `config.yml` and modify the values.
```yaml
managers:
- manager
- ids
prefix: "preferred-prefix"
token: "bot-token"
version: 'bot-version'
mongo: "mongo-uri"
bot_name: "bot-name"
```
### Example Config
```yaml
managers:
- 219567539049594880
prefix: "="
token: "Th1s1s4vE5yG0odT0k3n1.M4yB3.To0G6DT0B3Tr93z" # Fake token
version: '1.0'
mongo: "mongodb+srv://dbuser:dbpassword@cluster0.r4nd0m.mongodb.net/"
bot_name: "BytesBump"
```
### Modifying `settings.json`
- `settings.json` contains data regarding the bot's functionality. You may modify all of the values.
```json
{
    "cooldown": 3600, // Bump cooldown in seconds
    "show_motd": false, // Show motd.txt after bumping
    "show_motd_wait": 10, // Time to wait before showing motd.txt
    "enable_serverlist": false, // Enable server list. Scroll down for more info.
    "serverlist_url": "http://127.0.0.1:5000/" // Index URL for the server list (with the slash at the end)
}
```
If you decide to copy the above config, remove the comments pls.

# Preparing the Database
To be able to store the server data you will require a **Mongo Database**. You can get a free **500MB** Database from [MongoDB Atlas](https://www.mongodb.com/cloud/atlas). That's enough for dozens of servers.

Head over to Atlas and create a new account. You will then be greeted with this panel.
![Panel View](https://user-images.githubusercontent.com/44692189/64170897-1297a600-ce73-11e9-910e-38b78c3ac315.jpg)

Select the `FREE` one and give it a name. Follow these steps;
- Go to `Database Access` section under the `Security` tab and click `+ ADD NEW USER`. Give it `Read and write to any database` permissions so the bot can properly store the data. Give it a username and a **secure** password. Save the password only.
![New User](https://i.imgur.com/zfhxyNX.png)
- To allow the bot to actually access the database, you should whitelist all IP's. Go to `Network Access` section under the `Security` tab and click `+ ADD IP ADDRESS`. Click the `Allow Access From Everywhere` and `0.0.0.0/0` should appear in the `Whitelist Entry`. If it doesn't, enter it manually. Lastly, click confirm.
![Whitelist All IP's](https://i.imgur.com/UgIYkoA.png)
- Time to connect to the Database! Go to `Cluster` under the `DATA STORAGE` tab. If your database is still setting up, please wait until it's done! Once it is, click the `CONNECT` button and `Connect Your Application`. Copy a link that **looks** like this; `mongodb+srv://<username>:<password>@cluster0.r4nd0m.mongodb.net/myFirstDatabase?retryWrites=true&w=majority`
- Lastly, remove the `myFirstDatabase?retryWrites=true&w=majority` part and replace `<username>` with your user's name (sometimes it is already replaced in if there's only one user), and `<password>` with your saved password. Take the link and paste it as the value of `mongo` in `config.yml`!
- Your database is done!

# Server List Extension
Your bot is basically done. You can start using it right away! However, we provide you with a server list website where all servers stored in the database will appear! You can check out **[this repo](https://github.com/Nemika-Haj/BytesBumpList)** to setup the server list.

# Additional Information
## Support
If you have any questions, visit **[BytesToBits | Coding](https://discord.gg/kETeDB3)**!

## Contributing
You are welcome to contribute and help improve the bot. Contributions must only concern the main part of the bot. In other words, if it has to do with the server list, this is not the right place.