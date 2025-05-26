CREATE TABLE `sessions` (
	`id` text PRIMARY KEY NOT NULL,
	`user_id` text,
	`expires_at` integer DEFAULT '"2025-05-23T05:53:45.950Z"' NOT NULL,
	FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON UPDATE no action ON DELETE no action
);
--> statement-breakpoint
CREATE TABLE `todos` (
	`id` text PRIMARY KEY NOT NULL,
	`user_id` text,
	`title` text NOT NULL,
	`contents` text,
	`checked` integer DEFAULT false,
	`created_at` integer DEFAULT '"2025-05-16T05:53:45.950Z"',
	`updated_at` integer DEFAULT '"2025-05-16T05:53:45.950Z"',
	FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON UPDATE no action ON DELETE no action
);
--> statement-breakpoint
CREATE TABLE `users` (
	`id` text PRIMARY KEY NOT NULL,
	`username` text,
	`password_hash` text NOT NULL,
	`email` text DEFAULT '',
	`created_at` integer DEFAULT '"2025-05-16T05:53:45.950Z"',
	`updated_at` integer DEFAULT '"2025-05-16T05:53:45.950Z"'
);
--> statement-breakpoint
CREATE UNIQUE INDEX `users_username_unique` ON `users` (`username`);