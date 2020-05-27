const fs = require('fs');
const express = require('express');
const Discord = require('discord.js');
const request = require('request');
const config = require('./config.json');
const packageInfo = require('./package.json');

const client = new Discord.Client();
const prefix = config.prefix;
const urls = {};

function login(token = null) {
    client.login(token || config.token);
}

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
    console.log(`Logged in as ${client.user.tag}!`);
    client.guilds.cache.forEach(guild => {
        console.log(`name: ${guild.name} id: ${guild.id}`)
    })

    // client channel
    // client.guilds.cache.get('606986012715122726').channels.cache.get('606986012715122734').send('Howdy! I am a test bot! I am currently stupid.');
    // bot channel
    client.guilds.cache.get('606986012715122726').channels.cache.get('714696455977435188').send('Bot is online!');
    
    // console.log(client.channels);
})

client.on('message', msg => {
    if (msg.content == `${prefix}about` || msg.content == `${prefix}info`) {
        msg.reply(`Github: ${urls.repo.protocol}${urls.repo.url}`);
    }
});

client.on('message', msg => {
    if (msg.content == `${prefix}test`) {
        msg.reply('test');
    }
});



login();
