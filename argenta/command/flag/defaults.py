from argenta.command.flag import Flag
import re


help_flag = Flag(flag_name='help', possible_flag_values=False)
short_help_flag = Flag(flag_name='h', flag_prefix='-', possible_flag_values=False)

info_flag = Flag(flag_name='info', possible_flag_values=False)
short_info_flag = Flag(flag_name='i', flag_prefix='-', possible_flag_values=False)

all_flag = Flag(flag_name='all', possible_flag_values=False)
short_all_flag = Flag(flag_name='a', flag_prefix='-', possible_flag_values=False)

host_flag = Flag(flag_name='host', possible_flag_values=re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'))
short_host_flag = Flag(flag_name='h', flag_prefix='-', possible_flag_values=re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'))

port_flag = Flag(flag_name='port', possible_flag_values=re.compile(r'^\d{1,5}$'))
short_port_flag = Flag(flag_name='p', flag_prefix='-', possible_flag_values=re.compile(r'^\d{1,5}$'))
