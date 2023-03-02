from flask import Flask, render_template, request
import requests 
import json
from urllib.parse import urlparse

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
    res = requests.get(url)
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

if __name__ == '__main__':
    app.run(debug=True)
