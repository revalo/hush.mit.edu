## hush.mit.edu
[![Website](https://img.shields.io/website-up-down-green-red/http/shields.io.svg)](http://hush.mit.edu) [![Facebook](http://i.imgur.com/fep1WsG.png)](http://fb.me/hushmit)

[hush.mit.edu](http://hush.mit.edu) is an anonymous discussion forum for MIT Students

<p align="center">
	<img src="https://github.com/revalo/hush.mit.edu/raw/master/screenshot.png" alt="screenshot" width="700" />
</p>

### Getting Started

Get all the requirements,
```
pip install -r requirements.txt
```

Run your local PostgresSQL instance.

Rename `config.example.py` and `constants.example.py` and fill in the configuration details.

Start the debug server,
```
python runserver.py
```

Use gunicorn for production deployment.
```
gunicorn -b :8112 -w 4 confess:app
```

### Development

The current version heavily relies on the ORM backend to be PostgresSQL to do the ranking calculations and global level table locking for facebook posts.

### Contributing

This is fairly badly written software right now and I'd love for you to help out! The best way to contribute is to submit patches via pull requests.

### Notes

Inspired by wmoses showing me tjbash.org

<!-- Grab your social icons from https://github.com/carlsednaoui/gitsocial -->