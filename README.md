# audio-extract-webapp

audio-extract-webapp is a Client-Server [Django] web application for extracting audio from video in one click!

## Features

 - Extract audio from local video file (MP4 format)
 - Extract audio from a Youtube link

## Getting Started

To get you started you can simply clone the audio-extract-webapp repository, install the dependencies and start
 converting:

### Installation
```sh
$ git clone https://github.com/o5k/audio-extract-webapp.git
$ cd audio-extract-webapp
$ pip install requirements.txt
```
### Run the project

```sh
$ ./manage.py runserver
```
Then, browse the project at http://localhost:8000

### Usage

The usage is very simple. The user can extract the audio with a simple click, by providing the source
 (browsing a local video, or providing a Youtube link) and starting the audio provisioning process.

## TODO

 - Save list of converted videos and generated audio files to database for future access
 - Avoid duplication and directly serve an already converted video
 - Support for more video formats

## Contributions

Have a suggestion? Want to contribute? Great!

Please feel free to fork the repo and make a pull request or simply create an issue if you find a bug.

## License

This project is licensed under the terms of the [MIT] license.

## Contact
To get in touch about audio-extract-webapp feel free to contact me via http://oussamakrifa.com

[Django]: https://docs.djangoproject.com/
[MIT]: http://opensource.org/licenses/MIT