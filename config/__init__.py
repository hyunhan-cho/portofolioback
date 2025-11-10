try:
	import pymysql  # Windows 환경에서 mysqlclient 대체
	pymysql.install_as_MySQLdb()
except Exception:
	# PyMySQL 미설치 시 무시 (requirements 설치 후 활성)
	pass
