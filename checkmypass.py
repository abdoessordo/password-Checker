import requests
import hashlib


def request_api_data(query_char):
	url = f'https://api.pwnedpasswords.com/range/{query_char}'
	response = requests.get(url)
	if response.status_code != 200:
		raise RuntimeError(f'Error fetching: {response.status_code}, check the api and try again')
	return response


def get_password_leaks_count(response, hash):
	response = (line.split(':') for line in response.text.splitlines())
	for h, count in response:
		if h == hash:
			return count
	return 0

def encode_password(password):
	sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
	return sha1password[:5], sha1password[5:]


def pwned_api_check(password):
	#check password if exists in API response
	first5, tail = encode_password(password)[0] , encode_password(password)[1]
	response = request_api_data(first5)
	return get_password_leaks_count(response, tail)


def main(*args):
	for password in args:
		count = pwned_api_check(password)
		if count:
			print(f'"{password}" was hacked {count}. You should change it !')
		else:
			print(f'"{password}" was never hacked.')

if __name__ == '__name__':
	main('123', 'Hello', 'Salam', '123456789', 'asdasfaifbasdnasjdn')
