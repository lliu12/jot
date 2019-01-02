Lucy Liu
CS50 Final Project: Jot

Jot is a webapp written with Python, Flask, CSS, HTML and Jinja. It allows users, once registered and logged in, to record journal
entries organized with tags. Users are offered default tags to use, but can also add tags of their own that they'd like to include.

The most challenging design choice in creating Jot was figuring out how to code the tagging system. Since different users might want
different tags, different posts might have different amounts of tags, and different tags might be associated with different amounts
of entries, there was a lot of variability to consider, which made working with SQL a little challenging. In the end, I had
three databases for users, journal entries, and tags, which worked pretty well. In a future iteration of this project, I'd like to adjust
the journal entry process so users can add as many tags as they'd like, instead of only three.

I chose to use the tagging system because in journals, people keep track of lots of different things: diary entries, song recommendations,
etc. It made sense that when going back through a journal, users would want a way to view specific content.

A design decision I'm proud of is the choice to move away from blank backgrounds and pull in a random wallpaper from Unsplash to use
as each page's background. Similarly, I made design choices to round the corners of the shapes enclosing journal entries and make
the white background behind them slightly transparent. I think these choices make the app significantly more pleasant to use.  After
all, journaling should be a pleasant and relaxing experience. For me at least, I just want to
keep using Jot to see what pictures will come up. It was actually pretty hard for me to figure out how to make the background image cover the screen
the way I wanted, but in the end I think it was worth it.
