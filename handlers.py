from aiogram import F , Router , Bot
from aiogram.filters import CommandStart ,Command , CommandObject
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message , CallbackQuery , LabeledPrice , PreCheckoutQuery
from aiogram.fsm.state import StatesGroup ,State
from aiogram.fsm.context import FSMContext
import os
import aiofiles
import shutil
import psutil
import json

router = Router()

ADMIN_ID = 1000000 #change to your telegram id

class Mkdir(StatesGroup):
    name = State()

class Mkfile(StatesGroup):
    name = State()

class files(StatesGroup):
    file_name = State()

class Directory(StatesGroup):
    directory_path = State()

class files_delete(StatesGroup):
    files_name = State()

class mkfileread(StatesGroup):
    name = State()

class mkfilewrte(StatesGroup):
    name = State()
    text = State()

class copyfile(StatesGroup):
    name = State()
    dir = State()

class movefile(StatesGroup):
    name = State()
    dir = State()

@router.message(CommandStart())
async def start(message:Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer('🖥️Welcome to your computer')
    else:
        await message.answer('❌Access denied, you are not an admin')

@router.message(Command('directory'))
async def dirictory(message:Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer(f'Current directory: {os.getcwd()}')
    else:
        await message.answer('❌Access denied, you are not an admin')

@router.message(Command('mkdir'))
async def mkdir(message:Message, state:FSMContext):
    if message.from_user.id == ADMIN_ID:
        await state.set_state(Mkdir.name)
        await message.answer(f'The folder will be added to: {os.getcwd()} \nEnter the folder name..')
    else:
        await message.answer('❌Access denied, you are not an admin')


@router.message(Mkdir.name)
async def create(message:Message , state:FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()
    try:
        directory_path = os.path.join(os.getcwd(), data["name"])
        os.mkdir(directory_path)
        await message.answer(f'✅A new folder has been created: "{data["name"]}"\nPath: {directory_path}')
    except Exception as e:
        message.answer(f'❌An error occurred while creating the folder:{e}')
    await state.clear()

@router.message(Command('remove'))
async def removefile(message:Message, state:FSMContext):
    if message.from_user.id == ADMIN_ID:
        await state.set_state(files_delete.files_name)
        await message.answer(f'Deletion path: {os.getcwd()}Please enter the folder name..')
    else:
        await message.answer('❌Access denied, you are not an admin')

@router.message(files_delete.files_name)
async def removes(message:Message , state:FSMContext):
    await state.update_data(files_name=message.text)
    data = await state.get_data()

    directory_path = os.path.join(os.getcwd(), data["files_name"])

    print(f'Deleting a folder: {directory_path}')

    try:
        try:
            shutil.rmtree(directory_path)
        except:
            os.remove(directory_path)
        await message.answer(f'✅The folder "{data["files_name"]}" in the directory: {os.getcwd()} has been successfully deleted.')
    except Exception as e:
        await message.answer(f'❌An error occurred: {e}')
    await state.clear()

@router.message(Command('up'))
async def up(message:Message):
    if message.from_user.id == ADMIN_ID:
        os.chdir('..')
        await message.answer(f'✅The directory has been updated: {os.getcwd()}')
    else:
        await message.answer('❌Access denied, you are not an admin')

@router.message(Command('into'))
async def intodir(message:Message,state:FSMContext):
    if message.from_user.id == ADMIN_ID:
        await message.answer('Enter the directory..')
        await state.set_state(Directory.directory_path)
    else:
        await message.answer('❌Access denied, you are not an admin')

@router.message(Directory.directory_path)
async def new_directory(message:Message , state:FSMContext):
    await state.update_data(dirictory_path=message.text)
    data = await state.get_data()

    print(f'Transition along the path:  {data["dirictory_path"]}')

    try:
        os.chdir(data["dirictory_path"])
        await message.answer(f'✅The directory has been updated to the current one: {os.getcwd()}')
    except Exception as e:
        await message.answer(f'❌An error occurred: {e}')
    await state.clear()

@router.message(Command('open_r'))
async def open(message:Message , state:FSMContext):
    if message.from_user.id == ADMIN_ID:
        await message.answer('Enter the folder name..')
        await state.set_state(files.file_name)
    else:
        await message.answer('❌Access denied, you are not an admin')

@router.message(files.file_name)
async def info(message:Message , state:FSMContext):
    await state.update_data(file_name=message.text)
    data = await state.get_data()

    directory = os.path.join(os.getcwd(), data["file_name"])
    print(directory)


    try:
        async with aiofiles.open(directory,'r') as file:
            data_file = file.read()
            await message.answer(data_file)
    except Exception as e:
        await message.answer(f'❌An error occurred: {e}')
    finally:
        file.close()

    await state.clear()
@router.message(Command('help'))
async def help(message:Message):
    await message.answer('List of all commands:\n' 
    '/start - restart the bot \n' 
    '/mkdir - create a folder in the current directory \n'
    '/remove - delete file/foldern\n' 
    '/into - move to the specified directoryn\n' 
    '/up - go up the directory aboven\n'
    '/viewdir - show all files in the current directory\n'
    '/mkwrite - write data to a file\n'
    '/mkfile - create a file in the current directory\n'
    '/copy - copies the file to the specified directory\n'
    '/move - moves the file to the specified directory\n'
    '/process - prints all processes to the console pc')

@router.message(Command('viewdir'))
async def viewdir(message:Message):
    if message.from_user.id == ADMIN_ID:
        directory = os.getcwd()
        file_list = []
        file_count = 1
        for root, dirs, files in os.walk(directory):
            for file in files:
                full_path = os.path.join(root, file)
                await message.answer(f'File number {file_count}: {full_path}')
                file_count += 1

@router.message(Command('mkfile'))
async def mkfile(message:Message , state:FSMContext):
    if message.from_user.id == ADMIN_ID:
        await message.answer(f'Creating a file at the path: {os.getcwd()}\nEnter the file name with its extension..')
        await state.set_state(Mkfile.name)
    else:
        await message.answer('❌Access denied, you are not an admin')

@router.message(Mkfile.name)
async def file_create(message:Message , state:FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()

    directory_path = os.path.join(os.getcwd())

    print(directory_path)

    try:
       file_path = os.path.join(directory_path, data['name'])
       async with aiofiles.open(file_path, 'w') as file:
          file.write('')
          file.close()

       await message.answer(f'✅File at path: {file_path} has been successfully created.')
    except FileNotFoundError:
       await message.answer('❌File not found')
    except OSError as e:
       await message.answer(f'❌An error occurred while reading the file: {str(e)}')
    except Exception as e:
       await message.answer(f'❌An unknown error occurred.: {str(e)}')      
    await state.clear()



@router.message(Command('process'))
async def process(message:Message):
    if message.from_user.id == ADMIN_ID:
        processes = []
        for proc in psutil.process_iter(['pid', 'name']):
           try:
               processes.append(proc.info)
               processes_json = json.dumps(processes)
               print(processes_json)

           except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
               pass
       
@router.message(Command('chdir'))
async def hdir(message:Message,state:FSMContext):
    if message.from_user.id == ADMIN_ID:
        await message.answer('Enter the name of the folder from the current directory..')
        await state.set_state(Directory.directory_path)
    else:
        await message.answer('❌Access denied, you are not an admin')

@router.message(Directory.directory_path)
async def hdir_dir(message:Message,state:FSMContext):
    await state.update_data(directory_path=message.text)
    data = await state.get_data()

    try:
        os.chdir(data['directory_path'])
        await message.answer(f'✅You have successfully logged into {data["directory_path"]}, the current directory is {os.getcwd()}')
    except NotADirectoryError as e:
        await message.answer(f'❌An error occurred: there is no such directory!\n{e}')
    

    await state.clear()

@router.message(Command('mkread'))
async def mkread(message:Message,state:FSMContext):
    if message.from_user.id == ADMIN_ID:
        await message.answer('Enter the file name and extension..')
        await state.set_state(mkfileread.name)
    else:
        await message.answer('❌Access denied, you are not an admin')

@router.message(mkfileread.name)
async def mkreadd(message:Message,state:FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()

    directory_path = (os.getcwd())
    print(directory_path)

    file_path = os.path.join(directory_path, data['name'])
    print('Файл путь',file_path)

    try:
        async with aiofiles.open(file_path,'r') as file:
            content = await file.read()
            file.close()
            await message.answer(f'The file at the path: {file_path} contains the data: {content}')
    except FileNotFoundError:
        await message.answer('❌File not found')
    except:
        await message.answer('❌An error occurred')
    await state.clear()

@router.message(Command('mkwrite'))
async def mkwrite(message:Message,state:FSMContext):
    if message.from_user.id == ADMIN_ID:
        await state.set_state(mkfilewrte.name)
        await message.answer('Enter the file names..')
    else:
        await message.answer('❌Access denied, you are not an admin')
    
@router.message(mkfilewrte.name)
async def mkwrite(message:Message,state:FSMContext):
    await state.set_state(mkfilewrte.text)
    await state.update_data(name=message.text)
    await message.answer('Enter data..')

@router.message(mkfilewrte.text)
async def mkwrite(message:Message,state:FSMContext):
    await state.update_data(text=message.text)
    data = await state.get_data()

    print(f'Имя:{data['name']} ,текст:{data["text"]}')
    directory_path = (os.getcwd())

    file_path = os.path.join(directory_path, data['name'])
    print(data['text'])

    try:
        async with aiofiles.open(file_path,'w') as file:
            await file.write(data['text'])
            await message.answer(f'Data added to the file at the path: {file_path}: {data['text']}')
    except FileNotFoundError as e:
        await message.answer(f'❌File not found error:{e}')
    except:
        await message.answer('❌An error occurred')

    await state.clear()

@router.message(Command('copy'))
async def start_copy(message: Message, state: FSMContext):
    if message.from_user.id == ADMIN_ID:
        await state.set_state(copyfile.name)
        await message.answer('Enter the file name..')
    else:
        await message.answer('❌Access denied, you are not an admin')

@router.message(copyfile.name)
async def get_file_name(message: Message, state: FSMContext):
    await state.set_state(copyfile.dir)
    await state.update_data(name=message.text)
    await message.answer('Enter the copy path..')

@router.message(copyfile.dir)
async def copy_file(message: Message, state: FSMContext):
    await state.update_data(dir=message.text)
    data = await state.get_data()

    directory_path = os.getcwd()
    directory_copy = data['dir']

    print(f'Имя {data["name"]}, путь {data["dir"]}')

    file_path = os.path.join(directory_path, data['name'])
    file_copy = os.path.join(directory_copy, data['name'])

    try:
        async with aiofiles.open(file_path, 'r') as file:
            data_file = await file.read()
            async with aiofiles.open(file_copy, 'w') as new_file:
                await new_file.write(data_file)
        await message.answer(f'✅File {data['name']} has been successfully copied to {file_copy}')
    except FileNotFoundError:
        await message.answer('❌File not found')
    except PermissionError:
        await message.answer('❌Access error: check write permissions in the directory')
    except Exception as e:
        await message.answer(f'❌An error occurred: {e}')

    await state.clear()

@router.message(Command('move'))
async def move(message:Message,state:FSMContext):
    if message.from_user.id == ADMIN_ID:
        await state.set_state(movefile.name)
        await message.answer('Enter the file name..')
    else:
        await message.answer('❌Access denied, you are not an admin')

@router.message(movefile.name)
async def move(message:Message,state:FSMContext):
    await state.set_state(movefile.dir)
    await state.update_data(name=message.text)
    await message.answer('Enter the movement path..')

@router.message(movefile.dir)
async def move(message:Message,state:FSMContext):
    await state.update_data(dir=message.text)
    data = await state.get_data()

    directory_path = os.getcwd()
    file_name = data['name']
    new_directory_path = os.path.join(data['dir'], file_name)

    print(new_directory_path)

    try:
        shutil.move(os.path.join(directory_path, file_name), new_directory_path)
        await message.answer(f'✅The file "{file_name}" has been successfully transferred from {directory_path} to {new_directory_path}')
    except FileNotFoundError:
        await message.answer('❌File not found')
    except Exception as e:
        await message.answer(f'❌An error occurred: {e}')

    await state.clear()
