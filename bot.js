const mineflayer = require('mineflayer');
const { pathfinder, Movements } = require('mineflayer-pathfinder');
const { GoalFollow } = require('mineflayer-pathfinder').goals;
const collectBlock = require('mineflayer-collectblock').plugin;
const autoEat = require('mineflayer-auto-eat').plugin;
const armorManager = require('mineflayer-armor-manager');
const pvp = require('mineflayer-pvp').plugin;

const args = process.argv.slice(2);
const host = args[0];
const port = parseInt(args[1]);
const username = args[2];
const password = args[3];
const auth = args[4];

const options = {
    host,
    port,
    username,
    auth
};
if (password) options.password = password;

const bot = mineflayer.createBot(options);

bot.loadPlugin(pathfinder);
bot.loadPlugin(collectBlock);
bot.loadPlugin(autoEat);
bot.loadPlugin(armorManager);
bot.loadPlugin(pvp);

bot.once('spawn', () => {
    console.log(`Bot ${username} spawned on ${host}:${port}`);
    const mcData = require('minecraft-data')(bot.version);
    const movements = new Movements(bot, mcData);
    bot.pathfinder.setMovements(movements);
    bot.autoEat.options = {
        priority: 'foodPoints',
        startAt: 14,
        eatingTimeout: 3
    };
});

bot.on('chat', (sender, message) => {
    console.log(`${sender}: ${message}`);
});

bot.on('error', (err) => console.log(`Error: ${err.message}`));
bot.on('kicked', (reason) => console.log(`Kicked: ${reason}`));
bot.on('death', () => console.log('Bot died'));
bot.on('health', () => {
    if (bot.food < 15 || bot.health < 15) {
        bot.autoEat.eat((err) => {
            if (err) console.log(`Eat error: ${err}`);
        });
    }
});

process.stdin.setEncoding('utf8');
process.stdin.on('data', (data) => {
    const parts = data.trim().split(' ');
    const cmd = parts[0].toLowerCase();
    const arg = parts.slice(1).join(' ');
    switch (cmd) {
        case 'exec':
            bot.chat(arg);
            console.log(`Sent chat: ${arg}`);
            break;
        case 'follow':
            const player = bot.players[arg];
            if (player && player.entity) {
                bot.pathfinder.setGoal(new GoalFollow(player.entity, 1), true);
                console.log(`Following ${arg}`);
            } else {
                console.log(`Player ${arg} not found`);
            }
            break;
        case 'stop':
            bot.pathfinder.setGoal(null);
            bot.pvp.stop();
            console.log('Stopped movement and actions');
            break;
        case 'mine':
            const blockType = bot.registry.blocksByName[arg];
            if (blockType) {
                const block = bot.findBlock({ matching: blockType.id, maxDistance: 64 });
                if (block) {
                    bot.collectBlock.collect(block, (err) => {
                        if (err) console.log(`Mine error: ${err}`);
                        else console.log(`Mined ${arg}`);
                    });
                } else {
                    console.log(`No ${arg} found nearby`);
                }
            } else {
                console.log(`Unknown block: ${arg}`);
            }
            break;
        case 'attack':
            const target = bot.players[arg]?.entity;
            if (target) {
                bot.pvp.attack(target);
                console.log(`Attacking ${arg}`);
            } else {
                console.log(`Target ${arg} not found`);
            }
            break;
        case 'equip':
            bot.armorManager.equipAll();
            console.log('Equipped best armor and tools');
            break;
        case 'eat':
            bot.autoEat.eat((err) => {
                if (err) console.log(`Eat error: ${err}`);
                else console.log('Ate food');
            });
            break;
        default:
            console.log(`Unknown command: ${cmd}`);
    }
});