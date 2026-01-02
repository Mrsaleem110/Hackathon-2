-- PostgreSQL Schema for Todo App

-- Create the priority enum type first (if it doesn't exist)
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'priority') THEN
        CREATE TYPE priority AS ENUM ('low', 'medium', 'high');
    END IF;
END
$$;

-- Table: user
CREATE TABLE IF NOT EXISTS "user" (
	email VARCHAR NOT NULL,
	username VARCHAR NOT NULL,
	first_name VARCHAR NOT NULL,
	last_name VARCHAR NOT NULL,
	id SERIAL NOT NULL,
	hashed_password VARCHAR NOT NULL,
	is_active BOOLEAN NOT NULL DEFAULT true,
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
	updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
	PRIMARY KEY (id),
	UNIQUE (email),
	UNIQUE (username)
);

-- Table: item
CREATE TABLE IF NOT EXISTS item (
	title VARCHAR NOT NULL,
	description VARCHAR NOT NULL,
	completed BOOLEAN NOT NULL DEFAULT false,
	priority priority DEFAULT 'medium',
	category VARCHAR,
	due_date TIMESTAMP WITHOUT TIME ZONE,
	recurring VARCHAR,
	id SERIAL NOT NULL,
	owner_id INTEGER NOT NULL,
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
	updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
	PRIMARY KEY (id),
	FOREIGN KEY(owner_id) REFERENCES "user" (id) ON DELETE CASCADE
);

-- Table: session
CREATE TABLE IF NOT EXISTS session (
	token VARCHAR NOT NULL,
	expires_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	id SERIAL NOT NULL,
	user_id INTEGER NOT NULL,
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
	PRIMARY KEY (id),
	UNIQUE (token),
	FOREIGN KEY(user_id) REFERENCES "user" (id) ON DELETE CASCADE
);