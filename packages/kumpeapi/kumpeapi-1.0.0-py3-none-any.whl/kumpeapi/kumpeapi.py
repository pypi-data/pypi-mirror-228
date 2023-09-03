import pymysql
from datetime import date
import datetime
import requests
from flask import request
import string
import random


class kapi:
    def __init__(
        self,
        apikey: str,
        mysql_creds={'username': '', 'password': ''}
    ):
        self.apikey = apikey
        self.mysql_creds = mysql_creds

    def create_user(
        self,
        username,
        password,
        email,
        first_name,
        last_name,
        comment="Added via API"
    ):
        data = {
            "_key": self.apikey,
            "login": username,
            "pass": password,
            "email": email,
            "name_f": first_name,
            "name_l": last_name,
            "comment": comment
            }
        response = requests.post(
            'https://www.kumpeapps.com/api/users',
            data=data
            )
        return response.json()

    def create_subuser(
        self,
        username,
        password,
        email,
        first_name,
        last_name,
        master_id,
        comment="Added via API"
    ):
        data = {
            "_key": self.apikey,
            "login": username,
            "pass": password,
            "email": email,
            "name_f": first_name,
            "name_l": last_name,
            "comment": comment,
            "subusers_parent_id": master_id}
        response = requests.post(
            'https://www.kumpeapps.com/api/users',
            data=data
            )
        return response.json()

    def authenticate_user(self, username, password):
        data = {
            "_key": self.apikey,
            "login": username,
            "pass": password
            }
        response = requests.get(
            'https://www.kumpeapps.com/api/check-access/by-login-pass',
            params=data
            )
        return response.json()

    def add_access(
        self,
        user_id,
        product_id,
        begin_date=date.today(),
        expire_date='2037-12-31',
        comment='Added via API'
    ):
        data = {
            "_key": self.apikey,
            "user_id": user_id,
            "product_id": product_id,
            "begin_date": begin_date,
            "expire_date": expire_date,
            "comment": comment
            }
        response = requests.post(
            'https://www.kumpeapps.com/api/access',
            data=data
            )
        return response.json()

    def get_user_info(self, username):
        if self.mysql_creds['username'] != '':
            db = self.mysql_connect()
            cursor = db.cursor(
                pymysql.cursors.DictCursor
                )
            sql = "SELECT * FROM vw_am_user WHERE 1=1 AND login = %s;"
            cursor.execute(sql, (username,))
            results = cursor.fetchone()
            cursor.close()
            db.close()
            return results
        else:
            raise PermissionError("MySQL Creds required for this function")

    def get_authkey_info(self, auth_key):
        if self.mysql_creds['username'] != '':
            db = self.mysql_connect()
            cursor = db.cursor(pymysql.cursors.DictCursor)
            sql = "SELECT * FROM %s WHERE 1=1 AND auth_key = %s;"
            cursor.execute(sql, ('Core_RESTAPI.v5__vw_Auth_Keys', auth_key,))
            results = cursor.fetchone()
            cursor.close()
            db.close()
            return results
        else:
            raise PermissionError("MySQL Creds required for this function")

    def get_user_info_byid(self, user_id):
        if self.mysql_creds['username'] != '':
            db = self.mysql_connect()
            cursor = db.cursor(pymysql.cursors.DictCursor)
            sql = "SELECT * FROM vw_am_user WHERE 1=1 AND user_id = %s;"
            cursor.execute(sql, (user_id,))
            results = cursor.fetchone()
            cursor.close()
            db.close()
            return results
        else:
            raise PermissionError("MySQL Creds required for this function")

    def delete_user(self, user_id):
        data = {
            "_key": self.apikey,
            "_method": "DELETE"
            }
        response = requests.post(
            f'https://www.kumpeapps.com/api/users/{user_id}',
            data=data
            )
        return response.json()

    def expire_access(self, user_id, product_id, comment="Expired via API"):
        if self.mysql_creds['username'] != '':
            today = date.today()
            yesterday = today - datetime.timedelta(days=1)
            db = self.mysql_connect()
            cursor = db.cursor(pymysql.cursors.DictCursor)
            sql = """SELECT access_id, expire_date FROM
            Core_KumpeApps.am_access WHERE 1=1
            AND user_id = %s AND product_id = %s AND
            expire_date > now();"""
            cursor.execute(sql, (user_id, product_id))
            results = cursor.fetchall()
            cursor.close()
            db.close()
            if not results:
                return
            for access in results:
                access_id = access['access_id']
                data = {
                    "_key": self.apikey,
                    "expire_date": yesterday,
                    "comment": comment
                    }
                requests.put(
                    f'https://www.kumpeapps.com/api/access/{access_id}',
                    data=data
                    )
            return
        else:
            raise PermissionError("MySQL Creds required for this function")

    def update_user(
        self,
        user_id,
        username,
        email,
        first_name,
        last_name,
        comment="Updated via API"
    ):
        data = {
            "_key": self.apikey,
            "_method": "PUT",
            "login": username,
            "email": email,
            "name_f": first_name,
            "name_l": last_name,
            "comment": comment
            }
        response = requests.post(
            f'https://www.kumpeapps.com/api/users/{user_id}',
            data=data
            )
        return response

    def access_log_insert(self, user_id, referrer, url):
        if self.mysql_creds['username'] != '':
            ip = request.environ['HTTP_X_FORWARDED_FOR']
            db = self.mysql_connect()
            cursor = db.cursor(pymysql.cursors.DictCursor)
            sql = """INSERT INTO
            `am_access_log`(`user_id`, `time`, `url`, `remote_addr`,
            `referrer`) VALUES (%s,now(),%s,%s,%s)"""
            cursor.execute(sql, (user_id, url, ip, referrer, ))
            db.commit()
            cursor.close()
            return
        else:
            raise PermissionError("MySQL Creds required for this function")

    def create_auth_link(
        self,
        master_id,
        auth_user_id,
        link_user_id,
        link="https://khome.kumpeapps.com/portal/wish-list.php",
        scope="WishList",
        scope2="none",
        scope3="none",
        scope4="none",
        kiosk=0
    ):
        if self.mysql_creds['username'] != '':
            randomstring = string.ascii_letters + string.digits
            authToken = ''.join(random.choice(randomstring) for i in range(10))
            db = pymysql.connect(
                db='Web_KumpeHome',
                user=self.mysql_creds['username'],
                passwd=self.mysql_creds['password'],
                host='sql.kumpedns.us',
                port=3306
                )
            cursor = db.cursor(pymysql.cursors.DictCursor)
            sql = """INSERT INTO `Web_KumpeHome`.`AuthenticatedLinks`
            (`master_id`,`authenticated_user_id`,`link_user_id`,`link`,
            `expiration`,`token`,`scope`,`scope2`,`scope3`,`scope4`,
            `is_kiosk`) VALUES (%s,%s,%s,%s,NOW() + INTERVAL 365 DAY,
            %s,%s,%s,%s,%s,%s);"""
            cursor.execute(
                sql,
                (
                    master_id,
                    auth_user_id,
                    link_user_id,
                    link,
                    authToken,
                    scope,
                    scope2,
                    scope3,
                    scope4,
                    kiosk,
                    )
                )
            db.commit()
            cursor.close()
            db.close()
            return link+'?token='+authToken
        else:
            raise PermissionError("MySQL Creds required for this function")

    def mysql_connect(self):
        db = pymysql.connect(
            db='Core_KumpeApps',
            user=self.mysql_creds['username'],
            passwd=self.mysql_creds['password'],
            host='sql.kumpedns.us',
            port=3306
            )
        return db