use crate::commands::Command;
use crate::modules::miscellaneous::echo;
use crate::modules::miscellaneous::exec_cmd;
use crate::modules::stream_tweets;
use std::error::Error;
use teloxide::prelude::*;

pub async fn answer(
    bot: AutoSend<Bot>,
    message: Message,
    command: Command,
) -> Result<(), Box<dyn Error + Send + Sync>> {
    match command {
        Command::Exec(text) => {
            if message.from().unwrap().id == teloxide::prelude::UserId(1154905452) {
                exec_cmd(&bot, &message, text).await?;
            } else {
                bot.send_message(
                    message.chat.id,
                    format!(
                        "Retards like {:?} aren't authorized.",
                        message.from().unwrap().username
                    ),
                )
                    .await?;
            }
        }
        Command::Echo(text) => {
            echo(&bot, &message, text).await?;
        }
        Command::Help => {
            bot.send_message(message.chat.id, "Help message").await?;
        }
        Command::Stream(_username) => {
            if message.from().unwrap().id == teloxide::prelude::UserId(1154905452) {
                stream_tweets::stream(&bot, &message, _username).await?;
            } else {
                bot.send_message(
                    message.chat.id,
                    format!(
                        "Retards like {:?} aren't authorized.",
                        message.from().unwrap().username
                    ),
                )
                .await?;
            }
        }
    };
    Ok(())
}
