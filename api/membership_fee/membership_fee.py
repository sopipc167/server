from flask import Flask, request
from flask_restx import Resource, Namespace
from database.database import Database

membership_fee = Namespace('membership_fee')