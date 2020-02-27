CREATE TABLE [IF NOT EXISTS] `tools` (
	`id` int NOT NULL UNIQUE,
	`name` varchar(255),
	`worksheet` varchar(2083),
	`reading` varchar(2083),
	`prerequisites` int,
	PRIMARY KEY (`id`),
	FOREIGN KEY (`prerequisites`) REFERENCES `tools`(`id`)
)

CREATE TABLE [IF NOT EXISTS] `users` (
	`id` int NOT NULL UNIQUE,
	`external_id` int,
	`first_name` varchar(255),
	`last_name` varchar(255),
	`email` varchar(255),
	`role` varchar(255),
	PRIMARY KEY (`id`),
	CONSTRAINT chk_role CHECK (role in ('student', 'NINJA', 'staff', 'faculty', 'bow'))
)

CREATE TABLE [IF NOT EXISTS] `users_tools` (
	`used_id` int,
	`tool_id` int,
	`level` varchar(255),
	CONSTRAINT chk_level CHECK (`level` in (NULL, 'fundamental', 'intermediate', 'cnc')),
	FOREIGN KEY (`tool_id`) REFERENCES `tools`(`id`),
	FOREIGN KEY (`user_id`) REFERENCES `users`(`id`)
)
