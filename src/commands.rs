use teloxide::utils::command::BotCommands;

#[derive(BotCommands, Clone)]
#[command(rename = "lowercase", description = "These commands are supported:")]
pub enum Command {
    #[command(description = "display this text.")]
    Help,
    #[command(description = "Echo text.")]
    Echo(String),
    #[command(description = "Stream a tweet from a user")]
    Stream(String),
    #[command(description = "Exec a shell command")]
    Exec(String),
}
