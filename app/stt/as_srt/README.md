Reference:
> https://www.lifewire.com/srt-file-4135479

## How to Create an SRT File
You can build your own SRT file using any text editor, so long as you keep the format correct and save it with the .SRT file extension. However, an easier way to build your own subtitle file is to use a dedicated tool, such as Aegisub or Jubler.

An SRT file has a particular format it has to exist in. Here's an example of just a snippet from one:

```
 1097
01:20:45,138 --> 01:20:48,164
You'd say anything now
to get what you want.
```

Here's what those lines mean:

- The first number is the order that this subtitle chunk should take in relation to all the others. In the full SRT file, the next section is called 1098, and then 1099, and so on.
- The second line is the timecode for how long the text should be displayed on the screen. It's set up in the format of HH:MM:SS,MIL, which is hours:minutes:seconds,milliseconds. This explains how long the text should display on the screen. In that example, those words would remain on the screen for about 3 seconds (48-45 seconds).
- The other lines are the text that should show up during the time period defined right above it.

After one section, there needs to be a line of blank space before you start the next, which in this example would be:

```
1098
01:20:52,412 --> 01:20:55,142
You want to feel sorry for yourself,
don't you?
```

Nothing special needs to be included at the very start or end of the SRT file. Just start and end like you'd write the examples we've given here.

The very end of this file might look something like this:

```
1120
01:33:50,625 --> 01:33:52,293
This is finally the end.
```