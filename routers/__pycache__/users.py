from fastapi import APIRouter, HTTPException, status
from service.database import load_database, save_database
from models.users_class import User, UserDB, UserUpdate

router = APIRouter()
database_user = load_database()



def search_user(id: int):
    user = next((user for user in database_user["users"] if user["id"] == id), None)
    print(user)
    if user: return User(**user)
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="No se encontro al usuario"
        )

def registered_user(data_user: UserDB):
    database_user = load_database()
    user = next((user for user in database_user["users"] if user["id"] == data_user.id), None)
    if user:
        raise HTTPException(
        status_code=status.HTTP_409_CONFLICT, 
        detail="id del usuario ya existe"
        )
    
    user = next((user for user in database_user["users"] if user["email"] == data_user.email), None)
    if user:
        raise HTTPException(
        status_code=status.HTTP_409_CONFLICT, 
        detail="el correo ya existe"
        )
    return data_user

@router.get("/users")
async def users():
    database = load_database()
    return database["users"]

@router.get("/")
async def user(id: int):
    return search_user(id)

@router.post("/")
async def create_user(data_user: UserDB):
    user = registered_user(data_user)
    database = load_database()
    database["users"].append(user.dict())
    save_database(database)
    return {"message": "Usuario registrado exitosamente"}

@router.patch("/")
async def update_user(id: int, update_data_user: UserUpdate):
    database = load_database()
    
    for index, user in enumerate(database["users"]):
        if user["id"] == id:
            new_data = update_data_user.dict(exclude_unset=True)
            user.update(new_data)
            database["users"][index] = user  
            save_database(database)
            return {"message": "Usuario actualizado!", "User": user}
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="No se encontro el usuario"
        )

@router.delete("/")
async def delete(id: int):
    database = load_database()
    try:
        for index,user in enumerate(database_user["users"]):
            if user["id"] == id:
                database["users"].pop(index)
                save_database(database)
                return {"message": "Eliminado!"}
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontro al usuario"
            )