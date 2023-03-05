from flask import Flask, render_template, request, jsonify
import requests 
import json
from urllib.parse import urlparse
import os
def get_route(url):
    parsed_url = urlparse(url)
    base_domain = parsed_url.netloc
    route = parsed_url.path
    if parsed_url.query:
        route += '?' + parsed_url.query
    if parsed_url.fragment:
        route += '#' + parsed_url.fragment
    return route

def jsongen(url):
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "X-Forwarded-For": "IN"
}
    res = requests.get(url, headers = headers)
    y = json.loads(res.text)
    return y

def get_results(link):
    details_api = "https://seo.mxplay.com/v1/api/seo/get-url-details?url="
    response = jsongen(details_api+get_route(link))
    type = response['data']['type']
    id = response['data']['id']
    video_api=f"https://api.mxplay.com/v1/web/detail/video?type={type}&id={id}"
    video_response = jsongen(video_api)
    stream = []
    for x in video_response['stream'].values():
        if isinstance(x, str):
            if ".m3u8" in x:
                stream.append(x)
        if isinstance(x,dict):
            for y in x.values():
                if isinstance(y,str):
                    if ".m3u8" in y:
                        stream.append(y)
    return stream



app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        link = request.form['link']
        try:
            if not "https" in get_results(link)[0]:
                link = "https://media-content.akamaized.net/" + get_results(link)[0]
                data = ":-)"
            else:
                link = get_results(link)[0]
                data = ":-)"
        except:
            data = "Error! Pass the url of page containing player."
            link = None
        return render_template('results.html', link=link, data = data)
    else:
        return render_template('index.html')

@app.route('/url',methods = ['GET'])
def url():
    link = request.args.get("u")
    try:
        if not "https" in get_results(link)[0]:
            data = "https://media-content.akamaized.net/" + get_results(link)[0]
        else:
            data = get_results(link)[0]
    except:
        data = "Error! Pass the url of page containing player."
    
    return data,200


@app.route('/log',methods=["GET"])
def log():
    ip = request.args.get("ip")
    route = request.args.get("r")
    token = os.environ.get("TOKEN")
    chat = os.environ.get("CHAT")
    url = f"http://ip-api.com/json/{ip}"
    data = "mxplayer"+ "\n" + route + "\n" + str(jsongen(url))
    posturl = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat}&text={data}"
    requests.get(posturl)
    return "success!`" 
if __name__ == '__main__':
    app.run(debug=True)
