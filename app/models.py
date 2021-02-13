from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class Tournament(db.Model):
    """
    Model for a tournament.
    """
    tournament_id = db.Column(db.Integer, primary_key=True)
    tournament_name = db.Column(db.String(255))
    tournament_description = db.Column(db.String(500))
    date = db.Column(db.DateTime, default=datetime.utcnow)

    tournament_status_id = db.Column(db.Integer, db.ForeignKey('tournament_status.tournament_status_id'))
    tournament_status = db.relationship('TournamentStatus', foreign_keys=[tournament_status_id])


class TournamentStatus(db.Model):
    """
    Lookup table for tournament statuses
    """
    tournament_status_id = db.Column(db.Integer, primary_key=True)
    tournament_status_name = db.Column(db.String(255))


class Match(db.Model):
    """
    A match always belongs to a tournament.
    """
    match_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    participant_a_score = db.Column(db.Integer, default=0)
    participant_b_score = db.Column(db.Integer, default=0)
    match_number = db.Column(db.Integer)

    participant_a_id = db.Column(db.Integer, db.ForeignKey('participant.participant_id'))
    participant_a = db.relationship('Participant', back_ref='matches', foreign_keys=[participant_a_id])
    participant_b_id = db.Column(db.Integer, db.ForeignKey('participant.participant_id'))
    participant_b = db.relationship('Participant', back_ref='matches', foreign_keys=[participant_b_id])
    match_status_id = db.Column(db.Integer, db.ForeignKey('match_status.match_status_id'))
    match_status = db.relationship('MatchStatus', foreign_keys=[match_status_id])
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournament.tournament_id'))
    tournament = db.relationship('Tournament', backref='matches', lazy='dynamic', foreign_keys=[tournament_id])


class MatchStatus(db.Model):
    """
    Lookup table for match statuses
    """
    match_status_id = db.Column(db.Integer, primary_key=True)
    match_status_name = db.Column(db.String(255))


class Participant(db.Model):
    """
    A participant is a single entity participating in a tournament.
    Participants are unique to every tournament since a participant may/may not have a user account tied to it.
    """
    participant_id = db.Column(db.Integer, primary_key=True)
    participant_name = db.Column(db.String(255))
    seed = db.Column(db.Integer)

    tournament_id = db.Column(db.Integer, db.ForeignKey('tournament.tournament_id'))
    tournament = db.relationship('Tournament', backref='participants', lazy='dynamic', foreign_keys=[tournament_id])


