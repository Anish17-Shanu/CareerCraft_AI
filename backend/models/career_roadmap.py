from database import db

class CareerRoadmap(db.Model):
    __tablename__ = "career_roadmaps"

    career_id = db.Column(
        db.Integer,
        db.ForeignKey("careers.career_id"),
        primary_key=True
    )
    step_order = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
