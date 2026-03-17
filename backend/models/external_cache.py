from database import db


class ExternalCache(db.Model):
    __tablename__ = "external_cache"
    cache_key = db.Column(db.Text, primary_key=True)
    response_json = db.Column(db.JSON)
    fetched_at = db.Column(db.DateTime)
    ttl_seconds = db.Column(db.Integer, default=86400)
