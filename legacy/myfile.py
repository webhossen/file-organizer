import os
import shutil

path = input("Enter folder path: ").strip().strip('"')

if not os.path.isdir(path):
    print("Error: The folder path does not exist.")
    raise SystemExit

for file in os.listdir(path):
    source = os.path.join(path, file)

    # Skip folders; process files only
    if not os.path.isfile(source):
        continue

    # Get the file extension
    filename, extension = os.path.splitext(file)
    extension = extension[1:].lower()

    # Handle files without extensions
    if not extension:
        extension = "No Extension"

    # Create the destination folder
    destination_folder = os.path.join(path, extension)

    os.makedirs(destination_folder, exist_ok=True)

    # Prevent moving a file onto itself
    destination = os.path.join(destination_folder, file)

    # Avoid overwriting files with the same name
    if os.path.exists(destination):
        name, ext = os.path.splitext(file)
        counter = 1

        while os.path.exists(os.path.join(destination_folder, f"{name}_{counter}{ext}")):
            counter += 1

        destination = os.path.join(destination_folder, f"{name}_{counter}{ext}")

    try:
        shutil.move(source, destination)
        print(f"Moved: {file} -> {extension}/")
    except OSError as error:
        print(f"Could not move {file}: {error}")

print("File organization complete!")
