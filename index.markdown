---
layout: default
title: "The Comedy Conspiracy: A Data-Driven Mystery"
---

<div style="text-align: center;">
  <img src="assets/img/image1.png" alt="Illustration1" width="600">
</div>

#### “ What makes a comedy great ? ”

<hr style="border: none; border-top: 2px solid white; margin: 20px 0;">

## Act 1: The Mystery Unfolds

"Welcome to the Comedy Conspiracy, where we investigate the secret ingredients of cinematic laughter. Some say it’s all about the plot. Others claim it’s the actors or the timing of the release. But what if it’s a combination of things we’ve never considered? Our first clue lies in the numbers."

### Act 1, Scene 1: The Sentiment Sleuths

<div style="text-align: center;">
  <img src="assets/img/detective_sticker.png" alt="Illustration2" style="float: right; width: 200px; margin-left: 20px;">
</div>


<iframe src="assets/data_story_graphs/1_1.html" style="width: 100%; height: 500px; border: none;"></iframe>
<iframe src="assets/data_story_graphs/1_2.html" style="width: 100%; height: 500px; border: none;"></iframe>
<iframe src="assets/data_story_graphs/1_3.html" style="width: 100%; height: 500px; border: none;"></iframe>
<iframe src="assets/data_story_graphs/1_4.html" style="width: 100%; height: 500px; border: none;"></iframe>


The correlation between the sentiment analysis mean scores and the ratings of the user is quite low (<0.4) and does not permit drawing conclusions on the accuracy of these factors to validate if a movie is ‘good’. Indeed, low correlation value and high spreading of the points show that a rating does not necessarily reflect the sentiment transmitted by the review. A bias that could have been expected would be to observe more positive sentiment for comedies than for other types of movies. Even though the 2 groups are significantly different, statistically speaking, comedies do not display much higher sentiment scores than other types of movies.

<iframe src="assets/data_story_graphs/2_1.html" style="width: 100%; height: 500px; border: none;"></iframe>
<iframe src="assets/data_story_graphs/2_2.html" style="width: 100%; height: 500px; border: none;"></iframe>

While comedies are generally thought to spread joy, sentiment analysis shows their emotional impact isn’t much higher than other genres. A low correlation between ratings and sentiment tells us that being “happy” doesn’t guarantee being “good.”

**Detective:** “So you’re telling me people’s feelings don’t always match the stars they give? Reviews are too subjective. Let’s dig into some numerical parameters” 

<hr style="border: none; border-top: 2px solid white; margin: 20px 0;">


## Act 2: The Case of the Missing Awards

<div style="text-align: center;">
  <img src="assets/img/clown_on_red_carpet.png" alt="Illustration3" width="500">
</div>

**Detective:** "Comedies rarely walk the red carpet, but why? Our next stop takes us to the glamorous world of Oscars and critical acclaim." 

### Act 2, Scene 1: The Award Alibi

<iframe src="assets/data_story_graphs/3.html" style="width: 100%; height: 500px; border: none;"></iframe>
<iframe src="assets/data_story_graphs/4.html" style="width: 100%; height: 500px; border: none;"></iframe>

**Detective:** “Look at this—100% of Oscar-winning films from Slovenia are comedies. Impressive, until you realize… they’ve only won one Oscar.”

To uncover which countries produce the most critically acclaimed comedies, we analyzed Oscar nominations and wins. By calculating the percentage of Oscar-winning comedies out of all award-winning films from each country, we uncovered some unexpected insights.
Countries like Slovenia, Azerbaijan, Zimbabwe, and Bosnia and Herzegovina boast a 100% success rate for comedies—every Oscar-winning film from these nations is a comedy. However, a deeper look at the data reveals that these perfect scores come from a single Oscar win in each country, which happened to be for a comedy.

To get a more balanced perspective, we examined the tradeoff between the total number of critically acclaimed films and the percentage that are comedies. This reveals Ireland as a standout destination for finding high-quality, critically praised comedies.

**Detective:** "So Ireland’s got the goods. But what about the rest of the world? Time to follow the money."

<hr style="border: none; border-top: 2px solid white; margin: 20px 0;">


## Act 3: The Measure of Success

**Detective:** "When it comes to comedy, the money trail doesn’t lie. But it tells a story of its own."

### Act 3, Scene 1: The Box Office Break-In

<iframe src="assets/data_story_graphs/5.html" style="width: 100%; height: 500px; border: none;"></iframe>
<iframe src="assets/data_story_graphs/10.html" style="width: 100%; height: 500px; border: none;"></iframe>

**Detective:** “The USA dominates in absolute dollars, but Serbia’s punching above its weight in comedy percentages. Small fish, big laughs.”

Comedy consistently contributes to box office revenues across countries, with some nations showing particularly strong reliance on this genre.Even though comedies revenues represent a smaller percentage of the United States box office revenues than Serbia or Montenegro, in absolute value  it is still more profitable to make a comedy in the USA, since the United State of America produces such an important part of the movies.

