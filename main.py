import json
import shutil
import uuid
from datetime import datetime
from pathlib import Path


CATEGORIES = {
	".jpg": "Images",
	".jpeg": "Images",
	".png": "Images",
	".gif": "Images",
	".pdf": "Documents",
	".doc": "Documents",
	".docx": "Documents",
	".txt": "Documents",
	".mp3": "Audio",
	".wav": "Audio",
	".mp4": "Videos",
	".mov": "Videos",
	".zip": "Archives",
	".tar": "Archives",
	".gz": "Archives",
}
LOG_FILE_NAME = ".organizer_log.txt"


def scan_directory(directory):
	folder = Path(directory).expanduser()
	if not folder.exists():
		raise FileNotFoundError(f"Folder does not exist: {folder}")
	if not folder.is_dir():
		raise NotADirectoryError(f"Path is not a folder: {folder}")

	return [
		str(file_path)
		for file_path in sorted(
		file_path
		for file_path in folder.iterdir()
		if file_path.name != LOG_FILE_NAME
		and not file_path.is_symlink()
		and file_path.is_file()
		)
	]


def get_category(file_name):
	return CATEGORIES.get(Path(file_name).suffix.lower(), "Other")


def log_file(message, log_path=None):
	timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	if log_path is None:
		log_path = Path("organizer_log.txt")
	if isinstance(message, dict):
		line = json.dumps({"timestamp": timestamp, **message}, ensure_ascii=False)
	else:
		line = f"[{timestamp}] {message}"
	with Path(log_path).open("a", encoding="utf-8") as log:
		log.write(f"{line}\n")


def start_organizer(main_folder, files=None, return_details=False, transaction_id=None):
	if main_folder is None or (isinstance(main_folder, str) and not main_folder.strip()):
		raise ValueError("A folder path is required.")
	folder = Path(main_folder).expanduser()
	if not folder.exists():
		raise FileNotFoundError(f"Folder does not exist: {folder}")
	if not folder.is_dir():
		raise NotADirectoryError(f"Path is not a folder: {folder}")
	folder = folder.resolve()

	files_to_move = scan_directory(folder) if files is None else files
	moved_files = []
	failed_files = []
	log_errors = []
	log_path = folder / LOG_FILE_NAME
	transaction_id = transaction_id or uuid.uuid4().hex

	for file_path in files_to_move:
		source = Path(file_path).expanduser()
		try:
			if source.is_symlink() or not source.is_file():
				raise ValueError(f"Not a regular file or no longer exists: {source}")
			if source.name == LOG_FILE_NAME:
				continue

			category = get_category(source.name)
			target_folder = folder / category
			if source.resolve().parent == target_folder.resolve():
				continue

			target_folder.mkdir(parents=True, exist_ok=True)
			target = target_folder / source.name
			base_name = source.stem
			extension = source.suffix
			counter = 1
			while target.exists() or target.is_symlink():
				target = target_folder / f"{base_name} ({counter}){extension}"
				counter += 1

			shutil.move(str(source), str(target))
			moved_files.append((str(source), str(target)))
			try:
				log_file(
					{
						"action": "move",
						"transaction_id": transaction_id,
						"source": str(source.resolve()),
						"target": str(target.resolve()),
					},
					log_path,
				)
			except OSError as error:
				log_errors.append(str(error))
		except (OSError, ValueError) as error:
			failed_files.append((str(source), str(error)))

	if return_details:
		return moved_files, failed_files, log_errors
	return moved_files


def undo_organizer(main_folder, transaction_id):
	folder = Path(main_folder).expanduser().resolve()
	log_path = folder / LOG_FILE_NAME
	if not log_path.exists():
		return [], ["The organizer log was not found."]

	try:
		with log_path.open("r", encoding="utf-8") as log:
			records = []
			for line in log:
				if not line.strip():
					continue
				try:
					records.append(json.loads(line))
				except json.JSONDecodeError:
					continue
	except OSError as error:
		return [], [f"Could not read the organizer log: {error}"]

	restored_files = []
	undo_errors = []
	for record in records:
		if not isinstance(record, dict):
			continue
		if record.get("action") != "move" or record.get("transaction_id") != transaction_id:
			continue
		source_value = record.get("source")
		target_value = record.get("target")
		if not isinstance(source_value, str) or not isinstance(target_value, str):
			undo_errors.append("A move entry in the log is missing its source or target path.")
			continue

		source = Path(source_value)
		target = Path(target_value)
		try:
			if target.is_symlink() or not target.is_file():
				raise FileNotFoundError(f"Moved file is no longer available: {target}")
			if source.exists() or source.is_symlink():
				raise FileExistsError(f"Original path already exists; not overwriting: {source}")
			source.parent.mkdir(parents=True, exist_ok=True)
			shutil.move(str(target), str(source))
			restored_files.append((str(target), str(source)))
		except OSError as error:
			undo_errors.append(str(error))

	return restored_files, undo_errors


def ask_yes_no(prompt):
	while True:
		answer = input(prompt).strip().lower()
		if answer in {"y", "n"}:
			return answer == "y"
		print("Please enter y or n.")


def main():
	print("Welcome to the file organizer.")
	try:
		directory = input("Enter the folder path to organize (or leave blank to cancel): ").strip()
		if len(directory) >= 2 and directory[0] == directory[-1] and directory[0] in "\"'":
			directory = directory[1:-1]
		if not directory:
			print("Operation cancelled.")
			return

		files = scan_directory(directory)
		if not files:
			print("No files found directly in the selected folder.")
			return

		print("Files to be organized:")
		for file_path in files:
			print(f"- {file_path} -> {get_category(Path(file_path).name)}")
		if not ask_yes_no("Proceed with moving these files? (y/n): "):
			print("Operation cancelled. No files were moved.")
			return

		transaction_id = uuid.uuid4().hex
		moved_files, failed_files, log_errors = start_organizer(
			directory,
			files=files,
			return_details=True,
			transaction_id=transaction_id,
		)
		print(f"Done: moved {len(moved_files)} file(s).")
		for source, error in failed_files:
			print(f"Could not move {source}: {error}")
		for error in log_errors:
			print(f"File moved, but could not write to the log: {error}")

		if moved_files:
			if ask_yes_no("Do you like the organization? (y/n): "):
				print("Happy to serve you!")
			else:
				restored_files, undo_errors = undo_organizer(directory, transaction_id)
				print(f"Undo complete: restored {len(restored_files)} file(s).")
				for error in undo_errors:
					print(f"Could not undo a move: {error}")
	except KeyboardInterrupt:
		print("Operation stopped by the user.")
	except EOFError:
		print("No folder path was entered. Operation cancelled.")
	except (OSError, ValueError) as error:
		print(f"Could not organize files: {error}")


if __name__ == "__main__":
	main()
