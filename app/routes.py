import json
import logging
import boto3
import botocore
import os
import time
import pickle
from flask import (
    abort,
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    session,
    jsonify,
)
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse

from app.factory import db, PROJECT_NAME
from app.ld import LaunchDarklyApi
from app.models import User, Plan
from app.util import artifical_delay

core = Blueprint("core", __name__)


@core.route("/")
def index():
    """
    Controller for Public home page.
    Includes a server side experiment for trial duration. The duration
    can either be 14 days or 30 days. We show a different variation to
    each user randomly. Then we track the registration rate as our
    conversion event.
    """
    current_app.logger.info(current_app.config)
    if current_user.is_authenticated:
        return redirect(url_for("core.dashboard"))

    user = current_user.get_ld_user()
    req_headers = request.user_agent
    current_app.logger.error(req_headers)
    user['custom']['browser'] = req_headers.browser
    session["ld_user"] = user

    flag_name = "trial-duration"
    trial_duration = current_app.ldclient.variation_detail(flag_name, user, "15")

    start_time = time.time()

    if current_app.ldclient.variation('artificial-delay', user, False):
        artifical_delay(trial_duration.value)

    # Calculate the server processing time based on flag evaluation
    end_time = time.time() - start_time
    data_export = {
        "flag": flag_name,
        "variation": trial_duration.variation_index,
        "time": end_time,
    }
    current_app.ldclient.track("trial-rendering", user, data_export)

    session["trial_duration"] = trial_duration.value
    bootstrap = current_app.ldclient.all_flags_state(user)
    user_template = json.dumps(user)
    broken_release = current_app.ldclient.variation("accessibility-styling", user, False)
    register_color = current_app.ldclient.variation("registration-button-color", user, "#28A745")

    return render_template("home.html", all_flags=bootstrap.to_json_string(), register_color=register_color, broken_release=broken_release, user_template=user_template, trial_duration=trial_duration.value)


@core.route("/dashboard")
@login_required
def dashboard():
    theme = request.args.get("theme")
    user = current_user.get_ld_user()
    user['agent'] = request.headers.get('User-Agent')

    if theme:
        updateTheme(theme)

    dark_theme = current_app.ldclient.variation(
        "dark-theme", user, False
    )

    user_template = json.dumps(user)
    bootstrap = current_app.ldclient.all_flags_state(user)

    set_theme = "{0}/index.html".format(current_user.set_path)

    return render_template(
        set_theme,
        title="Home",
        dark_theme=dark_theme,
        user_template=user_template,
        all_flags=bootstrap.to_json_string(),
    )

def updateTheme(theme):

    if theme == "dark":
        current_user.set_path = "beta"
    else:
        current_user.set_path = "default"

    db.session.commit()


@core.route("/dark")
def darkTheme():
    return render_template(set_theme, title="Dark Theme")


@core.route("/experiments")
def experiments():
    theme = request.args.get("theme")
    if theme:
        updateTheme(theme)

    set_theme = "{0}/exp.html".format(current_user.set_path)

    user = current_user.get_ld_user()
    random_user = current_user.get_random_ld_user()

    user_template = json.dumps(user)
    bootstrap = current_app.ldclient.all_flags_state(user)

    show_nps = current_app.ldclient.variation("show-nps-survery", random_user, False)

    return render_template(
        set_theme,
        title="Experiments",
        show_nps=show_nps,
        random_user=random_user,
        user_template=user_template,
        all_flags=bootstrap.to_json_string(),
    )


@core.route("/operational")
def operational():
    theme = request.args.get("theme")
    if theme:
        updateTheme(theme)

    set_theme = "{0}/operation.html".format(current_user.set_path)

    bootstrap = current_app.ldclient.all_flags_state(current_user.get_ld_user())

    return render_template(
        set_theme, title="Operational", all_flags=bootstrap.to_json_string()
    )


@core.route("/dataexport")
def dataexport():

    theme = request.args.get("theme")

    if theme:
        updateTheme(theme)

    user = current_user.get_ld_user()
    session["ld_user"] = user

    set_theme = "{0}/dataexport.html".format(current_user.set_path)

    return render_template(set_theme, title="dataexport")