Despite differences in scale, one thing is clear: comedy consistently contributes to box office success worldwide. But financial triumph doesn’t always align with critical acclaim. The team devises a “Popularity Score” to crack the code.

<div style="text-align: center;">
  <img src="assets/img/detective_sticker.png" alt="Illustration2" style="float: right; width: 100px; margin-left: 20px;">
</div>

**Detective:** "Indeed the money is important, but in order to measure the success of a comedy shouldn’t we also look at its popularity?"

### Act 3, Scene 2: The Popularity Analysis

GRAPH

The scatter plot illustrates the relationship between audience scores (X-axis) and critics' scores (Tomato Meter, Y-axis) for comedies. A clear positive correlation is visible, it shows significant variability and underlines the difference between experts and non-experts.

**Detective:** "Audience and critic perceptions often diverge, a good score from both of them brings us close to  what could be called a ‘good’ comedy."


<hr style="border: none; border-top: 2px solid white; margin: 20px 0;">


## Act 4: The Comedies Anatomy

<div style="text-align: center;">
  <img src="assets/img/Detective_and_chalkboard.png" alt="Illustration4" width="500">
</div>

**Narrator:** "With the bigger picture in focus, we dive into the finer details. What makes audiences laugh, and why does it work?"

### Act 4, Scene 1: The Genre & Topics Investigation

**Narrator:** "Throughout the age of cinema the trends have evolved, we need to be up to date with the comedy movie landscape in order to make the best of the situation."

<iframe src="assets/data_story_graphs/6.html" style="width: 100%; height: 500px; border: none;"></iframe>

The evolution of the genres that can be found in comedy movies throughout the decades is represented in this graph. The variety of genres associated with comedies have not stopped growing since the Hollywood golden age, while some genres are always well represented throughout the year such as *comedy-drama* there are some newcomers for example the 2010’s have seen the emergence of the *Horror comedy* genre.

What topics, based on plot summary analysis, are the 

GRAPH

Evolution of movie topics

*Love* and *money* emerge as a consistently prominent theme, showing a steady and positive proportion throughout the decades, reinforcing their timeless important role in the comedy genre. War exhibits a declining trend after the 1940’s, this could be due to the post-traumatic period of the second world war.

GRAPH

Evolution of movie topics in box office revenues

**Detective:** "The same themes appear across all box-office revenue ranges, but their proportions vary, topics like *love* and *money* dominate in higher revenue brackets."

For a producer aiming to maximize box office revenues, focusing on a comedy with a *love* theme is a statistically safer bet than a comedy centered around the gender theme. While a gender-themed comedy can still achieve success, romantic comedies have a higher probability of thriving at the box office, making them a more reliable choice for financial success.

GRAPH

The heatmap illustrates the frequency of sub-genre combinations in comedy movies, with darker colors representing lower occurrences and brighter colors indicating higher occurrences.
Insight : The data reveals that certain sub-genre pairings, like romantic comedies or family-oriented films, are tried-and-true formulas in the domain. Less common combinations, such as comedies incorporating "Thriller" or "Crime," could offer opportunities for innovation but might also come with higher risks of negative reactions due to their niche nature.

**Detective:** "Romance rules, and family-friendly laughs are always a hit, but hey—there’s gold in those untapped niches if you’ve got the guts to dig for it."

<iframe src="assets/data_story_graphs/7.html" style="width: 100%; height: 500px; border: none;"></iframe>

The success of comedy genres varies significantly based on the cultural and regional context in which a movie is produced. For instance, if we aim to produce a successful comedy in the USA, a *romantic comedy* would maximize our chances of success. Conversely, in France, a **comedy-drama* would be the ideal choice, it certainly aligns better with the tastes of the French viewers. Understanding these regional nuances is crucial for tailoring comedic elements to the audience's cultural expectations.

**Detective:** "Comedy is a chameleon—it changes its colors depending on where it’s born. In the U.S., love gets the laughs, but in France, it’s the drama that seals the deal."

<div style="text-align: center;">
  <img src="assets/img/detective_sticker.png" alt="Illustration2" style="float: right; width: 100px; margin-left: 20px;">
</div>

**Detective:** "Comedy is a chameleon—it changes its colors depending on where it’s born. In the U.S., love gets the laughs, but in France, it’s the drama that seals the deal."


### Act 4, Scene 2: The Collaboration Chronicles


Average revenue of the duos with most collaborations

GRAPH

One-time duos that generated more revenues 

GRAPH

GRAPH

The most successful comedies aren’t necessarily those featuring recurring duos. Instead, for pairs that have collaborated in only one movie, the same names appear repeatedly : Johnny Depp, Keith Richards, Greg Ellis… 

We can conclude that success isn’t limited to acting alone, music and direction also play integral roles in creating hit films.

