import pymongo
from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv()
mongodb_cloud_db_key = os.environ.get('MONGODB_CLOUD_DB_KEY')

# Functions to get/put data from the database


def mongodb_connection():
    # Establish Connection with MongoDB
    client = pymongo.MongoClient(
        f"mongodb+srv://altafz:{mongodb_cloud_db_key}@zeeshan.ybtmt9f.mongodb.net/?retryWrites=true&w=majority&appName=zeeshan")
    return client


def insert_period(period_data):
    client = mongodb_connection()
    db = client["Income_Expense_Tracker"]
    coll1 = db["monthly_reports"]
    coll1.insert_one({"period": period_data})


def get_period(period):
    client = mongodb_connection()
    db = client["Income_Expense_Tracker"]
    coll1 = db["monthly_reports"]
    for period in coll1.find({"period.Period": period}, {"_id": 0}):
        return period['period']


def get_all_periods():
    client = mongodb_connection()
    db = client["Income_Expense_Tracker"]
    coll1 = db["monthly_reports"]
    period_list = []
    for period in coll1.find({}, {"_id": 0, "period": 1}):
        period_list.append(period['period']['Period'])
    return period_list
