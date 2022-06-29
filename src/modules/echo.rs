use std::error::Error;
use teloxide::prelude::*;

pub async fn echo(
    bot: &AutoSend<Bot>,
    message: &Message,
    text: String,
) -> Result<(), Box<dyn Error + Sync + Send + 'static>> {
    bot.send_message(message.chat.id, text).await?;
    Ok(())
}