**Detective:** “Comedy’s a team sport. Chemistry isn’t just on-screen—it’s behind the camera too.”

### Act 4, Scene 3: Don’t push your success too far !

**Detective:** "Sequels often face a tough crowd. Can they maintain the magic of the original?"

GRAPH

Evolution of audience scores for some movies and their sequels

Features:
- Interactive movie selection: A dropdown menu allows to choose a specific movie, displaying its sequels and corresponding audience scores.
- Trend visualization: The graph highlights how audience ratings evolve, from the original film to its sequels.

The data reveals a common trend: sequels often experience a decline in popularity over time, reflected in progressively lower audience scores.

GRAPH

The dynamic graph charts the evolution of audience scores across movie franchises and their sequels. On the horizontal axis, we see movie titles paired with their release years, while the vertical axis tracks audience scores. Each point represents a sequel group, with bubble sizes reflecting the number of films in each category.

Insights:
- The decline: Original films (Sequel 1) boast the highest average audience score (~67) across 89 films. However, Sequel 2 experiences a steep drop (~50), despite having an equally large sample size.
- Survival of the fittest: Beyond Sequel 2, only the most successful franchises endure. By Sequel 3, the pool shrinks to just 14 films, and numbers dwindle further for Sequels 4 and 5.
- Lessons from the data: Franchises often lose their charm with sequels, leading studios to discontinue less popular series. Yet, those that retain audience favor evolve into iconic multi-sequel sagas.

<div style="text-align: center;">
  <img src="assets/img/detective_sticker.png" alt="Illustration2" style="float: right; width: 100px; margin-left: 20px;">
</div>

**Detective:** "The numbers don’t lie—most sequels struggle to keep audiences entertained. But those that succeed? They redefine cinematic legacy."

<hr style="border: none; border-top: 2px solid white; margin: 20px 0;">


## Act 5: The Final Puzzle Pieces

### Act 5, Scene 1: The Title Trap

<div style="text-align: center;">
  <img src="assets/img/Perfect_title.png" alt="Illustration5" width="400">
</div>

Titles have the unique challenge of encapsulating a movie's essence in just a handful of words. In comedy, certain keywords not only resonate deeply with audiences but also appear consistently in the titles of successful films.

GRAPH

The graph highlights popular words from comedy titles, with the size of each point representing the frequency of that word in successful films. The X and Y axes organize these words by their meanings, forming clusters of similar themes.

Frequently occurring humor-related keywords, such as ***Adventure*, *Love*, and *Crazy*, dominate the titles of hit comedies.

**Detective:**"A title’s like a first impression, choose the right words, and you could get the audience attention before the first laugh."

### Act 5, Scene 2: Timing Is Everything !

<div style="text-align: center;">
  <img src="assets/img/Calendar_june.png" alt="Illustration6" width="400">
</div>

**Detective:** "When it comes to box office success, timing can make or break a movie."

<iframe src="assets/data_story_graphs/8.html" style="width: 100%; height: 500px; border: none;"></iframe>

From the graph, it’s evident that releasing a movie in June significantly boosts its chances of performing well at the box office. This trend holds true not just for comedies but for films across all genres.

<iframe src="assets/data_story_graphs/9.html" style="width: 100%; height: 500px; border: none;"></iframe>

Interestingly, since the 1980s, the proportion of comedy movies released has been relatively low compared to their contribution to box office revenues. This imbalance highlights the genre’s enduring popularity and profitability, showing that comedies remain a lucrative choice for filmmakers.

<div style="text-align: center;">
  <img src="assets/img/detective_sticker.png" alt="Illustration2" style="float: right; width: 100px; margin-left: 20px;">
</div>

**Detective:** "June’s the sweet spot—and comedy, it seems, has been pulling its weight and then some."

## Act 6: The Big Reveal

<div style="text-align: center;">
  <img src="assets/img/pic_conclu.png" alt="Illustration6" width="500">
</div>

**Detective:** "After unraveling the numbers, the themes, and the trends, it’s clear that crafting a successful comedy is both an art and a science. From timeless themes like love that resonates with audiences across decades, to the importance of timing, titles, and cultural context, the formula is anything but simple. A strong collaboration behind the scenes and a balance between audience and critic expectations are key ingredients. While sequels often fails, the right mix of originality and familiarity can keep the comedy genre going. Remember, comedy may be subjective, but if you get it right, the rewards are universal. Case closed !"

<hr style="border: none; border-top: 2px solid white; margin: 20px 0;">


## Epilogue: The Prediction Machine

<div style="text-align: center;">
  <img src="assets/img/detective_sticker.png" alt="Illustration2" style="float: right; width: 200px; margin-left: 20px;">
</div>

*The detective pins a final chart to the wall, a prediction model that takes all these factors into account.*

**Detective:** “We’ve cracked the case. Now, let’s test it. Who’s ready to laugh?”

*The screen fades to black, with the words: “Coming Soon: The Ultimate Comedy”*

## References