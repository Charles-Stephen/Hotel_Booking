from flask import Flask, render_template, request, url_for, session, jsonify
from flask_mysqldb import MySQL
import datetime
import hashlib
import random

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'hotel_booking_system'

# foe session
app.config['SECRET_KEY'] = 'Hotel-SG'

mysql = MySQL(app)


# ================================================================================================
# =================================         Frontend         =====================================
# ================================================================================================

def fetch_rows_as_dicts(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

# ======================================
# =============   Home   =============
# ======================================
@app.route("/")
def index():
    pg = "home"
    conn = mysql.connection.cursor()
    check_my_session = session.get("role")

    if check_my_session is None:
        admindata = "none"
    else:
        admindata = {
            "role": session.get("role"),
            "id": session.get("id"),
            "name": session.get("name"),
            "email": session.get("email"),
            "phone": session.get("phone")
        }
    # Slider
    st = "show"
    conn.execute("SELECT * FROM slider WHERE status = %s", (st,))
    slidedata = fetch_rows_as_dicts(conn)
    # Rooms
    conn.execute("SELECT r.id, r.cover_img, r.room_number, p.name, p.price FROM rooms r INNER JOIN `package` p ON r.package_id = p.id LIMIT 3")
    show_room = fetch_rows_as_dicts(conn)
    conn.close()
    return render_template("frontend/index.html", pg=pg, slidedata=slidedata, show_room=show_room, admindata=admindata)


# ======================================
# ==============  Rooms  ===============
# ======================================
@app.route("/rooms")
def room():
    pg = "room"
    conn = mysql.connection.cursor()
    check_my_session = session.get("role")

    if check_my_session is None:
        admindata = "none"
    else:
        admindata = {
            "role": session.get("role"),
            "id": session.get("id"),
            "name": session.get("name"),
            "email": session.get("email"),
            "phone": session.get("phone")
        }

    # Rooms
    conn.execute("SELECT r.id, r.cover_img, r.room_number, p.name, p.price FROM rooms r INNER JOIN `package` p ON r.package_id = p.id")
    show_room = fetch_rows_as_dicts(conn)
    conn.close()
    return render_template("frontend/room.html", pg=pg, admindata=admindata, show_room=show_room)


# ======================================
# =========== Rooms Details  ===========
# ======================================
@app.route("/room-details", methods=["GET", "POST"])
def room_details():
    pg = "room"
    check_my_session = session.get("role")

    if check_my_session is None:
        admindata = "none"
    else:
        admindata = {
            "role": session.get("role"),
            "id": session.get("id"),
            "name": session.get("name"),
            "email": session.get("email"),
            "phone": session.get("phone")
        }

    conn = mysql.connection.cursor()
    if request.method == "POST":
        detail_id = request.form["detail_id"]

        conn.execute("SELECT * FROM rooms WHERE id = %s", (detail_id,))
        sel_room = fetch_rows_as_dicts(conn)

        # Query and Values
        room_query = "SELECT r.id, r.cover_img, r.img_1, r.img_2, r.img_3, r.img_4, r.room_number"
        room_join = ""

        for rm in sel_room:
            # Adding in Query And Values
            # facility 1
            if rm["facilities_1"] != 0:
                room_query += ", f1.name AS faci1"
                room_join += " INNER JOIN facilities f1 ON r.facilities_1 = f1.id"
            # facility 2
            if rm["facilities_2"] != 0:
                room_query += ", f2.name AS faci2"
                room_join += " INNER JOIN facilities f2 ON r.facilities_2 = f2.id"
            # facility 3
            if rm["facilities_3"] != 0:
                room_query += ", f3.name AS faci3"
                room_join += " INNER JOIN facilities f3 ON r.facilities_3 = f3.id"
            # facility 4
            if rm["facilities_4"] != 0:
                room_query += ", f4.name AS faci4"
                room_join += " INNER JOIN facilities f4 ON r.facilities_4 = f4.id"
            # facility 5
            if rm["facilities_5"] != 0:
                room_query += ", f5.name AS faci5"
                room_join += " INNER JOIN facilities f5 ON r.facilities_5 = f5.id"
            # facility 6
            if rm["facilities_6"] != 0:
                room_query += ", f6.name AS faci6"
                room_join += " INNER JOIN facilities f6 ON r.facilities_6 = f6.id"
        final_q = room_query + ", p.name, p.price FROM rooms r INNER JOIN `package` p ON r.package_id = p.id" + room_join + " WHERE r.id = " + detail_id
        conn.execute(final_q)
        show_room = fetch_rows_as_dicts(conn)
        conn.close()
        return render_template("frontend/room-detail.html", show_room=show_room, admindata=admindata, pg=pg)


# ======================================
# =============    About   =============
# ======================================
@app.route("/about")
def about():
    pg = "about"
    check_my_session = session.get("role")

    if check_my_session is None:
        admindata = "none"
    else:
        admindata = {
            "role": session.get("role"),
            "id": session.get("id"),
            "name": session.get("name"),
            "email": session.get("email"),
            "phone": session.get("phone")
        }
    return render_template("frontend/about.html", pg=pg, admindata=admindata)


# ======================================
# =============    Login   =============
# ======================================
@app.route("/login", methods=["GET", "POST"])
def login():
    pg = "login"

    myrole = session.get("role")
    if myrole == 0:
        return """<Script>
                window.location.assign("/admin");
                </Script>"""
    elif myrole == 1:
        return """<Script>
                window.location.assign("/");
                </Script>"""
    return render_template("frontend/login.html", pg=pg)


# ======================================
# ============   Register   ============
# ======================================
@app.route("/register", methods=["GET", "POST"])
def register():
    pg = "login"

    myrole = session.get("role")
    if myrole == 0:
        return """<Script>
                window.location.assign("/admin");
                </Script>"""
    elif myrole == 1:
        return """<Script>
                window.location.assign("/");
                </Script>"""
    return render_template("frontend/register.html", pg=pg)


# ======================================
# =========  Forgot Password   =========
# ======================================
@app.route("/forgot", methods=["GET", "POST"])
def forgot_password():
    pg = "login"
    myrole = session.get("role")
    if myrole == 0:
        return """<Script>
                window.location.assign("/admin");
                </Script>"""
    elif myrole == 1:
        return """<Script>
                window.location.assign("/");
                </Script>"""
    else:
        if request.method == "POST":
            c_email = request.form["v_email"]
            c_phone = request.form["v_phone"]

            conn = mysql.connection.cursor()

            # Check if email or phone already exists
            conn.execute("SELECT * FROM users WHERE email = %s AND phone = %s", (c_email, c_phone))
            existing_user = conn.fetchone()

            if existing_user:
                adminid = int(existing_user[7])
                if adminid == 1:
                    session["role"] = adminid
                    session["id"] = existing_user[0]
                    session["name"] = existing_user[1]
                    session["email"] = existing_user[2]
                    session["phone"] = existing_user[4]

                    conn.close()

                    return """
                            <script>
                                window.location.assign("/renew-password");
                            </script>
                            """
                else:
                    return """
                            <script>
                                alert('Incorrect Email OR Phone!');
                                window.location.assign("/forgot");
                            </script>
                            """
            else:
                return """
                        <script>
                            alert('Incorrect Email OR Phone!');
                            window.location.assign("/forgot");
                        </script>
                        """
    return render_template("frontend/forgot-password.html", pg=pg)


# ======================================
# =========  Renew Password   =========
# ======================================
@app.route("/renew-password", methods=["GET", "POST"])
def renew_password():
    pg = "login"
    adminrole = session.get("role")
    user_id = session.get("id")
    admindata = {
        "role": session.get("role"),
        "id": session.get("id"),
        "name": session.get("name"),
        "email": session.get("email"),
        "phone": session.get("phone")
    }
    if adminrole == 1:
        if request.method == "POST":
            mynew_password = request.form["pass"]
            converted_password = hashlib.md5(mynew_password.encode()).hexdigest()
            up_on = datetime.datetime.now()
            upd_on = up_on.strftime("%d-%m-%Y - %I:%M")

            conn = mysql.connection.cursor()

            # Update password based on user_id
            conn.execute("UPDATE users SET password = %s, updated_on = %s WHERE id = %s", (converted_password, upd_on, user_id))
            mysql.connection.commit()

            conn.close()

            return """<Script>
            window.location.assign("/");
            </Script>"""
    else:
        return """<Script>
            window.location.assign("/login");
            </Script>"""

    return render_template("frontend/renew-password.html", admindata=admindata, pg=pg)


# ======================================
# ===========   Contact Us   ===========
# ======================================
@app.route("/contact-us", methods=["GET", "POST"])
def contact():
    pg = "contact"
    conn = mysql.connection.cursor()
    check_my_session = session.get("role")

    if check_my_session is None:
        admindata = "none"
    else:
        admindata = {
            "role": session.get("role"),
            "id": session.get("id"),
            "name": session.get("name"),
            "email": session.get("email"),
            "phone": session.get("phone")
        }

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        msg = request.form["message"]

        conn.execute("INSERT INTO contact (name, email, message) VALUES (%s, %s, %s)", (name, email, msg))
        mysql.connection.commit()
        conn.close()
        return """
                <script>
                    alert('Your query has been submitted!');
                    window.location.assign("/contact-us");
                </script>
                """

    return render_template("frontend/contact.html", admindata=admindata, pg=pg)


# ======================================
# ===========   Profile   ==============
# ======================================
@app.route("/profile", methods=["GET", "POST"])
def profile():
    pg = "profile"
    conn = mysql.connection.cursor()
    check_my_session = session.get("role")

    if check_my_session is None:
        return """
                <script>
                    alert('Please login to view this page!');
                    window.location.assign("/");
                </script>
                """
    else:
        admindata = {
            "role": session.get("role"),
            "id": session.get("id"),
            "name": session.get("name"),
            "email": session.get("email"),
            "phone": session.get("phone")
        }
    bk = "booked"
    ds = "disapprove"
    cs = "cancle"
    conn.execute("SELECT r.cover_img, b.id, u.name, u.email, r.room_number, b.total_cost, b.status, p.name AS pname, b.booking_date, b.starting_date, b.ending_date, b.credit_card_number, b.room_cost FROM room_booking b INNER JOIN users u ON b.user_id = u.id INNER JOIN rooms r ON b.room_id = r.id INNER JOIN package p ON r.package_id = p.id WHERE b.user_id = %s AND b.status = %s ORDER BY b.id DESC", (admindata["id"], bk))
    booked = fetch_rows_as_dicts(conn)

    conn.execute("SELECT r.cover_img, b.id, u.name, u.email, r.room_number, b.total_cost, b.status, p.name AS pname, b.booking_date, b.starting_date, b.ending_date, b.credit_card_number, b.room_cost FROM room_booking b INNER JOIN users u ON b.user_id = u.id INNER JOIN rooms r ON b.room_id = r.id INNER JOIN package p ON r.package_id = p.id WHERE b.user_id = %s AND b.status = %s ORDER BY b.id DESC", (admindata["id"], ds))
    dis_b = fetch_rows_as_dicts(conn)

    conn.execute("SELECT r.cover_img, b.id, u.name, u.email, r.room_number, b.total_cost, b.status, p.name AS pname, b.booking_date, b.starting_date, b.ending_date, b.credit_card_number, b.room_cost FROM room_booking b INNER JOIN users u ON b.user_id = u.id INNER JOIN rooms r ON b.room_id = r.id INNER JOIN package p ON r.package_id = p.id WHERE b.user_id = %s AND b.status = %s ORDER BY b.id DESC", (admindata["id"], cs))
    can_b = fetch_rows_as_dicts(conn)

    if request.method == "POST":
        delid = request.form["delid"]
        conn.execute("DELETE FROM `room_booking` WHERE id = %s", (delid,))
        mysql.connection.commit()
        conn.close()
        return """
                <script>
                    alert('Please login to view this page!');
                    window.location.assign("/profile");
                </script>
                """

    return render_template("frontend/profile.html", pg=pg, admindata=admindata, booked=booked, can_b=can_b, dis_b=dis_b)



# ================================================================================================
# ==================================         Common         ======================================
# ================================================================================================


# ======================================
# ===========   Login Code   ===========
# ======================================
@app.route("/logincode", methods=["GET", "POST"])
def login_code():
    if request.method == "POST":
        userrole = int(request.form["userrole"])
        _email = request.form["email"]
        _pass = request.form["pass"]
        converted_pass = hashlib.md5(_pass.encode()).hexdigest()

        conn = mysql.connection.cursor()

        if userrole == 0:
            # Check if email or phone already exists
            conn.execute("SELECT * FROM users WHERE email = %s AND password = %s AND role = %s", (_email, converted_pass, userrole))
            # existing_user = fetch_rows_as_dicts(conn)
            existing_user = conn.fetchone()
            if existing_user:
                session["role"] = userrole
                session["id"] = existing_user[0]
                session["name"] = existing_user[1]
                session["email"] = existing_user[2]
                session["phone"] = existing_user[4]

                return """<Script>
                        window.location.assign("/admin");
                        </Script>"""
            else:
                return """
                        <script>
                            alert('Incorrect Email OR Password!');
                            window.location.assign("/admin/login");
                        </script>
                        """
        elif userrole == 1:
            # Check if email or phone already exists
            conn.execute("SELECT * FROM users WHERE email = %s AND password = %s AND role = %s", (_email, converted_pass, userrole))
            existing_user = conn.fetchone()
            if existing_user:
                session["role"] = userrole
                session["id"] = existing_user[0]
                session["name"] = existing_user[1]
                session["email"] = existing_user[2]
                session["phone"] = existing_user[4]
                return """
                        <script>
                            window.location.assign("/");
                        </script>
                        """
            else:
                return """
                        <script>
                            alert('Incorrect Email OR Password!');
                            window.location.assign("/login");
                        </script>
                        """
        conn.close()
        return "Login"


# ======================================
# =============   logout   =============
# ======================================
@app.route("/logout")
def logout():
    session.clear()
    return """<Script>
            window.location.assign("/");
            </Script>"""


# ======================================
# ========  Add/Register User)  ========
# ======================================
@app.route("/add-user", methods=["GET", "POST"])
def add_user():
    if request.method == "POST":
        name = request.form["name"]
        email_address = request.form["email"]
        password = request.form["pass"]
        converted_password = hashlib.md5(password.encode()).hexdigest()
        phone = request.form["phone"]
        reg_on = datetime.datetime.now()
        regis_on = reg_on.strftime("%d-%m-%Y - %I:%M")

        # Connection
        conn = mysql.connection.cursor()

        # Check if email or phone already exists
        conn.execute("SELECT * FROM users WHERE email = %s OR phone = %s", (email_address, phone))
        existing_user = fetch_rows_as_dicts(conn)

        myrole = session.get("role")

        if existing_user:
            if myrole == 0:
                return """
                        <script>
                            alert('User Email OR Phone Already Exists!');
                            window.location.assign("/admin");
                        </script>
                        """
            else:
                return """
                        <script>
                            alert('User Email OR Phone Already Exists!');
                            window.location.assign("/register");
                        </script>
                        """
        else:
            conn.execute("INSERT INTO users (name, email, password, phone, created_on) VALUES (%s, %s, %s, %s, %s)", (name, email_address, converted_password, phone, regis_on))
            mysql.connection.commit()
            conn.close()

            if myrole == 0:
                return """
                        <script>
                            alert('User Added Successfully!');
                            window.location.assign("/admin");
                        </script>
                        """
            else:
                return """
                        <script>
                            window.location.assign("/login");
                        </script>
                        """
    return "Add user"


# ======================================
# ============   Edit User  ============
# ======================================
@app.route("/edit-user", methods=["GET", "POST"])
def edit_user():
    myrole = session.get("role")

    if request.method == "POST":

        # Connection
        conn = mysql.connection.cursor()

        user_id = request.form["user_id"]

        conn.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        users = fetch_rows_as_dicts(conn)

        for user in users:
            # name
            if request.form["name"] == '':
                name = user["name"]
            elif user["name"] != request.form["name"]:
                name = request.form["name"]
            else:
                name = user["name"]

            # email_address
            if request.form["email"] == '':
                email_address = user["email"]
            elif user["email"] != request.form["email"]:
                email_address = request.form["email"]
            else:
                email_address = user["email"]

            # password
            if request.form["pass"] == '':
                converted_password = user["password"]
            elif user["password"] == hashlib.md5(request.form["pass"].encode()).hexdigest():
                converted_password = user["password"]
            else:
                converted_password = hashlib.md5(request.form["pass"].encode()).hexdigest()

            # phone
            if request.form["phone"] == '':
                phone = user["phone"]
            elif user["phone"] != request.form["phone"]:
                phone = request.form["phone"]
            else:
                phone = user["phone"]


        upd_on = datetime.datetime.now()
        update_on = upd_on.strftime("%d-%m-%Y - %I:%M")

        conn.execute("SELECT * FROM users WHERE (email = %s OR phone = %s) AND id != %s", (email_address, phone, user_id))
        existing_user = fetch_rows_as_dicts(conn)

        if existing_user:
            if myrole == 0:
                return """<script>
                        alert('User Email OR Phone Already Exists!');
                        window.location.assign("/admin");
                        </script>"""
            else:
                return """<script>
                        alert('User Email OR Phone Already Exists!');
                        window.location.assign("/");
                        </script>"""
        else:
            conn.execute(
                "UPDATE users SET name = %s, email = %s, password = %s, phone = %s, updated_on = %s WHERE id = %s",
                (name, email_address, converted_password, phone, update_on, user_id))
            mysql.connection.commit()

            conn.close()

            if myrole == 0:
                if session.get("email") == email_address:
                    session["role"] = myrole
                    session["id"] = user_id
                    session["name"] = name
                    session["email"] = email_address
                    session["phone"] = phone
                    return """<script>
                            alert('Admin Profile Successfully Updated!');
                            window.location.assign("/admin");
                            </script>"""
                else:
                    return """<script>
                            alert('User Profile Successfully Updated!');
                            window.location.assign("/admin");
                            </script>"""
            else:
                session["role"] = myrole
                session["id"] = user_id
                session["name"] = name
                session["email"] = email_address
                session["phone"] = phone
                return """<script>
                        alert('Profile Successfully Updated!');
                        window.location.assign("/");
                        </script>"""
    return "Edit"


# ================================================================================================
# ==================================        Backend         ======================================
# ================================================================================================


# ======================================
# ============   Register   ============
# ======================================
@app.route("/admin/register", methods=["GET", "POST"])
def admin_reg():
    myrole = session.get("role")
    if myrole == 0:
        return """<Script>
                window.location.assign("/admin");
                </Script>"""
    elif myrole == 1:
        return """<Script>
                window.location.assign("/");
                </Script>"""
    else:
        if request.method == "POST":
            name = request.form["name"]
            email_address = request.form["email"]
            password = request.form["pass"]
            converted_password = hashlib.md5(password.encode()).hexdigest()
            phone = request.form["phone"]
            reg_on = datetime.datetime.now()
            regis_on = reg_on.strftime("%d-%m-%Y - %I:%M")
            userrole = 0

            # Connection
            conn = mysql.connection.cursor()

            # Check if email or phone already exists
            conn.execute("SELECT * FROM users WHERE email = %s OR phone = %s", (email_address, phone))
            existing_user = fetch_rows_as_dicts(conn)

            if existing_user:
                return """
                        <script>
                            alert('User Email OR Phone Already Exists!');
                            window.location.assign("/admin/register");
                        </script>
                        """
            else:
                conn.execute("INSERT INTO users (name, email, password, phone, created_on, role) VALUES (%s, %s, %s, %s, %s, %s)",(name, email_address, converted_password, phone, regis_on, userrole))
                mysql.connection.commit()

                conn.close()

                return """
                        <script>
                            alert('User Email OR Phone Already Exists!');
                            window.location.assign("/admin/login");
                        </script>
                        """
    return render_template("backend/register.html")


# ======================================
# ==============  Login   ==============
# ======================================
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    myrole = session.get("role")
    if myrole == 0:
        return """<Script>
                window.location.assign("/admin");
                </Script>"""
    elif myrole == 1:
        return """<Script>
                window.location.assign("/");
                </Script>"""
    return render_template("backend/login.html")


# ======================================
# =========  Renew Password   =========
# ======================================
@app.route("/admin/renew_password", methods=["GET", "POST"])
def admin_renew_password():
    adminrole = session.get("role")
    user_id = session.get("id")
    admindata = {
        "role": session.get("role"),
        "id": session.get("id"),
        "name": session.get("name"),
        "email": session.get("email"),
        "phone": session.get("phone")
    }
    if adminrole == 0:
        if request.method == "POST":
            mynew_password = request.form["pass"]
            converted_password = hashlib.md5(mynew_password.encode()).hexdigest()
            up_on = datetime.datetime.now()
            upd_on = up_on.strftime("%d-%m-%Y - %I:%M")

            conn = mysql.connection.cursor()

            # Update password based on user_id
            conn.execute("UPDATE users SET password = %s, updated_on = %s WHERE id = %s", (converted_password, upd_on, user_id))
            mysql.connection.commit()

            conn.close()

            return """<Script>
            window.location.assign("/admin");
            </Script>"""
    else:
        return """<Script>
            window.location.assign("/admin/login");
            </Script>"""

    return render_template("backend/renew_password.html", admindata=admindata)


# ======================================
# =========  Forgot Password   =========
# ======================================
@app.route("/admin/forgot-password", methods=["GET", "POST"])
def admin_forgot_password():
    myrole = session.get("role")
    if myrole == 0:
        return """<Script>
            window.location.assign("/admin");
            </Script>"""
    elif myrole == 1:
        return """<Script>
            window.location.assign("/");
            </Script>"""
    else:
        if request.method == "POST":
            admin_email = request.form["v_email"]
            admin_phone = request.form["v_phone"]

            conn = mysql.connection.cursor()

            # Check if email or phone already exists
            conn.execute("SELECT * FROM users WHERE email = %s AND phone = %s", (admin_email, admin_phone))
            existing_user = conn.fetchone()

            if existing_user:
                adminid = int(existing_user[7])
                if adminid == 0:
                    session["role"] = adminid
                    session["id"] = existing_user[0]
                    session["name"] = existing_user[1]
                    session["email"] = existing_user[2]
                    session["phone"] = existing_user[4]

                    conn.close()

                    return render_template("backend/renew_password.html")
                else:
                    return """
                            <script>
                                alert('Incorrect Email OR Phone!');
                                window.location.assign("/admin/forgot-password");
                            </script>
                            """
            else:
                return """
                        <script>
                            alert('Incorrect Email OR Phone!');
                            window.location.assign("/admin/forgot-password");
                        </script>
                        """
    return render_template("backend/forgot-password.html")


# ======================================
# ============  Dashboard   ============
# ======================================
@app.route("/admin")
def admin():
    admindata = {
        "role": session.get("role"),
        "id": session.get("id"),
        "name": session.get("name"),
        "email": session.get("email"),
        "phone": session.get("phone"),
        "pg": "dashboard"
    }

    if admindata["role"] == 0:
        conn = mysql.connection.cursor()
        conn.execute("SELECT * FROM users ORDER BY id DESC")
        users = fetch_rows_as_dicts(conn)
        return render_template("backend/index.html", admindata=admindata, users=users)
    elif admindata["role"] == 1:
        return """<Script>
                window.location.assign("/");
                </Script>"""
    return """<Script>
            window.location.assign("/admin/login");
            </Script>"""


# ======================================
# ==  Dashboard Part 2 (Delete User)  ==
# ======================================
@app.route("/delete-user", methods=["GET", "POST"])
def delete_user():
    if request.method == "POST":
        userid = request.form["userid"]
        conn = mysql.connection.cursor()
        conn.execute("DELETE FROM users WHERE id = %s", (userid,))
        mysql.connection.commit()
        conn.close()
        return """<script>
                alert('User Successfully Deleted!');
                window.location.assign("/admin");
                </script>"""
    return "Delete User"


# ======================================
# ============  Contacts   ============
# ======================================
@app.route("/admin/contacts", methods=["GET", "POST"])
def admin_contact():
    conn = mysql.connection.cursor()
    conn.execute("SELECT * FROM contact ORDER BY id DESC")
    contacts = fetch_rows_as_dicts(conn)

    admindata = {
        "role": session.get("role"),
        "id": session.get("id"),
        "name": session.get("name"),
        "email": session.get("email"),
        "phone": session.get("phone"),
        "pg": "contacts"
    }
    if admindata["role"] == 0:
        if request.method == "POST":
            stats = "read"
            user_id = request.form["read"]
            conn.execute("UPDATE contact SET status = %s WHERE id = %s", (stats, user_id))
            mysql.connection.commit()
            return """<Script>
                    window.location.assign("/admin/contacts");
                    </Script>"""
        conn.close()
        return render_template("backend/contact.html", admindata=admindata, contacts=contacts)
    elif admindata["role"] == 1:
        return """<Script>
                window.location.assign("/");
                </Script>"""
    return """<Script>
            window.location.assign("/admin/login");
            </Script>"""


# ======================================
# ============  Sliders   =============
# ======================================
@app.route("/admin/slider", methods=["GET", "POST"])
def slider():
    admindata = {
        "role": session.get("role"),
        "id": session.get("id"),
        "name": session.get("name"),
        "email": session.get("email"),
        "phone": session.get("phone"),
        "pg": "slider"
    }

    if admindata["role"] == 0:
        conn = mysql.connection.cursor()
        conn.execute("SELECT * FROM slider ORDER BY status DESC")
        slidedata = fetch_rows_as_dicts(conn)

        if 'img' in request.files:
            myimage = request.files['img']
            if myimage.filename != '':

                converted_num = str(random.randrange(9999999999999999999999999999999999))
                newname = converted_num + 'image.jpg'  # Change this to the desired new name

                conn.execute("SELECT * FROM slider WHERE img = %s", (newname,))
                ch_img = fetch_rows_as_dicts(conn)
                if ch_img:
                    return """
                            <script>
                                alert('An error occurred, please try again!');
                                window.location.assign("/admin/slider");
                            </script>
                            """
                else:
                    conn.execute("INSERT INTO slider (img) VALUES (%s)", (newname,))
                    mysql.connection.commit()
                    conn.close()

                    myimage.save('static/frontend/slider/' + newname)
                    return """<Script>
                            window.location.assign("/admin/slider");
                            </Script>"""
            return """
                    <script>
                        alert('An error occurred, please try again!');
                        window.location.assign("/admin/slider");
                    </script>
                    """
        return render_template("backend/slider.html", admindata=admindata, slidedata=slidedata)
    elif admindata["role"] == 1:
        return """<Script>
                window.location.assign("/");
                </Script>"""
    return """<Script>
            window.location.assign("/admin/login");
            </Script>"""


# ======================================
# =====  Sliders Part 2 (Remove)  ======
# ======================================
@app.route("/manage", methods=["GET", "POST"])
def manage():
    if request.method == "POST":
        slide_id = request.form["slideid"]
        slide_status = "hide"
        conn = mysql.connection.cursor()
        conn.execute("UPDATE slider SET status = %s WHERE id = %s", (slide_status, slide_id))
        mysql.connection.commit()
        conn.close()

        return """<Script>
                window.location.assign("/admin/slider");
                </Script>"""


# ======================================
# =====  Sliders Part 3 (SELECT)  ======
# ======================================
@app.route("/select", methods=["GET", "POST"])
def select():
    if request.method == "POST":
        slide_id = request.form["slideid"]
        slide_status = "show"
        conn = mysql.connection.cursor()
        conn.execute("UPDATE slider SET status = %s WHERE id = %s", (slide_status, slide_id))
        mysql.connection.commit()
        conn.close()

        return """<Script>
                window.location.assign("/admin/slider");
                </Script>"""


# ======================================
# =============  Profile  ==============
# ======================================
@app.route("/admin/profile")
def admin_profile():
    admindata = {
        "role": session.get("role"),
        "id": session.get("id"),
        "name": session.get("name"),
        "email": session.get("email"),
        "phone": session.get("phone"),
        "pg": "Profile"
    }

    if admindata["role"] == 0:
        return render_template("backend/profile.html", admindata=admindata)
    elif admindata["role"] == 1:
        return """<Script>
                window.location.assign("/");
                </Script>"""
    return """<Script>
            window.location.assign("/admin/login");
            </Script>"""


# ======================================
# ============  Facilities  ============
# ======================================
@app.route("/admin/facilities", methods=["GET", "POST"])
def admin_facilities():
    admindata = {
        "role": session.get("role"),
        "id": session.get("id"),
        "name": session.get("name"),
        "email": session.get("email"),
        "phone": session.get("phone"),
        "pg": "facilities"
    }

    conn = mysql.connection.cursor()

    if request.method == "POST":
        facility_name = request.form["facility_name"]
        conn.execute("SELECT * FROM facilities WHERE name = %s", (facility_name,))
        ch_facility = fetch_rows_as_dicts(conn)
        if ch_facility:
            return """<script>
                    alert('Facility Already Exists!');
                    window.location.assign("/admin/facilities");
                    </script>"""
        else:
            conn.execute("INSERT INTO facilities (name) VALUES (%s)", (facility_name,))
            mysql.connection.commit()
            return """<script>
                    window.location.assign("/admin/facilities");
                    </script>"""

    if admindata["role"] == 0:
        conn.execute("SELECT * FROM facilities ORDER BY id DESC")
        facilities = fetch_rows_as_dicts(conn)
        conn.close()
        return render_template("backend/facilities.html", admindata=admindata, facilities=facilities)
    elif admindata["role"] == 1:
        return """<Script>
                window.location.assign("/");
                </Script>"""
    return """<Script>
            window.location.assign("/admin/login");
            </Script>"""


# ======================================
# =============  Packages  =============
# ======================================
@app.route("/admin/package", methods=["GET", "POST"])
def admin_packages():
    admindata = {
        "role": session.get("role"),
        "id": session.get("id"),
        "name": session.get("name"),
        "email": session.get("email"),
        "phone": session.get("phone"),
        "pg": "packages"
    }

    conn = mysql.connection.cursor()

    if request.method == "POST":
        package_name = request.form["package_name"]
        price = request.form["price"]
        conn.execute("Select * FROM package WHERE name = %s", (package_name,))
        ch_pack = fetch_rows_as_dicts(conn)

        if ch_pack:
            return """<script>
                    alert('Package Already Exists!');
                    window.location.assign("/admin/package");
                    </script>"""
        else:
            conn.execute("INSERT INTO package (name, price) VALUES (%s, %s)", (package_name, price))
            mysql.connection.commit()
            return """<script>
                    window.location.assign("/admin/package");
                    </script>"""

    if admindata["role"] == 0:
        conn.execute("SELECT * FROM package ORDER BY id DESC")
        package = fetch_rows_as_dicts(conn)
        conn.close()
        return render_template("backend/packages.html", admindata=admindata, package=package)
    elif admindata["role"] == 1:
        return """<Script>
                window.location.assign("/");
                </Script>"""
    return """<Script>
            window.location.assign("/admin/login");
            </Script>"""


# ======================================
# =====  Packages Part 2 (Delete)  =====
# ======================================
@app.route("/delete-package", methods=["GET", "POST"])
def admin_delete_package():
    if request.method == "POST":
        pack_id = request.form["packid"]

        conn = mysql.connection.cursor()
        conn.execute("DELETE FROM package WHERE id = %s", (pack_id,))
        mysql.connection.commit()
        conn.close()
        return """<script>
                alert('Package Successfully Deleted!');
                window.location.assign("/admin/package");
                </script>"""
    return "Delete Package"


# ======================================
# =====  Packages Part 2 (Update)  =====
# ======================================
@app.route("/update-package", methods=["GET", "POST"])
def admin_update_package():
    if request.method == "POST":
        pack_id = request.form["pack_id"]
        update_package_name = request.form["update_package_name"]
        update_price = request.form["update_price"]

        conn = mysql.connection.cursor()
        conn.execute("Select * FROM package WHERE name = %s AND id != %s", (update_package_name, pack_id))
        ch_pack = fetch_rows_as_dicts(conn)

        if ch_pack:
            return """<script>
                    alert('Package Already Exists!');
                    window.location.assign("/admin/package");
                    </script>"""
        else:
            conn.execute("SELECT * FROM package WHERE id = %s", (pack_id,))
            pack = fetch_rows_as_dicts(conn)

            if update_package_name == '':
                package_name = pack["name"]
            elif update_package_name == pack["name"]:
                package_name = pack["name"]
            else:
                package_name = update_package_name

            if update_price == '':
                price = pack["price"]
            elif update_price == pack["price"]:
                price = pack["price"]
            else:
                price = update_price

            conn.execute("UPDATE package SET name = %s, price = %s WHERE id = %s", (package_name, price, pack_id))
            mysql.connection.commit()
            conn.close()
            return """<script>
                    alert('Package Successfully Updated!');
                    window.location.assign("/admin/package");
                    </script>"""
    return "Update Package"


# ======================================
# =============  Rooms  =============
# ======================================
@app.route("/admin/rooms", methods=["GET", "POST"])
def admin_rooms():
    admindata = {
        "role": session.get("role"),
        "id": session.get("id"),
        "name": session.get("name"),
        "email": session.get("email"),
        "phone": session.get("phone"),
        "pg": "rooms"
    }

    conn = mysql.connection.cursor()

    if request.method == "POST":
        roomnumber = request.form["room_number"]
        name_coverimage = request.files['name_coverimage']
        if 'name_coverimage' in request.files:
            name_image1 = request.files['name_image1']
            name_image2 = request.files['name_image2']
            name_image3 = request.files['name_image3']
            name_image4 = request.files['name_image4']

            if name_coverimage.filename != '':
                # Cover Image
                converted_num = str(random.randrange(9999999999999999999999999999999999))
                covername = converted_num + 'coverimage.jpg'  # Change this to the desired new name

                # Image 1
                if name_image1.filename != '':
                    converted_num1 = str(random.randrange(9999999999999999999999999999999999))
                    imgname1 = converted_num1 + 'image1.jpg'  # Change this to the desired new name
                else:
                    imgname1 = ''

                # Image 2
                if name_image2.filename != '':
                    converted_num2 = str(random.randrange(9999999999999999999999999999999999))
                    imgname2 = converted_num2 + 'image2.jpg'  # Change this to the desired new name
                else:
                    imgname2 = ''

                # Image 3
                if name_image3.filename != '':
                    converted_num3 = str(random.randrange(9999999999999999999999999999999999))
                    imgname3 = converted_num3 + 'image3.jpg'  # Change this to the desired new name
                else:
                    imgname3 = ''

                # Image 4
                if name_image4.filename != '':
                    converted_num4 = str(random.randrange(9999999999999999999999999999999999))
                    imgname4 = converted_num4 + 'image4.jpg'  # Change this to the desired new name
                else:
                    imgname4 = ''

                # Query and Values
                query = "SELECT * FROM rooms WHERE cover_img = %s OR room_number = %s"
                values = (covername, roomnumber,)

                # Adding in Query And Values
                # Image 1
                if imgname1 != '':
                    query += " OR img_1 = %s"
                    values += (imgname1,)
                # Image 2
                if imgname2 != '':
                    query += " OR img_2 = %s"
                    values += (imgname2,)
                # Image 3
                if imgname3 != '':
                    query += " OR img_3 = %s"
                    values += (imgname3,)
                # Image 4
                if imgname4 != '':
                    query += " OR img_4 = %s"
                    values += (imgname4,)

                conn.execute(query, values)
                ch_img = fetch_rows_as_dicts(conn)
                if ch_img:
                    conn.execute("SELECT * FROM rooms WHERE room_number = %s", (roomnumber,))
                    q2 = fetch_rows_as_dicts(conn)
                    if q2:
                        return """
                                <script>
                                    alert('Room already exists!');
                                    window.location.assign("/admin/rooms");
                                </script>
                                """
                    else:
                        return """
                                <script>
                                    alert('An error occurred, please try again!');
                                    window.location.assign("/admin/rooms");
                                </script>
                                """
                else:
                    facility1 = request.form['facility1']
                    facility2 = request.form['facility2']
                    facility3 = request.form['facility3']
                    facility4 = request.form['facility4']
                    facility5 = request.form['facility5']
                    facility6 = request.form['facility6']
                    mypackage = request.form['mypackage']

                    conn.execute("INSERT INTO rooms (cover_img, img_1, img_2, img_3, img_4, room_number, facilities_1, facilities_2, facilities_3, facilities_4, facilities_5, facilities_6, package_id) VALUES( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (covername, imgname1, imgname2, imgname3, imgname4, roomnumber, facility1, facility2, facility3, facility4, facility5, facility6, mypackage))
                    mysql.connection.commit()
                    conn.close()

                    # Cover Image
                    name_coverimage.save('static/frontend/room/' + covername)
                    # Image 1
                    if imgname1 != '':
                        name_image1.save('static/frontend/room/' + imgname1)
                    # Image 2
                    if imgname2 != '':
                        name_image2.save('static/frontend/room/' + imgname2)
                    # Image 3
                    if imgname3 != '':
                        name_image3.save('static/frontend/room/' + imgname3)
                    # Image 4
                    if imgname4 != '':
                        name_image4.save('static/frontend/room/' + imgname4)
                    return """<Script>
                                    window.location.assign("/admin/rooms");
                                    </Script>"""
            else:
                return """
                            <script>
                                alert('An error occurred, please try again!');
                                window.location.assign("/admin/slider");
                            </script>
                            """
        return """
                <script>
                    alert('An error occurred, please try again!');
                    window.location.assign("/admin/rooms");
                </script>
                """

    if admindata["role"] == 0:

        conn.execute("SELECT * FROM package")
        package = fetch_rows_as_dicts(conn)

        conn.execute("SELECT * FROM facilities")
        facilities = fetch_rows_as_dicts(conn)

        conn.execute("SELECT r.id, r.cover_img, r.room_number, p.name FROM rooms r INNER JOIN `package` p ON r.package_id = p.id")
        show_room = fetch_rows_as_dicts(conn)
        conn.close()
        return render_template("backend/rooms.html", admindata=admindata, package=package, facilities=facilities, show_room=show_room)
    elif admindata["role"] == 1:
        return """<Script>
                window.location.assign("/");
                </Script>"""
    return """<Script>
            window.location.assign("/admin/login");
            </Script>"""


# ======================================
# ======  Rooms Part 2 (Details)  ======
# ======================================
@app.route("/admin/room-details", methods=["GET", "POST"])
def admin_room_details():
    admindata = {
        "role": session.get("role"),
        "id": session.get("id"),
        "name": session.get("name"),
        "email": session.get("email"),
        "phone": session.get("phone"),
        "pg": "rooms"
    }

    conn = mysql.connection.cursor()
    if admindata["role"] == 0:
        if request.method == "POST":
            detail_id = request.form["detail_id"]

            conn.execute("SELECT * FROM rooms WHERE id = %s", (detail_id,))
            sel_room = fetch_rows_as_dicts(conn)

            # Query and Values
            room_query = "SELECT r.id, r.cover_img, r.img_1, r.img_2, r.img_3, r.img_4, r.room_number"
            room_join = ""

            for rm in sel_room:
                # Adding in Query And Values
                # facility 1
                if rm["facilities_1"] != 0:
                    room_query += ", f1.name AS faci1"
                    room_join += " INNER JOIN facilities f1 ON r.facilities_1 = f1.id"
                # facility 2
                if rm["facilities_2"] != 0:
                    room_query += ", f2.name AS faci2"
                    room_join += " INNER JOIN facilities f2 ON r.facilities_2 = f2.id"
                # facility 3
                if rm["facilities_3"] != 0:
                    room_query += ", f3.name AS faci3"
                    room_join += " INNER JOIN facilities f3 ON r.facilities_3 = f3.id"
                # facility 4
                if rm["facilities_4"] != 0:
                    room_query += ", f4.name AS faci4"
                    room_join += " INNER JOIN facilities f4 ON r.facilities_4 = f4.id"
                # facility 5
                if rm["facilities_5"] != 0:
                    room_query += ", f5.name AS faci5"
                    room_join += " INNER JOIN facilities f5 ON r.facilities_5 = f5.id"
                # facility 6
                if rm["facilities_6"] != 0:
                    room_query += ", f6.name AS faci6"
                    room_join += " INNER JOIN facilities f6 ON r.facilities_6 = f6.id"
            final_q = room_query + ", p.name, p.price FROM rooms r INNER JOIN `package` p ON r.package_id = p.id" + room_join + " WHERE r.id = " + detail_id
            conn.execute(final_q)
            show_room = fetch_rows_as_dicts(conn)
            conn.close()
            return render_template("backend/room-details.html", admindata=admindata, show_room=show_room)
        else:
            return """<Script>
                        window.location.assign("/admin");
                        </Script>"""

    elif admindata["role"] == 1:
        return """<Script>
                window.location.assign("/");
                </Script>"""
    return """<Script>
            window.location.assign("/admin/login");
            </Script>"""


# ======================================
# ======   Rooms Part 2 (Update)  ======
# ======================================
@app.route("/admin/update-rooms", methods=["GET", "POST"])
def admin_room_update():
    admindata = {
        "role": session.get("role"),
        "id": session.get("id"),
        "name": session.get("name"),
        "email": session.get("email"),
        "phone": session.get("phone"),
        "pg": "rooms"
    }
    conn = mysql.connection.cursor()
    if request.method == "POST":
        # ID and Room Number
        upid = request.form["upid"]
        uproomnumber = request.form["uproom_number"]

        # query
        up_query = "UPDATE `rooms` SET room_number = %s"
        up_value = (uproomnumber,)

        # Facility #1
        upfacility1 = request.form['upfacility1']
        if upfacility1 != '-':
            up_query += ", facilities_1 = %s"
            up_value += (upfacility1,)

        # Facility #2
        upfacility2 = request.form['upfacility2']
        if upfacility2 != '-':
            up_query += ", facilities_2 = %s"
            up_value += (upfacility2,)

        # Facility #3
        upfacility3 = request.form['upfacility3']
        if upfacility3 != '-':
            up_query += ", facilities_3 = %s"
            up_value += (upfacility3,)

        # Facility #4
        upfacility4 = request.form['upfacility4']
        if upfacility4 != '-':
            up_query += ", facilities_4 = %s"
            up_value += (upfacility4,)

        # Facility #5
        upfacility5 = request.form['upfacility5']
        if upfacility5 != '-':
            up_query += ", facilities_5 = %s"
            up_value += (upfacility5,)

        # Facility #6
        upfacility6 = request.form['upfacility6']
        if upfacility6 != '-':
            up_query += ", facilities_6 = %s"
            up_value += (upfacility6,)

        # Package
        upmypackage = request.form['upmypackage']
        if upmypackage != '-':
            up_query += ", package_id = %s"
            up_value += (upmypackage,)

        # Cover Image
        upname_coverimage = request.files['upname_coverimage']
        if 'upname_coverimage' in request.files and request.files['upname_coverimage'].filename != '':
            upconverted_num = str(random.randrange(9999999999999999999999999999999999))
            upcovername = upconverted_num + 'coverimage.jpg'  # Change this to the desired new name
            conn.execute("SELECT * FROM rooms WHERE cover_img = %s", (upcovername,))
            upch_img = fetch_rows_as_dicts(conn)
            if len(upch_img) == 0:
                # Cover Image
                upname_coverimage.save('static/frontend/room/' + upcovername)
                up_query += ", cover_img = %s"
                up_value += (upcovername,)
            else:
                return """
                    <script>
                        alert('An error occurred, please try again!');
                        window.location.assign("/admin/rooms");
                    </script>
                    """

        # Image #1
        upname_image1 = request.files['upname_image1']
        if 'upname_image1' in request.files and request.files['upname_image1'].filename != '':
            upconverted_num1 = str(random.randrange(9999999999999999999999999999999999))
            upimgname1 = upconverted_num1 + 'image1.jpg'  # Change this to the desired new name
            conn.execute("SELECT * FROM rooms WHERE img_1 = %s", (upimgname1,))
            upch_img1 = fetch_rows_as_dicts(conn)
            if len(upch_img1) == 0:
                # Image #1
                upname_image1.save('static/frontend/room/' + upimgname1)
                up_query += ", img_1 = %s"
                up_value += (upimgname1,)
            else:
                return """
                    <script>
                        alert('An error occurred, please try again!');
                        window.location.assign("/admin/rooms");
                    </script>
                    """

        # Image #2
        upname_image2 = request.files['upname_image2']
        if 'upname_image2' in request.files and request.files['upname_image2'].filename != '':
            upconverted_num2 = str(random.randrange(9999999999999999999999999999999999))
            upimgname2 = upconverted_num2 + 'image2.jpg'  # Change this to the desired new name
            conn.execute("SELECT * FROM rooms WHERE img_2 = %s", (upimgname2,))
            upch_img2 = fetch_rows_as_dicts(conn)
            if len(upch_img2) == 0:
                # Image #2
                upname_image2.save('static/frontend/room/' + upimgname2)
                up_query += ", img_2 = %s"
                up_value += (upimgname2,)
            else:
                return """
                    <script>
                        alert('An error occurred, please try again!');
                        window.location.assign("/admin/rooms");
                    </script>
                    """

        # Image #3
        upname_image3 = request.files['upname_image3']
        if 'upname_image3' in request.files and request.files['upname_image3'].filename != '':
            upconverted_num3 = str(random.randrange(9999999999999999999999999999999999))
            upimgname3 = upconverted_num3 + 'image3.jpg'  # Change this to the desired new name
            conn.execute("SELECT * FROM rooms WHERE img_3 = %s", (upimgname3,))
            upch_img3 = fetch_rows_as_dicts(conn)
            if len(upch_img3) == 0:
                # Image #3
                upname_image3.save('static/frontend/room/' + upimgname3)
                up_query += ", img_3 = %s"
                up_value += (upimgname3,)
            else:
                return """
                    <script>
                        alert('An error occurred, please try again!');
                        window.location.assign("/admin/rooms");
                    </script>
                    """

        # Image #4
        upname_image4 = request.files['upname_image4']
        if 'upname_image4' in request.files and request.files['upname_image4'].filename != '':
            upconverted_num4 = str(random.randrange(9999999999999999999999999999999999))
            upimgname4 = upconverted_num4 + 'image4.jpg'  # Change this to the desired new name
            conn.execute("SELECT * FROM rooms WHERE img_4 = %s", (upimgname4,))
            upch_img4 = fetch_rows_as_dicts(conn)
            if len(upch_img4) == 0:
                # Image #4
                upname_image4.save('static/frontend/room/' + upimgname4)
                up_query += ", img_4 = %s"
                up_value += (upimgname4,)
            else:
                return """
                    <script>
                        alert('An error occurred, please try again!');
                        window.location.assign("/admin/rooms");
                    </script>
                    """

        # Updating query
        up_value += (upid,)
        final_q = up_query + " WHERE id = %s"
        conn.execute(final_q, up_value)
        mysql.connection.commit()
        conn.close()
        return """
            <script>
                alert('Room Successfully Updated!');
                window.location.assign("/admin/rooms");
            </script>
            """


# ======================================
# ============   Bookings   ============
# ======================================
def calculate_total_cost(starting_date, ending_date, room_cost_per_day):
    starting_date = datetime.datetime.strptime(starting_date, '%Y-%m-%d').date()
    ending_date = datetime.datetime.strptime(ending_date, '%Y-%m-%d').date()
    days = (ending_date - starting_date).days + 1
    total_cost = int(days) * int(room_cost_per_day)
    return total_cost

@app.route("/admin/bookings", methods=["GET", "POST"])
def admin_orders():
    admindata = {
        "role": session.get("role"),
        "id": session.get("id"),
        "name": session.get("name"),
        "email": session.get("email"),
        "phone": session.get("phone"),
        "pg": "bookings"
    }
    
    conn = mysql.connection.cursor()
    conn.execute("SELECT * FROM rooms")
    room = fetch_rows_as_dicts(conn)

    conn.execute("SELECT b.id, u.name, u.email, r.room_number, b.total_cost, b.status, p.name AS pname, b.booking_date, b.starting_date, b.ending_date, b.credit_card_number, b.room_cost FROM room_booking b INNER JOIN users u ON b.user_id = u.id INNER JOIN rooms r ON b.room_id = r.id INNER JOIN package p ON r.package_id = p.id WHERE status = 'booked' ORDER BY b.id DESC")
    book = fetch_rows_as_dicts(conn)

    if request.method == "POST":
        dis = request.form["dis"]
        if dis == "false":
            # User ID
            usid = int(request.form["usid"])
            # Room ID
            room_number = request.form["room_number"]
            # Booking Date
            book_date = datetime.datetime.now()
            finalbook_date = book_date.strftime("%Y-%m-%d")
            # Starting Date
            starting_date = request.form["starting_date"]
            # Ending Date
            ending_date = request.form["ending_date"]
            # Room Price
            room_price = request.form["room_price"]
            # Total Cost
            total_cost = calculate_total_cost(starting_date, ending_date, room_price)
            # Credit Card
            cd_num = request.form["cd_num"]

            # Check if the room is available for the specified dates
            available = "True"
            conn.execute("SELECT * FROM room_booking WHERE room_id = %s", (room_number,))
            room_booking = fetch_rows_as_dicts(conn)

            for booking in room_booking:
                # existing_start = datetime.datetime.strptime(booking["starting_date"], "%Y-%m-%d").date()
                # existing_end = datetime.datetime.strptime(booking["ending_date"], "%Y-%m-%d").date()
                existing_start = datetime.datetime.strptime(booking["starting_date"], "%Y-%m-%d").strftime("%Y%m%d")
                existing_end = datetime.datetime.strptime(booking["ending_date"], "%Y-%m-%d").strftime("%Y%m%d")

                # Convert starting_date and ending_date to datetime.date objects
                # input_start = datetime.datetime.strptime(starting_date, "%Y-%m-%d").date()
                # input_end = datetime.datetime.strptime(ending_date, "%Y-%m-%d").date()
                input_start = datetime.datetime.strptime(starting_date, "%Y-%m-%d").strftime("%Y%m%d")
                input_end = datetime.datetime.strptime(ending_date, "%Y-%m-%d").strftime("%Y%m%d")

                if (input_start <= existing_end) and (input_end >= existing_start):
                    available = "False"
                    break

            if available == "True":
                status = "booked"
                query = "INSERT INTO room_booking (user_id, room_id, booking_date, starting_date, ending_date, room_cost, total_cost, credit_card_number, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                values = (usid, room_number, finalbook_date, starting_date, ending_date, room_price, total_cost, cd_num, status)
                conn.execute(query, values)
                mysql.connection.commit()

                conn.execute("SELECT * FROM `amount` ORDER BY `id` DESC LIMIT 1")
                t_amount = fetch_rows_as_dicts(conn)
                for tm in t_amount:
                    add_amount = int(tm["total_capital"]) + total_cost

                conn.execute("INSERT INTO amount (total_capital) VALUES (%s)", (add_amount,))
                mysql.connection.commit()

                if admindata["role"] == 0:
                    return """
                            <script>
                                alert('Room Successfully Booked!');
                                window.location.assign("/admin/bookings");
                            </script>
                            """
                elif admindata["role"] == 1:
                    return """
                            <script>
                                alert('Room Successfully Booked!');
                                window.location.assign("/");
                            </script>
                            """
            else:
                if admindata["role"] == 0:
                    return """
                            <script>
                                alert('Room is not available for the specified dates!');
                                window.location.assign("/admin/bookings");
                            </script>
                            """
                elif admindata["role"] == 1:
                    return """
                            <script>
                                alert('Room is not available for the specified dates!');
                                window.location.assign("/");
                            </script>
                            """
        else:
            bookid = request.form["bookid"]
            bookprice = request.form["bookprice"]
            bookstatus = "disapprove"
            conn.execute("UPDATE room_booking SET status = %s WHERE id = %s", (bookstatus, bookid))
            mysql.connection.commit()
            conn.execute("SELECT * FROM amount ORDER BY id DESC LIMIT 1")
            bookam = conn.fetchone()
            minus_amount = int(bookam[1]) - int(bookprice)
            adding_amount = int(bookam[2]) + int(bookprice)
            conn.execute("INSERT INTO amount (total_capital, returned_capital) VALUES (%s, %s)", (minus_amount, adding_amount))
            mysql.connection.commit()
            conn.close()
            return """
                    <script>
                        alert('You've disapproved a customers room!');
                        window.location.assign("/admin/bookings");
                    </script>
                    """
    
    return render_template("backend/bookings.html", admindata=admindata, room=room, book=book)

@app.route("/get-room-price", methods=["POST"])
def get_room_price():
    room_id = request.form.get("id")

    # Connect to the database
    with mysql.connection.cursor() as conn:
        query = "SELECT p.price,p.name FROM rooms r INNER JOIN package p ON r.package_id = p.id WHERE r.id = %s"
        conn.execute(query, (room_id,))
        price = conn.fetchone()

    return jsonify({"price": price[0], "name": price[1]})


if __name__ == "__main__":
    app.run(debug=True)