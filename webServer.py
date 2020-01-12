from flask import Flask, escape, request, jsonify
import db

app = Flask(__name__)


@app.route('/activities')
def getActivities():
    activities = db.getAllActivities()
    return jsonify(activities)


@app.route('/domains')
def getDomains():
    domains = db.getAllDomains()
    return jsonify(domains)


@app.route('/segments')
def getSegments():
    segments = db.getAllSegments()
    return jsonify(segments)