@core.route("/release")
def release():
    theme = request.args.get("theme")
    if theme:
        updateTheme(theme)

    set_theme = "{0}/release.html".format(current_user.set_path)
    return render_template(set_theme, title="Dark Theme")


@core.route("/register", methods=["GET", "POST"])
def register():
    # track registration attempts
    # ld_user will be in session if user got to the registration
    # page by clicking a link on the home page (where they saw the ab test)
    if session.get("ld_user"):
        current_app.logger.info(
            "Sending track event for {0}".format(session.get("ld_user"))
        )
        current_app.ldclient.track("started-registration", session["ld_user"])

    if current_user.is_authenticated:
        return redirect(url_for("core.dashboard"))

    if request.method == "POST":
        user = User(email=request.form["userEmail"])
        # check if userName exist
        if User.query.filter_by(email=request.form["userEmail"]).first() is not None:
            flash("Email is already taken. Please choose another email")
            return redirect(url_for("core.register"))
        # check if passwords match
        if request.form["inputPassword"] != request.form["confirmPassword"]:
            flash("Passwords must match")
            return redirect(url_for("core.register"))
        user.set_password(request.form["inputPassword"])
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")

        # track registration completion
        # ld_user will be in session if user got to the registration
        # page by clicking a link on the home page (where they saw the ab test)
        if session.get("ld_user"):
            current_app.logger.info(
                "Sending track event for {0}".format(session.get("ld_user"))
            )
            current_app.ldclient.track("registered", session["ld_user"])

        login_user(user)
        return redirect(url_for("core.dashboard"))
    return render_template("beta/auth/register.html", title="Support Request")


@core.route("/login", methods=["GET", "POST"])
def login(theme="default"):
    if current_user.is_authenticated:
        return redirect(url_for("core.dashboard"))
    if request.method == "POST":
        user = User.query.filter_by(email=request.form["userEmail"]).first()
        if user is None or not user.check_password(request.form["inputPassword"]):
            flash("Invalid username or password")
            return redirect(url_for("core.login"))
        login_user(user)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("core.dashboard")
        return redirect(next_page)
    return render_template("beta/auth/login.html", title="Sign In")


@core.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("core.index"))


@core.route("/profile")
@login_required
def profile():
    bootstrap = current_app.ldclient.all_flags_state(current_user.get_ld_user())

    user = User.query.filter_by(id=current_user.id).first()
    return render_template(
        "default/profile.html", user=user, all_flags=bootstrap.to_json_string()
    )


@core.route("/people")
@login_required
def people():
    bootstrap = current_app.ldclient.all_flags_state(current_user.get_ld_user())
    page = request.args.get("page", 1, type=int)
    users = User.query.order_by(User.id).paginate(page, 15, False)
    next_url = url_for("core.people", page=users.next_num) if users.has_next else None
    prev_url = url_for("core.people", page=users.prev_num) if users.has_prev else None
    return render_template(
        "default/people.html",
        users=users.items,
        next_url=next_url,
        prev_url=prev_url,
        all_flags=bootstrap.to_json_string(),
    )


@core.route("/settings")
@login_required
def settings():
    bootstrap = current_app.ldclient.all_flags_state(current_user.get_ld_user())
    plans = Plan.query.all()
    return render_template(
        "default/settings.html", plans=plans, all_flags=bootstrap.to_json_string()
    )


@core.route("/upgrade")
@login_required
def upgrade():
    current_user.plan_id = request.args.get("plan")
    db.session.commit()

    return redirect(request.referrer)


@core.route("/environments")
def environments():
    webhook = current_app.ldclient.variation(
        "environments-webhook", current_user.get_ld_user(), False
    )
    url = url_parse(request.url)
    subdomain = url.host.split(".")[0]

    if subdomain == "admin" and webhook:
        try:
            ld = LaunchDarklyApi(os.environ.get("LD_API_KEY"))
            project = ld.get_project(PROJECT_NAME)
            project_pick = pickle.dumps(project)
            current_app.redis_client.set(PROJECT_NAME, project_pick)
            return jsonify({"response": 200})
        except Exception as e:
            current_app.logger.error(e)
            abort(500)
    else:
        abort(403)
