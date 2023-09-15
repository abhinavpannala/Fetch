import psycopg2
from utils.read_json import read
cred_file_path = "credentials.json"

postgres_config = read(cred_file_path, "postgres")
database = postgres_config['database']  
user = postgres_config['user']
password = postgres_config['password']
host = postgres_config['host']
port = postgres_config['port']

def write_to_postgres(data):
		user_id = data['user_id'] 
		app_version = data['app_version']   
		device_type = data['device_type']  
		masked_ip = data['masked_ip'] 
		masked_device_id = data['masked_device_id'] 
		locale = data['locale'] 
		create_date = data['create_date'] 

		conn = psycopg2.connect(
				   database=database, 
				   user=user, 
				   password=password, 
				   host=host, 
				   port=port
			   )
		cursor = conn.cursor()

		sql = '''INSERT INTO user_logins(user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date) 
			      VALUES(%s, %s, %s, %s, %s, %s, %s);'''
		cursor.execute(sql, (user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date))

		conn.commit()
		conn.close()

