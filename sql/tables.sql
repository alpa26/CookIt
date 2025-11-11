
CREATE TABLE IF NOT EXISTS cuisines (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    description TEXT
) ;

CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    description TEXT
) ;

CREATE TABLE IF NOT EXISTS tags (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    parent_name VARCHAR(255),
    parent_slug VARCHAR(255)
)

CREATE TABLE IF NOT EXISTS ingredients_all (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL
)

CREATE TABLE IF NOT EXISTS ingredient_groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL
)

CREATE TABLE IF NOT EXISTS recipes (
    id SERIAL PRIMARY KEY,
    source TEXT,
    category_id INTEGER REFERENCES categories(id),
    category_name VARCHAR(255),
    title VARCHAR(500) NOT NULL,
    description TEXT,
    note TEXT,
    cuisine_id INTEGER REFERENCES cuisines(id),
    cuisine_name VARCHAR(255),
    poster TEXT,
    difficulty VARCHAR(100),
    cooktime TEXT,
    preparetime TEXT,
    video TEXT,
    vegan BOOLEAN,
    rec_create_user TEXT,
    rec_json JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

CREATE TABLE IF NOT EXISTS recipe_tags (
    recipe_id INTEGER REFERENCES recipes(id) ON DELETE CASCADE,
    tag_id INTEGER REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (recipe_id, tag_id)
)

CREATE TABLE IF NOT EXISTS recipe_ingredient_groups (
    id SERIAL PRIMARY KEY,
    recipe_id INTEGER REFERENCES recipes(id) ON DELETE CASCADE,
    group_id INTEGER REFERENCES ingredient_groups(id) ON DELETE CASCADE,
    sort_order INTEGER
)

CREATE TABLE IF NOT EXISTS recipe_ingredients (
    id SERIAL PRIMARY KEY,
    recipe_group_id INTEGER REFERENCES recipe_ingredient_groups(id) ON DELETE CASCADE,
    ingredient_id INTEGER REFERENCES ingredients_all(id) ON DELETE CASCADE,
    name VARCHAR(255),
    value VARCHAR(100),
    type VARCHAR(100),
    amount VARCHAR(100),
    notes TEXT,
    sort_order INTEGER
)

CREATE TABLE IF NOT EXISTS instructions (
    id SERIAL PRIMARY KEY,
    recipe_id INTEGER REFERENCES recipes(id) ON DELETE CASCADE,
    text TEXT NOT NULL,
    image TEXT,
    step_number INTEGER
)

CREATE INDEX IF NOT EXISTS idx_recipes_category_id ON recipes(category_id)
CREATE INDEX IF NOT EXISTS idx_recipes_cuisine_id ON recipes(cuisine_id)
CREATE INDEX IF NOT EXISTS idx_recipe_tags_recipe_id ON recipe_tags(recipe_id)
CREATE INDEX IF NOT EXISTS idx_recipe_tags_tag_id ON recipe_tags(tag_id)
CREATE INDEX IF NOT EXISTS idx_recipe_ingredients_ingredient_id ON recipe_ingredients(ingredient_id)
CREATE INDEX IF NOT EXISTS idx_recipes_json ON recipes USING GIN(rec_json)