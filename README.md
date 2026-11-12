# awesome-minecraft-bots

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![Link check](https://github.com/codewithkrrish/awesome-minecraft-bots/actions/workflows/links.yml/badge.svg)](https://github.com/codewithkrrish/awesome-minecraft-bots/actions/workflows/links.yml)

A curated list of the frameworks, plugins, tools, and hosting I actually trust for running Minecraft bots — the stuff that keeps a bot online instead of stuck in a wall.

I run a mineflayer bot 24/7 on my friends' survival server, and most lists I found were either dead links or tools nobody maintains anymore. So I built the one I wanted: every link here was checked by hand (and re-checked weekly by a script in `scripts/`), and anything I haven't personally run is marked as such.

## Contents

- [Frameworks & libraries](#frameworks--libraries)
- [Mineflayer plugins](#mineflayer-plugins)
- [Viewers & dashboards](#viewers--dashboards)
- [Bedrock & cross-play](#bedrock--cross-play)
- [AI & research bots](#ai--research-bots)
- [Servers to test against](#servers-to-test-against)
- [Monitoring & status](#monitoring--status)
- [Hosting](#hosting)
- [Docs & protocol references](#docs--protocol-references)
- [My setup](#my-setup)
- [Contributing](#contributing)

## Frameworks & libraries

The starting point. Pick one of these and the rest of the list plugs into it.

- [mineflayer](https://github.com/PrismarineJS/mineflayer) — The standard JavaScript bot framework. High-level API, supports basically every version from old to new, and the plugin ecosystem below is built for it. Start here unless you have a reason not to.
- [node-minecraft-protocol](https://github.com/PrismarineJS/node-minecraft-protocol) — The low-level protocol library mineflayer sits on. Use it when you need raw packets or are writing your own framework.
- [minecraft-data](https://github.com/PrismarineJS/minecraft-data) — Block, item, entity and recipe data for every version, as JSON. Mineflayer uses it under the hood; handy on its own for tooling.
- [prismarine-auth](https://github.com/PrismarineJS/prismarine-auth) — Microsoft account auth for bots (device-code flow included). You will need this the moment your bot joins a server with online mode on.
- [prismarine-registry](https://github.com/PrismarineJS/prismarine-registry) — Version registry that ties protocol versions, data and features together.
- [node-vec3](https://github.com/PrismarineJS/node-vec3) — Small 3D vector library used across the PrismarineJS projects.
- [prismarine-chat](https://github.com/PrismarineJS/prismarine-chat) — Parse and build Minecraft chat messages, including the newer signed-chat formats.
- [Baritone](https://github.com/cabaletta/baritone) — Java pathfinding bot (A* over real terrain, with goals like "go to X" or "mine this"). Famous for a reason; pairs with Meteor Client.
- [Azalea](https://github.com/azalea-rs/azalea) — A Minecraft bot framework in Rust. Fast, and the one to watch if you want many bots without Node's memory footprint.
- [go-mc](https://github.com/Tnze/go-mc) — Minecraft client and server libraries in Go. Good if your whole stack is already Go.
- [mcproto](https://github.com/py-mine/mcproto) — A Python implementation of the Minecraft protocol. The best starting point for Python bots.
- [Quarry](https://github.com/barneygale/quarry) — Python library for the Minecraft protocol, from the author of the protocol docs. Solid if you prefer writing bots in Python.
- [Meteor Client](https://github.com/MeteorDevelopment/meteor-client) — A Fabric utility client, not a bot framework — I keep it here because its Baritone integration and automation modules are what a lot of bot ideas get prototyped against.

## Mineflayer plugins

Mineflayer on its own can connect, chat and look around. These plugins are what make it actually do things.

- [mineflayer-pathfinder](https://github.com/PrismarineJS/mineflayer-pathfinder) — Movement and pathfinding: goals, parkour-aware jumps, and safe pathing around lava and cliffs. The first plugin I install on any bot.
- [mineflayer-pvp](https://github.com/PrismarineJS/mineflayer-pvp) — Combat: attacking, strafing, and using the right weapon. Works with pathfinder.
- [mineflayer-collectblock](https://github.com/PrismarineJS/mineflayer-collectblock) — Find and collect blocks (wood, ores, crops) with pathfinder driving the movement.
- [mineflayer-tool](https://github.com/PrismarineJS/mineflayer-tool) — Automatically picks the best tool for the block being mined.
- [mineflayer-statemachine](https://github.com/PrismarineJS/mineflayer-statemachine) — Small state machines for bot behaviour (idle → follow → mine → return). Keeps bot logic readable once it grows past a few behaviours.
- [mineflayer-navigate](https://github.com/PrismarineJS/mineflayer-navigate) — An older navigation plugin. Superseded by pathfinder for most cases, but still referenced in a lot of tutorials.
- [mineflayer-auto-eat](https://github.com/linkle69/mineflayer-auto-eat) — Eats food automatically when hunger drops. (The original PrismarineJS repo is gone; this maintained fork is the one to use.)
- [MineflayerArmorManager](https://github.com/PrismarineJS/MineflayerArmorManager) — Auto-equips the best armour from the inventory.
- [mineflayer-auto-totem](https://github.com/ranguli/mineflayer-auto-totem) — Keeps a totem in the off-hand and replaces it after it pops.
- [mineflayer-web-inventory](https://github.com/imharvol/mineflayer-web-inventory) — A web UI for the bot's inventory. Useful for checking what a farming bot actually collected without logging in.

## Viewers & dashboards

Watching a bot is half the debugging.

- [prismarine-viewer](https://github.com/PrismarineJS/prismarine-viewer) — Renders the bot's view in a browser, first-person. The quickest way to see what your bot sees.
- [prismarine-web-client](https://github.com/PrismarineJS/prismarine-web-client) — Play Minecraft in the browser, built on the same protocol stack. Handy for testing a bot against a real-ish player.

## Bedrock & cross-play

If any of your players are on phones or consoles, you need this layer.

- [bedrock-protocol](https://github.com/PrismarineJS/bedrock-protocol) — Bedrock Edition protocol in JavaScript; the mineflayer equivalent for Bedrock clients.
- [Geyser](https://github.com/GeyserMC/Geyser) — Lets Bedrock players join Java servers. Practically mandatory for any mixed friends server.
- [Floodgate](https://github.com/GeyserMC/floodgate) — Goes with Geyser: lets Bedrock players join without a Java account.

## AI & research bots

Bots that learn or reason, rather than follow a script.

- [Voyager](https://github.com/MineDojo/Voyager) — An LLM-powered agent that explores and learns skills in Minecraft, building a library of code as it goes. The reference implementation for "AI plays Minecraft".
- [MineDojo](https://github.com/MineDojo/MineDojo) — The research framework behind Voyager: a simulator, tasks, and benchmarks for embodied agents.

## Servers to test against

Never test a bot on a server your friends play on. Spin up one of these locally first.

- [flying-squid](https://github.com/PrismarineJS/flying-squid) — A lightweight Minecraft server in JavaScript. Starts in seconds, perfect for bot tests.
- [Minestom](https://github.com/Minestom/Minestom) — A Java server framework for building custom servers from scratch. Overkill for testing, great if you want a server shaped around your bot.
- [Feather](https://github.com/feather-rs/feather) — A Minecraft server written in Rust. Light and fast.
- [Pumpkin](https://github.com/Pumpkin-MC/Pumpkin) — Another Rust server implementation, actively developed.
- [itzg/docker-minecraft-server](https://github.com/itzg/docker-minecraft-server) — Run a real Java/Paper server in Docker with one command. This is how I test bots against Paper before they touch my friends' server.

## Monitoring & status

- [mcstatus](https://github.com/py-mine/mcstatus) — Ping a Java or Bedrock server from Python and get players, version and latency. I use it in a tiny script that tells me if my server (or bot) went down.

## Hosting

Where the bot actually lives. Free tiers are listed first because that's where most people start; paid hosts are the ones I see recommended most often, not ones I've paid for.

- [Aternos](https://aternos.org) — Free Minecraft server hosting. Sleeps when empty, which is exactly why people run anti-AFK bots on it.
- [Minehut](https://minehut.com) — Free hosting with a plugin panel, similar idea to Aternos.
- [Exaroton](https://exaroton.com) — Pay-per-use hosting from the Aternos team. Good middle ground before a monthly plan.
- [Oracle Cloud Free Tier](https://www.oracle.com/cloud/free/) — A genuinely free ARM VPS (the "always free" tier) that can run a small server and a bot. Setup takes an afternoon; the price is right.
- [PebbleHost](https://pebblehost.com) — Budget paid hosting, popular for small friend groups.
- [BisectHosting](https://www.bisecthosting.com) — Paid hosting with a big modpack catalogue.
- [Sparked Host](https://sparkedhost.com) — Budget paid hosting with a clean panel.
- [Bloom Host](https://bloom.host) — Paid hosting, often recommended for performance per dollar.

## Docs & protocol references

- [mineflayer docs](https://mineflayer.prismarine.js.org/) — The official mineflayer API docs and examples. Read the examples folder before writing your own bot; most beginner mistakes are answered there.
- [mineflayer docs on GitHub](https://github.com/PrismarineJS/mineflayer/blob/master/docs/README.md) — Same docs, in the repo, if the site is ever down.
- [PrismarineJS](https://prismarinejs.com/) — The home of the whole PrismarineJS ecosystem, with links to every project above.
- [wiki.vg](https://wiki.vg/Protocol) — The community protocol documentation. When a packet behaves oddly, the answer is usually here.

## My setup

What I actually run, so you know where this list comes from:

- Bot: mineflayer + pathfinder + collectblock + auto-eat + auto-totem
- Server: Paper, with Geyser so Bedrock friends can join, and a login plugin since the server runs offline-mode
- Hosting: a small VPS, bot kept alive with an anti-AFK loop so the server doesn't sleep when nobody's online
- Testing: flying-squid or a Docker Paper server first, friends' server last

## Contributing

Found a dead link, a better tool, or something I missed? See [CONTRIBUTING.md](CONTRIBUTING.md). One rule: only suggest things that are maintained or historically important, and that you've actually used or can vouch for.

## License

MIT — see [LICENSE](LICENSE).

## Author

Krrish — [github.com/codewithkrrish](https://github.com/codewithkrrish). I build Minecraft bots and the tools around them; if this list saved you an evening, a star is the easiest thanks.
