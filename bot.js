const fs = require('fs');
const express = require('express');
const Discord = require('discord.js');
const client = new Discord.Client();
const config = require('./config.json');
const prefix = config.prefix;

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
        msg.reply('Github: https://github.com/cmasterx/Discord-Bot-Server');
    }
});

client.on('message', msg => {
    if (msg.content == `${prefix}test`) {
        msg.reply('test');
    }
});

function login(token = null) {
    client.login(token || config.token);
}

function test() 
{

}

function sayHi(user) {
    alert(`Hello, ${user}!`);
  }
  
  function sayBye(user) {
    alert(`Bye, ${user}!`);
  }
  
//   export {sayHi, sayBye, logi+n}; // a list of exported variables

// console.log("test");
export {login, test};