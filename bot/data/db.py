import aiosqlite
from async_class import AsyncClass

path_db = 'bot/data/database.db'

#Преобразование результата в словарь
def dict_factory(cursor, row):
    save_dict = {}

    for idx, col in enumerate(cursor.description):
        save_dict[col[0]] = row[idx]

    return save_dict

# Форматирование запроса без аргументов
def query(sql, parameters: dict):
    if "XXX" not in sql: sql += " XXX "
    values = ", ".join([
        f"{item} = ?" for item in parameters
    ])
    sql = sql.replace("XXX", values)

    return sql, list(parameters.values())

# Форматирование запроса с аргументами
def query_args(sql, parameters: dict):
    sql = f"{sql} WHERE "

    sql += " AND ".join([
        f"{item} = ?" for item in parameters
    ])

    return sql, list(parameters.values())

#Проверка и создание бд
class DB(AsyncClass):
    async def __ainit__(self):
        self.con = await aiosqlite.connect(path_db)
        self.con.row_factory = dict_factory
        
    # Получение всех пользователей из БД
    async def all_users(self):
        row = await self.con.execute("SELECT * FROM users")
        return await row.fetchall()
    
    # Получение пользователя из БД
    async def get_user(self, **kwargs):
        queryy = "SELECT * FROM users"
        queryy, params = query_args(queryy, kwargs)
        row = await self.con.execute(queryy, params)
        return await row.fetchone()
    
    async def get_status_apl(self, **kwargs):
        queryy = "SELECT * FROM applications"
        queryy, params = query_args(queryy, kwargs)
        row = await self.con.execute(queryy, params)
        return await row.fetchall()
    
    async def get_info_apl(self, **kwargs):
        queryy = "SELECT * FROM applications"
        queryy, params = query_args(queryy, kwargs)
        row = await self.con.execute(queryy, params)
        return await row.fetchone()
    
    # Редактирование пользователя
    async def del_appl(self, id, **kwargs):
        queryy = f"UPDATE applications SET"
        queryy, params = query(queryy, kwargs)
        params.append(id)
        await self.con.execute(queryy + "WHERE id = ?", params)
        await self.con.commit()
    
    
    # Редактирование пользователя
    async def update_user(self, id, **kwargs):
        queryy = f"UPDATE users SET"
        queryy, params = query(queryy, kwargs)
        params.append(id)
        await self.con.execute(queryy + "WHERE user_id = ?", params)
        await self.con.commit()
    
    # Регистрация пользователя в БД
    async def register_user(self, user_id, user_name, first_name):
        await self.con.execute("INSERT INTO users("
                                "user_id, user_name, first_name)"
                                "VALUES (?,?,?)",
                                [user_id, user_name, first_name])
        await self.con.commit()
        
    # Новая заявка
    async def new_applications(self, user_id, first_photo, second_photo, third_photo, fourth_photo, fifth_photo, text_photo, status):
        await self.con.execute("INSERT INTO applications("
                                "user_id, first_photo, second_photo, third_photo, fourth_photo, fifth_photo, text_photo, status)"
                                "VALUES (?,?,?,?,?,?,?,?)",
                                [user_id, first_photo, second_photo, third_photo, fourth_photo, fifth_photo, text_photo, status])
        await self.con.commit()
        
    # Получение текста
    async def get_text(self):
        row = await self.con.execute("SELECT * FROM settings")
        return await row.fetchall()
    
    # Обновление текста
    async def update_text(self, id, **kwargs):
        queryy = f"UPDATE settings SET"
        queryy, params = query(queryy, kwargs)
        params.append(id)
        await self.con.execute(queryy + "WHERE id = ?", params)
        await self.con.commit()
    
    #Проверка на существование бд и ее создание
    async def create_db(self):
        users_info = await self.con.execute("PRAGMA table_info(users)")
        if len(await users_info.fetchall()) == 4:
            print("database was found (Users | 1/3)")
        else:
            await self.con.execute("CREATE TABLE users ("
                                   "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                                   "user_id INTEGER,"
                                   "user_name TEXT,"
                                   "first_name TEXT)")
            print("database was not found (Users | 1/3), creating...")
            await self.con.commit()
            
        applications_info = await self.con.execute("PRAGMA table_info(applications)")
        if len(await applications_info.fetchall()) == 9:
            print("database was found (Applications | 2/3)")
        else:
            await self.con.execute("CREATE TABLE applications ("
                                   "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                                   "user_id INTEGER,"
                                   "first_photo TEXT,"
                                   "second_photo TEXT,"
                                   "third_photo TEXT,"
                                   "fourth_photo TEXT,"
                                   "fifth_photo TEXT,"
                                   "text_photo TEXT,"
                                   "status TEXT)")
            print("database was not found (Applications | 2/3), creating...")
            await self.con.commit()
            
        settings_info = await self.con.execute("PRAGMA table_info(settings)")
        if len(await settings_info.fetchall()) == 2:
            print("database was found (Settings | 3/3)")
        else:
            await self.con.execute("CREATE TABLE settings ("
                                   "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                                   "start_text TEXT)")
            print("database was not found (Settings | 3/3), creating...")
            
            await self.con.execute("INSERT INTO settings("
                                   "start_text) "
                                   "VALUES (?)", ['Стартовый текст'])
            
        await self.con.commit()