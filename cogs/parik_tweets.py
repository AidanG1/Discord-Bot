tweets = [
    'Good morning everyone. Since $TSLA hit my previous price target I spent last night doing some more analysis. I am proud to say I am very bullish. My revised price target is $1,264. I calculated this by taking the current share price and adding the $600 stimulus check.',
    "If you own #bitcoin you do NOT have to worry about Biden's tax plan",
    "Don't cry because it's falling. Smile because it rose.",
    "If we simply rebranded #bitcoin with a picture of a cute dog it would go back up to $60K",
    '"I was right all along!" - Peter Schiff, who called #bitcoin a scam at $300',
    "If you liked #bitcoin at $60,000 you'll LOVE it at $30,000",
    "To stop inflation the Fed should start burning money instead of printing money",
    "My portfolio is down 69% but after dividends it's down 68% so in reality I'm actually up 1%",
    "Elon Musk has made it so that instead of losing money 5 days this week I lost money 7 days this week",
    '"If you only do what you can do you will never be more than you are now" - Master Shifu',
    "Everyone gangsta till Elon Musk tweets something",
    "Elon Musk is playing chess while we're all playing checkers",
    "The CDC has said that you still have to wear a mask if your portfolio is down YTD",
    "Me: I hate the Fed\nAlso me: The stock market is crashing where is the Fed?!",
    "Okay hear me out. Inflation, but for my portfolio.",
    'The year is 2025. Crude oil is trading at $200 a barrel. The average home costs a million dollars. The Fed still views inflation as "transitory".',
    "We only have two lives. The second begins when we realize that YOLOing money into companies without revenue isn't an investment strategy.",
    "If I were the climate I would simply not change",
    "Finance students will literally put $100 into bitcoin and then lecture everyone about escaping the rat race",
    "I was today years old when I found out that the green new deal is about the environment and not weed",
    "According to Melinda Gates, Bill just didn't Excel at his marriage. Apparently he had no Power Points in bed, and he always had to have the last Word.",
    "If you're looking for clues as to why Bill Gates's marriage failed, the words micro and soft should tell you enough",
    "Surprised Melinda didn't leave Bill Gates after Windows Vista was released tbh",
    "Bill Gates divorcing his wife Melinda Gates after reportedly seeing Melinda using a macbook",
    "Bill Gates should marry Mackenzie Scott and Jeff Bezos should marry Melinda",
    "If Warren Buffett smoked weed he'd be called Warren Puffett",
    "Okay hear me out. Tinder, but matching people based on their stock picks.",
    "Why does it take five weeks to lose just a little bit of weight but only five minutes to lose half my portfolio?",
    "If you think lumber is expensive here just wait until someone mints an NFT of a log",
    "The Treasury should just insider trade instead of raising taxes",
    "People will literally spend more time writing up a $50 shopping weekly list than a $5,000 watchlist for stocks",
    "Twitter is incredible. We all went from maritime shipping experts to commodities experts to tax experts in the space of a month.",
    "I'm not worries about Biden's capital gains tax. My portfolio is down 69% YTD. Guess I'm just built different.",
    "If you think Dogecoin is a joke just wait until you see the Fed's balance sheet",
    "When Dogecoin hits $100k I'm gonna buy Goldman Sachs and rename it Parikman Sachs",
    "Imagine saving all your life and investing regularly so you can stop working at 65 only to be beaten to retirement by some teenager who YOLOd his savings on Dogecoin",
    "It is better to have traded and been margin called than to have never traded at all",
    "If coinbase simply did a 4-1 stock split their valuation would quadruple from here",
    "If you think Coinbase is expensive here just imagine what the valuation would be if their CEO tweeted memes and told the SEC to suck his cock",
    "Nikola is still a great environmentally friendly vehicle company because rolling a truck down a hill releases zero carbon emissions",
    "Men will literally lever up their fund by 500% and lose $110 billion instead of going to therapy",
    "The price of a big mac could hit $1,000 and the Fed would still say they see no signs of inflation",
    'Can I refund my stocks back to their previous owners for the original price?',
    'Good morning to everyone except for the moron who got stuck in the Suez Canal',
    'Gamestop ecommerce sales were up 175%. With this growth the company could eventually be bigger than Amazon!',
    '$GME misses on revenue and EPS but who the hell cares because we like the stock',
    'GameStop management should’ve done their earnings call on clubhouse imo',
    'A year ago today the stock market bottomed out and went on an epic tear to hit new all time highs but you didn’t get to ride any of that because you panic sold at the top and were too scared to buy the dip',
    'If the treasury just invested all their money in $TSLA stock we could wipe out the whole national debt within a few years',
    'Crazy to think how the popular image of tech went from nice guys who wear hoodies to evil manipulators who control the world',
    'Nobody:\nNot a single damn soul:\nFinance TikTok: “Here’s how you can turn your $1,400 stimulus check into a million dollars in just three easy steps”',
    'Yeah I work 9-5\n9am to 5am',
    'Yeah sex is good but have you ever bought at the bottom and sold at the top because me neither',
    'Maybe it was never about the stocks but the bonds we made along the way',
    'Just received my $1,400. Gonna name my kid Stimothy.',
    'You’re in her DMs. I’m in her email inbox sending her the latest broker reports and helping her find new ways to generate consistent risk-adjusted alpha. We aren’t the same bro.',
    'So I just found out that Warren Buffett is now worth ,over $100 billion. That means he could literally give a billion dollars to every person on earth and still have $93 billion left. Some people are so greedy.',
    'Okay so apparently the real reason Gamestop just dropped is because investors are rotating from value stocks like $GME to tech stocks like $RBLX',
    'Gamestop is like bitcoin and all the other meme stocks are like alt-coins',
    '$TSLA now has a P/E ratio of just 942. This makes it a generational buying opportunity.',
    'Gamestonk!!',
    '“These SPACs feel like the DotCom bubble all over again” - Jimmy, an 11 year old kid who wasn’t alive during the DotCom bubble',
    'Jeff Bezos is retiring at the old age of 57! Did you know that you could retire much earlier by making your coffee at home and investing in a low cost S&P 500 index fund?',
    'Imagine hiring dozens of guys with MBAs and PhDs and paying them 6 figure salaries only for your fund to be down 53% in one month',
    'The best performing assets of 2021 are:\n- A failing video game retailer\n- A cinema chain close to bankruptcy\n- A dog-themed cryptocurrency',
    "Chamath hasn't even lost his virginity because he never loses",
    "Michael Burry is that annoying kid who did something cool once and now thinks he's relevant in every situation known to man",
    "deleted all my dating apps because I want to meet somebody the old fashioned way (arranged marriage)",
    "THREAD: One year ago I had 0 followers. Today, I have over 300,000. Here's how I did it Down pointing backhand indexDown pointing backhand index\nPosted some dank memes lol",
    'The devil works hard but Dr. Parik Patel, BA, CFA, ACCA Esq. works harder',
    'If Warren Buffett married Elizabeth Warren and took her surname he’d be called Warren Warren',
    'The Fed be like "the internet outage is only transitory"',
    'Maybe the President of El Salvador is Satoshi Nakomoto',
    'If I were a member of Congress I too would trade using inside information',
    'Reasons to become a member of Congress:\nFight inequality ❌\nSolve climate change ❌\nTrade using inside information :white_check_mark:',
    'Top 5 hedge fund managers:\n- George Soros\n- Jim Rogers\n- Bill Ackman\n- Ray Dalio\n- Nancy Pelosi',
    "On this day in 1994, Amazon was founded by Jeff Bezos in his garage.\nIf he didn't have a garage, there would be no Amazon.\nLesson? If you want to build a company, first build a garage.",
    'Why buy a lobster roll when you can buy a kebab roll?',
    'Tinder profiles should require resumes where you list your dating history and experience',
    'Sure the fire in the Gulf of Mexico looked bad but wait until you see my portfolio',
    'If George Washington were alive today he would tell you to buy bitcoin',
    'The declaration of independence clearly states that the stock market should be open at the weekend',
    'They didn’t risk their lives in 1776 so you could short 130% of the float of an illiquid meme stock',
    'Happy Fourth of July to everyone except for short sellers',
    'Men will literally set fire to water instead of going to therapy',
    'Yeah sex is good but have you ever set the sea on fire?',
    "Ladies if he:\n- Keeps calling you margin\n- Sells your data to Citadel\n- Shuts you down \n- Misleads you\nHe's not your man. He's the trading app Robinhood.",
    'If you try to short the Robinhood IPO on Robinhood Vlad will personally issue you a margin call',
    'Robinhood should IPO under the ticker $ROB it would be more accurate',
    'If I were Robinhood I would simply call myself Citadel Securities',
    'Newly released data shows that police officers are the biggest investors in the Krispy Kreme IPO',
    "If I were the Fed I would simply not tell people that I'm printing more money",
    "Imagine being a portfolio manager and spending hundreds of hours of your life analyzing stocks only to outperform the S&P 500 by 2% when you could've just invested in dogecoin and been up 4,200% YTD",
    'Peter Thiel has a $5 billion tax free pot of money in his Roth-IRA after building PayPal, Palantir, and running his own venture capital fund. If he had simply grown and sold tomatoes, he would have a $10 billion pot of money. Scale matters. Few understand this.',
    'If I had a $5 billion Roth-IRA I would blow it all on out-of-the-money options',
    'Crypto\nCrypt\nCryp\nCry :cry:',
    'BREAKING: Nancy Pelosi reportedly bought $3,000,000 of call options on the Taliban just hours before they stormed Afghanistan.',
    'OnlyFans banning porn is like LinkedIn banning obnoxious humblebrags',
    'OnlyFans without porn is like Dr. Parik Patel without the BA, CFA, ACCA Esq.',
    'You’ve just taken over a country. Do you?\na) fix the treasury\nb) rebuild the army\nc) ride bumper cars with an m-16',
    'Have we tried simply getting a group of celebrities to make a motivational video asking the Taliban to stop',
    "The secret to becoming extremely wealthy isn't saving and investing. It's selling a JPEG of a rock for $200,000.",
    'Every CNBC market headline is like stocks rise/fall because [COVID / inflation / interest rates]',
    "I can't wait till Robinhood suspends trading on its own stock for going down"
]