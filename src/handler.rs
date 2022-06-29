use crate::commands::Command;
use crate::modules::echo::echo;
use std::error::Error;
use teloxide::prelude::*;

pub async fn answer(
    bot: AutoSend<Bot>,
    message: Message,
    command: Command,
) -> Result<(), Box<dyn Error + Send + Sync>> {
    match command {
        Command::Echo(text) => {
            echo(&bot, &message, text).await?;
        }
        Command::Help => {
            bot.send_message(message.chat.id, "Message!").await?;
        }
        Command::Username(username) => {
            bot.send_message(message.chat.id, format!("Your username is @{username}."))
                .await?;
        }
    };
    Ok(())
}
