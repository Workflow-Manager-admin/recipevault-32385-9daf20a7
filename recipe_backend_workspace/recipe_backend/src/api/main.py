from fastapi import FastAPI, HTTPException, Depends, status, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.openapi.docs import get_swagger_ui_html
from pydantic import BaseModel, Field
from typing import List, Optional
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError

# In-memory stores for demo (replace with a real database in prod)
FAKE_USER_DB = {}
FAKE_RECIPE_DB = {}
RECIPE_ID_SEQUENCE = 1
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# --- MODELS ---

class User(BaseModel):
    id: int
    username: str = Field(..., description="Unique username for the user")
    hashed_password: str
 


class UserIn(BaseModel):
    username: str = Field(..., description="Desired username")
    password: str = Field(..., description="User password")


class UserOut(BaseModel):
    id: int
    username: str


class Token(BaseModel):
    access_token: str
    token_type: str


class RecipeBase(BaseModel):
    title: str = Field(..., description="Title of the recipe")
    description: Optional[str] = Field(None, description="Description of the recipe")
    ingredients: List[str] = Field(..., description="List of ingredients")
    steps: List[str] = Field(..., description="Preparation steps")
    author_id: int = Field(..., description="User ID of the recipe author")


class RecipeCreate(RecipeBase):
    pass


class RecipeUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    ingredients: Optional[List[str]]
    steps: Optional[List[str]]


class RecipeOut(RecipeBase):
    id: int


# --- UTILS ---


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def get_user_by_username(username: str) -> Optional[User]:
    for user in FAKE_USER_DB.values():
        if user["username"] == username:
            return User(**user)
    return None


def get_user(user_id: int) -> Optional[User]:
    user = FAKE_USER_DB.get(user_id)
    if not user:
        return None
    return User(**user)


def authenticate_user(username: str, password: str):
    user = get_user_by_username(username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


# This will be used as a dependency to get the current user from token
# PUBLIC_INTERFACE
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Dependency to get the current user from JWT access token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )
    payload = decode_access_token(token)
    if payload is None or "sub" not in payload:
        raise credentials_exception
    user_id = int(payload["sub"])
    user = get_user(user_id)
    if user is None:
        raise credentials_exception
    return user


# --- FASTAPI APP INIT ---


app = FastAPI(
    title="Recipe App Backend API",
    version="1.0.0",
    description=(
        "Backend API for managing users and recipes (CRUD, search, auth)."
    ),
    openapi_tags=[
        {"name": "Users", "description": "User registration and authentication endpoints."},
        {"name": "Recipes", "description": "CRUD operations for recipes."},
        {"name": "Search", "description": "Recipe search functionality."}
    ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- ROUTES ---


@app.get("/", tags=["Health"])
def health_check():
    """Check service health status."""
    return {"message": "Healthy"}


# -- Auth and Users --


# PUBLIC_INTERFACE
@app.post(
    "/auth/register",
    response_model=UserOut,
    tags=["Users"],
    summary="Register a new user",
    description="Register a new user with username and password"
)
def register_user(user_in: UserIn):
    if get_user_by_username(user_in.username):
        raise HTTPException(
            status_code=409, detail="Username already exists"
        )
    user_id = len(FAKE_USER_DB) + 1
    hashed = get_password_hash(user_in.password)
    user = User(id=user_id, username=user_in.username, hashed_password=hashed)
    FAKE_USER_DB[user_id] = user.model_dump()
    return UserOut(id=user.id, username=user.username)


# PUBLIC_INTERFACE
@app.post(
    "/auth/token",
    response_model=Token,
    tags=["Users"],
    summary="User login",
    description="Login as a user and receive a Bearer access token"
)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401, detail="Incorrect username or password"
        )
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}


# PUBLIC_INTERFACE
@app.get(
    "/users/me",
    response_model=UserOut,
    tags=["Users"],
    summary="Get current user",
    description="Get the current authenticated user"
)
def read_users_me(current_user: User = Depends(get_current_user)):
    return UserOut(id=current_user.id, username=current_user.username)


