from database import db

class Question(db.Model):
    __tablename__ = "questions"
    question_id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.Text)
    category = db.Column(db.Text)
    trait = db.Column(db.Text)
    response_type = db.Column(db.Text)
    difficulty = db.Column(db.Integer)
    active = db.Column(db.Boolean, default=True)


class QuestionMeta(db.Model):
    __tablename__ = "question_metadata"
    question_id = db.Column(
        db.Integer,
        db.ForeignKey("questions.question_id"),
        primary_key=True
    )
    required = db.Column(db.Boolean, default=True)
    why = db.Column(db.Text)
    min_label = db.Column(db.Text)
    max_label = db.Column(db.Text)
    evidence_high = db.Column(db.Text)
    evidence_low = db.Column(db.Text)
    placeholder = db.Column(db.Text)


class QuestionOption(db.Model):
    __tablename__ = "question_options"
    option_id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(
        db.Integer,
        db.ForeignKey("questions.question_id"),
        nullable=False
    )
    label = db.Column(db.Text)
    value = db.Column(db.Text)
    detail = db.Column(db.Text)
    traits = db.Column(db.JSON)
