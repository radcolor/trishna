use std::error::Error;
use std::fs;
use std::path::PathBuf;
use std::process::Command as ExeCmd;
use teloxide::prelude::*;
use teloxide::types::{InputFile, ParseMode};
use teloxide::utils::html::escape;

pub async fn echo(
    bot: &AutoSend<Bot>,
    message: &Message,
    text: String,
) -> Result<(), Box<dyn Error + Sync + Send + 'static>> {
    bot.send_message(message.chat.id, text).await?;
    Ok(())
}

pub async fn exec_cmd(
    bot: &AutoSend<Bot>,
    message: &Message,
    command: String,
) -> Result<(), Box<dyn Error + Sync + Send + 'static>> {
    if message.from().unwrap().id == teloxide::prelude::UserId(1154905452) {
        let shout = ExeCmd::new("bash")
            .arg("-c")
            .arg(command)
            .output()
            .expect("FAIL");
        if String::from_utf8_lossy(&shout.stdout).chars().count() > 2500 {
            fs::write("output.txt", &shout.stdout).expect("Unable to write file");

            let file = InputFile::file(PathBuf::from("output.txt"));

            bot.send_document(message.chat.id, file)
                .parse_mode(ParseMode::Html)
                .reply_to_message_id(message.id)
                .await?;
        } else {
            bot.send_message(
                message.chat.id,
                format!(
                    "<i>{}</i>
<code>{}</code>
<code>{}</code>",
                    shout.status,
                    escape(&String::from_utf8_lossy(&shout.stdout)),
                    String::from_utf8_lossy(&shout.stderr)
                ),
            )
            .parse_mode(ParseMode::Html)
            .reply_to_message_id(message.id)
            .await?;
        }
    } else {
        bot.send_message(
            message.chat.id,
            format!("Retards like {:?} aren't authorized.", message.from().unwrap().username),
        )
        .await?;
    }
    Ok(())
}
