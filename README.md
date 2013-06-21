Fism
====

Fism<sup><a href="#fn1" id="ref1">1</a></sup> is a tool for Podcasters using one, two or all of the following list:

1. [Auphonic](http://auphonic.com)
2. [Firtz](http://github.com/eazyliving/firtz)
3. [App.net](http://app.net)

It has three modules handling these three use cases.

## 1. Auphonic
The Auphonic module is a rudimentary client for the API of 
[Auphonic](http://auphonic.com). It allows starting a new production if you provide it with
* a base filename / episode slug
* an audio file
* an episode title
* an episode subtitle
* a track number
* an episode summary
* (optional) tags
* (optional) a chapters file

The module uploads the file, sets up the metadata and starts the production.

## 2. Firtz
The Firtz provides functionality to generate epi files for the podcast 
publishing solution [Firtz](https://github.com/eazyliving/firtz).
Most Firtz-users will probably use Auphonic anyway, so this module doesn't 
have to do much, since the Firtz is able to generate most of the episode 
metadata from Auphonic production data.
This module allows generating and uploading (via FTP) an epi file if you 
provide it with
* a base filename / episode slug
* (optional) ```epi_dict``` a set of key-value pairs by the user per episode to be added to 
the epi file. This is useful for example, if you want to manually adjust the 
publication date of the episode. The key-value pair would be 'date':'2013-01-01'
* (optional) ```prep_epi``` a prepared episode file this module will add to. This is useful, 
for example if you want to write extensive shownotes in the "article"-section 
of the episode file that you deem too big for the "summary"-section of 
the auphonic metadata.
* (optional) Via settings file, a set of filetypes to generate URLs for can be
specified. Typically these will be files not handled by Auphonic that are 
still part of the downloads of the episode. In my own podcast, for instance, 
these filetypes are: epub, mobi, pdf.

## 3. App.net
The App.net module let's you specify a post text, generates a link to your 
episode and posts it to your stream on [app.net](http://alpha.app.net) via an
API call.
It retains the post ID and can write it to the epi file for the Firtz. This 
enables using the app.net thread as a comment thread.

**You need an app.net token to use this.** You can get one if you either have a 
developer account or you can get one using Jonathan Duerig's service [Dev-Lite](http://dev-lite.jonathonduerig.com).
Pick one with the scope "Write post".

## Usage
Fism has two command line interfaces, at the moment:

1. Single call with options
2. Interactive mode

I plan to add a GUI using PyGObject, soon.

### Single call
Run ```python fism-cli.py -h``` to see a list of the mandatory and optional 
arguments.
For example a call containing all the arguments could look like this:
```
python fism-cli.py sup001-crazy-title --audio "recordings/audio.ogg" --title "SUP001 Crazy Title" --subtitle "A moderately crazy subtitle" --summary "A boringly normal summary, containing lots of text." --track 001 --tags "some, tag, or, another" --chapters "data/chapters.txt" --epi_dict "'date':'2013-01-01', 'somekey':'somevalue'" --prep_epi "article.epi" --post "I just published a new #podcast episode: SUP001 Crazy Title"
```
In this case, Fism would upload a file called audio.ogg to auphonic, create a production with all the specified metadata and start said production. When auphonic finishes Fism would create an epi file (using a prepared epi file called article.epi to work on) adding a custom date (and some other thingy). It would upload this file to the Firtz, make a post on app.net, and then update the epi file on the server with the post id.
Long example, you get the drift. 

### Interactive
The interactive mode will ask you step by step to enter all the needed information.
For example, running
```
python fism-interactive.py
```
Will prompt you to answer:
```
What's the slug of the episode going to be? e.g. "spc001-crazy-title":
```

## Settings
All the settings that don't change with every episode, but are set up on a per 
podcast basis, are located in the settings file (default: ```settings.json```)
If you want to see an example, have a look at ```example_settings.json```.
I wrote a little interactive tool to generate a settings file. Run:
```
python setup.py
```
It will guide you through the process.

## Dependencies
Fism depends on [python-requests](http://docs.python-requests.org/en/latest/).

The app.net Module uses Simon de la Rouviere's [Python-App.net-API-Wrapper]('https://github.com/simondlr/Python-App.net-API-Wrapper), which is included in Fism.

## License
GPLv3.

If you want to use Fism or parts of it in a FLOSS project imcompatible with the
GPLv3, contact me via email (software@webdings.de) or via 
[app.net](http://alpha.app.net/hirnbloggade), I'll probably be willing to dual 
license for you.

<hr></hr>

<sup id="fn1">1. You can decide what Fism means: 1) An phonetic approximation of 
[FSM](https://en.wikipedia.org/wiki/Flying_Spaghetti_Monster), 2) A new ism, 
because it's finally time for a new ism. And if Fism is your ism, then you can 
call yourself a fist. Maybe you like that... 3) Firtz ihm seine Mama (German 
for "Firtz'ses his Mom"). More suggestions are welcome ;-) <a href="#ref1" title="Jump back to footnote 1 in the text.">↩</a></sup>
