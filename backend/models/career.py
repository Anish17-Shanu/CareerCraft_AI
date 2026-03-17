from database import db

class Career(db.Model):
    __tablename__ = "careers"

    career_id = db.Column(db.Integer, primary_key=True)
    career_name = db.Column(db.Text, unique=True, nullable=False)
    domain = db.Column(db.Text)
    description = db.Column(db.Text)


class CareerTrait(db.Model):
    __tablename__ = "career_traits"

    career_id = db.Column(
        db.Integer,
        db.ForeignKey("careers.career_id"),
        primary_key=True
    )
    trait = db.Column(db.Text, primary_key=True)
    required_level = db.Column(db.Float)
    weight = db.Column(db.Float, default=1.0)


class CareerTag(db.Model):
    __tablename__ = "career_tags"

    career_id = db.Column(
        db.Integer,
        db.ForeignKey("careers.career_id"),
        primary_key=True
    )
    tag = db.Column(db.Text, primary_key=True)


class CareerReason(db.Model):
    __tablename__ = "career_reasons"

    career_id = db.Column(
        db.Integer,
        db.ForeignKey("careers.career_id"),
        primary_key=True
    )
    reason_order = db.Column(db.Integer, primary_key=True)
    reason_text = db.Column(db.Text)


class CareerRole(db.Model):
    __tablename__ = "career_roles"

    career_id = db.Column(
        db.Integer,
        db.ForeignKey("careers.career_id"),
        primary_key=True
    )
    role_order = db.Column(db.Integer, primary_key=True)
    role_title = db.Column(db.Text)
