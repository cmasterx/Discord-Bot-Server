const fs = require('fs');
const url = require('url')
const path = require('path');
const express = require('express');
const cors = require('cors');
const cookieParser = require('cookie-parser');
const bodyParser = require('body-parser');
const Discord = require('discord.js');
const request = require('request');
const chalk = require('chalk');

// check for config file create if not exist
try {
    if (!fs.existsSync(path.join(__dirname, './config.json'))) {
        console.log('config.json not found. Creating from template.')
        fs.copyFileSync(path.join(__dirname, './resources/model.config.json'), path.join(__dirname, './config.json'));
        console.log('config.json created. Edit this file and start program again.')
        process.exit();    
    }
}
catch (err) {
    console.error(err);
    console.error(chalk.redBright("error"), "Error trying to check if config.json exists");
}

// get json file
const config = require(path.join(__dirname, './config.json'));
const packageInfo = require(path.join(__dirname, './package.json'));

// check config file for any missing keys
{
    let changed = false;
    let modelConfig = require(path.join(__dirname, './resources/model.config.json'));
    
    // check for each key in model config
    for (var key in modelConfig) {
        if (!(key in config)) {
            config[key] = modelConfig[key];
            changed = true;
        }
    }
    
    // check for version
    if (config.version !== modelConfig.version) {
        config.version = modelConfig.version;
        changed = true;
    }

    fs.writeFileSync(path.join(__dirname, './config.json'), JSON.stringify(config));
}

const client = new Discord.Client();
const prefix = config.prefix;
const urls = {};

// express initialization
const app = express();
const port = process.env.PORT || "8000";
const staticPath = path.join(__dirname, './public');

app.use(cors());
app.use(cookieParser());
app.use(express.static(staticPath));
app.use(bodyParser.json())


// Setting up urls
// parses package.json for repository url
{
    let repoURL = packageInfo.repository.url;
    let idx = repoURL.indexOf('http');
    let offset = repoURL.indexOf('https://') != -1 ? 8 : 7;
    urls.repo = {};
    urls.repo.url = repoURL.substr(idx + offset);
    
    switch (offset) {
        case 7:
            urls.repo.protocol = "http://";
            break;
        case 8:
            urls.repo.protocol = "https://";
            break;
    }

    if (repoURL.endsWith('.git')) {
        urls.repo.url = urls.repo.url.substr(0, urls.repo.url.lastIndexOf('.git'));
    }
}


// Set up discord message responses

client.on('ready', () => {
    console.log('Logged in as', chalk.cyanBright(`${client.user.tag}!`));
    client.guilds.cache.forEach(guild => {
        console.log(`Guild: '${guild.name}' id: ${guild.id}`)
    })

    // client channel
    // client.guilds.cache.get('606986012715122726').channels.cache.get('606986012715122734').send('Howdy! I am a test bot! I am currently stupid.');
    // bot channel
    client.guilds.cache.get('606986012715122726').channels.cache.get('714696455977435188').send('Bot is online!');
    
    // console.log(client.channels);
})

client.on('message', msg => {
    if (msg.content === `${prefix}help`) {
        msg.channel.send('TODO: Implement this feature');
    }
})

client.on('message', msg => {
    if (msg.content === `${prefix}about` || msg.content == `${prefix}info`) {
        msg.reply(`Github: ${urls.repo.protocol}${urls.repo.url}`);
    }
});

client.on('message', msg => {
    if (msg.content === `${prefix}test`) {
        msg.reply('test');
    }
});

client.on('message', msg => {
    if (msg.content === `${prefix}minecraft start`) {

        if (msg.channel.type === "dm") {
            msg.reply('This command cannot be used as DM to a bot. Send this command to a channel instead.');
        }
        else {
            msg.reply('Starting minecraft server.');

            request.post(
                { 
                    url: url.resolve(config.processRunnerURL, config.processRunnerToken + '/start'),
                    json: {
                        "program": ["/home/charliew/Documents/mcserver/start.sh"]
                    }
                },
                function (error, res, body) {
                    if (error) {
                        console.error(error);
                        msg.channel.send('Uh oh... There seems to be an error! Tell Charlie about this! The error is: ');
                        msg.channel.send(error.toString());

                        
                        return;
                    }

                    if ('success' in body && body.success === true && 'ip' in body) {
                        msg.channel.send(`Server is online! The IP address is ${body.ip}`)
                    }

                    msg.channel.send('DEBUG MODE - Pytho Server Resonse: ' + JSON.stringify(body));
                }
            );
            
            // request.post(, , (error, res, body) => {
            //     if (error) {
            //         console.error(error);
            //         msg.channel.send('Uh oh... There seems to be an error! Tell Charlie about this! The error is: ');
            //         msg.channel.send(error);
            //         return;
            //     }

            //     msg.channel.send('DEBUG MODE: ');
            //     console.log(body)
            // })
        }
    }
})

client.on('message', msg => {
    if (msg.content === `${prefix}minecraft stop`) {

        if (msg.channel.type === "dm") {
            msg.reply('This command cannot be used as DM to a bot. Send this command to a channel instead.');
        }
        else {
            msg.reply('Stopping minecraft server.');
        }
    }
})

client.on('message', msg => {
    if (msg.content === `${prefix}minecraft running`) {

        if (msg.channel.type === "dm") {
            msg.reply('This command cannot be used as DM to a bot. Send this command to a channel instead.');
        }
        else {
            msg.reply('Stopping minecraft server.');
        }
    }
})


/**
 * Routes for website
 */
app.get('/*', (req, res) => {
    res.status(404).send("Error 404. You got the wrong link!");
})

// start webserver
app.listen(config.website_port, () => {
    console.log(`Listening to requests on http://localhost:${port}`);
})

// login to discord
let response = client.login(config.token);
response.catch(err => {
    console.error(chalk.redBright("error"), "Failed to login to Discord. Check if your discord bot token in", chalk.greenBright("config.json"), "is valid.");
    process.exit(0);        
})
