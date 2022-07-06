use std::error::Error;
use reqwest::header::USER_AGENT;
use scraper::{Html, Selector};
use teloxide::prelude::*;
use teloxide::types::ParseMode;

pub async fn scrap_notice_site(
    bot: &AutoSend<Bot>,
    message: &Message,
) -> Result<(), Box<dyn Error + Sync + Send + 'static>> {
    // Carbon whyred URL
    let url = "";
    let blocking_task = tokio::task::spawn_blocking(move || {
        let client = reqwest::blocking::Client::new();
        let req = client
            .get(url)
            .header(USER_AGENT, "Tracker")
            .send().unwrap();
        let _status = req.status().is_success();
        let content = req.text().unwrap();

        let fragment = Html::parse_fragment(&content);
        let selector = Selector::parse(r#"a[rel="bookmark"]"#).unwrap();

        // Select the nth(0) of &selector as we want the latest published notice
        let url = fragment
            .select(&selector)
            .nth(0)
            .unwrap()
            .value()
            .attr("href")
            .unwrap()
            .replace(" ", "%20");

        let atext = fragment
            .select(&selector)
            .nth(0)
            .unwrap()
            .text().collect::<String>();

        let final_html = client.get(url).header(USER_AGENT, "Tracker").send().unwrap();
        let fragment_final = Html::parse_fragment(final_html.text().unwrap().as_str());

        let selector_final = Selector::parse(r#"a[class="pdfemb-viewer"]"#).unwrap();

        // Select the "pdfemb-viewer" class from the &fragment_final
        let url = fragment_final
            .select(&selector_final)
            .nth(0)
            .unwrap()
            .value()
            .attr("href")
            .unwrap()
            .replace(" ", "%20");

        vec![atext, url]
    }).await?;

    let data = format!("<b>New Notice(s) Found</b>\n\n<a href=\"{}\">{}</a>", 
                            blocking_task[1], blocking_task[0]);

    bot.send_message(message.chat.id, 
        data.as_str())
        .parse_mode(ParseMode::Html).disable_web_page_preview(true).await?;
    Ok(())
}