import re
import smtplib
import logging
import socket
import validate_email

def main1():
	print("hello")

def main():
	is_valid = validate_email.validate_email('example@example.com',verify=True)
	print(is_valid)

if __name__ == '__main__':
	main()