# -- Recipes CRUD --


# PUBLIC_INTERFACE
@app.post(
    "/recipes/",
    response_model=RecipeOut,
    tags=["Recipes"],
    summary="Add a new recipe",
    description="Create a new recipe (authenticated)"
)
def create_recipe(recipe: RecipeCreate, current_user: User = Depends(get_current_user)):
    global RECIPE_ID_SEQUENCE
    recipe_id = RECIPE_ID_SEQUENCE
    RECIPE_ID_SEQUENCE += 1
    recipe_data = recipe.model_dump()
    recipe_data["id"] = recipe_id
    FAKE_RECIPE_DB[recipe_id] = recipe_data
    return RecipeOut(**recipe_data)


# PUBLIC_INTERFACE
@app.get(
    "/recipes/",
    response_model=List[RecipeOut],
    tags=["Recipes"],
    summary="List all recipes",
    description="Get a list of all recipes (public)"
)
def list_recipes(skip: int = 0, limit: int = 20):
    recipes = list(FAKE_RECIPE_DB.values())
    return [RecipeOut(**r) for r in recipes][skip:skip + limit]


# PUBLIC_INTERFACE
@app.get(
    "/recipes/{recipe_id}",
    response_model=RecipeOut,
    tags=["Recipes"],
    summary="Get recipe details",
    description="Get details of a specific recipe (public)"
)
def get_recipe(recipe_id: int):
    recipe = FAKE_RECIPE_DB.get(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return RecipeOut(**recipe)


# PUBLIC_INTERFACE
@app.patch(
    "/recipes/{recipe_id}",
    response_model=RecipeOut,
    tags=["Recipes"],
    summary="Update a recipe",
    description="Edit a recipe (must be owner)"
)
def update_recipe(
    recipe_id: int,
    recipe_update: RecipeUpdate,
    current_user: User = Depends(get_current_user)
):
    recipe = FAKE_RECIPE_DB.get(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    if recipe["author_id"] != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to edit this recipe"
        )
    update_data = recipe_update.model_dump(exclude_unset=True)
    for key, val in update_data.items():
        recipe[key] = val
    FAKE_RECIPE_DB[recipe_id] = recipe
    return RecipeOut(**recipe)


# PUBLIC_INTERFACE
@app.delete(
    "/recipes/{recipe_id}",
    status_code=204,
    tags=["Recipes"],
    summary="Delete a recipe",
    description="Delete a recipe (must be owner)"
)
def delete_recipe(recipe_id: int, current_user: User = Depends(get_current_user)):
    recipe = FAKE_RECIPE_DB.get(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    if recipe["author_id"] != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this recipe"
        )
    del FAKE_RECIPE_DB[recipe_id]
    return


# --- Search ---


# PUBLIC_INTERFACE
@app.get(
    "/search/",
    response_model=List[RecipeOut],
    tags=["Search"],
    summary="Search recipes",
    description="Search recipes by title or ingredient (public)"
)
def search_recipes(
    q: Optional[str] = Query(None, description="Search keyword for title or ingredient"),
    skip: int = 0,
    limit: int = 20
):
    results = []
    if not q:
        # No query -- return all
        results = list(FAKE_RECIPE_DB.values())
    else:
        q_lower = q.lower()
        for r in FAKE_RECIPE_DB.values():
            if (
                q_lower in r["title"].lower()
                or any(q_lower in ing.lower() for ing in r["ingredients"])
            ):
                results.append(r)
    return [RecipeOut(**r) for r in results][skip:skip + limit]


# --- Custom Docs Route for WebSocket Help (not needed for REST, but as instructed) ---


# PUBLIC_INTERFACE
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    """Override /docs to show Swagger UI for API documentation."""
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Docs"
    )
