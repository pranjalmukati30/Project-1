from typing import Annotated, Literal
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field, EmailStr, validate_email
# for DB
from database import engine, SessionLocal
from sqlalchemy import text
# for Frontend
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

class User(BaseModel):
    name : Annotated[str, Field(..., description='Enter User Name')]
    email : Annotated[EmailStr, Field(..., description='Enter User Email-Id')]
    gender : Annotated[Literal['Male', 'Female', 'Other'], Field(..., description="Enter User's Gender")]
    age : Annotated[int, Field(..., description='Enter User Age', gt=0, lt=120)]
    city : Annotated[str, Field(..., description="Enter User's City")]


# @app.get('/', response_class=PlainTextResponse)
# def greet():
#     return ('Hello Everyone'
#             '\nWelcome!')
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/testing")
def testing(request: Request):
    return templates.TemplateResponse("t.html", {"request": request})


# -->>>  Testing Connection of FastAPI and MySQL
@app.get('/test-db')
def test_db():
    try:
        with engine.connect() as connection:
            return {'message' : 'Database Connected Successfully'}
    except:
        return {'message' : 'Database Connection Failed'}

@app.get('/users')
def show_users():
    db = SessionLocal()
    try:
        result = db.execute(text("select * from users"))
        users = result.fetchall()

        return {'data' : [dict(row._mapping) for row in users]}
    finally:
        db.close()

@app.post("/create_users")
def create_user(user: User):
    db = SessionLocal()
    try:
        query = text("""
            INSERT INTO users (name, email, gender, age, city)
            VALUES (:name, :email, :gender, :age, :city)
        """)

        db.execute(query, {
            "name": user.name,
            "email": user.email,
            "gender": user.gender,
            "age": user.age,
            "city": user.city
        })

        db.commit()

        return {"message": "User created successfully"}

    except Exception as e:
        return {"error": str(e)}

    finally:
        db.close()

@app.put("/users/{user_id}")
def update_user(user_id: int, user: User):
    db = SessionLocal()
    try:
        query = text("""
            UPDATE users
            SET name = :name,
                gender = :gender,
                age = :age,
                email = :email,
                city = :city
            WHERE id = :id
        """)

        result = db.execute(query, {
            "id": user_id,
            "name": user.name,
            "gender": user.gender,
            "age": user.age,
            "email": user.email,
            "city": user.city
        })

        db.commit()

        if result.rowcount == 0:
            return {"message": "User not found"}

        return {"message": "User updated successfully"}

    except Exception as e:
        return {"error": str(e)}

    finally:
        db.close()


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    db = SessionLocal()
    try:
        query = text("DELETE FROM users WHERE id = :id")

        result = db.execute(query, {"id": user_id})
        db.commit()

        if result.rowcount == 0:
            return {"message": "User not found"}

        return {"message": "User deleted successfully"}

    except Exception as e:
        return {"error": str(e)}

    finally:
        db.close()