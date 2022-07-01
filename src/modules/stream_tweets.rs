use std::env;
use egg_mode::tweet::Tweet;
use egg_mode::user::UserID;
use egg_mode::Token::Access;
use egg_mode::{tweet, KeyPair};
use regex::Regex;
use teloxide::prelude::*;
use std::error::Error;

pub async fn stream(
    bot: &AutoSend<Bot>,
    message: &Message,
    userid: String,
) -> Result<(), Box<dyn Error + Sync + Send + 'static>> {    let consumer = KeyPair::new(
        env::var("CONSUMER_KEY").unwrap(),
        env::var("CONSUMER_KEY_SECRET").unwrap(),
    );
    let access = KeyPair::new(
        env::var("ACCESS_TOKEN").unwrap(),
        env::var("ACCESS_TOKEN_SECRET").unwrap(),
    );

    let token = Access { consumer, access };

    let user_id: UserID = userid.into();
    let timeline = tweet::user_timeline(user_id, false, false, &token).with_page_size(1);

    let (_, feed) = timeline.start().await?;
    let tweet = feed.response.get(0).unwrap();

    let re = Regex::new(
        r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
    )
    .unwrap();

    println!("Tweet ID = {:?}", tweet.id);
    println!("Tweet = {:?}", re.replace_all(tweet.text.as_str(), ""));
    println!("Hashtags = {:?}", tweet.entities.hashtags);
    println!("Mentions = {:?}", tweet.entities.user_mentions);
    println!("Has media = {:?}", tweet_has_media(&tweet).await);

    if tweet_has_media(&tweet).await == false {
        bot.send_message(message.chat.id, re.replace_all(tweet.text.as_str(), ""))
            .await?;
    }
    Ok(())
}

pub async fn tweet_has_media(tweet: &Tweet) -> bool {
    tweet.extended_entities.is_some() || tweet.entities.media.is_some()
}
