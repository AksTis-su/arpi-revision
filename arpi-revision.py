#!/usr/bin/env python3
#
# AksTis Raspberry Pi Revision
#
# Описание:
#   Получение номера ревизии Raspberry Pi
#   Скрипт выводит номер ревизии из /proc/cpuinfo и по этому номеру определяет модель Raspberry Pi
#
# Использование:
#   1. Загрузите скрипт:
#      git clone https://github.com/akstis-su/arpi-revision.git
#   2. Дайте права на выполнение:
#      chmod +x arpi-revision.sh
#   3. Запустите:
#      ./arpi-revision.sh
#
# Автор: AksTis
# https://akstis.su/
#
# Версия: 1.0
# Дата: 20 Апреля 2025
# Лицензия: MIT

def get_rpi_revision():
	try:
		with open('/proc/cpuinfo', 'r') as f:
			for line in f:
				if line.startswith('Revision'):
					revision = line.split(':')[1].strip()
					return revision
	except FileNotFoundError:
		return "Не удалось прочитать /proc/cpuinfo"
	return "Ревизия не найдена"

def get_rpi_model(revision):
	# Словарь для старых четырехсимвольных ревизий
	legacy_revision_map = {
		'0002': 'Model B, CPU BCM2835, 256MB, PCB Rev 1.0, Egoman',
		'0003': 'Model B, CPU BCM2835, 256MB, PCB Rev 1.0, Egoman',
		'0004': 'Model B, CPU BCM2835, 256MB, PCB Rev 2.0, Sony',
		'0005': 'Model B, CPU BCM2835, 256MB, PCB Rev 2.0, Qisda',
		'0006': 'Model B, CPU BCM2835, 256MB, PCB Rev 2.0, Egoman',
		'0007': 'Model A, CPU BCM2835, 256MB, PCB Rev 2.0, Egoman',
		'0008': 'Model A, CPU BCM2835, 256MB, PCB Rev 2.0, Sony',
		'0009': 'Model A, CPU BCM2835, 256MB, PCB Rev 2.0, Qisda',
		'000d': 'Model B, CPU BCM2835, 512MB, PCB Rev 2.0, Egoman',
		'000e': 'Model B, CPU BCM2835, 512MB, PCB Rev 2.0, Sony',
		'000f': 'Model B, CPU BCM2835, 512MB, PCB Rev 2.0, Qisda',
		'0010': 'Model B+, CPU BCM2835, 512MB, PCB Rev 1.0, Sony',
		'0011': 'Compute Module, CPU BCM2835, 512MB, PCB Rev 1.0, Sony',
		'0012': 'Model A+, CPU BCM2835, 256MB, PCB Rev 1.1, Sony',
		'0013': 'Model B+, CPU BCM2835, 512MB, PCB Rev 1.2, Embest',
		'0014': 'Compute Module, CPU BCM2835, 512MB, PCB Rev 1.0, Embest',
		'0015': 'Model A+, CPU BCM2835, 256MB/512MB, PCB Rev 1.1, Embest',
	}

	# Словари для расшифровки шестисимвольных ревизий
	# NOQu uuWu FMMM CCCC PPPP TTTTTTTT RRRR

	# FMMM New flag + Memory size
	memory_map = {
		'8': '256MB',   # F=1, MMM=000
		'9': '512MB',   # F=1, MMM=001
		'a': '1GB',     # F=1, MMM=010
		'b': '2GB',     # F=1, MMM=011
		'c': '4GB',     # F=1, MMM=100
		'd': '8GB',     # F=1, MMM=101
		'e': '16GB',    # F=1, MMM=110
	}

	# CCCC Manufacturer
	manufacturer_map = {
		'0': 'SONY UK',
		'1': 'Egoman',
		'2': 'Embest',
		'3': 'SONY Japan',
		'4': 'Embest',
		'5': 'Stadium',
	}

	# PPPP Processor
	processor_map = {
		'0': 'BCM2835',
		'1': 'BCM2836',
		'2': 'BCM2837',
		'3': 'BCM2711',
		'4': 'BCM2712',
	}

	# TTTTTTTT Type
	model_map = {
		'00': 'Model A',
		'01': 'Model B',
		'02': 'Model A+',
		'03': 'Model B+',
		'04': 'Model 2B',
		'05': 'Alpha (early prototype)',
		'06': 'Compute Module',
		'08': 'Model 3B',
		'09': 'Zero',
		'0a': 'Compute Module 3',
		'0c': 'Zero W',
		'0d': 'Model 3B+',
		'0e': 'Model 3A+',
		'0f': 'Internal use only',
		'10': 'Compute Module 3+',
		'11': 'Model 4B',
		'12': 'Zero 2W',
		'13': 'Model 400',
		'14': 'Compute Module 4',
		'15': 'Compute Module 4S',
		'16': 'Internal use only',
		'17': 'Model 5',
		'18': 'Compute Module 5',
		'19': 'Model 500',
		'1a': 'Compute Module 5 Lite',
	}

		# RRRR Revision
	pcb_map = {
		'0': '1.0',
		'1': ' 1.1',
		'2': '1.2',
		'3': '1.3',
		'4': '1.4',
		'5': '1.5',
	}

	# Обработка ревизии
	if len(revision) == 4:
		return legacy_revision_map.get(revision, 'Unknown Model (Legacy Revision)')

	if len(revision) == 6:
		try:
			memory = memory_map.get(revision[0], 'Unknown Memory')
			manufacturer = manufacturer_map.get(revision[1], 'Unknown Manufacturer')
			processor = processor_map.get(revision[2], 'Unknown Processor')
			model = model_map.get(revision[3:5], 'Unknown Model')
			pcb = pcb_map.get(revision[5], 'Unknown PCB')

			return (f"{model}, {processor}, {memory}, PCB Rev {pcb}, {manufacturer}")
		except IndexError:
			return "Invalid 6-character revision format"

	return "Unknown Revision"

if __name__ == "__main__":
	revision = get_rpi_revision()
	model = get_rpi_model(revision)
	print(f"Ревизия: {revision}")
	print(f"Модель: {model}")
