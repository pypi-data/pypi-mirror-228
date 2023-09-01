<div align="center">

# BattleBit Community Server API
_A re-implementation of the official community server API for BattleBit_

[![Discord](https://img.shields.io/discord/1146329100567466074?logo=discord&label=Support%20Server&link=https%3A%2F%2Fdiscord.gg%2FSBhZ8EjNhC)](https://discord.gg/SBhZ8EjNhC)
[![Stability](https://img.shields.io/badge/Stability-stable-green)](./)
[![Stage](https://img.shields.io/badge/Stage-Beta-darkgreen)](./)
[![Official API Version](https://img.shields.io/badge/Official%20API%20Version-1.0.7.1-green)](https://github.com/MrOkiDoki/BattleBit-Community-Server-API/blob/main/CommunityServerAPI.csproj)
[![LICENSE](https://img.shields.io/badge/Licence-WTFPL-yellow)](https://git.jdrodenkirchen.de/drodenkirchen/battlebit-community-server-api/-/blob/main/LICENSE)

</div>

**ATTENTION: This project is still in Beta. You might encounter bugs sometimes. If you do, please report them via the [Discord server](https://discord.gg/SBhZ8EjNhC)**

## Preamble

The goal of this project is to create an alternate, Python-implementation to the [official community server API](https://github.com/MrOkiDoki/BattleBit-Community-Server-API), which is written in C#. This project is still under development and can not yet be considered production-ready.

## Prerequisites

- Python 3.10 or later
- A running, whitelisted BattleBit Server (Version 2.1.10)

## Usage

As a user of this API, there are two important things to know, `Handler`s and `Command`s. More on those in the following paragraphs. Basic examples on how to use this project can be found in `/battlebit_community_server_api/example`.

### Handlers

Handlers are the users way of hooking themselves onto certain events that are happening. Such as "A player joins the server" and "A player sent a chat message".

For each event, the user can register their own handler with the `ApiServer.register_handler` method. This method takes  an `OpCodes` value and any `Callable`.

**IMPORTANT:** Each handler has the signature `async def handler(d: bytes) -> bytes`. It receives the raw TCP message as an input and returns a TCP message.

Use `TcpParsingService` to parse the incoming data into the datamodel objects. Use `OutgoingGameServerMessage` to return data. Refer to the examples for further information.

#### Default Handlers

If there is no `Handler` registered for an OP-Code, the default `Handler` for that event is executed. The user can also use default `Handler`s in their own `Handler`, see `example/SendingCommands.py`.

#### Implementation status of default handlers

| Event                           | Status                                                         | Behavior                                            | Associated Parser (from `TcpParingService`) |
|---------------------------------|----------------------------------------------------------------|-----------------------------------------------------|---------------------------------------------|
| HAIL                            | ![Implemented](https://img.shields.io/badge/Implemented-green) | HAIL is accepted                                    | `parse_hail_message`                        |
| PLAYER_CONNECTED                | ![Unneeded](https://img.shields.io/badge/Unneeded-yellow)      | Event does not expect a response                    | `parse_player_connected`                    |
| PLAYER_DISCONNECTED             | ![Unneeded](https://img.shields.io/badge/Unneeded-yellow)      | Event does not expect a response                    | `parse_player_disconnected`                 |
| ON_PLAYER_TYPED_MESSAGE         | ![Implemented](https://img.shields.io/badge/Implemented-green) | Allows message via `RESPOND_PLAYER_MESSAGE`         | `parse_on_player_typed_message`             |
| ON_PLAYER_KILLED_ANOTHER_PLAYER | ![Unneeded](https://img.shields.io/badge/Unneeded-yellow)      | Event does not expect a response                    | `parse_on_player_killed_another_player`     |
| ON_PLAYER_JOINING               | ![Implemented](https://img.shields.io/badge/Implemented-green) | Official Stats are returned via `SEND_PLAYER_STATS` | `parse_on_player_joining`                   |
| SAVE_PLAYER_STATS               | ![Unneeded](https://img.shields.io/badge/Unneeded-yellow)      | Event does not expect a response                    | `parse_save_player_stats`                   |
| ON_PLAYER_ASKING_TO_CHANGE_ROLE | ![Implemented](https://img.shields.io/badge/Implemented-green) | Allows requested role change via `SetRoleTo`        | `parse_on_player_asking_to_change_role`     |
| ON_PLAYER_CHANGED_ROLE          | ![Unneeded](https://img.shields.io/badge/Unneeded-yellow)      | Event does not expect a response                    | `parse_on_player_changed_role`              |
| ON_PLAYER_JOINED_A_SQUAD        | ![Unneeded](https://img.shields.io/badge/Unneeded-yellow)      | Event does not expect a response                    | `parse_on_player_joined_a_squad`            |
| ON_PLAYER_LEFT_SQUAD            | ![Unneeded](https://img.shields.io/badge/Unneeded-yellow)      | Event does not expect a response                    | `parse_on_player_left_squad`                |
| ON_PLAYER_CHANGED_TEAM          | ![Unneeded](https://img.shields.io/badge/Unneeded-yellow)      | Event does not expect a response                    | `parse_on_player_changed_team`              |
| ON_PLAYER_REQUESTING_TO_SPAWN   | ![Implemented](https://img.shields.io/badge/Implemented-green) | Request is granted via `SPAWN_PLAYER`               | `parse_on_player_requesting_to_spawn`       |
| ON_PLAYER_REPORT                | ![Unneeded](https://img.shields.io/badge/Unneeded-yellow)      | Event does not expect a response                    | `parse_on_player_report`                    |
| ON_PLAYER_SPAWN                 | ![Unneeded](https://img.shields.io/badge/Unneeded-yellow)      | Event does not expect a response                    | `parse_on_player_spawn`                     |
| ON_PLAYER_DIE                   | ![Unneeded](https://img.shields.io/badge/Unneeded-yellow)      | Event does not expect a response                    | `parse_on_player_die`                       |
| NOTIFY_NEW_MAP_ROTATION         | ![Unneeded](https://img.shields.io/badge/Unneeded-yellow)      | Event does not expect a response                    | `parse_notify_new_map_rotation`             |
| NOTIFY_NEW_GAME_MODE_ROTATION   | ![Unneeded](https://img.shields.io/badge/Unneeded-yellow)      | Event does not expect a response                    | `parse_notify_new_gamemode_rotation`        |
| NOTIFY_NEW_ROUND_STATE          | ![Unneeded](https://img.shields.io/badge/Unneeded-yellow)      | Event does not expect a response                    | `parse_new_round_state`                     |
| ON_PLAYER_ASKING_TO_CHANGE_TEAM | ![Implemented](https://img.shields.io/badge/Implemented-green) | Allows requested team change via `SetTeamTo`        | `parse_on_player_asking_to_change_team`     |
| GAME_TICK                       | ![Unneeded](https://img.shields.io/badge/Unneeded-yellow)      | Event does not expect a response                    | `parse_game_tick`                           |
| ON_PLAYER_GIVEN_UP              | ![Unneeded](https://img.shields.io/badge/Unneeded-yellow)      | Event does not expect a response                    | `parse_on_player_given_up`                  |
| ON_PLAYER_REVIVED_ANOTHER       | ![Unneeded](https://img.shields.io/badge/Unneeded-yellow)      | Event does not expect a response                    | `parse_on_player_revived_another`           |
| ON_SQUAD_POINTS_CHANGED         | ![Unneeded](https://img.shields.io/badge/Unneeded-yellow)      | Event does not expect a response                    | `parse_on_squad_points_changed`             |
| NOTIFY_NEW_ROUND_ID             | ![Unneeded](https://img.shields.io/badge/Unneeded-yellow)      | Event does not expect a response                    | `parse_notify_new_round_id`                 |
| LOG                             | ![Unneeded](https://img.shields.io/badge/Unneeded-yellow)      | Logs will be written to logger on DEBUG level       | `parse_log`                                 |
| ON_SQUAD_LEADER_CHANGED         | ![Unneeded](https://img.shields.io/badge/Unneeded-yellow)      | Event does not expect a response                    | `parse_on_squad_leader_changed`             |
| UPDATE_NEW_GAME_DATA            | ![Unneeded](https://img.shields.io/badge/Unneeded-yellow)      | Event does not expect a response                    | `parse_update_new_game_data`                |
| UPDATE_CONNECTED_PLAYERS        | ![Unneeded](https://img.shields.io/badge/Unneeded-yellow)      | Event does not expect a response                    | `parse_update_connected_players`            |


### Commands

While Handlers are triggered on an event and respond to the server, `Command`s can be executed at any point.

To execute an `Command`, pick a `Command` from the `Command` module (for example `Command.SayToChat`), use its initializer to prepare it, and then queue it for execution.

You can also build your own commands by using the `Command` base class.

To execute a command, use `ApiServer.add_command_to_queue`.

#### Predefined commands

| Command              | Effect                                                                         |
|----------------------|--------------------------------------------------------------------------------|
| ForceStartGame       | Starts the Round                                                               |
| ForceStartGame       | Ends the Round                                                                 |
| SayToAllChat         | Sends chat message into All-Chat                                               |
| SayToChat            | Sends chat message that is only visible to a specific player                   |
| SetRoleTo            | Sets the role of player                                                        |
| SetTeamTo            | Sets the team of player                                                        |
| SetNewPassword       | Sets a new password for the server                                             |
| SetPingLimit         | Sets a new ping limit for the server                                           |
| AnnounceShort        | Displays an announcement to all players for a short duration                   |
| AnnounceLong         | Displays an announcement to all players for a long duration                    |
| UILogOnServer        | Displays a log message on the server for a set duration                        |
| SetLoadingScreenText | Sets the text that is displayed to players in the loading screen               |
| SetRulesScreenText   | Sets the text that is displayed to the players in the rules screen             |
| StopServer           | Stops the server                                                               |
| CloseServer          | Announces that the server will close                                           |
| KickAllPlayers       | Kicks every player                                                             |
| KickPlayer           | Kicks specific player, optionally with a text that is displayed to the player  |
| KillPlayer           | Kills specific player                                                          |
| SwapTeam             | Swaps specific player to the other team                                        |
| KickFromSquad        | Kicks specific player from squad                                               |
| JoinSquad            | Joins specific player into a squad                                             |
| DisbandPlayerSquad   | Disbands a squad                                                               |
| PromoteSquadLeader   | Promotes specific player to be the squadleader of the squad he is currently in |
| WarnPlayer           | Displays warn message to player                                                |
| MessageToPlayer      | Displays message to player (not in chat, use `SayToChat` if you want that)     |
| SetPlayerHp          | Sets a specific player's HP                                                    |
| DamagePlayer         | Damage specific player                                                         |
| HealPlayer           | Heal specific player                                                           |
| SetSquadPoints       | Sets squadpoints for a specific squad                                          |
| SetMapRotation       | Sets the map rotation                                                          |
| SetGamemodeRotation  | Sets the gamemode rotation                                                     |

#### Adding commands from outside

At some point you might want to queue Commands or OutgoingGameServerMessages from outside the API loop.
You can find an example doing just that at `example/SetNewRoomSettings.py`.

## Contributing

The current state of development does not yet allow for productive, cooperative contribution.

## Licence

```
           DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                   Version 2, December 2004

Copyright (C) 2023 David Rodenkirchen <davidr.develop@gmail.com>

Everyone is permitted to copy and distribute verbatim or modified
copies of this license document, and changing it is allowed as long
as the name is changed.

           DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
  TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

 0. You just DO WHAT THE FUCK YOU WANT TO.
```