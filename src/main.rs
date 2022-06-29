mod commands;
mod handler;
mod modules;

use crate::commands::Command;
use crate::handler::answer;
use teloxide::{prelude::*, utils::command::BotCommands, Bot};

#[tokio::main]
async fn main() {
    // Initialising pretty_env_logger
    pretty_env_logger::init();
    log::info!("Starting TrishnaBot...");

    let bot = Bot::from_env().auto_send();
    teloxide::commands_repl(bot, answer, Command::ty()).await;
}
